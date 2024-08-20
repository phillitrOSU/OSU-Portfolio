from flask import Flask, request, send_file, jsonify
from google.cloud import datastore, storage
from google.cloud.datastore import query
from google.cloud.datastore.query import PropertyFilter

import requests
import json

from six.moves.urllib.request import urlopen
from jose import jwt
from authlib.integrations.flask_client import OAuth

import io

# Error Messages
ERROR_INVALID_REQUEST_BODY= {"Error": "The request body is invalid"}, 400
ERROR_UNAUTHORIZIED = {"Error": "Unauthorized"}, 401
ERROR_NO_PERMISSION = {"Error": "You don't have permission on this resource"}, 403
ERROR_NOT_FOUND = {"Error": "Not found"}, 404
ERROR_INVALID_ENROLLMENT = {"Error": "Enrollment data is invalid"}, 409

# Auth0 Access
CLIENT_ID = 'MehecM0QdoyXfdsuQhH0ogX3URd4wZtU'
CLIENT_SECRET = '0lSilCKpvSWvVybCv2QOugqZaaLvCppaAoY9oR6g4KgLBGRoijMMcZtiUQp8O9XV'
DOMAIN = 'dev-y2v7r1wm8jztsha7.us.auth0.com'


ALGORITHMS = ["RS256"]
APP_URL = "https://hw7-phillitr.wl.r.appspot.com"

# Cloud Storage and Datastore Kinds
client = datastore.Client()
PHOTO_BUCKET='m8_phillitr_photobucket'
USERS='users'
COURSES='courses'
# Additional links
STUDENTS='students'
AVATAR='avatar'

app = Flask(__name__)
oauth = OAuth(app)
app.secret_key = 'SECRET_KEY'

auth0 = oauth.register(
    'auth0',
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    api_base_url="https://" + DOMAIN,
    access_token_url="https://" + DOMAIN + "/oauth/token",
    authorize_url="https://" + DOMAIN + "/authorize",
    client_kwargs={
        'scope': 'openid profile email',
    },
)

##############
# HELPER FUNCTIONS
##############

# Add a course to user data
def add_user_course(user_id, course_id):
    user_key = client.key(USERS, user_id)
    user = client.get(key=user_key)
    # Append course to users courses or initialize new array if first course.
    try:
        # Skip if already in course
        if course_id in user['courses']:
            pass
        else:
            user['courses'].append(course_id)
    except: # If no courses yet...
        user.update({'courses': [course_id]})
    client.put(user)

# Drop a course from user data
def drop_user_course(user_id, course_id):
    user_key = client.key(USERS, user_id)
    user = client.get(key=user_key)
    try:
        user['courses'].remove(course_id)
        if user['courses'] == []:
            del user['courses']
        client.put(user)
    except: # If no courses yet...
        return False

# Verify that a sub is associated with admin priveleges
def verify_admin(sub):
    query = client.query(kind=USERS)
    query.add_filter(filter=PropertyFilter('sub', '=', sub))
    r = list(query.fetch())
    if r[0]['role'] != 'admin':
        return False

    return True

# Verify that an id is associated with an instructor
def verify_instructor_id(id):
    try:
        user_key = client.key(USERS, id)
        user = client.get(key=user_key)
        if user['role'] != 'instructor':
            return False
        return True
    except: # No user found
        return False

# Verify id is associated with instructor role
def is_instructor(id):
    try:
        # Get user
        user_key = client.key(USERS, id)
        user = client.get(user_key)
        # Check if user is instructor
        if user['role'] == 'instructor':
            return True
        else:
            return False
    # No user associated with id
    except:
        return False

# Verifies that sub is instructor of provided course
def verify_instructor(sub, course_id):
    # Get course from id
    course_key = client.key(COURSES, course_id)
    course = client.get(key=course_key)
    # Find user from sub
    query = client.query(kind=USERS)
    query.add_filter(filter=PropertyFilter('sub', '=', sub))
    r = list(query.fetch())
    # Verify user id matches course instructor_id.
    if r[0].key.id == course['instructor_id']:
        return True

    return False

