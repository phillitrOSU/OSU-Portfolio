//Initialize event listeners for input.
box = document.getElementById("box1");
box.addEventListener("blur", total);

box = document.getElementById("box2");
box.addEventListener("blur", total);

box = document.getElementById("box3");
box.addEventListener("blur", total);

box = document.getElementById("box4");
box.addEventListener("blur", total);

box = document.getElementById("box5");
box.addEventListener("blur", total);

box = document.getElementById("box6");
box.addEventListener("blur", total);

box = document.getElementById("box7");
box.addEventListener("blur", total);

box = document.getElementById("box8");
box.addEventListener("blur", total);

box = document.getElementById("box1");
box.addEventListener("blur", total);

box = document.getElementById("box9");
box.addEventListener("blur", total);

box = document.getElementById("box10");
box.addEventListener("blur", total);


// Update total number of input names.
function total(old, newi){
    var total = 0;

    // Count total number of names
    for(let i=0; i < 10; i++) {
        var name = document.getElementById("name-table").rows[i].cells[0].children[0].value; 
        if(name !== ""){
            total++;
        }
    }

     // Update HTML value and text
     document.getElementById("totalNum").innerText = total;
     document.getElementById("totalNum").value = total;
    return total;
}

// Clear all names from cells.
function clearNames() {
    
    //Set total value to 0
    const total = document.getElementById("totalNum");
    total.innerText = 0;

    //Iterate through rows, deleting data.
    for(let i=0; i < 17; i++) {
        var name = document.getElementById("name-table").rows[i].cells[0].children[0];
        name.value = "";
    }
}

  
