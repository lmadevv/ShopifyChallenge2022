baseurl = "http://127.0.0.1:5000"

function getInventoryItems() {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("GET", baseurl + "/getinventory", true);
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
            var items = JSON.parse(xmlhttp.responseText);
            var table = `<table><tr><th>Id</th><th>Name</th><th>Description</th><th>Amount</th></tr>`;
            for (i = 0; i < items.length; i++) {
                table += "<tr><td>" + items[i].id + "</td><td>" + items[i].name + "</td><td>" + items[i].description + "</td><td>" + items[i].amount + "</td></tr>"
            }
            table += "</table>"
            document.getElementById("itemList").innerHTML = table;
        }
    };
    xmlhttp.send();
}

window.onload = (event) => {
    getInventoryItems();
  };

function createInventoryItem() {
    var nameInput = document.getElementById("nameInput").value;
    if (nameInput == null || nameInput.trim() === ''){
        document.getElementById("warningText").innerHTML = "You need a name input.";
        return;
    }
    var amountInput = document.getElementById("amountInput").value;
    if (amountInput == null || amountInput.trim() === ''){
        document.getElementById("warningText").innerHTML = "You need an amount input.";
        return;
    }
    var descriptionInput = document.getElementById("descriptionInput").value;
    if (descriptionInput == null || descriptionInput.trim() === ''){
        descriptionInput = ""
    }
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("POST", baseurl + "/createinventory", true);
    xmlhttp.setRequestHeader("Content-Type", "application/json");
    xmlhttp.send(JSON.stringify({"name": nameInput, "description": descriptionInput, "amount": amountInput}));
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
            getInventoryItems();
            document.getElementById("warningText").innerHTML = ""
        }
    };
}

function deleteInventoryItem() {
    var idInput = document.getElementById("idInput").value;
    if (idInput == null || idInput.trim() === ''){
        document.getElementById("warningText").innerHTML = "You need an ID input.";
        return;
    }
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("DELETE", baseurl + "/deleteinventory/" + idInput, true);
    xmlhttp.send();
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
            getInventoryItems();   
            document.getElementById("warningText").innerHTML = ""
        } else {
            document.getElementById("warningText").innerHTML = "You need an ID that exists in the table.";
            return;
        }
    };
}

function editInventoryItem() {
    var idInput = document.getElementById("idInput").value;
    if (idInput == null || idInput.trim() === ''){
        document.getElementById("warningText").innerHTML = "You need an ID input.";
        return;
    }
    var nameInput = document.getElementById("nameInput").value;
    var descriptionInput = document.getElementById("descriptionInput").value;
    var amountInput = document.getElementById("amountInput").value;
    if (nameInput == "" && descriptionInput == "" && amountInput == "") {
        document.getElementById("warningText").innerHTML = "Please input something to change";
        return;
    }
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("PUT", baseurl + "/editinventory/" + idInput, true);
    xmlhttp.setRequestHeader("Content-Type", "application/json");
    if (nameInput != "" && descriptionInput != "" && amountInput != "") {
        xmlhttp.send(JSON.stringify({"name": nameInput, "description": descriptionInput, "amount": amountInput}));
    }
    else if (nameInput != "" && descriptionInput != "") {
        xmlhttp.send(JSON.stringify({"name": nameInput, "description": descriptionInput}));
    } else if (nameInput != "" && amountInput != "") {
        xmlhttp.send(JSON.stringify({"name": nameInput, "amount": amountInput}));
    } else if (amountInput != "" && descriptionInput != "") {
        xmlhttp.send(JSON.stringify({"description": descriptionInput, "amount": amountInput}));
    } else if (amountInput != "") {
        xmlhttp.send(JSON.stringify({"amount": amountInput}));
    } else if (nameInput != "") {
        xmlhttp.send(JSON.stringify({"name": nameInput}));
    }
    else if (descriptionInput != "") {
        xmlhttp.send(JSON.stringify({"description": descriptionInput}));
    }
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
            getInventoryItems();
            document.getElementById("warningText").innerHTML = ""
        } else {
            document.getElementById("warningText").innerHTML = "You need an ID that exists in the table.";
            return;
        }
    };
}

function exportData() {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("GET", baseurl + "/getinventory", true);
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
            var items = JSON.parse(xmlhttp.responseText);
            text = "Id, Name, Description, Amount\n"
            for (i = 0; i < items.length; i++) {
                text += items[i].id + ", " + items[i].name + ", " + items[i].description + ", " + items[i].amount + "\n"
            }
            var link = document.createElement('a');
            link.href = 'data:text/plain;charset=UTF-8,' + escape(text);
            link.download = 'output.txt';
            link.click();    
        }
    };
    xmlhttp.send();
}