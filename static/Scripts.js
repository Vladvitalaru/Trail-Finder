// Main Scripts

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

//Open/close advanced filters (Not in use)
function openFilters() {
    let filterModal = document.getElementById("filterModal");
    console.log(filterModal);
    filterModal.style.display = "block";

    let filterClose = document.getElementById("closeFilter");
    filterClose.onclick = function() {
        filterModal.style.display = "none";
    }
}


const searchWrapper = document.querySelector(".inputs");
const inputBox = document.querySelector("input");
const suggestionsBox = document.querySelector(".suggestionsBox");

// User pressing keys
inputBox.onkeyup = (e)=> {
    let userData = e.target.value; // user input data
    let emptyArray = []
    if (userData) {

        emptyArray = titles.filter((data)=>{
            // Filter array values to lowercase and return titles which start with user entered data
            return data.toLocaleUpperCase().startsWith(userData.toLocaleUpperCase());
        });
        emptyArray = emptyArray.map((data)=>{
            return data = '<li class=\"active\" >' + data + '</li>';
        });
    } 
    showSuggestions(emptyArray);
}

//Function to display user selected suggestion
function select(element) {
    let selectUserData = element.textContent;
    inputBox.value = selectUserData; // set input as clicked suggestion
}

//Display search suggestions
function showSuggestions(list) {
    let listData;
    console.log(listData)
    // Show own input if no suggestions
    if(!list.length) {
        userInput = inputBox.value;
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

    if (typeof listData === 'undefined') {
       listData = '<li> </li>';
    };
    suggestionsBox.innerHTML = listData;

    let allList = suggestionsBox.querySelectorAll(".active");
     // on click ability for suggestions
    for (let i = 0; i < allList.length; i++) {
        allList[i].setAttribute("onclick", "select(this)");
    }
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
