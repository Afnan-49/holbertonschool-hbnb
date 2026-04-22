/**
 * HBnB - Main Application Script
 * Handles Login, Places List, and Place Details
 */

// 1. CONFIGURATION TOGGLE
const isLocal = true; 
const API_BASE_URL = isLocal ? 'http://localhost:5000' : 'https://your-deployed-api.com';

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const placesListContainer = document.getElementById('places-list');
    const placeDetailsContainer = document.getElementById('place-details');

    // --- Page Dispatcher ---
    if (loginForm) {
        handleLoginSubmission(loginForm);
    }

    if (placesListContainer) {
        initPlacesPage(); // Renamed for clarity since we use place.html
    }

    if (placeDetailsContainer) {
        initPlaceDetailsPage();
    }
});

/* ==========================================
   SHARED UTILITIES
   ========================================== */

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

/* ==========================================
   TASK 1: LOGIN PAGE LOGIC
   ========================================== */

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
                // Store JWT token in a cookie
                document.cookie = `token=${data.access_token}; path=/; SameSite=Lax`;
                
                // REDIRECT UPDATE: Changed from index.html to place.html
                window.location.href = 'place.html';
            } else {
                const errorData = await response.json();
                alert('Login Failed: ' + (errorData.msg || 'Invalid credentials'));
            }
        } catch (err) {
            console.error('Login error:', err);
            alert('Could not connect to the server. Is your Python API running?');
        }
    });
}

/* ==========================================
   TASK 2: PLACES PAGE (LIST) LOGIC
   ========================================== */

function initPlacesPage() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (token) {
        if (loginLink) loginLink.style.display = 'none';
        fetchPlaces(token);
    } else {
        if (loginLink) loginLink.style.display = 'block';
        fetchPlaces(); 
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
            renderPlacesList(places);
        }
    } catch (err) {
        console.error('Fetch places error:', err);
    }
}

function renderPlacesList(places) {
    const container = document.getElementById('places-list');
    if (!container) return;
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
    if (!filter) return;

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

/* ==========================================
   TASK 3: PLACE DETAILS PAGE LOGIC
   ========================================== */

async function initPlaceDetailsPage() {
    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('id');
    const token = getCookie('token');

    if (!placeId) {
        // REDIRECT UPDATE: Changed from index.html to place.html
        window.location.href = 'place.html';
        return;
    }

    const addReviewSection = document.getElementById('add-review');
    if (token && addReviewSection) {
        addReviewSection.style.display = 'block';
        const reviewBtn = document.getElementById('add-review-button');
        if (reviewBtn) reviewBtn.href = `add_review.html?id=${placeId}`;
    }

    fetchPlaceDetails(placeId, token);
}

async function fetchPlaceDetails(placeId, token) {
    const headers = { 'Content-Type': 'application/json' };
    if (token) headers['Authorization'] = `Bearer ${token}`;

    try {
        const response = await fetch(`${API_BASE_URL}/places/${placeId}`, { headers });
        if (response.ok) {
            const place = await response.json();
            renderPlaceDetails(place);
        } else {
            const container = document.getElementById('place-details');
            if (container) container.innerHTML = '<h2>Place not found.</h2>';
        }
    } catch (err) {
        console.error('Error fetching details:', err);
    }
}

function renderPlaceDetails(place) {
    const detailsContainer = document.getElementById('place-details');
    if (detailsContainer) {
        detailsContainer.innerHTML = `
            <h1>${place.name}</h1>
            <div class="place-info">
                <p><strong>Price per night:</strong> $${place.price_by_night}</p>
                <p><strong>Description:</strong> ${place.description}</p>
                <p><strong>Host:</strong> ${place.host_name || 'Anonymous'}</p>
            </div>
        `;
    }

    const amenitiesList = document.getElementById('amenities-list');
    if (amenitiesList) {
        amenitiesList.innerHTML = '';
        if (place.amenities && place.amenities.length > 0) {
            place.amenities.forEach(amenity => {
                const li = document.createElement('li');
                li.textContent = amenity.name;
                amenitiesList.appendChild(li);
            });
        } else {
            amenitiesList.innerHTML = '<li>No amenities available.</li>';
        }
    }

    const reviewsList = document.getElementById('reviews-list');
    if (reviewsList) {
        reviewsList.innerHTML = '';
        if (place.reviews && place.reviews.length > 0) {
            place.reviews.forEach(review => {
                const reviewCard = document.createElement('div');
                reviewCard.className = 'review-card';
                reviewCard.innerHTML = `
                    <p><strong>${review.user_name}</strong> - ${review.rating} Stars</p>
                    <p>"${review.comment}"</p>
                `;
                reviewsList.appendChild(reviewCard);
            });
        } else {
            reviewsList.innerHTML = '<p>No reviews yet.</p>';
        }
    }
}