# Ensure validity of enrollment data
def verify_enrollement(data):
    add, remove = data['add'], data['remove']

    # Check for duplicates
    all_ids = add + remove
    if len(all_ids) != len(set(all_ids)):
        return False

    # Check each id is a valid user with role student.
    for id in all_ids:
        user_key = client.key(USERS, id)
        user = client.get(key=user_key)
        if user == None:
            return False
        if user['role'] != 'student':
            return False
    
    # If all users valid students, return True.
    return True

# Add user to course data
def add_user_to_course(user_id, course_id):
    # Find course by id
    course_key = client.key(COURSES, course_id)
    course = client.get(key=course_key)
    # Append student to enrollment array or initialize array if first student.
    try:
        if user_id not in course['enrollment']:
            course['enrollment'].append(user_id)
    except: # If no students yet...
        course.update({'enrollment': [user_id]})
    client.put(course)

# Drop user from course data
def drop_user_from_course(user_id, course_id):
    # Find course by id
    course_key = client.key(COURSES, course_id)
    course = client.get(key=course_key)
    # Remove student from course
    try:
        if user_id in course['enrollment']:
            course['enrollment'].remove(user_id)
            client.put(course)
    except: # If no students yet...
        return False

# Remove deleted course from students' and instructors' courses
def remove_enrolled(id):
    user_query = client.query(kind=USERS)
    results = list(user_query.fetch())

    # Remove course for all users
    for r in results:
        if 'courses' in r:
            for course in r['courses']:
                if course == id:
                    r['courses'].remove(course)
                    if r['courses'] == []:
                        del r['courses']
                    client.put(r)

# This code is adapted from https://auth0.com/docs/quickstart/backend/python/01-authorization?_ga=2.46956069.349333901.1589042886-466012638.1589042885#create-the-jwt-validation-decorator
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

# Verify the JWT in the request's Authorization header
def verify_jwt(request):
    if 'Authorization' in request.headers:
        auth_header = request.headers['Authorization'].split()
        token = auth_header[1]
    else:
        raise AuthError({"code": "no auth header",
                            "description":
                                "Authorization header is missing"}, 401)
    
    jsonurl = urlopen("https://"+ DOMAIN+"/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    try:
        unverified_header = jwt.get_unverified_header(token)
    except jwt.JWTError:
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Invalid header. "
                            "Use an RS256 signed JWT Access Token"}, 401)
    if unverified_header["alg"] == "HS256":
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Invalid header. "
                            "Use an RS256 signed JWT Access Token"}, 401)
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=CLIENT_ID,
                issuer="https://"+ DOMAIN+"/"
            )
        except jwt.ExpiredSignatureError:
            raise AuthError({"code": "token_expired",
                            "description": "token is expired"}, 401)
        except jwt.JWTClaimsError:
            raise AuthError({"code": "invalid_claims",
                            "description":
                                "incorrect claims,"
                                " please check the audience and issuer"}, 401)
        except Exception:
            raise AuthError({"code": "invalid_header",
                            "description":
                                "Unable to parse authentication"
                                " token."}, 401)

        return payload
    else:
        raise AuthError({"code": "no_rsa_key",
                            "description":
                                "No RSA key in JWKS"}, 401)


####################
#ROUTES
####################
@app.route('/')
def index():
    return "Please navigate to /courses to use this API"

# Generate a JWT from the Auth0 domain and return it
# Request: JSON body with 2 properties with "username" and "password"
#       of a user registered with this Auth0 domain
# Response: JSON with the JWT as the value of the property id_token
@app.route('/users/login', methods=['POST'])
def login_user():
    global APP_URL 
    APP_URL = request.root_url[:-1]

    content = request.get_json()
    # Check for valid request body
    if "username" not in content or "password" not in content:
        return ERROR_INVALID_REQUEST_BODY
    
    # Prepare request
    username = content["username"]
    password = content["password"]
    body = {'grant_type':'password','username':username,
            'password':password,
            'client_id':CLIENT_ID,
            'client_secret':CLIENT_SECRET
           }
    headers = { 'content-type': 'application/json' }
    url = 'https://' + DOMAIN + '/oauth/token'

    # Send request and log response as r
    r = json.loads(requests.post(url, json=body, headers=headers).text)
    try:
        token = r['id_token']
        return { 'token': token }, 200, {'Content-Type':'application/json'}
    # If no token, credentials are invalid
    except:
        return ERROR_UNAUTHORIZIED

