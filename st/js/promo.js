const create = document.getElementById("create-application")
const sells = document.getElementById("sells-application")
const history = document.getElementById("history-applications")

function createPage(){
    create.style.display = 'block';
    sells.style.display = 'none';
    history.style.display = 'none';
}
function sellsPage(){
    create.style.display = 'none';
    sells.style.display = 'block';
    history.style.display = 'none';
}
function historyPage(){
    create.style.display = 'none';
    sells.style.display = 'none';
    history.style.display = 'block';
}
function sendlead(){
    var address = document.getElementById('address-input').value
    var phone = document.getElementById('clientNumber-input').value
    var clientName = document.getElementById('clientName-input').value
    const data = {
        Address:address,
        Phone:phone,
        Name:clientName
        };
    fetch("/send_partner_lead", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
        })
        .then((response) => response.json())
        .then((data) => {
            location.reload()
        })
}
// КОД ДЛЯ ПОИСКОВИКА
const SearchBox = document.getElementById("address-input");
const url ="https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address";
const token = "37246a81de5e3317c98fb92126a5e5bf19aae2b2";
function CheckAddress(clicked) {
    var query = document.getElementById("address-input").value;
    const suggestionsContainer = document.getElementById("suggestions-container");
    if (query == "") {
    suggestionsContainer.innerHTML = ""
    }
    var options = {
    method: "POST",
    mode: "cors",
    headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
        Authorization: "Token " + token,
    },
    body: JSON.stringify({ query: query, count: 5 }),
    };
    fetch(url, options)
    .then((response) => response.text())
    .then(async (result) => {
        const suggestions = JSON.parse(result)
        .suggestions.filter((suggestion) => suggestion.data.fias_level < 10)
        .map((suggestion) => suggestion);
        setSuggestions(suggestions.map((suggestion) => suggestion.value));
    })
    .catch((error) => console.log("error", error));
}
const suggestionsContainer = document.getElementById("suggestions-container");
function setSuggestions(suggestions) {
    suggestionsContainer.innerHTML = "";
    suggestions.forEach((element) => {
        suggestion = document.createElement("div");
        suggestion.innerHTML = element;
        suggestion.onclick = function () {
        SelectSuggestion(element);
        };
        suggestionsContainer.appendChild(suggestion);
    });
}
function SelectSuggestion(text) {
    SearchBox.value = text;
    CheckAddress(true);
}
document.getElementById("address-input").addEventListener("oninput", CheckAddress());