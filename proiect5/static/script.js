document.addEventListener('DOMContentLoaded', () => {
    const btnShowForm = document.getElementById('btnShowForm');
    const formContainer = document.getElementById('formContainer');
    const submitBtn = document.getElementById('submitBtn');
    const btnCancel = document.getElementById('btnCancel');

    const itemNameInput = document.getElementById('itemName');
    const itemPriceInput = document.getElementById('itemPrice');
    const itemReviewInput = document.getElementById('itemReview');

    const itemsTableBody = document.querySelector('#itemsTable tbody');

    let editMode = false;
    let editItemId = null;

    btnShowForm.addEventListener('click', () => {
        showForm();
    });

    btnCancel.addEventListener('click', () => {
        hideForm();
    });

    function showForm() {
        formContainer.style.display = 'flex';
        btnShowForm.style.display = 'none';
        editMode = false;
        editItemId = null;
        clearForm();
    }

    function hideForm() {
        formContainer.style.display = 'none';
        btnShowForm.style.display = 'inline-block';
        clearForm();
        editMode = false;
        editItemId = null;
    }

    function clearForm() {
        itemNameInput.value = '';
        itemPriceInput.value = '';
        itemReviewInput.value = '';
        submitBtn.textContent = 'Trimite';
    }

    function loadItems() {
        fetch('/items')
            .then(res => res.json())
            .then(data => {
                itemsTableBody.innerHTML = '';
                data.forEach(item => {
                    const tr = document.createElement('tr');

                    tr.innerHTML = `
                        <td>${item.id}</td>
                        <td>${item.name}</td>
                        <td>${item.price.toFixed(2)} RON</td>
                        <td>${item.review.toFixed(1)}</td>
                        <td>
                            <button class="editBtn" data-id="${item.id}">Modifică</button>
                            <button class="deleteBtn" data-id="${item.id}" style="background-color:#e74c3c; margin-left:5px;">Șterge</button>
                        </td>`;

                    itemsTableBody.appendChild(tr);
                });

                // Adaug event listeners pentru butoanele Modifică și Șterge
                document.querySelectorAll('.editBtn').forEach(btn => {
                    btn.addEventListener('click', () => {
                        const id = btn.getAttribute('data-id');
                        enterEditMode(id);
                    });
                });
                document.querySelectorAll('.deleteBtn').forEach(btn => {
                    btn.addEventListener('click', () => {
                        const id = btn.getAttribute('data-id');
                        deleteItem(id);
                    });
                });
            })
            .catch(err => {
                alert("Eroare la încărcarea articolelor.");
                console.error('Eroare:', err);
            });
    }

    function submitItem() {
        const name = itemNameInput.value.trim();
        const price = parseFloat(itemPriceInput.value);
        const review = parseFloat(itemReviewInput.value);

        if (!name) {
            alert('Completează numele articolului!');
            return;
        }
        if (isNaN(price) || price < 0) {
            alert('Preț invalid!');
            return;
        }
        if (isNaN(review) || review < 1 || review > 5) {
            alert('Review trebuie să fie între 1 și 5!');
            return;
        }

        const itemData = { name, price, review };

        if (editMode && editItemId) {
            // Actualizare articol
            fetch('/items/' + editItemId, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(itemData)
            })
                .then(res => res.json())
                .then(data => {
                    if (data.eroare) {
                        alert('Eroare: ' + data.eroare);
                    } else {
                        alert('Articol actualizat cu succes!');
                        hideForm();
                        loadItems();
                    }
                })
                .catch(() => alert('Eroare la actualizare.'));
        } else {
            // Creare articol nou
            fetch('/items', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(itemData)
            })
                .then(res => res.json())
                .then(data => {
                    if (data.eroare) {
                        alert('Eroare: ' + data.eroare);
                    } else {
                        alert('Articol adăugat cu succes!');
                        hideForm();
                        loadItems();
                    }
                })
                .catch(() => alert('Eroare la adăugare.'));
        }
    }

    function enterEditMode(id) {
        fetch('/items/' + id)
            .then(res => res.json())
            .then(item => {
                editMode = true;
                editItemId = id;
                formContainer.style.display = 'flex';
                btnShowForm.style.display = 'none';

                itemNameInput.value = item.name;
                itemPriceInput.value = item.price;
                itemReviewInput.value = item.review;

                submitBtn.textContent = 'Actualizează';
            })
            .catch(() => alert('Eroare la încărcarea articolului.'));
    }

    function deleteItem(id) {
        if (confirm('Sigur dorești să ștergi articolul cu ID ' + id + '?')) {
            fetch('/items/' + id, { method: 'DELETE' })
                .then(res => {
                    if (res.ok) {
                        alert('Articol șters cu succes.');
                        loadItems();
                    } else {
                        alert('Eroare la ștergere.');
                    }
                })
                .catch(() => alert('Eroare la ștergere.'));
        }
    }

    submitBtn.addEventListener('click', submitItem);

    loadItems();
});