# Get all users (admin only)
@app.route('/' + USERS, methods=['GET'])
def get_users():
    # Verify JWT
    try:
        payload = verify_jwt(request)
    except:
        return ERROR_UNAUTHORIZIED
    
    # Require admin permission
    sub = payload['sub']
    if not verify_admin(sub):
        return ERROR_NO_PERMISSION
    
    # Generate list of users, adding id but hiding courses and avatar properties.
    query = client.query(kind=USERS)
    results = list(query.fetch())
    for r in results:
        r['id'] = r.key.id
        if 'courses' in r:
            del r['courses']
        if 'avatar' in r:
            del r['avatar']

    return results, 200

# Get a user (requestor must match requested user)
@app.route('/' + USERS + '/<int:id>', methods=['GET'])
def get_user(id):
    # Verify JWT
    try:
        payload = verify_jwt(request)
    except:
        return ERROR_UNAUTHORIZIED
    
    user_key = client.key(USERS, id)
    user = client.get(key=user_key)

    if user is None:
        return ERROR_NO_PERMISSION
 
    # Check user requested matches requestor JWT
    if user['sub'] != payload['sub'] and not verify_admin(payload['sub']):
        return ERROR_NO_PERMISSION

    # Add avatar link, id. Add courses for students.
    user['id'] = user.key.id
    if 'avatar' in user:
        del user['avatar']
        user['avatar_url'] = APP_URL + '/users/' + str(id) + '/avatar'

    # Return admin without courses
    if verify_admin(user['sub']): return user 

    # Update courses for students and instructors
    if 'courses' in user:
        for i in range(len(user['courses'])):
            course = user['courses'][i]
            user['courses'][i] = APP_URL + '/courses/' + str(course)

    else:
        user['courses'] = []

    return user

# Store user uploaded avatar
@app.route('/' + USERS + '/<int:id>/' + AVATAR, methods=['POST'])
def store_avatar(id):
    # First check if there is an entry in request.files with the key 'file'
    if 'file' not in request.files:
        return ERROR_INVALID_REQUEST_BODY
    
    # Verify JWT
    try:
        payload = verify_jwt(request)
    except:
        return ERROR_UNAUTHORIZIED
    
    user_key = client.key(USERS, id)
    user = client.get(key=user_key)
    
    # Requestor JWT does not match requested ID
    if user['sub'] != payload['sub']:
        return ERROR_NO_PERMISSION

    # Set file_obj to the file sent in the request
    file_obj = request.files['file']
    if 'tag' in request.form:
        tag = request.form['tag']

    # Get a handle on the bucket and create blob
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(PHOTO_BUCKET)
    # Upload file with filename = sub_avatar
    file_obj.filename = payload['sub'] + '_avatar'
    blob = bucket.blob(file_obj.filename)
    file_obj.seek(0)
    blob.upload_from_file(file_obj)

    # Update user avatar property and return avatar url
    avatar_url = APP_URL + '/users/' + str(id) + '/avatar'
    user['avatar'] = payload['sub'] + '_avatar'
    client.put(user)
    return ({'avatar_url': avatar_url}, 200)

