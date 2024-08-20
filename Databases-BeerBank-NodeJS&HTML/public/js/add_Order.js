// Get the objects we need to modify
let addOrderForm = document.getElementById('add-Order-form-ajax');

// Modify the objects we need
addOrderForm.addEventListener("submit", function (e) {
    
    // Prevent the form from submitting
    e.preventDefault();

    // Get form fields we need to get data from
    let inputCustomer = document.getElementById("input-customer_ID");
    let inputTotal = document.getElementById("input-total_Sales");
    let inputQuantity = document.getElementById("input-total_Beers");
    let inputDate = document.getElementById("input-date");

    // Get the values from the form fields
    let customerValue = inputCustomer.value;
    let totalValue = inputTotal.value;
    let quantityValue = inputQuantity.value;
    let dateValue = inputDate.value;

    // Put our data we want to send in a javascript object
    let data = {
        customer: customerValue,
        total: totalValue,
        quantity: quantityValue,
        date: dateValue
    };

    // Setup our AJAX request
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/add-Order-ajax", true);
    xhttp.setRequestHeader("Content-type", "application/json");

    // Tell our AJAX request how to resolve
    xhttp.onreadystatechange = () => {
        if (xhttp.readyState == 4 && xhttp.status == 200) {

            // On success, add the new data to the table and refresh page.
            window.location.href = "/Orders";

        }
        else if (xhttp.readyState == 4 && xhttp.status != 200) {
            console.log("There was an error with the input.")
        }
    }

    // Send the request and wait for the response
    xhttp.send(JSON.stringify(data));
})