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
            console.log(data)
        })
}