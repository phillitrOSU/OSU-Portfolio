
// Get the objects we need to modify
let updateBeerForm = document.getElementById('update-Beer-form-ajax');

// Modify the objects we need
updateBeerForm.addEventListener("submit", function (e) {
   
    // Prevent the form from submitting
    e.preventDefault();

    // Get form fields we need to get data from
    let inputID = document.getElementById("input-ID-update-ajax");
    let inputName = document.getElementById("input-Name-update-ajax");
    let inputBrewery = document.getElementById("input-Brewery-update-ajax");
    let inputStyle = document.getElementById("input-Style-update-ajax");
    let inputYear = document.getElementById("input-Year-update-ajax");
    let inputInventory = document.getElementById("input-Inventory-update-ajax");
    let inputPrice = document.getElementById("input-Price-update-ajax");

    // Get the values from the form fields
    let idValue = inputID.value;
    let nameValue = inputName.value;
    let breweryValue = inputBrewery.value;
    let styleValue = inputStyle.value;
    let yearValue = inputYear.value;
    let inventoryValue = inputInventory.value;
    let priceValue = inputPrice.value;

    
    // Put our data we want to send in a javascript object
    let data = {
        id: idValue,
        name: nameValue,
        brewery: breweryValue,
        style: styleValue,
        year: yearValue,
        inventory: inventoryValue,
        price: priceValue,
    }
    
    // Setup our AJAX request
    var xhttp = new XMLHttpRequest();
    xhttp.open("PUT", "/put-Beer-ajax", true);
    xhttp.setRequestHeader("Content-type", "application/json");

    // Tell our AJAX request how to resolve
    xhttp.onreadystatechange = () => {
        if (xhttp.readyState == 4 && xhttp.status == 200) {

            // On success, refresh page.
            window.location.href = "/Beer";            
        }
        else if (xhttp.readyState == 4 && xhttp.status != 200) {
            console.log("There was an error with the input.");
        }
    }

    // Send the request and wait for the response
    xhttp.send(JSON.stringify(data));
})