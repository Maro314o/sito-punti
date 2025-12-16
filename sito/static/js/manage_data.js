document.getElementById("classSelector").addEventListener("change", () => {
    document.getElementById("classForm").submit();
});
document.getElementById("dateSelector").addEventListener("change", () => {
    document.getElementById("dataForm").submit();
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
        sel.value = this.checked ? 'Presente' : 'Assenza';
    });
});

// overlay

const overlay = document.getElementById('overlay');
const cancelBtn = document.getElementById('cancelBtn');
const confirmBtn = document.getElementById('confirmBtn');
const openModalBtns = document.querySelectorAll('.open-modal-btn');

openModalBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
        // Prevent event from bubbling up if necessary (though type="button" handles form submission)
        e.preventDefault();
        overlay.classList.add('open');
    });
});

function closeModal() {
    overlay.classList.remove('open');
}

cancelBtn.addEventListener('click', closeModal);
confirmBtn.addEventListener('click', closeModal);

// Close overlay if clicked outside the modal
overlay.addEventListener('click', (e) => {
    if (e.target === overlay) {
        closeModal();
    }
});

// Add functionality to add rows to the vote table
const voteTableBody = document.getElementById('voteTableBody');

if (voteTableBody) {
    voteTableBody.addEventListener('click', (e) => {
        // Check if the clicked element or its parent is the add button
        const addBtn = e.target.closest('.add-vote-row');
        // Check if the clicked element or its parent is the remove button
        const removeBtn = e.target.closest('.remove-vote-row');

        if (addBtn) {
            addVoteRow();
        } else if (removeBtn) {
            removeVoteRow(removeBtn);
        }
    });
}

function addVoteRow() {
    const tbody = document.getElementById('voteTableBody');
    const rowCount = tbody.rows.length + 1;
    const newRow = document.createElement('tr');

    // Create the new row HTML structure. 
    // Note: 'Alunno' is hardcoded as per the existing pattern.
    newRow.innerHTML = `
        <td>${rowCount}</td>
        <td>Alunno</td>
        <td><input type="number" name="voto" min="0" max="10" class="input-modern" placeholder="Voto"></td>
        <td><input type="text" name="nota" class="input-modern" placeholder="Nota opzionale"></td>
        <td class="action-cell">
            <div class="action-buttons">
                <button type="button" class="btn round-btn remove-vote-row"><i class='bx bx-minus'></i></button>
                <button type="button" class="btn round-btn add-vote-row"><i class='bx bx-plus'></i></button>
            </div>
        </td>
    `;

    tbody.appendChild(newRow);
}

function removeVoteRow(btn) {
    const row = btn.closest('tr');
    if (row) {
        row.remove();

        // Re-index rows
        const tbody = document.getElementById('voteTableBody');
        Array.from(tbody.rows).forEach((row, index) => {
            row.cells[0].textContent = index + 1;
        });
    }
}
