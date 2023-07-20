// Main Scripts
const searchWrapper = document.querySelector(".inputs");
const inputBox = document.querySelector("input");
const suggestionsBox = document.querySelector(".suggestions-box");
let sIndex = -1;

// User pressing keys within search box
inputBox.onkeyup = (e)=> {
    let userData = e.target.value; // user input data

    let results = []
    if (userData) {

        results = titles.filter((data)=>{
            // Filter array values to lowercase and return titles which start with user entered data
            return data.toLocaleUpperCase().startsWith(userData.toLocaleUpperCase());
        });
        results = results.map((data)=>{
            return data = '<li class=\"active\" >' + data + '</li>';
        });
    } 

    // set suggestions for arrow keys
    var filtered = calculateSuggestions(results)
  
    let count = Object.keys(filtered).length - 1
    
    //If Down Arrow is pressed
    if (e.key === "ArrowDown") {
        if (sIndex === -1) {    //If not highlighted
            filtered[++sIndex].classList.add("highlight")
            select(filtered[sIndex]);
        }
        else if (sIndex === count) {    //If at last index
            filtered[sIndex].classList.remove("highlight");
            sIndex = 0;
            filtered[sIndex].classList.add("highlight");
        }
        else {      //All other cases
            filtered[sIndex].classList.remove("highlight");
            filtered[++sIndex].classList.add("highlight");
            select(filtered[sIndex]);
        }

    }
    //If Up Arrow is pressed
    else if (e.key === "ArrowUp") {
        if (sIndex === -1) {    //If not highlighted
            sIndex = count
            filtered[sIndex].classList.add("highlight");
            select(filtered[sIndex])
        }
        else if (sIndex === 0) {    //If at first index
            filtered[sIndex].classList.remove("highlight");
            sIndex = count;
            filtered[sIndex].classList.add("highlight");
        }
        else {      //All other cases
            filtered[sIndex].classList.remove("highlight");
            filtered[--sIndex].classList.add("highlight");
            select(filtered[sIndex]);
        }
    }
    else {
        // Display suggestions
        sIndex = -1;
        showSuggestions(results);
    }
}

//Function to display user selected suggestion
function select(element) {
    let selectUserData = element.textContent;
    inputBox.value = selectUserData; // set input as clicked suggestion
}

//Display search suggestions
function showSuggestions(list) {
    let listData;
    // Show own input if no suggestions
    if(!list.length) {
        var userInput = inputBox.value;
        listData = `<li>${userInput}</li>`;

    // if more than 6 suggestions, only show 6
    }else if (list.length >= 6) {
        let max = 6;
        let spliced = [];

        for (var i = 0; i < max; i++) {
            spliced.push(list[i]);
        }
       listData = spliced.join('');
    
    // Show suggestions
    } else {
        listData = list.join('');
    }

    if (typeof listData === "undefined") {
       listData = '<li> </li>';
    };
    suggestionsBox.innerHTML = listData;

    let allList = suggestionsBox.querySelectorAll(".active");
     // on click ability for suggestions
    for (let i = 0; i < allList.length; i++) {
        allList[i].setAttribute("onclick", "select(this)");
    }
}

function calculateSuggestions(list) {
    let listData;

    // if more than 6 suggestions, only calculate 6
    if (list.length >= 6) {
        let max = 6;
        let spliced = [];

        for (var i = 0; i < max; i++) {
            spliced.push(list[i]);
        }
       listData = spliced.join('');
    }
    let allList = suggestionsBox.querySelectorAll(".active");
     // on click ability for suggestions
    for (let i = 0; i < allList.length; i++) {
        allList[i].setAttribute("onclick", "select(this)");
    }
    return allList;
}

let titles = [];
function loadTitles(){
    file_path = "/static/titles.txt";
    let request = new XMLHttpRequest();
        // the function that will be called when the file is being loaded
        request.onreadystatechange = function() {
            // console.log( request.readyState );

            if( request.readyState != 4 ) { return; }
            if( request.status != 200 ) { 
                throw new Error( 'HTTP error when opening .txt file: ', request.statusText ); 
            }

            // now we know the file exists and is ready
			// load the file 

            let lines = request.responseText.split(/\r?\n/);
            lines.forEach(line=>titles.push(line));

            console.log( 'loaded ', file_path );
        };
        
        request.open( 'GET', file_path ); // initialize request. 
        request.send();                   // execute request
};

//Enlarge images
function enlarge(id) {
    let imgID = "myModal" + id.toString();
    let modal = document.getElementById(imgID);
    modal.style.display = "block";

    let close = "close" + id.toString();
    let closeButton = document.getElementById(close);
    closeButton.onclick = function() { 
        modal.style.display = "none";
    }
}

//Enlarge cloud
function enlargeCloud(id) {
    let imgID = "modal" + id.toString();
    let modal = document.getElementById(imgID);
    modal.style.display = "block";

    let close = "close" + id.toString();
    let closeButton = document.getElementById(close);
    closeButton.onclick = function() { 
        modal.style.display = "none";
    }
}

// Return to homepage
function homepage() {
    location.href = '/'
}

// Redirect to example trailpage
function exampleLink() {
    window.open("https://www.traillink.com/trail/praeri-rail-trail/",'_blank')
}

// Open link in new tab
function openTab(url) {
    window.open(url,'_blank')
}
