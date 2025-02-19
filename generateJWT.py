import jwt as pyjwt
import time

GITHUB_APP_ID = "1234567"
PRIVATE_KEY_PATH = "/Users/ekgra/workDir/poc/GHAPP/private-key.pem" 

def generate_jwt():
    """Generate a JWT token using the GitHub App private key."""
    with open(PRIVATE_KEY_PATH, "r") as key_file:
        private_key = key_file.read()

    payload = {
        "iat": int(time.time()),  # Issued at time
        "exp": int(time.time()) + 600,  # Expiration time (10 minutes)
        "iss": GITHUB_APP_ID  # App ID
    }
    
    return pyjwt.encode(payload, private_key, algorithm="RS256")

if __name__ == "__main__":
    print(generate_jwt())