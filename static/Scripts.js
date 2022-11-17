// Main Scripts
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

function openFilters() {
    let filterModal = document.getElementById("filterModal");
    console.log(filterModal);
    filterModal.style.display = "block";

    let filterClose = document.getElementById("closeFilter");
    filterClose.onclick = function() {
        filterModal.style.display = "none";
        

    }

}