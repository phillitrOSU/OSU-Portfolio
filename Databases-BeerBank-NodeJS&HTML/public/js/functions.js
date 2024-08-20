function openAddBeer() {
    document.getElementById("addBeerForm").style.display = "flex";
}

function openAddStyle() {
  document.getElementById("addStyleForm").style.display = "flex";
}

function openAddBrewery() {
  document.getElementById("addBreweryForm").style.display = "flex";
}

function openAddCustomer() {
  document.getElementById("addCustomerForm").style.display = "flex";
}

function openAddOrder() {
  document.getElementById("addOrderForm").style.display = "flex";
}


function openAddBeer_Order() {
  document.getElementById("addBeer_OrderForm").style.display = "flex";
}


function openUpdateStyle() {
  document.getElementById("updateStyleForm").style.display = "flex";
}

function openUpdateBrewery() {
  document.getElementById("updateBreweryForm").style.display = "flex";
}

function openUpdateCustomer() {
  document.getElementById("updateCustomerForm").style.display = "flex";
}

function openUpdateCustomer() {
  document.getElementById("updateCustomerForm").style.display = "flex";
}

function openUpdateOrder() {
  document.getElementById("updateOrderForm").style.display = "flex";
}

function openUpdateBeer_Order() {
  document.getElementById("updateBeer_OrderForm").style.display = "flex";
}

function closeAddBeer() {
    document.getElementById("addBeerForm").style.display = "none";
}

function closeAddBrewery() {
  document.getElementById("addBreweryForm").style.display = "none";
}

function closeAddCustomer() {
  document.getElementById("addCustomerForm").style.display = "none";
}

function closeAddStyle() {
  document.getElementById("addStyleForm").style.display = "none";
}

function closeAddOrder() {
  document.getElementById("addOrderForm").style.display = "none";
}

function closeAdd_BeerOrder() {
  document.getElementById("addBeer_OrderForm").style.display = "none";
}


function openUpdateBeer(element) {
  //Get table and row number.
  table = document.getElementById("Beer-table");
  row = element.parentNode.parentNode.rowIndex;

  //Get input elements
  id = document.getElementById("input-ID-update-ajax");
  Name = document.getElementById("input-Name-update-ajax");
  Brewery = document.getElementById("input-Brewery-update-ajax");
  Style = document.getElementById("input-Style-update-ajax");
  Year = document.getElementById("input-Year-update-ajax");
  Inventory = document.getElementById("input-Inventory-update-ajax");
  Price = document.getElementById("input-Price-update-ajax");

  //Pre fill input elements
  id.value = table.rows[row].cells[0].innerText;
  Name.value = table.rows[row].cells[1].innerText;

  //Pre-select Brewery Name by Matching to Drop Down options
  BreweryName = table.rows[row].cells[2].innerText;
  for(var i = 0; i < Brewery.options.length; i++) {
    if (Brewery.options[i].text == BreweryName) {
      Brewery.options[i].selected = true;
      break;
    }
  }

  //Pre-select Style by Matching to Drop Down options
  StyleName = table.rows[row].cells[3].innerText;
  for(var i = 0; i < Style.options.length; i++) {
    if (Brewery.options[i].text == BreweryName) {
      Style.options[i].selected = true;
      break;
    }
  }

  Year.value = parseInt(table.rows[row].cells[4].innerText);
  Inventory.value = parseInt(table.rows[row].cells[5].innerText);
  Price.value = table.rows[row].cells[6].innerText;
  
  //form = document.getElementById("updateBeerForm");
  document.getElementById("updateBeerForm").style.display = "flex";
}


function closeUpdateBeer() {
  document.getElementById("updateBeerForm").style.display = "none";
}