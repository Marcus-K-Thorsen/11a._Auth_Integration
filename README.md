# 11a [Individual/Pairs/Group] Auth Integration

Create a frontend that allows users to log in / sign up. 

You could use a federated identities service, SSO or a library that integrates with a third-party. The main point is integrating with a system external to yours. 

**Type**: Individual/Pairs/Group

You are allowed to work in pairs or groups of three for this assignment if you find that easier.

**Hand-in**:

1. Git link for the code. 

2. Documentation that goes through step by step on how you set it up. The guide should be so detailed that anyone can follow it and reproduce the result. 


**Hint**: Many services for federated identities exist. Part of the assignment is to research them. It would be a good idea to create a document that lists pros and cons and considerations during the research phase.  

**Hint 2**: If you are spending many hours implenting things yourself then you have likely misunderstood the assignment. The goal is to integrate with an existing solution.


## Purpose of the Assignment

The purpose of this assignment is to demonstrate the integration of **Google OAuth 2.0** authentication into a FastAPI application. The project showcases how to implement user login using Google's authentication system, retrieve user profile information, and dynamically update the frontend based on the authenticated user's data.

This project uses **Google OAuth 2.0** directly as the federated identity service. It does not use third-party tools. Instead, it implements the OAuth 2.0 flow manually to demonstrate a deeper understanding of how the protocol works.

---

## Flow of the Application

1. **Homepage** (`GET /`):
   - The application starts at the homepage, which is served by the `GET /` endpoint in [`app/main.py`](app/main.py).
   - This page displays a "Login with Google" button if the user is not logged in.
   - The purpose of this button is to allow the user to start the login process using their Google account.

2. **Google Consent** (`GET /auth/google/consent`):
   - When the user clicks the "Login with Google" button, they are redirected to the `GET /auth/google/consent` endpoint.
   - This endpoint initializes the Google OAuth 2.0 flow using the `Flow` class from the `google_auth_oauthlib.flow` library.
   - The application generates a special URL (called the authorization URL) that points to Google's login page. This URL includes information about the app (like its client ID) and the permissions it is requesting (e.g., access to the user's profile).
   - The user is then redirected to this URL, which takes them to Google's consent screen. Here, they can log in and grant permission for the app to access their profile.

3. **Google Callback** (`GET /auth/google/callback`):
   - After the user logs in and grants permission, Google redirects them back to the `GET /auth/google/callback` endpoint.
   - This redirection includes an authorization code, which is a temporary code that the app can use to request access tokens from Google.
   - The app exchanges this authorization code for access tokens by making a request to Google's token endpoint (`https://oauth2.googleapis.com/token`).
   - These tokens allow the app to securely access the user's Google profile information. The tokens are then serialized into a JSON string and appended as a query parameter to the homepage URL.

4. **Token Handling**:
   - When the user is redirected back to the homepage, the tokens are included in the URL as a query parameter.
   - The frontend JavaScript extracts these tokens from the URL and uses them to make a request to the `GET /auth/whoami` endpoint.

5. **User Info Retrieval** (`GET /auth/whoami`):
   - The `GET /auth/whoami` endpoint receives the tokens from the frontend and uses them to create `Credentials` objects.
   - These credentials are used to make a request to Google's API (`https://www.googleapis.com/oauth2/v2/userinfo`) to fetch the user's profile information, such as their name and profile picture.
   - The endpoint returns this information to the frontend.

6. **Dynamic Frontend Update**:
   - The frontend dynamically updates the homepage to display the user's profile information (e.g., their name and profile picture) based on the data received from the `GET /auth/whoami` endpoint.

---

## How OAuth with Google Works in `app/main.py`

1. **Environment Variables**:
   - The application uses environment variables (`CLIENT_ID`, `CLIENT_SECRET`, `REDIRECT_URI`) to configure the Google OAuth 2.0 flow.
   - These variables store sensitive information, such as the app's client ID and secret, which are required to communicate with Google's OAuth 2.0 API.
   - By storing them in environment variables, the app keeps this information secure and avoids hardcoding it into the source code.

2. **Google Consent Flow** (`GET /auth/google/consent`):
   - The `GET /auth/google/consent` endpoint initializes the OAuth flow using the `Flow` class from the `google_auth_oauthlib.flow` library.
   - It generates an authorization URL that includes:
     - The app's client ID (to identify the app to Google).
     - The redirect URI (where Google should send the user after they log in).
     - The requested scopes (permissions), such as access to the user's profile.
   - The user is redirected to this URL, which takes them to Google's login page. This is where Google comes into the picture, as it handles the user's authentication and consent.

3. **Callback Handling** (`GET /auth/google/callback`):
   - The `GET /auth/google/callback` endpoint processes the authorization code returned by Google.
   - It exchanges the code for access tokens by making a request to Google's token endpoint (`https://oauth2.googleapis.com/token`).
   - These tokens include:
     - An access token (used to access the user's profile).
     - A refresh token (used to get a new access token when the current one expires).
   - The tokens are serialized into a JSON object and appended as a query parameter to the homepage URL. This allows the frontend to access the tokens and use them to fetch the user's profile information.

4. **User Info Retrieval** (`GET /auth/whoami`):
   - The `GET /auth/whoami` endpoint uses the tokens to create `Credentials` objects, which are used to authenticate requests to Google's API.
   - It makes a request to the `https://www.googleapis.com/oauth2/v2/userinfo` endpoint to fetch the user's profile information.
   - This information is returned to the frontend, which updates the UI to display the user's name and profile picture.


---

## How to Start the Project

```bash
$ cd app
$ poetry run uvicorn main:app --reload
```

Open your browser and navigate to http://localhost:8000

Click the "Login with Google" button to authenticate and view your profile information.

Link to App on Google:
https://console.cloud.google.com/apis/credentials?inv=1&invt=Abw0xg&project=healthy-rarity-459207-j0&supportedpurview=project
