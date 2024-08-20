/*
    SETUP
*/

// Express
var express = require('express');
var app = express();
app.use(express.json())
app.use(express.urlencoded({extended: true}))

PORT = 3147;

// Database
var db = require('./database/db-connector');

// Handlebars
const { engine } = require('express-handlebars');
var exphbs = require('express-handlebars');     // Import express-handlebars
app.engine('.hbs', engine({extname: ".hbs"}));  // Create an instance of the handlebars engine to process templates
app.set('view engine', '.hbs');                 // Tell express to use the handlebars engine whenever it encounters a *.hbs file.

// Static Files
app.use(express.static('public'));

/*
    ROUTES
*/

// GET ROUTES
app.get('/Beer',function(req,res){
    let query1 = "SELECT Beer.beer_ID AS ID, Beer.beer_Name AS Name, Breweries.brewery_Name AS Brewery, Styles.style_Name AS Style, year as Year, inventory AS Inventory, price as Price FROM Beer INNER JOIN Styles ON Beer.style_ID = Styles.style_ID INNER JOIN Breweries ON Beer.brewery_ID = Breweries.brewery_ID ORDER BY Beer.beer_Name ASC;";
    let query2 = "SELECT * FROM Breweries";
    let query3 = "SELECT * FROM Styles";
    db.pool.query(query1, function(error, rows, fields){
        // Save beers
        let Beer = rows;
        db.pool.query(query2, (error, rows, fields) => {
            let Breweries = rows;
            db.pool.query(query3, (error, rows, fields) => {
                let Styles = rows;
                return res.render('Beer', {data: Beer, Breweries: Breweries, Styles: Styles});
            })
        })  
    })      
 });

app.get('/Breweries',function(req,res){
    let query1 = "SELECT Breweries.brewery_ID AS ID, Breweries.brewery_Name AS Name, Styles.style_Name AS Specialty, Breweries.region AS Region FROM Breweries INNER JOIN Styles ON Styles.style_ID = Breweries.style_ID;";
    let query2 = "SELECT * FROM Styles";
    db.pool.query(query1, function(error, rows, fields){
        let Breweries = rows;
        db.pool.query(query2, (error, rows, fields) => {
            let Styles = rows;
            return res.render('Breweries', {data: Breweries, Styles: Styles});
        })
    })
});

app.get('/Styles',function(req,res){
    let query1 = "SELECT Styles.style_ID AS ID, Styles.style_Name as Style FROM Styles;";
    db.pool.query(query1, function(error, rows, fields){
        res.render('Styles', {data: rows});
    })
});

app.get('/Orders',function(req,res){
    let query1 = "SELECT Orders.orders_ID AS ID, Customers.customer_Name AS Customer, Orders.total_Sales AS Total, Orders.total_Beers as Quantity, Orders.date AS Date FROM Orders INNER JOIN Customers on Customers.customer_ID = Orders.customer_ID;";
    let query2 = "SELECT * FROM Customers";
    db.pool.query(query1, function(error, rows, fields){
        let Orders = rows;
        db.pool.query(query2, (error, rows, fields) => {
            let Customers = rows;
            res.render('Orders', {data: Orders, Customers: Customers})
        })
    })   
});

app.get('/Customers',function(req,res){
    let query1 = "SELECT Customers.customer_ID AS ID, Customers.customer_Name AS Name, Customers.address AS Address, Customers.phone AS Phone FROM Customers;";
    db.pool.query(query1, function(error, rows, fields){
        res.render('Customers', {data: rows});
    })
});

