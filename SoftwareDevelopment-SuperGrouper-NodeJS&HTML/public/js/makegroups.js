let prevGroup = [];
let currentGroup = []

// Make groups
function makegroups() {

    //save previous Group
    prevGroup = currentGroup;

    // Determine array: [number of regular groups, names per group (size), remainder, total]
    groupMathArr = groupMath();

    //Unpack values from array.
    numGroups = groupMathArr[0]
    groupSize = groupMathArr[1];
    remainder = groupMathArr[2]
    total = groupMathArr[3];

    //Shuffle names
    const names = shuffle(getNames());

    // Generate group names by category.
    category = document.getElementById("category").value;
    var groupNames = generateNames(category, numGroups);

    // Generate and display groups and store as current group.
    groupsArray = dealNames(names, numGroups, groupNames);
    displayGroups(groupsArray);
    currentGroup = groupsArray;
}


// Generate group names based on the selected category.
function generateNames(category, length) {

    var colors = ["Red", "Yellow", "Blue", "Green", "Purple", "Orange"];
    shuffledColors = shuffle(colors);

    var nameArray = [];

    // Color names array generator.
    if(category == "Color"){
        for(i = 0; i < length; i++){
            nameArray[i] = shuffledColors[i];
        }
    }

    // Number names array generator.
    if(category == "Number"){
        for(i = 0; i < length; i++){
            nameArray[i] = i + 1;
        }
    }

    return nameArray;
}

//Calculates the number of groups and remainder size, given user input and selected options.
function groupMath() {

    const groupMath = [];

    // Store total names and user requested options.
    total = parseInt(document.getElementById("totalNum").innerText);
    userNum = parseInt(document.getElementById("number").value);
    grouping = document.getElementById("grouping").value;

    if(!userNum){
        alert("Enter number of groups or number per group!");
    }

    // User requests to group by a certain number of groups.
    if(grouping == "numberof"){

        //Calculate group size and remainder size.
        const groupSize = Math.floor(total/userNum);
        const remainder = total % userNum;

        //Add to array [number of groups, size, remainder]
        groupMath[0] = userNum;
        groupMath[1] = groupSize;
        groupMath[2] = remainder;

    }

    // User requests a specific number of individuals per group.
    if(grouping == "numberper"){

        //Calculate number of groups and remainder size.
        let numGroups = Math.floor(total/userNum);
        const remainder = total % userNum;

        //If remainder increment number of groups
        if(remainder > 0){
            numGroups++;
        }

        //Add to array [number of groups, size, remainder];
        groupMath[0] = numGroups;
        groupMath[1] = userNum;
        groupMath[2] = remainder;
    }

    // Return groupNumbers array.
    groupMath[3] = total;

    return groupMath
}


// Erases the currently displayed groups and displays the groups
// passed in through the groupsArray.
function displayGroups(groupsArray){
    //Delete previous groups.
    groupDisplay = document.getElementById("groupDisplay");
    groupDisplay.innerHTML = "";
    
    //Build each group from the sub-arrays of groups Array.
    for(i = 0; i < groupsArray.length; i++){

        //Initialize display object with group name header.
        newGroupFragment = initializeGroup(groupsArray[i][0]);
        
        //Append names.
        for(j = 1; j < groupsArray[i].length; j++){

            //Get the next name
            let name = groupsArray[i][j];
            //console.log(name);

            //Add a line with name to the group.
            const newLine = document.createElement("li");
            newLine.append(name);
            newGroupFragment.append(newLine);
        }

        //Add group to document.
        groupDisplay.appendChild(newGroupFragment);
    }
}

//Randomly assign names to group arrays. Returns an array of arrays with
// each sub-array representing a group.
function dealNames(shuffledNames, numGroups, groupNames) {

    grouping = document.getElementById("grouping").value;
    groupSize = parseInt(document.getElementById("number").value);

    const namesArray = [];
    
    //Add an array for each group with title.
    for(i = 0; i < numGroups; i++){
        namesArray[i] = [];
        namesArray[i].push(groupNames[i]);
    }

    if(grouping == "numberof")
        //Deal shuffled names evenly to groups until there are no more names.
        for(i = 0; i < shuffledNames.length; i++){
            group = i % numGroups;
            slot = Math.floor(i / numGroups) + 1;
            namesArray[group][slot] = shuffledNames[i];
        }


    if(grouping == "numberper"){

        let groupIndex = 0;
        let j = 1;
        let i = 0;
        while(i < shuffledNames.length){
            while(namesArray[groupIndex].length <= groupSize && i < shuffledNames.length){
                namesArray[groupIndex][j] = shuffledNames[i];
                j++;
                i++;
            }

            j = 1;
            groupIndex++
        }
    }

    return namesArray;
}

//Shuffles the array passed in and returns the shuffled array.
//citation:https://stackoverflow.com/questions/2450954/how-to-randomize-shuffle-a-javascript-array
function shuffle(array) {
    let currentIndex = array.length,  randomIndex;
  
    // While there remain elements to shuffle.
    while (currentIndex > 0) {
  
      // Pick a remaining element.
      randomIndex = Math.floor(Math.random() * currentIndex);
      currentIndex--;
  
      // And swap it with the current element.
      [array[currentIndex], array[randomIndex]] = [
        array[randomIndex], array[currentIndex]];
    }
  
    return array;
  }

// Returns a new document fragment with group name as header.
function initializeGroup(groupName){

        //Create new unordered list object with header.
        const group = new DocumentFragment();
        const newUL = document.createElement("ul");
        newUL.classList.add("group");
        const newheader = document.createElement("h2");

        //Set header to the current group number and append to UL.
        newheader.append(groupName);
        newUL.append(newheader);
        group.append(newUL);
        
        //Return the new un-ordered list object.
        return newUL;
}

// Scans the user input table and returns a list of names.
function getNames(){

    const names = []

    //Add each row to names array.
    for(let i=0; i < total; i++) {
        var name = document.getElementById("name-table").rows[i].cells[0].children[0].value; 
        names.push(name);
    }

    if(names.length == 0){
        alert("Please enter some names on the left-hand input bar!");
    }

    return names;
}

// Displays the previously generated group.
function previousGroup(){
    displayGroups(prevGroup);
}

