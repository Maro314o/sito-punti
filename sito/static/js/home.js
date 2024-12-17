let menu = document.querySelector('#menu-icon')
let navbarra = document.querySelector('.navbarra')

menu.onclick = () => {
    menu.classList.toggle('bx-x')
    navbarra.classList.toggle('open')
}

const sr = ScrollReveal({
    distance: '65px',
    duration: 2600,
    delay: 450,
    reset: true
})

sr.reveal('.bozo-testo',{delay:200, origin: 'top'});
