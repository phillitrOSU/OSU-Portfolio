// Get the objects we need to modify
let addCustomerForm = document.getElementById('add-Customer-form-ajax');

// Modify the objects we need
addCustomerForm.addEventListener("submit", function (e) {
    
    // Prevent the form from submitting
    e.preventDefault();

    // Get form fields we need to get data from
    let inputName = document.getElementById("input-customer_Name");
    let inputAddress = document.getElementById("input-address");
    let inputPhone = document.getElementById("input-phone");

    // Get the values from the form fields
    let nameValue = inputName.value;
    let addressValue = inputAddress.value;
    let phoneValue = inputPhone.value;

    // Put our data we want to send in a javascript object
    let data = {
        name: nameValue,
        address: addressValue,
        phone: phoneValue
    };

    // Setup our AJAX request
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/add-Customer-ajax", true);
    xhttp.setRequestHeader("Content-type", "application/json");

    // Tell our AJAX request how to resolve
    xhttp.onreadystatechange = () => {
        if (xhttp.readyState == 4 && xhttp.status == 200) {

            // On success, add the new data to the table and refresh page.
            window.location.href = "/Customers";

        }
        else if (xhttp.readyState == 4 && xhttp.status != 200) {
            console.log("There was an error with the input.")
        }
    }

    // Send the request and wait for the response
    xhttp.send(JSON.stringify(data));
})