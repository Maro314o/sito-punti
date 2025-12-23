const menuBar = document.querySelector('.content nav .bx.bx-menu');
const sideBar = document.querySelector('.sidebar');

menuBar.addEventListener('click', () => {
    sideBar.classList.toggle('close');
});


/*
document.getElementById("selectAllTelefono").addEventListener("change", function () {
    const allPlus = document.querySelectorAll(".plus");
    const allMinus = document.querySelectorAll(".minus");

    if (this.checked) {
        allPlus.forEach(cb => cb.checked = true);
        allMinus.forEach(cb => cb.checked = false);
    } else {
        allPlus.forEach(cb => cb.checked = false);
        allMinus.forEach(cb => cb.checked = false);
    }
});


document.querySelector('.selectAllPresenza').addEventListener('change', function () {
    const allSelects = document.querySelectorAll('.stato');

    allSelects.forEach(sel => {
        sel.value = this.checked ? 'Presente' : 'Assenza';
    });
});
*/

// overlay

