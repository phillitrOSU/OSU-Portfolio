/*
    SETUP
*/
const fetch = require("node-fetch");

// Express
var express = require('express');
var app = express();
app.use(express.static(__dirname + '/public'));

// Handle CORS
app.use((req, res, next) => {
    res.setHeader("Access-Control-Allow-Origin", "*");
    res.setHeader("Access-Control-Allow-Headers", "Content-Type");
    next();
  });

PORT = 3000;

// Handlebars
const { engine } = require('express-handlebars');
var exphbs = require('express-handlebars');     // Import express-handlebars
app.engine('.hbs', engine({extname: ".hbs"}));  // Create an instance of the handlebars engine to process templates
app.set('view engine', '.hbs');                 // Tell express to use the handlebars engine whenever it encounters a *.hbs file.


//Setup css, js access.
app.use(express.static(__dirname + '/public'));  

/*
    ROUTES
*/
app.get('/', function(req, res)
    {
        res.render('index');
    });

app.get('/help', function(req, res)
    {
        res.render('help');
    });

app.get('/about', function(req, res)
    {
        res.render('about');
    });


app.get('/loginpage', async function(req, res)
    {
        res.render('loginpage');
    });


/*
    LISTENER
*/
app.listen(PORT, function(){
    console.log('Express started on http://localhost:' + PORT + '; press Ctrl-C to terminate.')
});
