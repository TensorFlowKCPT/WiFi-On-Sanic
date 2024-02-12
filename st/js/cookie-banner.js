function setCookie(name, value, days) {
  var expires = "";
  if (days) {
      var date = new Date();
      date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
      expires = "; expires=" + date.toUTCString();
  }
  document.cookie = name + "=" + (value || "")  + expires + "; path=/";
}

const TermsDiv = document.getElementById('TermsDiv')
document.getElementById('TermsDivButton').addEventListener('click', function () {
  setCookie('Terms',true,100)
  TermsDiv.style.display = 'none'
})

// Функция для получения значения куки по имени
function getCookie(cookieName) {
  // Разбиваем строку cookie на отдельные куки
  var cookies = document.cookie.split(';');
  
  // Проходим по каждому куки
  for(var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i];
      // Удаляем пробелы из начала и конца строки
      cookie = cookie.trim();
      // Проверяем, начинается ли куки с имени, которое мы ищем
      if (cookie.indexOf(cookieName + '=') === 0) {
          // Если да, возвращаем значение куки
          return cookie.substring(cookieName.length + 1);
      }
  }
  // Если куки с указанным именем не найдено, возвращаем пустую строку
  return "";
}

// Пример использования
var TermsCookieValue = getCookie("Terms");
if(TermsCookieValue === 'true'){
  TermsDiv.style.display = 'none'
}