app.get('/Beer_Orders',function(req,res){
    //let query1 = "SELECT Beer_Orders.sales_ID AS ID, Beer.beer_Name AS Beer, Orders.orders_ID AS OrderID, Beer_Orders.quantity AS Quantity, Beer_Orders.total_Price AS LineTotal FROM Beer_Orders INNER JOIN Orders on Orders.orders_ID = Beer_Orders.orders_ID INNER JOIN Beer on Beer.beer_ID = Beer_Orders.beer_ID;";
    let query1 = "SELECT * FROM Beer_Orders;"
    let query2 = "SELECT * FROM Beer;";
    let query3 = "SELECT * FROM Orders;";
    db.pool.query(query1, function(error, rows, fields){
        let BeerOrders = rows;
        db.pool.query(query2, (error, rows, fields) => {
            let Beer = rows;
            db.pool.query(query3, (error, rows, fields) => {
                let Orders = rows;
                res.render('Beer_Orders', {data: BeerOrders, Beer: Beer, Orders: Orders});
            })
        })
    })
});

app.get('/', function(req, res)
{
    res.render('index');
});

/*Post Routes*/
app.post('/add-Beer-ajax', function(req, res)
{
     // Capture the incoming data and parse it back to a JS object
     let data = req.body;

     // Capture NULL values
     let style = parseInt(data.style);
     if (isNaN(style))
     {
         style = 'NULL'
     }
 
     let brewery = parseInt(data.brewery);
     if (isNaN(brewery))
     {
         brewery = 'NULL'
     }

     let inventory = parseInt(data.inventory);
     if (isNaN(inventory))
     {
         inventory = 'NULL'
     }

     let price = parseFloat(data.price);
     if (isNaN(price))
     {
         price = null;
     }

    // Create the query and run it on the database
    query1 = `INSERT INTO Beer (style_ID, brewery_ID, inventory, beer_Name, price, year) VALUES (${style}, ${brewery}, ${inventory}, "${data.name}", ${price}, ${data.year});`;
    console.log(query1);
    db.pool.query(query1, function(error, rows, fields){

        // Check to see if there was an error
        if (error) {

            // Log the error to the terminal so we know what went wrong, and send the visitor an HTTP response 400 indicating it was a bad request.
            console.log(error)
            console.log("Insert failed")
            res.sendStatus(400);
        }
        else
        {
            res.redirect('/Beer');
        }
    })
});

app.post('/add-Brewery-ajax', function(req, res)
{
     // Capture the incoming data and parse it back to a JS object
     let data = req.body;

     // Capture NULL values
     let specialty = parseInt(data.specialty);
     if (isNaN(specialty))
     {
         specialty = 'NULL'
     };
 

    // Create the query and run it on the database
    query1 = `INSERT INTO Breweries (style_ID, brewery_Name, region) VALUES (${specialty}, "${data.name}", "${data.region}");`;
    db.pool.query(query1, function(error, rows, fields){
        // Check to see if there was an error
        if (error) {

            // Log the error to the terminal so we know what went wrong, and send the visitor an HTTP response 400 indicating it was a bad request.
            console.log(error)
            console.log("Insert failed")
            res.sendStatus(400);
        }
        else
        {
            res.redirect('/Breweries');
        }
    })
});

app.post('/add-Customer-ajax', function(req, res)
{
     // Capture the incoming data and parse it back to a JS object
     let data = req.body;

    // Create the query and run it on the database
    query1 = `INSERT INTO Customers (customer_Name, address, phone) VALUES ("${data.name}", "${data.address}", "${data.phone}");`;
    db.pool.query(query1, function(error, rows, fields){
        // Check to see if there was an error
        if (error) {

            // Log the error to the terminal so we know what went wrong, and send the visitor an HTTP response 400 indicating it was a bad request.
            console.log(error)
            console.log("Insert failed")
            res.sendStatus(400);
        }
        else
        {
            res.redirect('/Customers');
        }
    })
});

app.post('/add-Style-ajax', function(req, res)
{
    // Capture the incoming data and parse it back to a JS object
    let data = req.body;

    // Create the query and run it on the database
    query1 = `INSERT INTO Styles (style_Name) VALUES ("${data.name}");`;
    db.pool.query(query1, function(error, rows, fields){
        // Check to see if there was an error
        if (error) {

            // Log the error to the terminal so we know what went wrong, and send the visitor an HTTP response 400 indicating it was a bad request.
            console.log(error)
            console.log("Insert failed")
            res.sendStatus(400);
        }
        else
        {
            res.redirect('/Styles');
        }
    })
});