# Retrieve user avatar
@app.route('/' + USERS + '/<int:id>/' + AVATAR, methods=['GET'])
def get_avatar(id):
    # Verify JWT
    try:
        payload = verify_jwt(request)
    except:
        return ERROR_UNAUTHORIZIED
    
    # Identify user and check permissions
    user_key = client.key(USERS, id)
    user = client.get(key=user_key)
    if user['sub'] != payload['sub']:
        return ERROR_NO_PERMISSION

    # Generate filename string
    file_name = user['sub'] + '_avatar'

    # Access storage client bucket and create blob
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(PHOTO_BUCKET)
    blob = bucket.blob(file_name)
    # Create a file object in memory using Python io package
    file_obj = io.BytesIO()
    # Download the file from Cloud Storage to the file_obj variable
    try:
        blob.download_to_file(file_obj)
    except:
        # No avatar found for user
        return ERROR_NOT_FOUND

    # Position the file_obj to its beginning
    file_obj.seek(0)
    # Send the object as a file in the response with the correct MIME type and file name
    return send_file(file_obj, mimetype='image/png', download_name=file_name)

# Delete user avatar
@app.route('/' + USERS + '/<int:id>/' + AVATAR, methods=['DELETE'])
def delete_avatar(id):
    # Verify JWT
    try:
        payload = verify_jwt(request)
    except:
        return ERROR_UNAUTHORIZIED
    
    # Identify user and check permissions
    user_key = client.key(USERS, id)
    user = client.get(key=user_key)
    if user['sub'] != payload['sub']:
        return ERROR_NO_PERMISSION
    
    # Generate filename string and find in storage.
    file_name = user['sub'] + '_avatar'
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(PHOTO_BUCKET)
    blob = bucket.blob(file_name)
    # Delete the file from Cloud Storage and from user properties
    try:
        blob.delete()
    except:
        return ERROR_NOT_FOUND
    del user['avatar']
    client.put(user)

    return '',204

# Create a new course
@app.route('/' + COURSES, methods=['POST'])
def create_course():
    # Verify JWT
    try:
        payload = verify_jwt(request)
    except:
        return ERROR_UNAUTHORIZIED
    
    # Verify admin priveleges
    if not verify_admin(payload['sub']):
        return ERROR_NO_PERMISSION
    
    # Verify content
    content = request.get_json()
    if len(content) < 5:
        return ERROR_INVALID_REQUEST_BODY
    
    # Verify that instructor is valid
    if not verify_instructor_id(content['instructor_id']):
        return ERROR_INVALID_REQUEST_BODY

    # Create new course entity with content provided.
    new_course = datastore.entity.Entity(key=client.key(COURSES))
    new_course.update({"subject": content["subject"],
                            "number": content["number"],
                            "title": content["title"],
                            "term": content["term"],
                            "instructor_id": content["instructor_id"]})
    client.put(new_course)

    # Update instructors courses
    add_user_course(content['instructor_id'], new_course.key.id)

    # Add id and self to response but not database.
    url_self = APP_URL + '/' + COURSES + '/' + str(new_course.key.id)
    new_course['id'] = new_course.key.id
    new_course['self'] = url_self
    
    return new_course, 201

# Get all courses
@app.route('/' + COURSES, methods=['GET'])
def get_courses():
    # Query for all subjects, order by subject.
    courses_query = client.query(kind=COURSES)
    courses_query.order = ['subject']
    
    # Set limit and offset.
    if request.args:
        limit = int(request.args.get('limit'))
        offset = int(request.args.get('offset'))
    else:
        limit, offset = 3, 0

    # Generate results based on limit and offset
    c_iterator = courses_query.fetch(limit=limit, offset=offset)
    pages = c_iterator.pages
    results = list(next(pages))

    # For each result add id, self and remove enrollment
    for r in results:
        r['id'] = r.key.id
        r['self'] = APP_URL + '/courses/' + str(r.key.id)
        if 'enrollment' in r:
            del r['enrollment']

    # Return results with next_url
    next_url = APP_URL + f'/courses?limit={3}&offset={offset+limit}'
    return {'courses' : results,
            'next' : next_url}, 200

# Get a course by id
@app.route('/' + COURSES + '/<int:id>', methods=['GET'])
def get_course(id):    
    # Get course by id
    course_key = client.key(COURSES, id)
    course = client.get(key=course_key)
    if course is None:
        return ERROR_NOT_FOUND
 
    # Add id and self link, remove enrollment
    course['id'] = course.key.id
    course['self'] = APP_URL + '/courses/' + str(id)
    if 'enrollment' in course:
        del course['enrollment']

    return course

