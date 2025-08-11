"""
pytest configuration and shared fixtures for yaml2sheet tests.
"""

import os
import tempfile
import pytest
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch
from typing import Dict, Any, Optional

# Test data directory
TEST_DATA_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_config_data():
    """Sample configuration data for testing."""
    return {
        "credentials_path": "credentials.json",
        "token_path": "token.json",
        "development_spreadsheet_id": "test_dev_spreadsheet_id",
        "production_spreadsheet_id": "test_prod_spreadsheet_id",
        "sheet_editor_email": "test@example.com",
        "log_level": "INFO",
        "base_url": "https://a11y-guidelines.freee.co.jp"
    }


@pytest.fixture
def sample_yaml_config_file(temp_dir, sample_config_data):
    """Create a sample YAML configuration file."""
    import yaml
    config_file = temp_dir / "test_config.yaml"
    with open(config_file, 'w') as f:
        yaml.dump(sample_config_data, f)
    return config_file




@pytest.fixture
def mock_credentials():
    """Mock Google API credentials."""
    mock_creds = Mock()
    mock_creds.valid = True
    mock_creds.expired = False
    mock_creds.refresh_token = "test_refresh_token"
    mock_creds.to_json.return_value = '{"test": "credentials"}'
    return mock_creds


@pytest.fixture
def mock_google_service():
    """Mock Google Sheets API service."""
    mock_service = Mock()
    
    # Mock spreadsheets resource
    mock_spreadsheets = Mock()
    mock_service.spreadsheets.return_value = mock_spreadsheets
    
    # Mock get method
    mock_get = Mock()
    mock_spreadsheets.get.return_value = mock_get
    mock_get.execute.return_value = {
        'sheets': [
            {
                'properties': {
                    'title': 'Test Sheet',
                    'sheetId': 123,
                    'index': 0,
                    'gridProperties': {
                        'rowCount': 1000,
                        'columnCount': 26
                    }
                }
            }
        ]
    }
    
    # Mock batchUpdate method
    mock_batch_update = Mock()
    mock_spreadsheets.batchUpdate.return_value = mock_batch_update
    mock_batch_update.execute.return_value = {
        'replies': [
            {
                'addSheet': {
                    'properties': {
                        'title': 'New Sheet',
                        'sheetId': 456
                    }
                }
            }
        ]
    }
    
    return mock_service


