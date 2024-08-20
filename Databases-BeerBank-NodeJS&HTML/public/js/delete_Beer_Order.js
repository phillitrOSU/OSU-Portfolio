function deleteBeer_Order(Beer_OrderID) {
    // Put our data we want to send in a javascript object
    let data = {
        id: Beer_OrderID
    };

    // Setup our AJAX request
    var xhttp = new XMLHttpRequest();
    xhttp.open("DELETE", "/delete-Beer_Order-ajax", true);
    xhttp.setRequestHeader("Content-type", "application/json");

    // Tell our AJAX request how to resolve
    xhttp.onreadystatechange = () => {
        if (xhttp.readyState == 4 && xhttp.status == 204) {

            // Add the new data to the table
            deleteRow(Beer_OrderID);

        }
        else if (xhttp.readyState == 4 && xhttp.status != 204) {
            console.log("There was an error with the input.")
        }
    }
    // Send the request and wait for the response
    xhttp.send(JSON.stringify(data));
}


function deleteRow(Beer_OrderID){
    let table = document.getElementById("Beer_Orders-table");
    for (let i = 0, row; row = table.rows[i]; i++) {
       console.log(table.rows[i].cells[0])
       //iterate through rows
       //rows would be accessed using the "row" variable assigned in the for loop
       if (table.rows[i].cells[0].innerText == Beer_OrderID) {
            table.deleteRow(i);
            break;
       }
    }
}