# Update specified values in course
@app.route('/' + COURSES + '/<int:id>', methods=['PATCH'])
def update_course(id):
    # Verify JWT
    try:
        payload = verify_jwt(request)
    except:
        return ERROR_UNAUTHORIZIED
    
    # Verify admin priveleges
    if not verify_admin(payload['sub']):
        return ERROR_NO_PERMISSION
    
    # Receive content and find course to update
    content = request.get_json()
    course_key = client.key(COURSES, id)
    course = client.get(key=course_key)
    if course is None:
        return ERROR_NO_PERMISSION
    
    # If instructor_id included, check valid.
    if 'instructor_id' in content:
        print('hi')
        if not is_instructor(content['instructor_id']):
            return ERROR_INVALID_REQUEST_BODY
        # Swap course between instructors, and update instructor_id.
        drop_user_course(course['instructor_id'], id)
        add_user_course(content['instructor_id'], id)
        course.update({'instructor_id': content['instructor_id']})
        client.put(course)
        del content['instructor_id']

    # Update provided properties
    for k, v in content.items():
        course.update({k: v})
        client.put(course)

    # Add self and id to response, hide enrollment
    url_self = APP_URL + '/' + COURSES + '/' + str(course.key.id)
    course['self'] = url_self
    course['id'] = course.key.id
    if 'enrollment' in course:
        del course['enrollment']

    return course, 200

# Delete a course
@app.route('/' + COURSES + '/<int:id>', methods=['DELETE'])
def delete_course(id):
    # Verify JWT
    try:
        payload = verify_jwt(request)
    except:
        return ERROR_UNAUTHORIZIED
    
    # Verify admin priveleges
    if not verify_admin(payload['sub']):
        return ERROR_NO_PERMISSION

    # Find course by id
    course_key = client.key(COURSES, id)
    course = client.get(key=course_key)
    if course is None:
        return ERROR_NO_PERMISSION
    
    # Update student course enrollment and delete course
    remove_enrolled(id)
    client.delete(course_key)
    return "", 204

@app.route('/' + COURSES + '/<int:id>/' + STUDENTS, methods=['PATCH'])
def update_enrollment(id):
    # Verify JWT
    try:
        payload = verify_jwt(request)
    except:
        return ERROR_UNAUTHORIZIED
    
    # Receive content and find course to update
    content = request.get_json()
    course_key = client.key(COURSES, id)
    course = client.get(key=course_key)
    if course is None:
        return ERROR_NO_PERMISSION
    
    # Verify privelege (instructor of course or admin)
    if not verify_instructor(payload['sub'], id) and not verify_admin(payload['sub']):
        return ERROR_NO_PERMISSION
    
    # Verify enrollemnt data
    if not verify_enrollement(content):
        return ERROR_INVALID_ENROLLMENT
    
    # Update enrollment of course.
    for s in content['add']:
        add_user_course(s, id)
        add_user_to_course(s, id)
    
    for s2 in content['remove']:
        drop_user_course(s2, id)
        drop_user_from_course(s2, id)

    return "", 200

@app.route('/' + COURSES + '/<int:id>/' + STUDENTS, methods=['GET'])
def get_course_enrollment(id):
    # Verify JWT
    try:
        payload = verify_jwt(request)
    except:
        return ERROR_UNAUTHORIZIED
    
    # Get course by id
    course_key = client.key(COURSES, id)
    course = client.get(key=course_key)
    if course is None:
        return ERROR_NO_PERMISSION
    
    # Verify privelege (admin or instructor of course)
    if not verify_instructor(payload['sub'], id) and not verify_admin(payload['sub']):
        return ERROR_NO_PERMISSION
    
    # Return enrollment
    if 'enrollment' in course:
        return course['enrollment'], 200
    # If no students, return empty array.
    else:
        return [], 200


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)