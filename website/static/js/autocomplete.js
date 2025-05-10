const apiKey = window.MAPBOX_API_KEY;

const destinationInput = document.getElementById('step-destination');
const suggestionBox = document.getElementById('suggestions');

destinationInput?.addEventListener('input', async () => {
    const query = destinationInput.value.trim();
    suggestionBox.innerHTML = '';
    if (query.length < 2) return;

    try {
        const url = `https://api.mapbox.com/geocoding/v5/mapbox.places/${encodeURIComponent(query)}.json?types=place&autocomplete=true&limit=5&access_token=${apiKey}`;
        const response = await fetch(url);
        const data = await response.json();

        // Defensive check AFTER fetching the data
        if (!data || !Array.isArray(data.features)) {
            console.error('Unexpected Mapbox response:', data);
            return;
        }

        if (data.features.length === 0) {
            suggestionBox.classList.add('hidden');
            return;
        } else {
            suggestionBox.classList.remove('hidden');
        }

        data.features.forEach(feature => {
            const li = document.createElement('li');
            li.textContent = feature.place_name;
            li.addEventListener('click', () => {
                destinationInput.value = feature.place_name;
                suggestionBox.innerHTML = '';
            });
            suggestionBox.appendChild(li);
        });
    } catch (error) {
        console.error('Mapbox API error:', error);
    }
});