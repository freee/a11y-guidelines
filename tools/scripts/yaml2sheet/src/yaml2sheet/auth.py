import os.path
import logging
from typing import Optional
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError

logger = logging.getLogger(__name__)

class GoogleAuthManager:
    """Manages Google API authentication and token management"""
    
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    
    def __init__(self, credentials_path: str = 'credentials.json', 
                 token_path: str = 'token.json'):
        """Initialize the auth manager with paths for credentials and token
        
        Args:
            credentials_path: Path to client secrets JSON file
            token_path: Path to save/load authentication token
        """
        self.credentials_path = credentials_path
        self.token_path = token_path
        
    def get_credentials(self) -> Credentials:
        """Retrieve Google API credentials, refreshing or creating if needed
        
        Returns:
            Credentials: Valid Google API credentials
            
        Raises:
            FileNotFoundError: If credentials file is missing
            Exception: If authentication fails
        """
        creds = None
        
        # Try to load saved token
        if os.path.exists(self.token_path):
            try:
                creds = Credentials.from_authorized_user_file(self.token_path, self.SCOPES)
                logger.info("Loaded existing authentication token")
            except Exception as e:
                logger.warning(f"Failed to load existing token: {e}")
                logger.warning("Will attempt to create a new token")
        
        # Handle invalid/expired token
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    logger.info("Refreshing expired token")
                    creds.refresh(Request())
                    logger.info("Token refresh successful")
                except RefreshError as e:
                    logger.warning(f"Token refresh failed, need to re-authenticate: {e}")
                    creds = None
                except Exception as e:
                    logger.warning(f"Failed to refresh token: {e}")
                    creds = None
            
            # Create new token if needed
            if not creds:
                if not os.path.exists(self.credentials_path):
                    raise FileNotFoundError(
                        f"Credentials file not found at {self.credentials_path}. "
                        "Please download it from Google Cloud Console."
                    )
                
                try:
                    logger.info("Starting authorization flow")
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_path, 
                        self.SCOPES
                    )
                    logger.info("A browser window will open for authentication. Please log in to your Google account.")
                    creds = flow.run_local_server(port=0)
                    logger.info("Authentication successful")
                except Exception as e:
                    logger.error(f"Authentication failed: {e}")
                    raise
            
            # Save new token
            try:
                with open(self.token_path, 'w') as token:
                    token.write(creds.to_json())
                logger.info(f"Saved authentication token to {self.token_path}")
            except Exception as e:
                logger.error(f"Failed to save token: {e}")
                logger.warning("Authentication succeeded but token could not be saved. "
                              "You may need to re-authenticate next time.")
                
        return creds

    def revoke_token(self) -> bool:
        """Revoke the current token and remove the token file
        
        Returns:
            bool: True if successfully revoked, False otherwise
        """
        if not os.path.exists(self.token_path):
            logger.warning("No token file found to revoke")
            return False
            
        try:
            creds = Credentials.from_authorized_user_file(self.token_path, self.SCOPES)
            
            # Try to revoke token
            try:
                from google_auth_httplib2 import Request
                import httplib2
                
                http = httplib2.Http()
                creds.refresh(Request(http))
                http = httplib2.Http()
                creds.revoke(Request(http))
                logger.info("Token successfully revoked")
            except Exception as e:
                logger.warning(f"Failed to revoke token: {e}")
                
            # Remove token file regardless of revoke success
            os.remove(self.token_path)
            logger.info(f"Removed token file {self.token_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error revoking token: {e}")
            return False
