document.getElementById("classSelector").addEventListener("change", () => {
    document.getElementById("classForm").submit();
});
document.getElementById("dateSelector").addEventListener("change", () => {
    document.getElementById("classForm").submit();
});


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
        sel.value = this.checked ? 'presente' : 'assente';
    });
});

