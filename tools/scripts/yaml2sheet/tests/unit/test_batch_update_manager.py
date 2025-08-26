"""Tests for batch_update_manager module."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from yaml2sheet.batch_update_manager import BatchUpdateManager


class TestBatchUpdateManager:
    """Test cases for BatchUpdateManager class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_api_client = Mock()
        self.mock_spreadsheet_manager = Mock()
        self.manager = BatchUpdateManager(self.mock_api_client, self.mock_spreadsheet_manager)

    def test_init(self):
        """Test BatchUpdateManager initialization."""
        assert self.manager.api_client == self.mock_api_client
        assert self.manager.spreadsheet_manager == self.mock_spreadsheet_manager

    def test_execute_batch_update_with_sheet_creation(self):
        """Test execute_batch_update with sheet creation requests."""
        # Setup
        initial_requests = [
            {'addSheet': {'properties': {'title': 'Test Sheet'}}},
            {'updateCells': {'range': {'sheetId': 123}}}
        ]
        version_info = {'version': '1.0.0', 'date': '2024-01-01'}
        
        # Mock responses
        self.mock_api_client.batch_update.return_value = {
            'replies': [
                {'addSheet': {'properties': {'sheetId': 456, 'title': 'Test Sheet'}}}
            ]
        }
        self.mock_spreadsheet_manager.get_first_sheet_id.return_value = 456
        
        # Execute
        self.manager.execute_batch_update(initial_requests, version_info)
        
        # Verify sheet creation was called
        creation_calls = [call for call in self.mock_api_client.batch_update.call_args_list 
                         if any('addSheet' in req for req in call[0][0])]
        assert len(creation_calls) == 1
        
        # Verify update_sheet_info was called
        self.mock_spreadsheet_manager.update_sheet_info.assert_called_once_with('Test Sheet', 456, 0)

    def test_execute_batch_update_without_sheet_creation(self):
        """Test execute_batch_update without sheet creation requests."""
        # Setup
        initial_requests = [
            {'updateCells': {'range': {'sheetId': 123}}},
            {'updateSheetProperties': {'properties': {'sheetId': 123}}}
        ]
        version_info = {'version': '1.0.0', 'date': '2024-01-01'}
        
        self.mock_spreadsheet_manager.get_first_sheet_id.return_value = 123
        
        # Execute
        self.manager.execute_batch_update(initial_requests, version_info)
        
        # Verify no sheet creation calls
        creation_calls = [call for call in self.mock_api_client.batch_update.call_args_list 
                         if any('addSheet' in req for req in call[0][0])]
        assert len(creation_calls) == 0
        
        # Verify update_sheet_info was not called
        self.mock_spreadsheet_manager.update_sheet_info.assert_not_called()

    def test_execute_batch_update_without_version_info(self):
        """Test execute_batch_update without version info."""
        # Setup
        initial_requests = [
            {'updateCells': {'range': {'sheetId': 123}}}
        ]
        
        # Execute
        self.manager.execute_batch_update(initial_requests)
        
        # Verify batch_update was called
        assert self.mock_api_client.batch_update.called

    def test_execute_batch_update_with_update_exception_no_raise(self):
        """Test execute_batch_update handles update exceptions without raising."""
        # Setup - Exception in update batch should be logged but not raised
        initial_requests = [
            {'updateCells': {'range': {'sheetId': 123}}}
        ]
        self.mock_api_client.batch_update.side_effect = Exception("API Error")
        
        # Execute - should not raise exception (batch errors are caught and logged)
        self.manager.execute_batch_update(initial_requests)
        
        # Verify batch_update was called
        assert self.mock_api_client.batch_update.called

    def test_execute_batch_update_with_sheet_creation_exception(self):
        """Test execute_batch_update handles sheet creation exceptions properly."""
        # Setup - Exception in sheet creation should be raised
        initial_requests = [
            {'addSheet': {'properties': {'title': 'Test Sheet'}}},
            {'updateCells': {'range': {'sheetId': 123}}}
        ]
        self.mock_api_client.batch_update.side_effect = Exception("Sheet creation failed")
        
        # Execute and verify exception is raised
        with pytest.raises(Exception, match="Sheet creation failed"):
            self.manager.execute_batch_update(initial_requests)

    def test_execute_sheet_creation_requests_with_sheets(self):
        """Test _execute_sheet_creation_requests with sheet creation requests."""
        # Setup
        initial_requests = [
            {'addSheet': {'properties': {'title': 'Sheet1'}}},
            {'addSheet': {'properties': {'title': 'Sheet2'}}},
            {'updateCells': {'range': {'sheetId': 123}}}
        ]
        
        self.mock_api_client.batch_update.return_value = {
            'replies': [
                {'addSheet': {'properties': {'sheetId': 456, 'title': 'Sheet1'}}},
                {'addSheet': {'properties': {'sheetId': 789, 'title': 'Sheet2'}}}
            ]
        }
        
        # Execute
        self.manager._execute_sheet_creation_requests(initial_requests)
        
        # Verify correct requests were sent
        call_args = self.mock_api_client.batch_update.call_args[0][0]
        assert len(call_args) == 2
        assert all('addSheet' in req for req in call_args)
        
        # Verify update_sheet_info was called for both sheets
        assert self.mock_spreadsheet_manager.update_sheet_info.call_count == 2

    def test_execute_sheet_creation_requests_without_sheets(self):
        """Test _execute_sheet_creation_requests without sheet creation requests."""
        # Setup
        initial_requests = [
            {'updateCells': {'range': {'sheetId': 123}}}
        ]
        
        # Execute
        self.manager._execute_sheet_creation_requests(initial_requests)
        
        # Verify no API calls were made
        self.mock_api_client.batch_update.assert_not_called()
        self.mock_spreadsheet_manager.update_sheet_info.assert_not_called()

    def test_execute_sheet_update_requests_with_version_info(self):
        """Test _execute_sheet_update_requests with version info."""
        # Setup
        initial_requests = [
            {'addSheet': {'properties': {'title': 'Sheet1'}}},
            {'updateCells': {'range': {'sheetId': 123}}}
        ]
        version_info = {'version': '1.0.0', 'date': '2024-01-01'}
        
        self.mock_spreadsheet_manager.get_first_sheet_id.return_value = 123
        
        with patch('yaml2sheet.batch_update_manager.create_version_info_request') as mock_create_version:
            mock_create_version.return_value = {'updateCells': {'range': {'sheetId': 123}}}
            
            # Execute
            self.manager._execute_sheet_update_requests(initial_requests, version_info)
            
            # Verify version info request was created
            mock_create_version.assert_called_once_with('1.0.0', '2024-01-01', 123)

    def test_execute_sheet_update_requests_without_version_info(self):
        """Test _execute_sheet_update_requests without version info."""
        # Setup
        initial_requests = [
            {'updateCells': {'range': {'sheetId': 123}}}
        ]
        
        # Execute
        self.manager._execute_sheet_update_requests(initial_requests)
        
        # Verify batch_update was called
        assert self.mock_api_client.batch_update.called

    def test_execute_sheet_update_requests_no_update_requests(self):
        """Test _execute_sheet_update_requests with only sheet creation requests."""
        # Setup
        initial_requests = [
            {'addSheet': {'properties': {'title': 'Sheet1'}}}
        ]
        
        # Execute
        self.manager._execute_sheet_update_requests(initial_requests)
        
        # Verify no API calls were made
        self.mock_api_client.batch_update.assert_not_called()

    def test_add_version_info_request(self):
        """Test _add_version_info_request adds version info correctly."""
        # Setup
        update_requests = [
            {'updateCells': {'range': {'sheetId': 123}}}
        ]
        version_info = {'version': '2.0.0', 'date': '2024-02-01'}
        
        self.mock_spreadsheet_manager.get_first_sheet_id.return_value = 456
        
        with patch('yaml2sheet.batch_update_manager.create_version_info_request') as mock_create_version:
            mock_version_request = {'updateCells': {'range': {'sheetId': 456}}}
            mock_create_version.return_value = mock_version_request
            
            # Execute
            self.manager._add_version_info_request(update_requests, version_info)
            
            # Verify version request was added
            assert len(update_requests) == 2
            assert update_requests[-1] == mock_version_request
            mock_create_version.assert_called_once_with('2.0.0', '2024-02-01', 456)

    def test_process_update_batches_single_batch(self):
        """Test _process_update_batches with requests fitting in single batch."""
        # Setup
        update_requests = [
            {'updateCells': {'range': {'sheetId': i}}} for i in range(10)
        ]
        
        # Execute
        self.manager._process_update_batches(update_requests)
        
        # Verify single batch call
        assert self.mock_api_client.batch_update.call_count == 1
        call_args = self.mock_api_client.batch_update.call_args[0][0]
        assert len(call_args) == 10

    def test_process_update_batches_multiple_batches(self):
        """Test _process_update_batches with requests requiring multiple batches."""
        # Setup - Create 120 requests (should create 3 batches of 50 each)
        update_requests = [
            {'updateCells': {'range': {'sheetId': i}}} for i in range(120)
        ]
        
        # Execute
        self.manager._process_update_batches(update_requests)
        
        # Verify multiple batch calls
        assert self.mock_api_client.batch_update.call_count == 3
        
        # Verify batch sizes
        call_args_list = self.mock_api_client.batch_update.call_args_list
        assert len(call_args_list[0][0][0]) == 50  # First batch
        assert len(call_args_list[1][0][0]) == 50  # Second batch
        assert len(call_args_list[2][0][0]) == 20  # Third batch

    def test_process_update_batches_with_batch_error(self):
        """Test _process_update_batches continues after batch error."""
        # Setup
        update_requests = [
            {'updateCells': {'range': {'sheetId': i}}} for i in range(120)
        ]
        
        # Mock first batch to fail, others to succeed
        self.mock_api_client.batch_update.side_effect = [
            Exception("Batch 1 failed"),
            None,  # Batch 2 succeeds
            None   # Batch 3 succeeds
        ]
        
        # Execute (should not raise exception)
        self.manager._process_update_batches(update_requests)
        
        # Verify all batches were attempted
        assert self.mock_api_client.batch_update.call_count == 3

    def test_process_update_batches_empty_requests(self):
        """Test _process_update_batches with empty request list."""
        # Setup
        update_requests = []
        
        # Execute
        self.manager._process_update_batches(update_requests)
        
        # Verify no API calls were made
        self.mock_api_client.batch_update.assert_not_called()

    @patch('yaml2sheet.batch_update_manager.logger')
    def test_logging_in_execute_batch_update(self, mock_logger):
        """Test that appropriate logging occurs during batch update execution."""
        # Setup
        initial_requests = [
            {'addSheet': {'properties': {'title': 'Test Sheet'}}},
            {'updateCells': {'range': {'sheetId': 123}}}
        ]
        
        self.mock_api_client.batch_update.return_value = {
            'replies': [
                {'addSheet': {'properties': {'sheetId': 456, 'title': 'Test Sheet'}}}
            ]
        }
        
        # Execute
        self.manager.execute_batch_update(initial_requests)
        
        # Verify logging calls were made
        assert mock_logger.info.called
        assert mock_logger.error.call_count == 0  # No errors should be logged

    @patch('yaml2sheet.batch_update_manager.logger')
    def test_logging_in_execute_batch_update_with_error(self, mock_logger):
        """Test error logging when batch update fails."""
        # Setup - Exception in sheet creation should be raised and logged
        initial_requests = [
            {'addSheet': {'properties': {'title': 'Test Sheet'}}}
        ]
        self.mock_api_client.batch_update.side_effect = Exception("Test error")
        
        # Execute and expect exception
        with pytest.raises(Exception):
            self.manager.execute_batch_update(initial_requests)
        
        # Verify error was logged
        mock_logger.error.assert_called_once()
        assert "Error executing batch update" in str(mock_logger.error.call_args)

    @patch('yaml2sheet.batch_update_manager.logger')
    def test_logging_in_process_update_batches_with_error(self, mock_logger):
        """Test error logging when individual batch fails but processing continues."""
        # Setup - Exception in update batch should be logged but not raised
        initial_requests = [
            {'updateCells': {'range': {'sheetId': 123}}}
        ]
        self.mock_api_client.batch_update.side_effect = Exception("Batch error")
        
        # Execute - should not raise exception
        self.manager.execute_batch_update(initial_requests)
        
        # Verify error was logged for the batch failure
        error_calls = [call for call in mock_logger.error.call_args_list 
                      if "Error in batch" in str(call)]
        assert len(error_calls) > 0

    def test_integration_full_workflow(self):
        """Test complete workflow with sheet creation, updates, and version info."""
        # Setup
        initial_requests = [
            {'addSheet': {'properties': {'title': 'Sheet1'}}},
            {'addSheet': {'properties': {'title': 'Sheet2'}}},
            {'updateCells': {'range': {'sheetId': 123}}},
            {'updateCells': {'range': {'sheetId': 456}}}
        ]
        version_info = {'version': '1.0.0', 'date': '2024-01-01'}
        
        # Mock responses
        self.mock_api_client.batch_update.return_value = {
            'replies': [
                {'addSheet': {'properties': {'sheetId': 789, 'title': 'Sheet1'}}},
                {'addSheet': {'properties': {'sheetId': 101112, 'title': 'Sheet2'}}}
            ]
        }
        self.mock_spreadsheet_manager.get_first_sheet_id.return_value = 789
        
        with patch('yaml2sheet.batch_update_manager.create_version_info_request') as mock_create_version:
            mock_create_version.return_value = {'updateCells': {'range': {'sheetId': 789}}}
            
            # Execute
            self.manager.execute_batch_update(initial_requests, version_info)
            
            # Verify sheet creation happened first
            assert self.mock_spreadsheet_manager.update_sheet_info.call_count == 2
            
            # Verify version info was added
            mock_create_version.assert_called_once()
            
            # Verify multiple batch_update calls (creation + updates)
            assert self.mock_api_client.batch_update.call_count >= 2
