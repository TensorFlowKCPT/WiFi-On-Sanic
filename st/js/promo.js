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