document.addEventListener('DOMContentLoaded', function () {
    const input = document.getElementById('username-search');
    const suggestionsBox = document.getElementById('suggestions');

    let currentResults = [];
    let selectedIndex = -1;

    function hideSuggestions() {
        suggestionsBox.innerHTML = '';
        suggestionsBox.style.display = 'none';
        currentResults = [];
        selectedIndex = -1;
    }

    function goToProfile(url) {
        window.location.href = url;
    }

    function renderSuggestions(results) {
        suggestionsBox.innerHTML = '';
        currentResults = results;
        selectedIndex = -1;

        if (!results.length) {
            hideSuggestions();
            return;
        }

        results.forEach((user, index) => {
            const item = document.createElement('a');
            item.className = 'suggestion-item';
            item.href = user.profile_url;
            item.textContent = user.username;
            item.dataset.index = index;

            item.addEventListener('mouseenter', function () {
                selectedIndex = index;
                updateActiveSuggestion();
            });

            suggestionsBox.appendChild(item);
        });

        suggestionsBox.style.display = 'block';
    }

    function updateActiveSuggestion() {
        const items = suggestionsBox.querySelectorAll('.suggestion-item');

        items.forEach(item => item.classList.remove('active'));

        if (selectedIndex >= 0 && items[selectedIndex]) {
            items[selectedIndex].classList.add('active');
        }
    }

    async function fetchSuggestions(query) {
        if (!query) {
            hideSuggestions();
            return;
        }

        try {
            const response = await fetch(SEARCH_USERS_URL + "?q=" + encodeURIComponent(query));
            const data = await response.json();
            renderSuggestions(data.results);
        } catch (error) {
            hideSuggestions();
        }
    }

    input.addEventListener('input', function () {
        const query = input.value.trim();
        fetchSuggestions(query);
    });

    input.addEventListener('keydown', function (e) {
        const items = suggestionsBox.querySelectorAll('.suggestion-item');

        if (suggestionsBox.style.display !== 'block' || !items.length) {
            return;
        }

        if (e.key === 'ArrowDown') {
            e.preventDefault();
            selectedIndex++;
            if (selectedIndex >= items.length) {
                selectedIndex = 0;
            }
            updateActiveSuggestion();
        }

        else if (e.key === 'ArrowUp') {
            e.preventDefault();
            selectedIndex--;
            if (selectedIndex < 0) {
                selectedIndex = items.length - 1;
            }
            updateActiveSuggestion();
        }

        else if (e.key === 'Enter') {
            if (selectedIndex >= 0 && currentResults[selectedIndex]) {
                e.preventDefault();
                goToProfile(currentResults[selectedIndex].profile_url);
            }
        }

        else if (e.key === 'Escape') {
            hideSuggestions();
        }
    });

    document.addEventListener('click', function (e) {
        if (!suggestionsBox.contains(e.target) && e.target !== input) {
            hideSuggestions();
        }
    });
});