app.post('/add-Order-ajax', function(req, res)
{
    // Capture the incoming data and parse it back to a JS object
    let data = req.body;

    // Create the query and run it on the database
    query1 = `INSERT INTO Orders (customer_ID, total_Sales, total_Beers, date) VALUES (${data.customer}, ${data.total}, ${data.quantity}, "${data.date}");`;
    db.pool.query(query1, function(error, rows, fields){
        // Check to see if there was an error
        if (error) {

            // Log the error to the terminal so we know what went wrong, and send the visitor an HTTP response 400 indicating it was a bad request.
            console.log(error)
            console.log("Insert failed")
            res.sendStatus(400);
        }
        else
        {
            res.redirect('/Orders');
        }
    })
});

app.post('/add-Beer_Order-ajax', function(req, res)
{
    // Capture the incoming data and parse it back to a JS object
    let data = req.body;

    // Create the query and run it on the database
    query1 = `INSERT INTO Beer_Orders (beer_ID, orders_ID, quantity, total_Price) VALUES (${data.beer}, ${data.order}, ${data.quantity}, ${data.total});`;
    db.pool.query(query1, function(error, rows, fields){
        // Check to see if there was an error
        if (error) {

            // Log the error to the terminal so we know what went wrong, and send the visitor an HTTP response 400 indicating it was a bad request.
            console.log(error)
            console.log("Insert failed")
            res.sendStatus(400);
        }
        else
        {
            res.redirect('/Beer_Orders');
        }
    })
});


/*Delete Routes*/
app.delete('/delete-Beer-ajax', function(req,res,next){
    let data = req.body;
    let BeerID = parseInt(data.id);
    let deleteBeer = `DELETE FROM Beer WHERE beer_ID = ?`;
    
    // Run the 1st query
    db.pool.query(deleteBeer, [BeerID], function(error, rows, fields){
        if (error) {
            // Log the error to the terminal so we know what went wrong, and send the visitor an HTTP response 400 indicating it was a bad request.
            console.log(error);
            res.sendStatus(400);
        }
        else {
            res.sendStatus(204);
        }
})});

app.delete('/delete-Beer_Order-ajax', function(req,res,next){
    let data = req.body;
    let Beer_OrderID = parseInt(data.id);
    let deleteBeer_Order = `DELETE FROM Beer_Orders WHERE sales_ID = ?`;
    
    // Run the 1st query
    db.pool.query(deleteBeer_Order, [Beer_OrderID], function(error, rows, fields){
        if (error) {
            // Log the error to the terminal so we know what went wrong, and send the visitor an HTTP response 400 indicating it was a bad request.
            console.log(error);
            res.sendStatus(400);
        }
        else {
            res.sendStatus(204);
        }
})});



/*Update Routes*/
app.put('/put-Beer-ajax', function(req,res){

    let data = req.body;

    let id = parseInt(data.id);
    let name = data.name;
    let brewery = parseInt(data.brewery)
    let style = parseInt(data.style);
    let year = parseInt(data.year);
    let inventory = parseInt(data.inventory);
    let price = parseFloat(data.price);

    //Handle null price formatting for SQL query.
    if(isNaN(price)){
        price = null;
    }
  

    let beerUpdate = `UPDATE Beer SET Beer.beer_Name = ?, Beer.brewery_ID = ?, Beer.style_ID = ?, Beer.year = ?, Beer.inventory = ?, Beer.price = ? WHERE Beer.beer_ID = ?;`;
  
    // Run the 1st query
    db.pool.query(beerUpdate, [name, brewery, style, year, inventory, price, id], function(error, rows, fields){
        if (error) {
            // Log the error to the terminal so we know what went wrong, and send the visitor an HTTP response 400 indicating it was a bad request.
            console.log(error);
            res.sendStatus(400);
        }

        else{
            res.sendStatus(200);
        }
  })});

/*
    LISTENER
*/
app.listen(PORT, function(){
    console.log('Express started on http://localhost:' + PORT + '; press Ctrl-C to terminate.')
});