function Unauthorise(){
    console.log(123)
    document.cookie = "session=; expires=Thu, 01 Jan 1970 00:00:00 UTC;";
    location.reload()
}