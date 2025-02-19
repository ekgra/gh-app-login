from fastapi import FastAPI, HTTPException
import pygit2
import os
import requests
from app.cloned_repo.generateJWT import generate_jwt

app = FastAPI()

GITHUB_APP_ID = "your_app_id"
REPO_URL = "https://github.com/ekgra/gh-app-login.git"
CLONE_PATH = "./cloned_repo"

def get_installation_token():
    """Obtain an installation token using the GitHub App JWT."""
    jwt_token = generate_jwt()
    
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github+json"
    }
    url = "https://api.github.com/app/installations"
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch installations.")
    
    installation_id = response.json()[0]["id"]  # Fetch the first installation ID
    
    # Get the access token using the installation ID
    token_url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"
    response = requests.post(token_url, headers=headers)
    
    if response.status_code != 201:
        raise HTTPException(status_code=500, detail="Failed to get installation token.")
    
    return response.json()["token"]

def clone_repository():
    """Clone repository using GitHub App installation token."""
    if os.path.exists(CLONE_PATH):
        return "Repository already cloned."
    
    token = get_installation_token()
    credentials = pygit2.UserPass(token, "x-oauth-basic")
    callbacks = pygit2.RemoteCallbacks(credentials=credentials)
    
    try:
        pygit2.clone_repository(REPO_URL, CLONE_PATH, callbacks=callbacks)
        return "Repository cloned successfully using GitHub App."
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error cloning repository: {str(e)}")

@app.get("/clone")
def clone_repo():
    return {"message": clone_repository()}
