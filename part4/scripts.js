const API_BASE_URL = 'https://your-api-url'; // REPLACE WITH YOUR ACTUAL API URL

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const placesList = document.getElementById('places-list');

    // PAGE DISPATCHER
    if (loginForm) {
        handleLoginSubmission(loginForm);
    }

    if (placesList) {
        initIndexPage();
    }
});

/* --- SHARED UTILITIES --- */
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

/* --- TASK 1: LOGIN LOGIC --- */
function handleLoginSubmission(form) {
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        try {
            const response = await fetch(`${API_BASE_URL}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });

            if (response.ok) {
                const data = await response.json();
                document.cookie = `token=${data.access_token}; path=/; SameSite=Lax`;
                window.location.href = 'index.html';
            } else {
                alert('Login Failed. Please check your credentials.');
            }
        } catch (err) {
            console.error('Login error:', err);
        }
    });
}

/* --- TASK 2: INDEX LOGIC --- */
function initIndexPage() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    // UI Auth Toggle
    if (token) {
        if (loginLink) loginLink.style.display = 'none';
        fetchPlaces(token);
    } else {
        if (loginLink) loginLink.style.display = 'block';
        fetchPlaces(); // Fetch anyway if API allows public viewing
    }

    setupPriceFilter();
}

async function fetchPlaces(token = null) {
    const headers = { 'Content-Type': 'application/json' };
    if (token) headers['Authorization'] = `Bearer ${token}`;

    try {
        const response = await fetch(`${API_BASE_URL}/places`, { headers });
        if (response.ok) {
            const places = await response.json();
            renderPlaces(places);
        }
    } catch (err) {
        console.error('Fetch places error:', err);
    }
}

function renderPlaces(places) {
    const container = document.getElementById('places-list');
    container.innerHTML = '';

    places.forEach(place => {
        const card = document.createElement('article');
        card.className = 'place-card';
        card.setAttribute('data-price', place.price_by_night);

        card.innerHTML = `
            <h3>${place.name}</h3>
            <p><strong>$${place.price_by_night}</strong> / night</p>
            <p>${place.description}</p>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        `;
        container.appendChild(card);
    });
}

function setupPriceFilter() {
    const filter = document.getElementById('price-filter');
    filter.addEventListener('change', (e) => {
        const maxPrice = e.target.value;
        const cards = document.querySelectorAll('.place-card');

        cards.forEach(card => {
            const price = parseFloat(card.getAttribute('data-price'));
            if (maxPrice === 'All' || price <= parseFloat(maxPrice)) {
                card.style.display = 'inline-block';
            } else {
                card.style.display = 'none';
            }
        });
    });
}
