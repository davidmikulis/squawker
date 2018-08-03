const accessToken = localStorage.getItem('squawkerAccessToken');
if (accessToken) {
    const url = 'http://127.0.0.1:5000/access_token';
    const data = {
        access_token: accessToken
    }
    const config = {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json'
        },
    }
    fetch(url, config)
    .then(response => response.json())
    .catch(error => console.error(error))
    .then(data => data)
}