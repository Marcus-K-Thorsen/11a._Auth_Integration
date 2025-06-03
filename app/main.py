from dotenv import load_dotenv
import os
import json
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
import googleapiclient.discovery
from fastapi.templating import Jinja2Templates
from fastapi.responses import Response


# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))


app = FastAPI()


# Serve static files from 'templates' folder
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# Google credentials
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
SCOPES = ["https://www.googleapis.com/auth/userinfo.profile"]

def get_google_auth_flow() -> Flow:
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [REDIRECT_URI]
            }
        },
        scopes=SCOPES
    )
    flow.redirect_uri = REDIRECT_URI
    
    return flow

@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})




# Route to request user consent
@app.get("/auth/google/consent")
async def google_consent():
    flow = get_google_auth_flow()
    auth_url, _ = flow.authorization_url(access_type='offline', include_granted_scopes='true')
    print(auth_url)
    return RedirectResponse(auth_url)




@app.get("/auth/google/callback")
async def google_callback(request: Request):
    try:
        code = request.query_params.get("code")


        flow = get_google_auth_flow()
        flow.fetch_token(code=code)
        credentials = flow.credentials


        tokens = {
            "token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "token_uri": credentials.token_uri,
            "client_id": credentials.client_id,
            "client_secret": credentials.client_secret,
            "scopes": credentials.scopes
        }


        # Redirect to the homepage with tokens in the query string
        tokens_json = json.dumps(tokens)
        return RedirectResponse(url=f"/?tokens={tokens_json}")
    except Exception as e:
        print("Callback Error:", e)
        return HTMLResponse(content="Error during authentication", status_code=500)


# IMPORTANT: Route to fetch user info
@app.get("/auth/whoami")
async def whoami(tokens: str):
    try:
        tokens_dict = json.loads(tokens)


        creds = Credentials(
            token=tokens_dict["token"],
            refresh_token=tokens_dict.get("refresh_token"),
            token_uri=tokens_dict["token_uri"],
            client_id=tokens_dict["client_id"],
            client_secret=tokens_dict["client_secret"],
            scopes=tokens_dict["scopes"]
        )


        service = googleapiclient.discovery.build("oauth2", "v2", credentials=creds)
        user_info = service.userinfo().get().execute()


        return user_info
    except Exception as e:
        print("Whoami Error:", e)
        return HTMLResponse(content="Error fetching user info", status_code=500)
   
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)  # No Content
