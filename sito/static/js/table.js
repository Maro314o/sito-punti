
const overlay = document.getElementById('overlay');
const cancelBtn = document.getElementById('confirmBtn');

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
            addVoteRow(addBtn);
        } else if (removeBtn) {
            removeVoteRow(removeBtn);
        }
    });
}

function addVoteRow(btn) {
    const row = btn.closest('tr');
    const studentId = row.dataset.studentId;
    const votesContainer = row.querySelector('.votes-container');

    const newRow = document.createElement('div');
	const voteRow = btn.closest('.vote-row');
    const container = voteRow.parentElement;

    const i=container.children.length;
    newRow.classList.add('vote-row');

    newRow.innerHTML = `
									  <input type="number" name="${studentId}_Voto_${i}" min="0" max="10" step="0.5"
																									  class="input-modern vote-input" placeholder="Voto">
									  <select name="${studentId}_tipo-Voto_${i}" class="input-modern note-input">
										  <option value="Verifica">Verifica</option>
										  <option value="Interrogazione">Interrogazione</option>
										  <option value="Progetto">Progetto</option>
									  </select>
									  <div class="action-buttons">
										  <button type="button" class="btn round-btn remove-vote-row"><i class='bx bx-minus'></i></button>
										  <button type="button" class="btn round-btn add-vote-row"><i class='bx bx-plus'></i></button>
									  </div>
    `;

    votesContainer.appendChild(newRow);
}

function removeVoteRow(btn) {
    const voteRow = btn.closest('.vote-row');
    const container = voteRow.parentElement;

    if (container.children.length > 1) {
        voteRow.remove();
    } else {
        // If it's the last row, just clear the values
        const inputs = voteRow.querySelectorAll('input, select');
        inputs.forEach(input => input.value = '');
    }
}
