document.getElementById('login-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const user_name = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const response = await fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_name, password })
    });

    if (response.ok) {
        const result = await response.json();
        document.cookie = `access_token=${result.token}; path=/`;
        alert('Login erfolgreich');
        window.location.href = '/';
    } else {
        alert('Login fehlgeschlagen: ' + response.statusText);
    }
});


