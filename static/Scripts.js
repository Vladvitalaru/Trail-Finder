// Main Scripts
function enlarge(id) {
    let img = document.getElementById(id)
    let imgID = "myModal" + id.toString();
    let modal = document.getElementById(imgID);
    modal.style.display = "block"

    let close = "close" + id.toString()
    let closeButton = document.getElementById(close);
    closeButton.onclick = function() { 
        modal.style.display = "none";
        console.log("test");
       }
}
