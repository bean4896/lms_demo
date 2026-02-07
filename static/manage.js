/**
 * Internal manage page: load resources, edit title and PDF/Video URL, save.
 */
(function () {
    var resourcesUrl = window.LMS_RESOURCES_URL;
    var saveUrl = window.LMS_SAVE_URL;
    var tbody = document.getElementById('manage-tbody');
    var btnSave = document.getElementById('btn-save');
    var statusEl = document.getElementById('manage-status');
    var resources = [];

    function isPdf(item) {
        return item.type !== 'recording' && item.title && item.title.indexOf('.pdf') !== -1;
    }

    function isRecording(item) {
        return item.type === 'recording';
    }

    function setStatus(msg, isError) {
        statusEl.textContent = msg || '';
        statusEl.className = 'manage-status' + (isError ? ' error' : '');
    }

    function renderRow(item, index) {
        var tr = document.createElement('tr');
        tr.dataset.index = index;
        var typeCell = document.createElement('td');
        typeCell.textContent = item.type || '';
        typeCell.className = 'col-type';
        tr.appendChild(typeCell);

        var titleCell = document.createElement('td');
        var titleInput = document.createElement('input');
        titleInput.type = 'text';
        titleInput.className = 'input-title';
        titleInput.value = item.title || '';
        titleInput.dataset.index = index;
        titleInput.dataset.field = 'title';
        titleCell.appendChild(titleInput);
        tr.appendChild(titleCell);

        var linkCell = document.createElement('td');
        if (isRecording(item)) {
            var videoInput = document.createElement('input');
            videoInput.type = 'url';
            videoInput.className = 'input-link';
            videoInput.placeholder = 'YouTube or video URL';
            videoInput.value = item.url || '';
            videoInput.dataset.index = index;
            videoInput.dataset.field = 'url';
            linkCell.appendChild(videoInput);
        } else if (isPdf(item)) {
            var pdfInput = document.createElement('input');
            pdfInput.type = 'url';
            pdfInput.className = 'input-link';
            pdfInput.placeholder = 'Paste PDF link (URL only, no upload). Blank = demo placeholder';
            pdfInput.value = item.pdf_url || '';
            pdfInput.dataset.index = index;
            pdfInput.dataset.field = 'pdf_url';
            linkCell.appendChild(pdfInput);
        } else {
            linkCell.textContent = '—';
        }
        tr.appendChild(linkCell);
        return tr;
    }

    function loadResources() {
        setStatus('Loading…');
        var xhr = new XMLHttpRequest();
        xhr.open('GET', resourcesUrl, true);
        xhr.setRequestHeader('Accept', 'application/json');
        xhr.onreadystatechange = function () {
            if (xhr.readyState !== 4) return;
            if (xhr.status === 200) {
                try {
                    var data = JSON.parse(xhr.responseText);
                    resources = data.resources || [];
                    renderTable();
                    setStatus('');
                } catch (e) {
                    setStatus('Failed to parse response.', true);
                }
            } else {
                setStatus('Failed to load resources.', true);
            }
        };
        xhr.send();
    }

    function renderTable() {
        tbody.innerHTML = '';
        resources.forEach(function (item, index) {
            tbody.appendChild(renderRow(item, index));
        });
        // Bind input changes to update in-memory resources
        tbody.querySelectorAll('input').forEach(function (input) {
            input.addEventListener('change', function () {
                var index = parseInt(input.dataset.index, 10);
                var field = input.dataset.field;
                if (resources[index] !== undefined) {
                    if (field === 'pdf_url') {
                        resources[index].pdf_url = input.value.trim();
                    } else if (field === 'url') {
                        resources[index].url = input.value.trim();
                    } else if (field === 'title') {
                        resources[index].title = input.value.trim();
                    }
                }
            });
            input.addEventListener('input', function () {
                var index = parseInt(input.dataset.index, 10);
                var field = input.dataset.field;
                if (resources[index] !== undefined) {
                    if (field === 'pdf_url') resources[index].pdf_url = input.value.trim();
                    else if (field === 'url') resources[index].url = input.value.trim();
                    else if (field === 'title') resources[index].title = input.value.trim();
                }
            });
        });
    }

    function collectFromForm() {
        tbody.querySelectorAll('input').forEach(function (input) {
            var index = parseInt(input.dataset.index, 10);
            var field = input.dataset.field;
            if (resources[index] === undefined) return;
            if (field === 'title') resources[index].title = input.value.trim();
            else if (field === 'url') resources[index].url = input.value.trim();
            else if (field === 'pdf_url') resources[index].pdf_url = input.value.trim();
        });
    }

    function saveResources() {
        collectFromForm();
        setStatus('Saving…');
        var xhr = new XMLHttpRequest();
        xhr.open('PUT', saveUrl, true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.setRequestHeader('Accept', 'application/json');
        xhr.onreadystatechange = function () {
            if (xhr.readyState !== 4) return;
            if (xhr.status === 200) {
                try {
                    var data = JSON.parse(xhr.responseText);
                    if (data.ok) {
                        setStatus('Saved.');
                        setTimeout(function () { setStatus(''); }, 2000);
                    } else {
                        setStatus('Save failed.', true);
                    }
                } catch (e) {
                    setStatus('Save failed.', true);
                }
            } else {
                setStatus('Save failed.', true);
            }
        };
        xhr.send(JSON.stringify({ resources: resources }));
    }

    if (btnSave) btnSave.addEventListener('click', saveResources);
    loadResources();
})();
