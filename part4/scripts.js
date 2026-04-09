document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            // 1. Prevent the page from refreshing
            event.preventDefault();

            // 2. Extract data from the input fields
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            // 3. Send the data to the API
            try {
                const response = await fetch('https://your-api-url/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email: email, password: password })
                });

                // 4. Handle the API's answer
                if (response.ok) {
                    const data = await response.json();
                    
                    // Store the JWT token in a cookie valid for the whole site
                    document.cookie = `token=${data.access_token}; path=/; SameSite=Lax`;
                    
                    // Redirect to the main page
                    window.location.href = 'index.html';
                } else {
                    // Handle errors (e.g., 401 Unauthorized)
                    const errorData = await response.json();
                    alert('Login failed: ' + (errorData.msg || 'Invalid credentials'));
                }
            } catch (error) {
                console.error('Error during login:', error);
                alert('Could not connect to the server.');
            }
        });
    }
});
