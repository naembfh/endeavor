const navMenu = document.getElementById("nav-menu");
const navLink = document.querySelectorAll(".nav-link");
const hamburger = document.getElementById("hamburger");

hamburger.addEventListener("click", ()=> {
    console.log('click')
    navMenu.classList.toggle("left-[0]");
    hamburger.classList.toggle("fi fi-rr-cross-small");
})

navLink.forEach(link=> {
    link.addEventListener("click" , () => {
        navMenu.classList.toggle("left-[0]");
        hamburger.classList.toggle("fi fi-rr-cross-small");
    })
})