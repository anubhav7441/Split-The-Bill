/* ── Upload page: file preview ── */
function previewFile(input) {
    const placeholder = document.getElementById('upload-placeholder');
    const preview     = document.getElementById('upload-preview');
    const nameEl      = document.getElementById('file-name');
    if (input.files && input.files[0]) {
        const f = input.files[0];
        nameEl.textContent = f.name + ' (' + (f.size / 1024).toFixed(0) + ' KB)';
        placeholder.style.display = 'none';
        preview.style.display = 'block';
    }
}

/* Drag-over highlight */
(function () {
    const zone = document.getElementById('upload-zone');
    if (!zone) return;
    zone.addEventListener('dragover', function (e) {
        e.preventDefault();
        zone.classList.add('drag-over');
    });
    zone.addEventListener('dragleave', function () {
        zone.classList.remove('drag-over');
    });
    zone.addEventListener('drop', function (e) {
        zone.classList.remove('drag-over');
        const fi = document.getElementById('file-input');
        if (fi && e.dataTransfer.files.length) {
            fi.files = e.dataTransfer.files;
            previewFile(fi);
        }
    });
})();

/* ── Review page: add / remove item rows ── */
function addRow() {
    const tbody     = document.querySelector('#items-table tbody');
    const template  = document.getElementById('row-template');
    const countInput = document.getElementById('item_count');
    if (!tbody || !template || !countInput) return;

    const idx   = parseInt(countInput.value, 10);
    const clone = template.content.cloneNode(true);
    clone.querySelectorAll('[name]').forEach(function (el) {
        el.name = el.name.replace('IDX', idx);
    });
    tbody.appendChild(clone);
    countInput.value = idx + 1;
}

function removeRow(button) {
    const row = button.closest('tr');
    if (row) row.remove();
}

/* ── People page: toggle checkbox enable/disable ── */
function toggleItemPeople(idx, isEveryone) {
    const container = document.getElementById('people-checks-' + idx);
    if (!container) return;
    container.querySelectorAll('input[type=checkbox]').forEach(function (cb) {
        cb.disabled = isEveryone;
        if (isEveryone) cb.checked = false;
    });
}

/* ── Demo Bills Interactions ── */
async function useDemoInUpload(imgUrl, fileName, event) {
    try {
        const btn = event ? event.currentTarget : null;
        const originalText = btn ? btn.innerHTML : '';
        if (btn) {
            btn.innerHTML = '⏳ Loading...';
            btn.disabled = true;
        }

        const res = await fetch(imgUrl);
        const blob = await res.blob();
        const file = new File([blob], fileName, { type: blob.type || (fileName.endsWith('.svg') ? 'image/svg+xml' : 'image/jpeg') });

        const dt = new DataTransfer();
        dt.items.add(file);

        const fi = document.getElementById('file-input');
        if (fi) {
            fi.files = dt.files;
            previewFile(fi);
        }

        const zone = document.getElementById('upload-zone');
        if (zone) {
            zone.scrollIntoView({ behavior: 'smooth', block: 'center' });
            zone.style.borderColor = 'var(--accent-2)';
            zone.style.boxShadow = '0 0 25px var(--accent-glow)';
            setTimeout(() => {
                zone.style.borderColor = '';
                zone.style.boxShadow = '';
            }, 1800);
        }

        if (btn) {
            btn.innerHTML = '✓ Attached!';
            setTimeout(() => {
                btn.innerHTML = originalText;
                btn.disabled = false;
            }, 2000);
        }
    } catch (err) {
        console.error('Failed to attach demo bill:', err);
        alert('Could not attach image automatically. You can right-click the image to save it.');
    }
}

function filterDemoBills(cat, btn) {
    document.querySelectorAll('.demo-filter-btn').forEach(b => b.classList.remove('active'));
    if (btn) btn.classList.add('active');

    const cards = document.querySelectorAll('.demo-card');
    cards.forEach(card => {
        const cardCat = card.getAttribute('data-category') || '';
        if (cat === 'all' || cardCat.toLowerCase().includes(cat.toLowerCase())) {
            card.style.display = 'flex';
        } else {
            card.style.display = 'none';
        }
    });
}

