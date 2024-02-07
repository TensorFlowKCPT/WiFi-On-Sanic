const emailDiv = document.getElementById("emailDiv");
const emailInput = document.getElementById("emailInput");
const codeDiv = document.getElementById("codeDiv");
const incorrectEmail = document.getElementById("incorrectEmail");
const sendEmailButton = document.getElementById("sendEmailButton");
const recoveryCodeInput = document.getElementById("recoveryCodeInput");
const ChangePasswordDiv = document.getElementById("ChangePasswordDiv");
const passwordInput = document.getElementById("passwordInput");
const passwordInput2 = document.getElementById("passwordInput2");
const TryCodeButton = document.getElementById("TryCodeButton");
const passwordsUnmatched = document.getElementById("passwordsUnmatched");
const codesUnmatched = document.getElementById("codesUnmatched");
const UpdatePasswordButton = document.getElementById("UpdatePasswordButton");

function SendRecoveryEmail() {
  sendEmailButton.disabled = true;
  var email = emailInput.value;
  const data = {
    email: email,
  };
  fetch("/send_recovery_email", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data === "ok") {
        emailDiv.style.display = "none";
        codeDiv.style.display = "flex";
      } else if (data === "usernotfound") {
        incorrectEmail.style.display = "flex";
        sendEmailButton.disabled = false;
      }
    });
}

function TryCode() {
  TryCodeButton.disabled = true;
  var code = recoveryCodeInput.value;
  const data = {
    code: code,
  };
  fetch("/send_recovery_code", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data === "ok") {
        codeDiv.style.display = "none";
        ChangePasswordDiv.style.display = "flex";
      } else if (data === "incorrectcode") {
        codesUnmatched.style.display = "flex";
        TryCodeButton.disabled = false;
      }
    });
}

function UpdatePassword() {
  UpdatePasswordButton.disabled = true;
  if (passwordInput.value != passwordInput2.value) {
    passwordsUnmatched.style.display = "flex";
    UpdatePasswordButton.disabled = false;
    return;
  }
  var password = passwordInput.value;
  const data = {
    password: password,
  };
  fetch("/recovery_update_password", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data === "ok") {
        window.location.href = "/auth";
      }
    });
}
