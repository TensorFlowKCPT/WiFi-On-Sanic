const cookieBannerButton = document.querySelector(".termsOfUs button");
const cookieBanner = document.querySelector(".termsOfUs");
cookieBannerButton.addEventListener("click", () => {
  cookieBanner.style.display = "none";
});
