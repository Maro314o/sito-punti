document.getElementById("classSelector").addEventListener("change", () => {
            document.getElementById("classForm").submit();
        });
        document.getElementById("dateSelector").addEventListener("change", () => {
            document.getElementById("classForm").submit();
        });
        document.getElementById('customFileInput').addEventListener('change', function (event) {
            var fileInput = event.target;
            var fileName = fileInput.files.length ? fileInput.files[0].name : '';

            if (fileName) {
                // Mostra l'icona e il nome del file selezionato
                document.getElementById('upload-icon').style.display = 'flex';
                document.getElementById('file-name').textContent = fileName;
            } else {
                // Nasconde l'icona se non c'è nessun file selezionato
                document.getElementById('upload-icon').style.display = 'none';
            }
        });

const selectAllCheckbox = document.getElementById('selectAll');
const alunniCheckboxes = document.querySelectorAll('.alunno');

selectAllCheckbox.addEventListener('change', () => {
    alunniCheckboxes.forEach(cb => cb.checked = selectAllCheckbox.checked);
});