@pytest.fixture
def sample_yaml_data():
    """Sample YAML data structure matching freee_a11y_gl output."""
    return {
        'version': '1.0.0',
        'date': '2024-01-01',
        'checks': {
            '0001': {
                'id': '0001',
                'sortKey': 100000,
                'severity': 'normal',
                'target': 'design',
                'platform': ['web', 'mobile'],
                'check': {
                    'ja': 'アイコンや画像に関して、3:1以上のコントラスト比が確保されている。',
                    'en': 'For icons and images, a contrast ratio of at least 3:1 is ensured.'
                },
                'conditions': [
                    {
                        'platform': 'web',
                        'type': 'or',
                        'conditions': [
                            {
                                'type': 'simple',
                                'id': '0001-content-00',
                                'tool': 'misc',
                                'procedure': {
                                    'ja': 'チェック対象の画面に、アイコンや画像が存在しない。',
                                    'en': 'There are no icons or images on the screen to be checked.'
                                }
                            },
                            {
                                'type': 'and',
                                'conditions': [
                                    {
                                        'type': 'simple',
                                        'id': '0001-content-01',
                                        'tool': 'misc',
                                        'procedure': {
                                            'ja': '画像内の重要な情報やアイコンと、その背景色とのコントラスト比が3:1以上である。',
                                            'en': 'The contrast ratio between important information or icons within the image and its background color is 3:1 or more.'
                                        }
                                    },
                                    {
                                        'type': 'simple',
                                        'id': '0001-content-02',
                                        'tool': 'misc',
                                        'procedure': {
                                            'ja': '画像や画像化されたテキストと、その隣接領域とのコントラスト比が3:1以上である。',
                                            'en': 'The contrast ratio between the image or image text and its adjacent area is 3:1 or more.'
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            '0002': {
                'id': '0002',
                'sortKey': 200000,
                'severity': 'major',
                'target': 'product',
                'platform': ['web'],
                'check': {
                    'ja': 'テストチェック項目2',
                    'en': 'Test check item 2'
                },
                'conditions': [
                    {
                        'platform': 'web',
                        'type': 'simple',
                        'id': '0002-test-01',
                        'tool': 'axe',
                        'procedure': {
                            'ja': 'テスト手順2',
                            'en': 'Test procedure 2'
                        }
                    }
                ]
            }
        }
    }


@pytest.fixture
def mock_freee_a11y_gl(sample_yaml_data):
    """Mock freee_a11y_gl.yaml_processor.process_yaml_data function."""
    with patch('yaml2sheet.yaml2sheet.process_yaml_data') as mock_process:
        mock_process.return_value = sample_yaml_data
        yield mock_process


@pytest.fixture
def mock_freee_a11y_gl_settings():
    """Mock freee_a11y_gl settings module."""
    with patch('yaml2sheet.yaml2sheet.GL') as mock_gl:
        mock_gl.get.return_value = "https://a11y-guidelines.freee.co.jp"
        mock_gl.update = Mock()
        yield mock_gl


@pytest.fixture
def mock_google_auth():
    """Mock Google authentication flow."""
    with patch('yaml2sheet.auth.InstalledAppFlow') as mock_flow_class, \
         patch('yaml2sheet.auth.Credentials') as mock_creds_class, \
         patch('yaml2sheet.auth.Request') as mock_request:
        
        # Mock flow
        mock_flow = Mock()
        mock_flow_class.from_client_secrets_file.return_value = mock_flow
        
        # Mock credentials
        mock_creds = Mock()
        mock_creds.valid = True
        mock_creds.expired = False
        mock_creds.refresh_token = "test_refresh_token"
        mock_creds.to_json.return_value = '{"test": "credentials"}'
        mock_flow.run_local_server.return_value = mock_creds
        mock_creds_class.from_authorized_user_file.return_value = mock_creds
        
        yield {
            'flow_class': mock_flow_class,
            'flow': mock_flow,
            'credentials_class': mock_creds_class,
            'credentials': mock_creds,
            'request': mock_request
        }


@pytest.fixture
def mock_build_service(mock_google_service):
    """Mock googleapiclient.discovery.build function."""
    with patch('yaml2sheet.sheet_generator.build') as mock_build:
        mock_build.return_value = mock_google_service
        yield mock_build




@pytest.fixture
def sample_check_with_subchecks():
    """Sample check data with subchecks for testing."""
    return {
        'id': '0100',
        'sortKey': 1000000,
        'severity': 'major',
        'target': 'design',
        'platform': ['web'],
        'check': {
            'ja': 'サブチェック付きのテストチェック',
            'en': 'Test check with subchecks'
        },
        'subchecks': {
            'design': {
                'count': 3,
                'conditions': [
                    {
                        'id': '0100-sub-01',
                        'conditions': [
                            {
                                'platform': 'web',
                                'type': 'simple',
                                'id': '0100-sub-01-proc',
                                'tool': 'misc',
                                'procedure': {
                                    'ja': 'サブチェック1の手順',
                                    'en': 'Subcheck 1 procedure'
                                }
                            }
                        ]
                    },
                    {
                        'id': '0100-sub-02',
                        'conditions': [
                            {
                                'platform': 'web',
                                'type': 'simple',
                                'id': '0100-sub-02-proc',
                                'tool': 'misc',
                                'procedure': {
                                    'ja': 'サブチェック2の手順',
                                    'en': 'Subcheck 2 procedure'
                                }
                            }
                        ]
                    },
                    {
                        'id': '0100-sub-03',
                        'conditions': [
                            {
                                'platform': 'web',
                                'type': 'simple',
                                'id': '0100-sub-03-proc',
                                'tool': 'misc',
                                'procedure': {
                                    'ja': 'サブチェック3の手順',
                                    'en': 'Subcheck 3 procedure'
                                }
                            }
                        ]
                    }
                ]
            }
        }
    }
