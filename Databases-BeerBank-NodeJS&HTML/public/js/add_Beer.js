// Get the objects we need to modify
let addBeerForm = document.getElementById('add-Beer-form-ajax');

// Modify the objects we need
addBeerForm.addEventListener("submit", function (e) {
    
    // Prevent the form from submitting
    e.preventDefault();

    // Get form fields we need to get data from
    let inputStyle = document.getElementById("input-style_ID-ajax");
    let inputBrewery = document.getElementById("input-brewery-ajax");
    let inputInventory = document.getElementById("input-inventory");
    let inputName = document.getElementById("input-beer_Name");
    let inputPrice = document.getElementById("input-price");
    let inputYear = document.getElementById("input-year");

    // Get the values from the form fields
    let styleValue = inputStyle.value;
    let breweryValue = inputBrewery.value;
    let inventoryValue = inputInventory.value;
    let nameValue = inputName.value;
    let priceValue = inputPrice.value;
    let yearValue = inputYear.value;

    // Put our data we want to send in a javascript object
    let data = {
        style: styleValue,
        brewery: breweryValue,
        inventory: inventoryValue,
        name: nameValue,
        price: priceValue,
        year: yearValue
    };

    // Setup our AJAX request
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/add-Beer-ajax", true);
    xhttp.setRequestHeader("Content-type", "application/json");

    // Tell our AJAX request how to resolve
    xhttp.onreadystatechange = () => {
        if (xhttp.readyState == 4 && xhttp.status == 200) {

            // On success, add the new data to the table and refresh page.
            window.location.href = "/Beer";

        }
        else if (xhttp.readyState == 4 && xhttp.status != 200) {
            console.log("There was an error with the input.")
        }
    }

    // Send the request and wait for the response
    xhttp.send(JSON.stringify(data));
})