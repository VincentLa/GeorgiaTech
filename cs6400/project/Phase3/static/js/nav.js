// Get the Sidenav
var mySidenav = document.getElementById("mySidenav");

// Get the DIV with overlay effect
var overlayBg = document.getElementById("myOverlay");

// Toggle between showing and hiding the sidenav, and add overlay effect
function w3_open() {
    if (mySidenav.style.display === 'block') {
        mySidenav.style.display = 'none';
        overlayBg.style.display = "none";
    } else {
        mySidenav.style.display = 'block';
        overlayBg.style.display = "block";
    }
}

// Close the sidenav with the close button
function w3_close() {
    mySidenav.style.display = "none";
    overlayBg.style.display = "none";
}

function resetLogin() {
    document.getElementById("username").value = "";
    document.getElementById("password").value = "";
    document.getElementById("loginMessage").innerHTML = "";
}

function resetForm(formName) {
    document.getElementById(formName).reset();
}

function checkDateFormat(dateVal) {
    var date_regex = "/^(0[1-9]|1[0-2])\/(0[1-9]|1\d|2\d|3[01])\/(19|20)\d{2}$/";

    if (!date_regex.test(dateVal))
    {
        return false;
    }
    else {
        return true;
    }
}

function searchOrderByCol(colName, tbFoodBank, tbItemType, tbStorageType, tbItemSubType, tbItemName, tbExpirationDate) {
    $.post('/inventory/searchItem/', {
        OrderByCol:colName,
        tbFoodBank:tbFoodBank,
        tbItemType:tbItemType,
        tbStorageType:tbStorageType,
        tbItemSubType:tbItemSubType,
        tbItemName:tbItemName,
        tbExpirationDate:tbExpirationDate
    }, function(result) { location.reload(); });
}
