const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const tokens = urlParams.get('tokens');

if (tokens) {
    (async () => {
        const response = await fetch(`/auth/whoami?tokens=${tokens}`, {
            method: 'GET',
        });

        const data = await response.json();

        if (data.error) {
            console.error(data.error);
            return;
        }

        document.getElementById('body').innerHTML = `
            <header class="header">
                <img class="profile-img" src="${data.picture}" alt="${data.name}"/>
                <a href="/" class="btn">Logout</a>
            </header>
            <div class="main">
                <div id="user">
                    <h1>Welcome ${data.name}</h1>
                </div>
            </div>
        `;
    })();
}
