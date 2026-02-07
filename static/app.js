/**
 * LMS Demo – AJAX search and recommendations.
 * Sends search query to Flask backend and updates results + recommendations in real time.
 */

(function () {
    var courseId = window.LMS_COURSE_ID;
    var searchUrl = window.LMS_SEARCH_URL;
    var searchInput = document.getElementById('global-search');
    var searchStatus = document.getElementById('search-status');
    var resultsHeading = document.getElementById('results-heading');
    var resultsList = document.getElementById('results-list');
    var recommendationsBox = document.getElementById('recommendations-box');
    var recommendationsList = document.getElementById('recommendations-list');
    var hint = document.getElementById('hint');
    var debounceTimer = null;
    var DEBOUNCE_MS = 200;
    // Dummy PDF used for all Preview/Download buttons (single placeholder file)
    var DUMMY_PDF_URL = window.LMS_DUMMY_PDF_URL || 'https://www.w3.org/WAI/demos/bad/after.pdf';
    var TYPE_ICONS = { lecture: '\uD83D\uDCDA', tutorial: '\uD83D\uDCCB', assignment: '\uD83D\uDCDD', project: '\uD83D\uDCC1', recording: '\u25B6\uFE0F' };

    function renderResource(item) {
        var li = document.createElement('li');
        if (item.type) li.classList.add(item.type);
        var typeSpan = document.createElement('span');
        typeSpan.className = 'resource-type';
        var icon = TYPE_ICONS[item.type] || '';
        typeSpan.textContent = icon ? (icon + ' ' + (item.type || '')) : (item.type || '');
        li.appendChild(typeSpan);
        var titleSpan = document.createElement('span');
        titleSpan.className = 'resource-title';
        if (item.url && item.type === 'recording') {
            var a = document.createElement('a');
            a.href = item.url;
            a.target = '_blank';
            a.rel = 'noopener noreferrer';
            a.textContent = item.title || '';
            a.className = 'resource-link';
            titleSpan.appendChild(a);
        } else {
            titleSpan.textContent = item.title || '';
        }
        li.appendChild(titleSpan);
        var isPdf = item.title && item.title.indexOf('.pdf') !== -1;
        if (isPdf) {
            var pdfUrl = (item.pdf_url && item.pdf_url.trim()) ? item.pdf_url.trim() : DUMMY_PDF_URL;
            var actions = document.createElement('span');
            actions.className = 'resource-actions';
            var previewBtn = document.createElement('a');
            previewBtn.href = pdfUrl;
            previewBtn.target = '_blank';
            previewBtn.rel = 'noopener noreferrer';
            previewBtn.className = 'btn-pdf btn-preview';
            previewBtn.textContent = 'Preview';
            var downloadBtn = document.createElement('a');
            downloadBtn.href = pdfUrl;
            downloadBtn.download = item.title || 'document.pdf';
            downloadBtn.className = 'btn-pdf btn-download';
            downloadBtn.textContent = 'Download';
            actions.appendChild(previewBtn);
            actions.appendChild(downloadBtn);
            li.appendChild(actions);
        }
        return li;
    }

    function showResults(data, query) {
        var results = data.results || [];
        var recommendations = data.recommendations || [];

        resultsHeading.textContent = query
            ? (results.length === 0 ? 'No matching resources' : 'Search results')
            : 'All resources';
        if (!query && results.length === 0) {
            resultsHeading.textContent = 'No resources';
        }
        resultsList.innerHTML = '';
        results.forEach(function (item) {
            resultsList.appendChild(renderResource(item));
        });

        recommendationsList.innerHTML = '';
        if (recommendations.length > 0) {
            recommendationsBox.classList.remove('hidden');
            recommendations.forEach(function (item) {
                recommendationsList.appendChild(renderResource(item));
            });
        } else {
            recommendationsBox.classList.add('hidden');
        }
    }

    function setStatus(msg) {
        searchStatus.textContent = msg || '';
    }

    function doSearch() {
        var q = searchInput.value.trim();
        hint.style.display = q ? 'none' : 'block';
        setStatus('Searching…');

        var url = searchUrl + (q ? '?q=' + encodeURIComponent(q) : '');
        var xhr = new XMLHttpRequest();
        xhr.open('GET', url, true);
        xhr.setRequestHeader('Accept', 'application/json');
        xhr.onreadystatechange = function () {
            if (xhr.readyState !== 4) return;
            setStatus('');
            if (xhr.status === 200) {
                try {
                    var data = JSON.parse(xhr.responseText);
                    showResults(data, q);
                } catch (e) {
                    setStatus('Could not parse results.');
                }
            } else {
                setStatus('Search failed. Please try again.');
            }
        };
        xhr.send();
    }

    function onInput() {
        if (debounceTimer) clearTimeout(debounceTimer);
        debounceTimer = setTimeout(doSearch, DEBOUNCE_MS);
    }

    if (searchInput) {
        searchInput.addEventListener('input', onInput);
        searchInput.addEventListener('keydown', function (e) {
            if (e.key === 'Enter') {
                if (debounceTimer) clearTimeout(debounceTimer);
                doSearch();
            }
        });
        // Show all resources when course page loads (no search yet)
        doSearch();
    }
})();
