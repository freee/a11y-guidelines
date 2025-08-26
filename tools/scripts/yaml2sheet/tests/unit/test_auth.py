"""
Tests for auth module.

Tests the existing implementation of Google API authentication including:
- Token loading and saving
- Token refresh functionality
- New authentication flow
- Error handling
"""

import os
import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, Mock, mock_open
import json

from yaml2sheet.auth import GoogleAuthManager


class TestGoogleAuthManager:
    """Test GoogleAuthManager authentication functionality."""
    
    def test_init_default_paths(self):
        """Test initialization with default paths."""
        auth_manager = GoogleAuthManager()
        assert auth_manager.credentials_path == 'credentials.json'
        assert auth_manager.token_path == 'token.json'
        assert auth_manager.SCOPES == ['https://www.googleapis.com/auth/spreadsheets']
    
    def test_init_custom_paths(self):
        """Test initialization with custom paths."""
        auth_manager = GoogleAuthManager(
            credentials_path='custom_creds.json',
            token_path='custom_token.json'
        )
        assert auth_manager.credentials_path == 'custom_creds.json'
        assert auth_manager.token_path == 'custom_token.json'
    
    @patch('yaml2sheet.auth.os.path.exists')
    @patch('yaml2sheet.auth.Credentials.from_authorized_user_file')
    def test_get_credentials_existing_valid_token(self, mock_from_file, mock_exists):
        """Test getting credentials with existing valid token."""
        # Mock existing token file
        mock_exists.return_value = True
        
        # Mock valid credentials
        mock_creds = Mock()
        mock_creds.valid = True
        mock_from_file.return_value = mock_creds
        
        auth_manager = GoogleAuthManager()
        result = auth_manager.get_credentials()
        
        assert result == mock_creds
        mock_exists.assert_called_once_with('token.json')
        mock_from_file.assert_called_once_with('token.json', auth_manager.SCOPES)
    
    @patch('yaml2sheet.auth.os.path.exists')
    @patch('yaml2sheet.auth.Credentials.from_authorized_user_file')
    def test_get_credentials_existing_token_load_error(self, mock_from_file, mock_exists):
        """Test handling of token loading error."""
        # Mock existing token file
        mock_exists.side_effect = lambda path: path == 'token.json'
        
        # Mock token loading error
        mock_from_file.side_effect = Exception("Token loading error")
        
        # Mock credentials file exists
        with patch('yaml2sheet.auth.os.path.exists') as mock_exists_inner:
            mock_exists_inner.side_effect = lambda path: path in ['token.json', 'credentials.json']
            
            # Mock successful authentication flow
            with patch('yaml2sheet.auth.InstalledAppFlow.from_client_secrets_file') as mock_flow:
                mock_flow_instance = Mock()
                mock_flow.return_value = mock_flow_instance
                
                mock_new_creds = Mock()
                mock_new_creds.to_json.return_value = '{"test": "token"}'
                mock_flow_instance.run_local_server.return_value = mock_new_creds
                
                with patch('builtins.open', mock_open()) as mock_file:
                    auth_manager = GoogleAuthManager()
                    result = auth_manager.get_credentials()
                    
                    assert result == mock_new_creds
                    mock_flow.assert_called_once_with('credentials.json', auth_manager.SCOPES)
                    mock_flow_instance.run_local_server.assert_called_once_with(port=0)
    
    @patch('yaml2sheet.auth.os.path.exists')
    @patch('yaml2sheet.auth.Credentials.from_authorized_user_file')
    @patch('yaml2sheet.auth.Request')
    def test_get_credentials_expired_token_refresh_success(self, mock_request, mock_from_file, mock_exists):
        """Test refreshing expired token successfully."""
        # Mock existing token file
        mock_exists.return_value = True
        
        # Mock expired credentials that can be refreshed
        mock_creds = Mock()
        mock_creds.valid = False
        mock_creds.expired = True
        mock_creds.refresh_token = "refresh_token"
        mock_creds.to_json.return_value = '{"test": "refreshed_token"}'
        mock_from_file.return_value = mock_creds
        
        with patch('builtins.open', mock_open()) as mock_file:
            auth_manager = GoogleAuthManager()
            result = auth_manager.get_credentials()
            
            assert result == mock_creds
            mock_creds.refresh.assert_called_once()
            mock_file.assert_called_with('token.json', 'w')
    
    @patch('yaml2sheet.auth.os.path.exists')
    @patch('yaml2sheet.auth.Credentials.from_authorized_user_file')
    def test_get_credentials_expired_token_refresh_failure(self, mock_from_file, mock_exists):
        """Test handling of token refresh failure."""
        from google.auth.exceptions import RefreshError
        
        # Mock existing token file
        mock_exists.side_effect = lambda path: path in ['token.json', 'credentials.json']
        
        # Mock expired credentials that fail to refresh
        mock_creds = Mock()
        mock_creds.valid = False
        mock_creds.expired = True
        mock_creds.refresh_token = "refresh_token"
        mock_creds.refresh.side_effect = RefreshError("Refresh failed")  # Use actual exception
        mock_from_file.return_value = mock_creds
        
        # Mock successful new authentication flow
        with patch('yaml2sheet.auth.InstalledAppFlow.from_client_secrets_file') as mock_flow:
            mock_flow_instance = Mock()
            mock_flow.return_value = mock_flow_instance
            
            mock_new_creds = Mock()
            mock_new_creds.to_json.return_value = '{"test": "new_token"}'
            mock_flow_instance.run_local_server.return_value = mock_new_creds
            
            with patch('builtins.open', mock_open()) as mock_file:
                auth_manager = GoogleAuthManager()
                result = auth_manager.get_credentials()
                
                # After refresh failure, creds is set to None and new auth flow creates new creds
                # The result should be the new credentials from the authentication flow
                assert result == mock_new_creds
                mock_creds.refresh.assert_called_once()
                mock_flow.assert_called_once_with('credentials.json', auth_manager.SCOPES)
                mock_flow_instance.run_local_server.assert_called_once_with(port=0)
    
    @patch('yaml2sheet.auth.os.path.exists')
    def test_get_credentials_no_token_no_credentials_file(self, mock_exists):
        """Test error when no token and no credentials file."""
        # Mock no files exist
        mock_exists.return_value = False
        
        auth_manager = GoogleAuthManager()
        
        with pytest.raises(FileNotFoundError, match="Credentials file not found"):
            auth_manager.get_credentials()
    
    @patch('yaml2sheet.auth.os.path.exists')
    @patch('yaml2sheet.auth.InstalledAppFlow.from_client_secrets_file')
    def test_get_credentials_new_authentication_success(self, mock_flow, mock_exists):
        """Test successful new authentication flow."""
        # Mock no token file, but credentials file exists
        mock_exists.side_effect = lambda path: path == 'credentials.json'
        
        # Mock successful authentication flow
        mock_flow_instance = Mock()
        mock_flow.return_value = mock_flow_instance
        
        mock_creds = Mock()
        mock_creds.to_json.return_value = '{"test": "new_token"}'
        mock_flow_instance.run_local_server.return_value = mock_creds
        
        with patch('builtins.open', mock_open()) as mock_file:
            auth_manager = GoogleAuthManager()
            result = auth_manager.get_credentials()
            
            assert result == mock_creds
            mock_flow.assert_called_once_with('credentials.json', auth_manager.SCOPES)
            mock_flow_instance.run_local_server.assert_called_once_with(port=0)
            mock_file.assert_called_with('token.json', 'w')
    
    @patch('yaml2sheet.auth.os.path.exists')
    @patch('yaml2sheet.auth.InstalledAppFlow.from_client_secrets_file')
    def test_get_credentials_authentication_failure(self, mock_flow, mock_exists):
        """Test authentication flow failure."""
        # Mock credentials file exists
        mock_exists.side_effect = lambda path: path == 'credentials.json'
        
        # Mock authentication failure
        mock_flow.side_effect = Exception("Authentication failed")
        
        auth_manager = GoogleAuthManager()
        
        with pytest.raises(Exception, match="Authentication failed"):
            auth_manager.get_credentials()
    
    @patch('yaml2sheet.auth.os.path.exists')
    @patch('yaml2sheet.auth.InstalledAppFlow.from_client_secrets_file')
    def test_get_credentials_token_save_failure(self, mock_flow, mock_exists):
        """Test handling of token save failure."""
        # Mock credentials file exists
        mock_exists.side_effect = lambda path: path == 'credentials.json'
        
        # Mock successful authentication
        mock_flow_instance = Mock()
        mock_flow.return_value = mock_flow_instance
        
        mock_creds = Mock()
        mock_creds.to_json.return_value = '{"test": "new_token"}'
        mock_flow_instance.run_local_server.return_value = mock_creds
        
        # Mock file write failure
        with patch('builtins.open', mock_open()) as mock_file:
            mock_file.side_effect = IOError("Cannot write file")
            
            auth_manager = GoogleAuthManager()
            result = auth_manager.get_credentials()
            
            # Should still return credentials even if save fails
            assert result == mock_creds
    
    @patch('yaml2sheet.auth.os.path.exists')
    @patch('yaml2sheet.auth.Credentials.from_authorized_user_file')
    def test_revoke_token_success(self, mock_from_file, mock_exists):
        """Test successful token revocation."""
        # Mock token file exists
        mock_exists.return_value = True
        
        # Mock credentials
        mock_creds = Mock()
        mock_from_file.return_value = mock_creds
        
        with patch('google_auth_httplib2.Request') as mock_request, \
             patch('httplib2.Http') as mock_http, \
             patch('yaml2sheet.auth.os.remove') as mock_remove:
            
            auth_manager = GoogleAuthManager()
            result = auth_manager.revoke_token()
            
            assert result is True
            mock_creds.refresh.assert_called_once()
            mock_creds.revoke.assert_called_once()
            mock_remove.assert_called_once_with('token.json')
    
    @patch('yaml2sheet.auth.os.path.exists')
    def test_revoke_token_no_file(self, mock_exists):
        """Test token revocation when no token file exists."""
        # Mock no token file
        mock_exists.return_value = False
        
        auth_manager = GoogleAuthManager()
        result = auth_manager.revoke_token()
        
        assert result is False
    
    @patch('yaml2sheet.auth.os.path.exists')
    @patch('yaml2sheet.auth.Credentials.from_authorized_user_file')
    def test_revoke_token_revoke_failure(self, mock_from_file, mock_exists):
        """Test token revocation when revoke fails but file is still removed."""
        # Mock token file exists
        mock_exists.return_value = True
        
        # Mock credentials with revoke failure
        mock_creds = Mock()
        mock_creds.revoke.side_effect = Exception("Revoke failed")
        mock_from_file.return_value = mock_creds
        
        with patch('google_auth_httplib2.Request') as mock_request, \
             patch('httplib2.Http') as mock_http, \
             patch('yaml2sheet.auth.os.remove') as mock_remove:
            
            auth_manager = GoogleAuthManager()
            result = auth_manager.revoke_token()
            
            assert result is True  # Should still return True as file is removed
            mock_remove.assert_called_once_with('token.json')
    
    @patch('yaml2sheet.auth.os.path.exists')
    @patch('yaml2sheet.auth.Credentials.from_authorized_user_file')
    def test_revoke_token_general_error(self, mock_from_file, mock_exists):
        """Test token revocation with general error."""
        # Mock token file exists
        mock_exists.return_value = True
        
        # Mock credentials loading failure
        mock_from_file.side_effect = Exception("Cannot load credentials")
        
        auth_manager = GoogleAuthManager()
        result = auth_manager.revoke_token()
        
        assert result is False
    
    def test_scopes_constant(self):
        """Test that SCOPES constant is correctly defined."""
        auth_manager = GoogleAuthManager()
        assert auth_manager.SCOPES == ['https://www.googleapis.com/auth/spreadsheets']
        
        # Test that SCOPES is a class attribute
        assert GoogleAuthManager.SCOPES == ['https://www.googleapis.com/auth/spreadsheets']
    
    @patch('yaml2sheet.auth.os.path.exists')
    @patch('yaml2sheet.auth.Credentials.from_authorized_user_file')
    def test_get_credentials_invalid_token_no_refresh_token(self, mock_from_file, mock_exists):
        """Test handling of invalid token without refresh token."""
        # Mock existing token file
        mock_exists.side_effect = lambda path: path in ['token.json', 'credentials.json']
        
        # Mock invalid credentials without refresh token
        mock_creds = Mock()
        mock_creds.valid = False
        mock_creds.expired = False
        mock_creds.refresh_token = None
        mock_creds.to_json.return_value = '{"test": "invalid_token"}'
        mock_from_file.return_value = mock_creds
        
        with patch('builtins.open', mock_open()) as mock_file:
            auth_manager = GoogleAuthManager()
            result = auth_manager.get_credentials()
            
            # According to the implementation, invalid credentials without refresh token
            # are returned as-is (this may be a bug in the implementation, but we test existing behavior)
            assert result == mock_creds
            # Should not attempt to refresh
            mock_creds.refresh.assert_not_called()
            # Should save the token (even though it's invalid)
            mock_file.assert_called_with('token.json', 'w')
    
    @patch('yaml2sheet.auth.os.path.exists')
    @patch('yaml2sheet.auth.Credentials.from_authorized_user_file')
    @patch('yaml2sheet.auth.Request')
    def test_get_credentials_refresh_general_exception(self, mock_request, mock_from_file, mock_exists):
        """Test handling of general exception during token refresh."""
        # Mock existing token file
        mock_exists.side_effect = lambda path: path in ['token.json', 'credentials.json']
        
        # Mock expired credentials that fail to refresh with general exception
        mock_creds = Mock()
        mock_creds.valid = False
        mock_creds.expired = True
        mock_creds.refresh_token = "refresh_token"
        mock_creds.refresh.side_effect = Exception("General refresh error")
        mock_from_file.return_value = mock_creds
        
        # Mock successful new authentication flow
        with patch('yaml2sheet.auth.InstalledAppFlow.from_client_secrets_file') as mock_flow:
            mock_flow_instance = Mock()
            mock_flow.return_value = mock_flow_instance
            
            mock_new_creds = Mock()
            mock_new_creds.to_json.return_value = '{"test": "new_token"}'
            mock_flow_instance.run_local_server.return_value = mock_new_creds
            
            with patch('builtins.open', mock_open()) as mock_file:
                auth_manager = GoogleAuthManager()
                result = auth_manager.get_credentials()
                
                assert result == mock_new_creds
                mock_creds.refresh.assert_called_once()
                mock_flow.assert_called_once_with('credentials.json', auth_manager.SCOPES)
