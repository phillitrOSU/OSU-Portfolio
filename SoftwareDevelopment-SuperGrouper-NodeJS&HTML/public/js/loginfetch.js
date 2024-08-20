//Sign up new users
async function signup() {

    //Get username and password
    username = document.getElementById("signupUsername").value;
    password = document.getElementById("signupPassword").value;

    // Send username and password to microservice to see if unique.
    try {
        const response = await fetch(
            `https://authentication-microservice-production-a9ec.up.railway.app/signup`,
            {
              method: "POST",
              body: JSON.stringify({
                email: username,
                password: password,
              }),
              headers: {
                "Content-Type": "application/json",
              },
            }
          );
  
        if (!response.ok) {
        const { message } = await response.json();
        throw new Error(message);
        }
      
        //If success alert user.
        const data = await response.json();
        console.log("Signup Success:", data);
        alert(`Signup Success! Username: ${username} Password: ${password}`);
        document.getElementById("signupUsername").value = ""
        document.getElementById("signupPassword").value = ""

    } catch (error) {
      console.error("Signup Failed:", error.message);
    }
}




// Login user based on credentials
async function login(username, password) {

  // Send username and password to microservice
  try {
      const response = await fetch(
          `https://authentication-microservice-production-a9ec.up.railway.app/login`,
          {
            method: "POST",
            body: JSON.stringify({
              email: username,
              password: password,
            }),
            headers: {
              "Content-Type": "application/json",
            },
          }
        );

      if (!response.ok) {
      const { message } = await response.json();
      throw new Error(message);
      }
    
      //If success return token
      const token = await response.json();
      console.log("Login Success:", token);
      return Object.values(token)[1]
  
  } catch (error) {
    console.error("Login Failed:", error.message);
  }
}

// Authenticate token based on user credentials
async function authenticate(username, password) {

  //Receive login token from user credentials
  token = await login(username, password);

  // Send token to microservice for authentication
  try {
      const response = await fetch(
          `https://authentication-microservice-production-a9ec.up.railway.app/authenticate`,
          {
            method: "POST",
            body: JSON.stringify({
              token: token,
            }),
            headers: {
              "Content-Type": "application/json",
            },
          }
        );

      if (!response.ok) {
      const { message } = await response.json();
      throw new Error(message);
      }

    const { user } = await response.json();
    console.log("Current user:", user);
    updateDisplayedUsername(user);
  } catch (error) {
    console.error("Authentication Failed:", error.message);
    alert("Invalid login");
  }
}

function updateDisplayedUsername(user){
      username = Object.values(user)[0]
      userInfo = document.getElementById("userInfo");
      userInfoText = ("Current User: ").concat(username);
      userInfo.innerText = userInfoText;
}
    
// Run login functions to update user information.
async function runLogin() {
  username = document.getElementById("loginUsername").value;
  password = document.getElementById("loginPassword").value;

  user = await authenticate(username, password);
}