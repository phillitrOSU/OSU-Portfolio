// Get the objects we need to modify
let addStyleForm = document.getElementById('add-Style-form-ajax');

// Modify the objects we need
addStyleForm.addEventListener("submit", function (e) {
    
    // Prevent the form from submitting
    e.preventDefault();

    // Get form fields we need to get data from
    let inputName = document.getElementById("input-style_Name");

    // Get the values from the form fields
    let nameValue = inputName.value;

    // Put our data we want to send in a javascript object
    let data = {
        name: nameValue
    };

    // Setup our AJAX request
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/add-Style-ajax", true);
    xhttp.setRequestHeader("Content-type", "application/json");

    // Tell our AJAX request how to resolve
    xhttp.onreadystatechange = () => {
        if (xhttp.readyState == 4 && xhttp.status == 200) {

            // On success, add the new data to the table and refresh page.
            window.location.href = "/Styles";

        }
        else if (xhttp.readyState == 4 && xhttp.status != 200) {
            console.log("There was an error with the input.")
        }
    }

    // Send the request and wait for the response
    xhttp.send(JSON.stringify(data));
})