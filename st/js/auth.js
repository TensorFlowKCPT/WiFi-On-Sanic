function TryToLogin(){
    login = document.getElementById('login').value
    password = document.getElementById('password').value
    fetch("/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            login: login,
            password: password,
        }),
        })
        .then((response) => {
            if (!response.ok) {
            throw new Error("Ошибка сети");
            }
            return response.json();
        })
        .then((data) => {
            if(data['status']){
                window.location.href = '/promo'
            }
            else{
                console.log('Неправильный логин или пароль')
            }
        })
        .catch((error) => {
            console.error("Произошла ошибка:", error);
        });
}