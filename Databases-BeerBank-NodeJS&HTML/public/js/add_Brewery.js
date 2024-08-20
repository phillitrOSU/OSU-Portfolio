// Get the objects we need to modify
let addBreweryForm = document.getElementById('add-Brewery-form-ajax');

// Modify the objects we need
addBreweryForm.addEventListener("submit", function (e) {
    
    // Prevent the form from submitting
    e.preventDefault();

    // Get form fields we need to get data from
    let inputName = document.getElementById("input-brewery_Name");
    let inputSpecialty = document.getElementById("input-specialty");
    let inputRegion = document.getElementById("input-region");


    // Get the values from the form fields
    let nameValue = inputName.value;
    let specialtyValue = inputSpecialty.value;
    let regionValue = inputRegion.value;

    // Put our data we want to send in a javascript object
    let data = {
        name: nameValue,
        specialty: specialtyValue,
        region: regionValue
    };

    // Setup our AJAX request
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/add-Brewery-ajax", true);
    xhttp.setRequestHeader("Content-type", "application/json");

    // Tell our AJAX request how to resolve
    xhttp.onreadystatechange = () => {
        if (xhttp.readyState == 4 && xhttp.status == 200) {

            // On success, add the new data to the table and refresh page.
            window.location.href = "/Breweries";

        }
        else if (xhttp.readyState == 4 && xhttp.status != 200) {
            console.log("There was an error with the input.")
        }
    }

    // Send the request and wait for the response
    xhttp.send(JSON.stringify(data));
})