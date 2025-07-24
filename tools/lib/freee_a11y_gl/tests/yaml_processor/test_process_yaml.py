import pytest
from unittest.mock import patch, MagicMock
from freee_a11y_gl.yaml_processor.process_yaml import process_yaml_data


class TestProcessYaml:
    """Test cases for process_yaml module."""

    @patch('freee_a11y_gl.yaml_processor.process_yaml.get_version_info')
    @patch('freee_a11y_gl.yaml_processor.process_yaml.setup_instances')
    @patch('freee_a11y_gl.yaml_processor.process_yaml.info_utils')
    @patch('freee_a11y_gl.yaml_processor.process_yaml.InfoRef')
    @patch('freee_a11y_gl.yaml_processor.process_yaml.Check')
    @patch('freee_a11y_gl.yaml_processor.process_yaml.rst_processor')
    def test_process_yaml_data_basic(self, mock_rst_processor, mock_check, mock_info_ref, 
                                   mock_info_utils, mock_setup, mock_version):
        """Test basic YAML data processing."""
        # Setup mocks
        mock_version.return_value = {
            'checksheet_version': '1.0.0',
            'checksheet_date': '2023-01-01'
        }
        
        mock_info_utils.get_info_links.return_value = {
            'ref1': {'text': {'ja': 'リンク1', 'en': 'Link 1'}}
        }
        
        mock_info_ref.list_all_internal.return_value = []
        
        mock_check.object_data_all.return_value = {
            'check1': {
                'id': 'check1',
                'check': {'ja': 'チェック1', 'en': 'Check 1'}
            }
        }
        
        mock_rst_processor.process_rst_text.return_value = 'processed text'
        
        # Call function
        result = process_yaml_data('/test/basedir')
        
        # Verify calls
        mock_version.assert_called_once_with('/test/basedir')
        mock_setup.assert_called_once_with('/test/basedir')
        mock_info_utils.get_info_links.assert_called_once_with('/test/basedir')
        mock_check.object_data_all.assert_called_once()
        
        # Verify result structure
        assert 'version' in result
        assert 'date' in result
        assert 'checks' in result
        assert result['version'] == '1.0.0'
        assert result['date'] == '2023-01-01'

    @patch('freee_a11y_gl.yaml_processor.process_yaml.get_version_info')
    @patch('freee_a11y_gl.yaml_processor.process_yaml.setup_instances')
    @patch('freee_a11y_gl.yaml_processor.process_yaml.info_utils')
    @patch('freee_a11y_gl.yaml_processor.process_yaml.InfoRef')
    @patch('freee_a11y_gl.yaml_processor.process_yaml.Check')
    @patch('freee_a11y_gl.yaml_processor.process_yaml.rst_processor')
    def test_process_yaml_data_with_info_refs(self, mock_rst_processor, mock_check, 
                                            mock_info_ref, mock_info_utils, mock_setup, mock_version):
        """Test YAML processing with info references."""
        # Setup mocks
        mock_version.return_value = {
            'checksheet_version': '1.0.0',
            'checksheet_date': '2023-01-01'
        }
        
        info_links = {
            'ref1': {'text': {'ja': 'リンク1', 'en': 'Link 1'}},
            'ref2': {'text': {'ja': 'リンク2', 'en': 'Link 2'}}
        }
        mock_info_utils.get_info_links.return_value = info_links
        
        # Mock info references
        mock_info1 = MagicMock()
        mock_info1.ref = 'ref1'
        mock_info2 = MagicMock()
        mock_info2.ref = 'ref2'
        mock_info3 = MagicMock()
        mock_info3.ref = 'ref3'  # Not in info_links
        
        mock_info_ref.list_all_internal.return_value = [mock_info1, mock_info2, mock_info3]
        
        mock_check.object_data_all.return_value = {}
        
        # Call function
        result = process_yaml_data()
        
        # Verify info references are set correctly
        mock_info1.set_link.assert_called_once_with(info_links['ref1'])
        mock_info2.set_link.assert_called_once_with(info_links['ref2'])
        mock_info3.set_link.assert_not_called()  # ref3 not in info_links

    @patch('freee_a11y_gl.yaml_processor.process_yaml.get_version_info')
    @patch('freee_a11y_gl.yaml_processor.process_yaml.setup_instances')
    @patch('freee_a11y_gl.yaml_processor.process_yaml.info_utils')
    @patch('freee_a11y_gl.yaml_processor.process_yaml.InfoRef')
    @patch('freee_a11y_gl.yaml_processor.process_yaml.Check')
    @patch('freee_a11y_gl.yaml_processor.process_yaml.rst_processor')
    def test_process_yaml_data_with_check_rst_processing(self, mock_rst_processor, mock_check, 
                                                       mock_info_ref, mock_info_utils, mock_setup, mock_version):
        """Test YAML processing with RST text processing in checks."""
        # Setup mocks
        mock_version.return_value = {
            'checksheet_version': '1.0.0',
            'checksheet_date': '2023-01-01'
        }
        
        info_links = {'ref1': {'text': {'ja': 'リンク1', 'en': 'Link 1'}}}
        mock_info_utils.get_info_links.return_value = info_links
        mock_info_ref.list_all_internal.return_value = []
        
        checks_data = {
            'check1': {
                'id': 'check1',
                'check': {
                    'ja': 'チェック1 :ref:`ref1`',
                    'en': 'Check 1 :ref:`ref1`'
                }
            }
        }
        mock_check.object_data_all.return_value = checks_data
        
        # Configure RST processor mock
        mock_rst_processor.process_rst_text.side_effect = lambda text, links, lang: f'processed_{text}'
        
        # Call function
        result = process_yaml_data()
        
        # Verify RST processing was called for each language
        assert mock_rst_processor.process_rst_text.call_count == 2
        mock_rst_processor.process_rst_text.assert_any_call(
            'チェック1 :ref:`ref1`', info_links, 'ja'
        )
        mock_rst_processor.process_rst_text.assert_any_call(
            'Check 1 :ref:`ref1`', info_links, 'en'
        )
        
        # Verify processed text is in result
        assert result['checks']['check1']['check']['ja'] == 'processed_チェック1 :ref:`ref1`'
        assert result['checks']['check1']['check']['en'] == 'processed_Check 1 :ref:`ref1`'

    @patch('freee_a11y_gl.yaml_processor.process_yaml.get_version_info')
    @patch('freee_a11y_gl.yaml_processor.process_yaml.setup_instances')
    @patch('freee_a11y_gl.yaml_processor.process_yaml.info_utils')
    @patch('freee_a11y_gl.yaml_processor.process_yaml.InfoRef')
    @patch('freee_a11y_gl.yaml_processor.process_yaml.Check')
    @patch('freee_a11y_gl.yaml_processor.process_yaml.rst_processor')
    def test_process_yaml_data_with_conditions(self, mock_rst_processor, mock_check, 
                                             mock_info_ref, mock_info_utils, mock_setup, mock_version):
        """Test YAML processing with conditions."""
        # Setup mocks
        mock_version.return_value = {
            'checksheet_version': '1.0.0',
            'checksheet_date': '2023-01-01'
        }
        
        info_links = {'ref1': {'text': {'ja': 'リンク1', 'en': 'Link 1'}}}
        mock_info_utils.get_info_links.return_value = info_links
        mock_info_ref.list_all_internal.return_value = []
        
        conditions = [
            {'type': 'simple', 'id': 'cond1'},
            {'type': 'and', 'conditions': []}
        ]
        
        checks_data = {
            'check1': {
                'id': 'check1',
                'check': {'ja': 'チェック1', 'en': 'Check 1'},
                'conditions': conditions
            }
        }
        mock_check.object_data_all.return_value = checks_data
        
        # Configure RST processor mock
        mock_rst_processor.process_rst_text.return_value = 'processed text'
        mock_rst_processor.process_rst_condition.side_effect = lambda cond, links: {**cond, 'processed': True}
        
        # Call function
        result = process_yaml_data()
        
        # Verify condition processing was called
        assert mock_rst_processor.process_rst_condition.call_count == 2
        for condition in conditions:
            mock_rst_processor.process_rst_condition.assert_any_call(condition, info_links)
        
        # Verify processed conditions are in result
        assert len(result['checks']['check1']['conditions']) == 2
        for cond in result['checks']['check1']['conditions']:
            assert cond['processed'] is True

    @patch('freee_a11y_gl.yaml_processor.process_yaml.get_version_info')
    @patch('freee_a11y_gl.yaml_processor.process_yaml.setup_instances')
    @patch('freee_a11y_gl.yaml_processor.process_yaml.info_utils')
    @patch('freee_a11y_gl.yaml_processor.process_yaml.InfoRef')
    @patch('freee_a11y_gl.yaml_processor.process_yaml.Check')
    def test_process_yaml_data_no_basedir(self, mock_check, mock_info_ref, 
                                        mock_info_utils, mock_setup, mock_version):
        """Test YAML processing without basedir argument."""
        # Setup mocks
        mock_version.return_value = {
            'checksheet_version': '1.0.0',
            'checksheet_date': '2023-01-01'
        }
        mock_info_utils.get_info_links.return_value = {}
        mock_info_ref.list_all_internal.return_value = []
        mock_check.object_data_all.return_value = {}
        
        # Call function without basedir
        result = process_yaml_data()
        
        # Verify None was passed to dependent functions
        mock_version.assert_called_once_with(None)
        mock_setup.assert_called_once_with(None)
        mock_info_utils.get_info_links.assert_called_once_with(None)

    @patch('freee_a11y_gl.yaml_processor.process_yaml.get_version_info')
    @patch('freee_a11y_gl.yaml_processor.process_yaml.setup_instances')
    @patch('freee_a11y_gl.yaml_processor.process_yaml.info_utils')
    @patch('freee_a11y_gl.yaml_processor.process_yaml.InfoRef')
    @patch('freee_a11y_gl.yaml_processor.process_yaml.Check')
    def test_process_yaml_data_checks_without_check_key(self, mock_check, mock_info_ref, 
                                                      mock_info_utils, mock_setup, mock_version):
        """Test processing checks that don't have 'check' key."""
        # Setup mocks
        mock_version.return_value = {
            'checksheet_version': '1.0.0',
            'checksheet_date': '2023-01-01'
        }
        mock_info_utils.get_info_links.return_value = {}
        mock_info_ref.list_all_internal.return_value = []
        
        # Check without 'check' key
        checks_data = {
            'check1': {
                'id': 'check1',
                'other_data': 'value'
            }
        }
        mock_check.object_data_all.return_value = checks_data
        
        # Call function
        result = process_yaml_data()
        
        # Verify no errors and result includes the check
        assert 'check1' in result['checks']
        assert result['checks']['check1']['other_data'] == 'value'

    @patch('freee_a11y_gl.yaml_processor.process_yaml.get_version_info')
    @patch('freee_a11y_gl.yaml_processor.process_yaml.setup_instances')
    @patch('freee_a11y_gl.yaml_processor.process_yaml.info_utils')
    @patch('freee_a11y_gl.yaml_processor.process_yaml.InfoRef')
    @patch('freee_a11y_gl.yaml_processor.process_yaml.Check')
    def test_process_yaml_data_checks_without_conditions_key(self, mock_check, mock_info_ref, 
                                                           mock_info_utils, mock_setup, mock_version):
        """Test processing checks that don't have 'conditions' key."""
        # Setup mocks
        mock_version.return_value = {
            'checksheet_version': '1.0.0',
            'checksheet_date': '2023-01-01'
        }
        mock_info_utils.get_info_links.return_value = {}
        mock_info_ref.list_all_internal.return_value = []
        
        # Check without 'conditions' key
        checks_data = {
            'check1': {
                'id': 'check1',
                'check': {'ja': 'チェック1', 'en': 'Check 1'}
            }
        }
        mock_check.object_data_all.return_value = checks_data
        
        # Call function
        result = process_yaml_data()
        
        # Verify no errors and result includes the check without conditions processing
        assert 'check1' in result['checks']
        assert 'conditions' not in result['checks']['check1']