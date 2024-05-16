var previusRace;

function selectRace(event) {
    var raceSelected = event.currentTarget;
    var radio = raceSelected.getElementsByTagName("input");
    radio[0].checked = true;
    if (previusRace != null) {
        previusRace.style.backgroundColor = "#D62828"; //return color
    }
    raceSelected.style.backgroundColor = "#ff6f6f"; //give new color
    previusRace = raceSelected; //save the new div
}

var previusItem;
  
function selectItem(event) {
    var raceSelected = event.currentTarget;
    var radio = raceSelected.getElementsByTagName("input");
    radio[0].checked = true;
    if (previusItem != null) {
        previusItem .style.backgroundColor = "#D62828"; //return color
    }
    raceSelected.style.backgroundColor = "#ff6f6f"; //give new color
    previusItem  = raceSelected; //save the new div
}

var previusWeapon;
 
function selectWeapon(event) {
    var raceSelected = event.currentTarget;
    var radio = raceSelected.getElementsByTagName("input");
    radio[0].checked = true;
    if (previusWeapon != null) {
        previusWeapon.style.backgroundColor = "#D62828"; //return color
    }
    raceSelected.style.backgroundColor = "#ff6f6f"; //give new color
    previusWeapon = raceSelected; //save the new div
} 

var previusGift;
 
function selectGift(event) {
    var raceSelected = event.currentTarget;
    var radio = raceSelected.getElementsByTagName("input");
    radio[0].checked = true;
    if (previusGift != null) {
        previusGift.style.backgroundColor = "#D62828"; //return color
    }
    raceSelected.style.backgroundColor = "#ff6f6f"; //give new color
    previusGift = raceSelected; //save the new div
} 

