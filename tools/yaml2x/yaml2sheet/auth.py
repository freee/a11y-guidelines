import os.path
import logging
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

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
                logger.info("Loaded existing token")
            except Exception as e:
                logger.warning(f"Failed to load existing token: {e}")
        
        # Handle invalid/expired token
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    logger.info("Refreshed expired token")
                except Exception as e:
                    logger.warning(f"Failed to refresh token: {e}")
                    creds = None
            
            # Create new token if needed
            if not creds:
                if not os.path.exists(self.credentials_path):
                    raise FileNotFoundError(
                        f"Credentials file not found at {self.credentials_path}. "
                        "Please download it from GCP Console."
                    )
                
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_path, 
                        self.SCOPES
                    )
                    creds = flow.run_local_server(port=0)
                    logger.info("Created new token through authentication flow")
                except Exception as e:
                    logger.error(f"Failed to authenticate: {e}")
                    raise
            
            # Save new token
            try:
                with open(self.token_path, 'w') as token:
                    token.write(creds.to_json())
                logger.info(f"Saved token to {self.token_path}")
            except Exception as e:
                logger.error(f"Failed to save token: {e}")
                # Continue even if token save fails since auth succeeded
                
        return creds
