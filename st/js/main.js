const SearchBox = document.getElementById("SearchBox")
const url = "http://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address";
const token = "37246a81de5e3317c98fb92126a5e5bf19aae2b2";
function CheckAddress(){
    var query = SearchBox.value
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
        console.log(JSON.parse(result))
        const suggestions = JSON.parse(result).suggestions.filter(
            (suggestion) => suggestion.data.fias_level < 9
            ).map((suggestion) => suggestion);
        if (suggestions[0].value === query&&suggestions[0].data.fias_level==8) {
            window.location.href = "/tariffs?address=" + query;
        }
        setSuggestions(suggestions.map((suggestion) => suggestion.value));
      })
      .catch((error) => console.log("error", error));
}
const suggestionsContainer = document.getElementById("SuggestionsContainer")
function setSuggestions(suggestions){
    suggestionsContainer.innerHTML = ""
    suggestions.forEach(element => {
        suggestion = document.createElement("div")
        suggestion.innerHTML = element
        suggestion.onclick =  function () {SelectSuggestion(element)}
        suggestionsContainer.appendChild(suggestion)
    });
    
}
function SelectSuggestion(text){
    SearchBox.value = text
    CheckAddress()
}