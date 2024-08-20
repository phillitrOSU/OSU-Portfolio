// Get the objects we need to modify
let addBeer_OrderForm = document.getElementById('add-Beer_Order-form-ajax');

// Modify the objects we need
addBeer_OrderForm.addEventListener("submit", function (e) {
    
    // Prevent the form from submitting
    e.preventDefault();

    // Get form fields we need to get data from
    let inputBeer = document.getElementById("input-beer_ID");
    let inputOrder = document.getElementById("input-order_ID");
    let inputQuantity = document.getElementById("input-quantity");
    let inputTotal = document.getElementById("input-total_Price");

    // Get the values from the form fields
    let beerValue = inputBeer.value;
    let orderValue = inputOrder.value;
    let quantityValue = inputQuantity.value;
    let totalValue = inputTotal.value;

    // Put our data we want to send in a javascript object
    let data = {
        beer: beerValue,
        order: orderValue,
        quantity: quantityValue,
        total: totalValue
    };

    // Setup our AJAX request
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/add-Beer_Order-ajax", true);
    xhttp.setRequestHeader("Content-type", "application/json");

    // Tell our AJAX request how to resolve
    xhttp.onreadystatechange = () => {
        if (xhttp.readyState == 4 && xhttp.status == 200) {

            // On success, add the new data to the table and refresh page.
            window.location.href = "/Beer_Orders";

        }
        else if (xhttp.readyState == 4 && xhttp.status != 200) {
            console.log("There was an error with the input.")
        }
    }

    // Send the request and wait for the response
    xhttp.send(JSON.stringify(data));
})