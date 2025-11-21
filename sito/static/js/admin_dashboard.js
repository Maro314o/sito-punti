const sideLinks = document.querySelectorAll('.sidebar .side-menu li a:not(.logout)');

sideLinks.forEach(item => {
    const li = item.parentElement;
    item.addEventListener('click', () => {
        sideLinks.forEach(i => {
            i.parentElement.classList.remove('active');
        })
        li.classList.add('active');
    })
});

const menuBar = document.querySelector('.content nav .bx.bx-menu');
const sideBar = document.querySelector('.sidebar');

menuBar.addEventListener('click', () => {
    sideBar.classList.toggle('close');
});

const searchBtn = document.querySelector('.content nav form .form-input button');
const searchBtnIcon = document.querySelector('.content nav form .form-input button .bx');
const searchForm = document.querySelector('.content nav form');

searchBtn.addEventListener('click', function (e) {
    if (window.innerWidth < 576) {
        e.preventDefault;
        searchForm.classList.toggle('show');
        if (searchForm.classList.contains('show')) {
            searchBtnIcon.classList.replace('bx-search', 'bx-x');
        } else {
            searchBtnIcon.classList.replace('bx-x', 'bx-search');
        }
    }
});

window.addEventListener('resize', () => {
    if (window.innerWidth < 768) {
        sideBar.classList.add('close');
    } else {
        sideBar.classList.remove('close');
    }
    if (window.innerWidth > 576) {
        searchBtnIcon.classList.replace('bx-x', 'bx-search');
        searchForm.classList.remove('show');
    }
});

const toggler = document.getElementById('theme-toggle');

toggler.addEventListener('change', function () {
    if (this.checked) {
        document.body.classList.add('dark');
    } else {
        document.body.classList.remove('dark');
    }
});

/* --- Class Management Logic --- */

const mockStudents = {
    "3A": [
        { name: "Rossi Mario" },
        { name: "Bianchi Luigi" },
        { name: "Verdi Anna" },
        { name: "Neri Paolo" },
        { name: "Gialli Francesca" }
    ],
    "4B": [
        { name: "Ferrari Luca" },
        { name: "Russo Giulia" },
        { name: "Esposito Marco" },
        { name: "Romano Sofia" },
        { name: "Colombo Alessandro" }
    ],
    "5C": [
        { name: "Ricci Elena" },
        { name: "Marino Antonio" },
        { name: "Greco Beatrice" },
        { name: "Bruno Davide" },
        { name: "Gallo Chiara" }
    ]
};

const classSelector = document.getElementById('classSelector');
const studentTableBody = document.getElementById('studentTableBody');

if (classSelector && studentTableBody) {
    classSelector.addEventListener('change', function () {
        const selectedClass = this.value;
        const students = mockStudents[selectedClass] || [];
        renderTable(students);
    });
}

function renderTable(students) {
    studentTableBody.innerHTML = ''; // Clear existing rows

    students.forEach((student, index) => {
        const row = document.createElement('tr');

        row.innerHTML = `
            <td>${student.name}</td>
            <td>
                <select>
                    <option value="presente">Presente</option>
                    <option value="assente">Assente</option>
                    <option value="strategica">Assenza Strategica</option>
                </select>
            </td>
            <td><input type="checkbox" name="bug_${index}"></td>
            <td><input type="checkbox" name="telefono_${index}"></td>
            <td><input type="checkbox" name="multiverso_${index}"></td>
            <td>
                <div class="ansia-container">
                    <input type="checkbox" class="ansia-checkbox" id="ansia_${index}">
                    <select class="ansia-select" id="ansia_select_${index}">
                        <option value="passata">Passata</option>
                        <option value="non_passata">Non passata</option>
                    </select>
                </div>
            </td>
        `;

        studentTableBody.appendChild(row);
    });

    // Re-attach event listeners for the new "Domanda Ansia" checkboxes
    attachAnsiaListeners();
}

function attachAnsiaListeners() {
    const ansiaCheckboxes = document.querySelectorAll('.ansia-checkbox');
    ansiaCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function () {
            const selectId = this.id.replace('ansia_', 'ansia_select_');
            const selectElement = document.getElementById(selectId);
            if (selectElement) {
                if (this.checked) {
                    selectElement.classList.add('visible');
                } else {
                    selectElement.classList.remove('visible');
                }
            }
        });
    });
}