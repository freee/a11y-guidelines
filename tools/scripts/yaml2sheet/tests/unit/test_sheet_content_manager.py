"""Tests for sheet_content_manager module."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from yaml2sheet.sheet_content_manager import SheetContentManager
from yaml2sheet.sheet_structure import SheetStructure
from yaml2sheet.cell_data import CellData, CellType


class TestSheetContentManager:
    """Test cases for SheetContentManager class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_api_client = Mock()
        self.mock_spreadsheet_manager = Mock()
        self.current_lang = "ja"
        self.current_target = "design_web"
        self.editor_email = "test@example.com"
        
        self.manager = SheetContentManager(
            self.mock_api_client,
            self.mock_spreadsheet_manager,
            self.current_lang,
            self.current_target,
            self.editor_email
        )

    def test_init(self):
        """Test SheetContentManager initialization."""
        assert self.manager.api_client == self.mock_api_client
        assert self.manager.spreadsheet_manager == self.mock_spreadsheet_manager
        assert self.manager.current_lang == self.current_lang
        assert self.manager.current_target == self.current_target
        assert self.manager.editor_email == self.editor_email
        assert self.manager.column_manager is not None

    def test_init_without_editor_email(self):
        """Test SheetContentManager initialization without editor email."""
        manager = SheetContentManager(
            self.mock_api_client,
            self.mock_spreadsheet_manager,
            self.current_lang,
            self.current_target
        )
        assert manager.editor_email == ""

    def test_add_sheet_content_requests_basic(self):
        """Test add_sheet_content_requests with basic data."""
        # Setup
        requests = []
        sheet_id = 123
        sheet_name = "Test Sheet"
        
        # Create test data
        header_row = [
            CellData("ID", CellType.PLAIN),
            CellData("Check", CellType.PLAIN)
        ]
        data_row = [
            CellData("C001", CellType.PLAIN),
            CellData("Test check", CellType.PLAIN)
        ]
        sheet_data = [header_row, data_row]
        
        sheet = SheetStructure("Test Sheet", 123)
        sheet.data = sheet_data
        
        # Mock dependencies
        self.mock_spreadsheet_manager.get_sheet_grid_properties.return_value = {
            'rowCount': 1000,
            'columnCount': 26
        }
        self.mock_spreadsheet_manager.protected_ranges = {}
        
        with patch.object(self.manager.column_manager, 'get_column_widths', return_value=[100, 200]):
            with patch.object(self.manager.column_manager, 'has_generated_data', return_value=False):
                # Execute
                self.manager.add_sheet_content_requests(requests, sheet_id, sheet_name, sheet)
        
        # Verify requests were added
        assert len(requests) > 0
        
        # Verify clear content request
        clear_requests = [req for req in requests if 'updateCells' in req and 'fields' in req['updateCells'] and req['updateCells']['fields'] == '*']
        assert len(clear_requests) == 1
        
        # Verify data update requests
        data_requests = [req for req in requests if 'updateCells' in req and 'rows' in req['updateCells']]
        assert len(data_requests) == 1

    def test_add_sheet_content_requests_with_exception(self):
        """Test add_sheet_content_requests handles exceptions properly."""
        # Setup
        requests = []
        sheet_id = 123
        sheet_name = "Test Sheet"
        sheet = SheetStructure("Test Sheet", 123)
        sheet.data = []
        
        # Mock to raise exception
        self.mock_spreadsheet_manager.get_sheet_grid_properties.side_effect = Exception("Test error")
        
        # Execute and verify exception is raised
        with pytest.raises(Exception, match="Test error"):
            self.manager.add_sheet_content_requests(requests, sheet_id, sheet_name, sheet)

    def test_adjust_sheet_size_no_adjustment_needed(self):
        """Test _adjust_sheet_size when no adjustment is needed."""
        # Setup
        sheet_id = 123
        sheet_name = "Test Sheet"
        data_length = 10
        column_count = 5
        
        self.mock_spreadsheet_manager.get_sheet_grid_properties.return_value = {
            'rowCount': 1000,
            'columnCount': 26
        }
        
        with patch('yaml2sheet.sheet_content_manager.adjust_sheet_size', return_value=[]) as mock_adjust:
            # Execute
            self.manager._adjust_sheet_size(sheet_id, sheet_name, data_length, column_count)
            
            # Verify adjust_sheet_size was called
            mock_adjust.assert_called_once_with(sheet_id, data_length, column_count, 1000, 26)
            
            # Verify no API calls were made
            self.mock_api_client.batch_update.assert_not_called()

    def test_adjust_sheet_size_with_adjustment(self):
        """Test _adjust_sheet_size when adjustment is needed."""
        # Setup
        sheet_id = 123
        sheet_name = "Test Sheet"
        data_length = 2000
        column_count = 30
        
        self.mock_spreadsheet_manager.get_sheet_grid_properties.return_value = {
            'rowCount': 1000,
            'columnCount': 26
        }
        
        size_requests = [{'updateSheetProperties': {'properties': {'sheetId': sheet_id}}}]
        
        with patch('yaml2sheet.sheet_content_manager.adjust_sheet_size', return_value=size_requests) as mock_adjust:
            # Execute
            self.manager._adjust_sheet_size(sheet_id, sheet_name, data_length, column_count)
            
            # Verify adjust_sheet_size was called
            mock_adjust.assert_called_once_with(sheet_id, data_length, column_count, 1000, 26)
            
            # Verify API call was made
            self.mock_api_client.batch_update.assert_called_once_with(size_requests)

    def test_adjust_sheet_size_no_grid_properties(self):
        """Test _adjust_sheet_size when grid properties are not available."""
        # Setup
        sheet_id = 123
        sheet_name = "Test Sheet"
        data_length = 10
        column_count = 5
        
        self.mock_spreadsheet_manager.get_sheet_grid_properties.return_value = None
        
        with patch('yaml2sheet.sheet_content_manager.adjust_sheet_size') as mock_adjust:
            # Execute
            self.manager._adjust_sheet_size(sheet_id, sheet_name, data_length, column_count)
            
            # Verify adjust_sheet_size was not called
            mock_adjust.assert_not_called()

    def test_add_clear_content_request_with_protected_ranges(self):
        """Test _add_clear_content_request with protected ranges."""
        # Setup
        requests = []
        sheet_id = 123
        data_length = 10
        column_count = 5
        
        # Mock protected ranges
        self.mock_spreadsheet_manager.protected_ranges = {123: [456, 789]}
        
        # Execute
        self.manager._add_clear_content_request(requests, sheet_id, data_length, column_count)
        
        # Verify protected range deletion requests
        delete_requests = [req for req in requests if 'deleteProtectedRange' in req]
        assert len(delete_requests) == 2
        assert delete_requests[0]['deleteProtectedRange']['protectedRangeId'] == 456
        assert delete_requests[1]['deleteProtectedRange']['protectedRangeId'] == 789
        
        # Verify clear content request
        clear_requests = [req for req in requests if 'updateCells' in req]
        assert len(clear_requests) == 1
        clear_request = clear_requests[0]
        assert clear_request['updateCells']['range']['sheetId'] == sheet_id
        assert clear_request['updateCells']['fields'] == '*'

    def test_add_clear_content_request_without_protected_ranges(self):
        """Test _add_clear_content_request without protected ranges."""
        # Setup
        requests = []
        sheet_id = 123
        data_length = 10
        column_count = 5
        
        # No protected ranges
        self.mock_spreadsheet_manager.protected_ranges = {}
        
        # Execute
        self.manager._add_clear_content_request(requests, sheet_id, data_length, column_count)
        
        # Verify no protected range deletion requests
        delete_requests = [req for req in requests if 'deleteProtectedRange' in req]
        assert len(delete_requests) == 0
        
        # Verify clear content request
        clear_requests = [req for req in requests if 'updateCells' in req]
        assert len(clear_requests) == 1

    def test_add_clear_content_request_no_protected_ranges_attribute(self):
        """Test _add_clear_content_request when protected_ranges attribute doesn't exist."""
        # Setup
        requests = []
        sheet_id = 123
        data_length = 10
        column_count = 5
        
        # Remove protected_ranges attribute
        if hasattr(self.mock_spreadsheet_manager, 'protected_ranges'):
            delattr(self.mock_spreadsheet_manager, 'protected_ranges')
        
        # Execute
        self.manager._add_clear_content_request(requests, sheet_id, data_length, column_count)
        
        # Verify no protected range deletion requests
        delete_requests = [req for req in requests if 'deleteProtectedRange' in req]
        assert len(delete_requests) == 0
        
        # Verify clear content request
        clear_requests = [req for req in requests if 'updateCells' in req]
        assert len(clear_requests) == 1

    def test_add_data_update_requests_small_dataset(self):
        """Test _add_data_update_requests with small dataset."""
        # Setup
        requests = []
        sheet_id = 123
        
        data = [
            [CellData("ID", CellType.PLAIN), CellData("Check", CellType.PLAIN)],
            [CellData("C001", CellType.PLAIN), CellData("Test check", CellType.PLAIN)]
        ]
        
        # Execute
        self.manager._add_data_update_requests(requests, sheet_id, data)
        
        # Verify single update request
        update_requests = [req for req in requests if 'updateCells' in req and 'rows' in req['updateCells']]
        assert len(update_requests) == 1
        
        update_request = update_requests[0]
        assert update_request['updateCells']['range']['sheetId'] == sheet_id
        assert len(update_request['updateCells']['rows']) == 2

    def test_add_data_update_requests_large_dataset(self):
        """Test _add_data_update_requests with large dataset requiring chunking."""
        # Setup
        requests = []
        sheet_id = 123
        
        # Create 250 rows of data (should create 3 chunks of 100 each)
        data = []
        for i in range(250):
            data.append([
                CellData(f"C{i:03d}", CellType.PLAIN),
                CellData(f"Check {i}", CellType.PLAIN)
            ])
        
        # Execute
        self.manager._add_data_update_requests(requests, sheet_id, data)
        
        # Verify multiple update requests
        update_requests = [req for req in requests if 'updateCells' in req and 'rows' in req['updateCells']]
        assert len(update_requests) == 3
        
        # Verify chunk sizes
        assert len(update_requests[0]['updateCells']['rows']) == 100
        assert len(update_requests[1]['updateCells']['rows']) == 100
        assert len(update_requests[2]['updateCells']['rows']) == 50

    def test_add_column_width_requests(self):
        """Test _add_column_width_requests."""
        # Setup
        requests = []
        sheet_id = 123
        
        with patch.object(self.manager.column_manager, 'get_column_widths', return_value=[100, 200, 150]):
            # Execute
            self.manager._add_column_width_requests(requests, sheet_id)
        
        # Verify column width requests
        width_requests = [req for req in requests if 'updateDimensionProperties' in req]
        assert len(width_requests) == 3
        
        # Verify first column width request
        first_request = width_requests[0]
        assert first_request['updateDimensionProperties']['range']['sheetId'] == sheet_id
        assert first_request['updateDimensionProperties']['properties']['pixelSize'] == 100

    def test_add_formatting_requests(self):
        """Test _add_formatting_requests."""
        # Setup
        requests = []
        sheet_id = 123
        data_length = 10
        
        sheet = SheetStructure("Test Sheet", 123)
        sheet.data = [
            [CellData("ID", CellType.PLAIN), CellData("Check", CellType.PLAIN)],
            [CellData("C001", CellType.PLAIN), CellData("Test check", CellType.PLAIN)]
        ]
        
        with patch('yaml2sheet.sheet_content_manager.SheetFormatter') as mock_formatter_class:
            mock_formatter = Mock()
            mock_formatter_class.return_value = mock_formatter
            mock_formatter.apply_basic_formatting.return_value = [{'format_request': 'basic'}]
            mock_formatter.add_protection_settings.return_value = [{'protection_request': 'settings'}]
            mock_formatter.protect_parent_check_cells.return_value = {'parent_protection': 'request'}
            
            # Execute
            self.manager._add_formatting_requests(requests, sheet_id, sheet, data_length)
            
            # Verify formatter was created with correct parameters
            mock_formatter_class.assert_called_once_with(self.current_lang, self.current_target, self.editor_email)
            
            # Verify formatter methods were called
            mock_formatter.apply_basic_formatting.assert_called_once_with(sheet_id, data_length)
            mock_formatter.add_protection_settings.assert_called_once_with(sheet_id, sheet)

    def test_add_column_visibility_requests_no_generated_data(self):
        """Test _add_column_visibility_requests without generated data."""
        # Setup
        requests = []
        sheet_id = 123
        column_count = 10
        data = [
            [CellData("ID", CellType.PLAIN), CellData("Check", CellType.PLAIN)],
            [CellData("C001", CellType.PLAIN), CellData("Test check", CellType.PLAIN)]
        ]
        
        with patch.object(self.manager.column_manager, 'has_generated_data', return_value=False):
            # Execute
            self.manager._add_column_visibility_requests(requests, sheet_id, data, column_count)
        
        # Verify visibility requests
        visibility_requests = [req for req in requests if 'updateDimensionProperties' in req]
        assert len(visibility_requests) == 2  # Reset all + hide column B
        
        # Verify column B is hidden
        hide_request = visibility_requests[1]
        assert hide_request['updateDimensionProperties']['range']['startIndex'] == 1
        assert hide_request['updateDimensionProperties']['range']['endIndex'] == 2
        assert hide_request['updateDimensionProperties']['properties']['hiddenByUser'] is True

    def test_add_column_visibility_requests_with_generated_data_no_subchecks(self):
        """Test _add_column_visibility_requests with generated data but no subchecks."""
        # Setup
        requests = []
        sheet_id = 123
        column_count = 10
        data = [
            [CellData("ID", CellType.PLAIN), CellData("Subcheck", CellType.PLAIN), CellData("Check", CellType.PLAIN)],
            [CellData("C001", CellType.PLAIN), CellData("", CellType.PLAIN), CellData("Test check", CellType.PLAIN)]
        ]
        
        with patch.object(self.manager.column_manager, 'has_generated_data', return_value=True):
            # Execute
            self.manager._add_column_visibility_requests(requests, sheet_id, data, column_count)
        
        # Verify visibility requests
        visibility_requests = [req for req in requests if 'updateDimensionProperties' in req]
        assert len(visibility_requests) == 2  # Reset all + hide columns B-D
        
        # Verify columns B-D are hidden
        hide_request = visibility_requests[1]
        assert hide_request['updateDimensionProperties']['range']['startIndex'] == 1
        assert hide_request['updateDimensionProperties']['range']['endIndex'] == 4
        assert hide_request['updateDimensionProperties']['properties']['hiddenByUser'] is True

    def test_add_column_visibility_requests_with_generated_data_with_subchecks(self):
        """Test _add_column_visibility_requests with generated data and subchecks."""
        # Setup
        requests = []
        sheet_id = 123
        column_count = 10
        data = [
            [CellData("ID", CellType.PLAIN), CellData("Subcheck", CellType.PLAIN), CellData("Check", CellType.PLAIN)],
            [CellData("C001", CellType.PLAIN), CellData("Sub1", CellType.PLAIN), CellData("Test check", CellType.PLAIN)]
        ]
        
        with patch.object(self.manager.column_manager, 'has_generated_data', return_value=True):
            # Execute
            self.manager._add_column_visibility_requests(requests, sheet_id, data, column_count)
        
        # Verify visibility requests
        visibility_requests = [req for req in requests if 'updateDimensionProperties' in req]
        merge_requests = [req for req in requests if 'mergeCells' in req]
        
        assert len(visibility_requests) == 2  # Reset all + hide column C
        assert len(merge_requests) == 1  # Merge A-B
        
        # Verify column C is hidden
        hide_request = visibility_requests[1]
        assert hide_request['updateDimensionProperties']['range']['startIndex'] == 2
        assert hide_request['updateDimensionProperties']['range']['endIndex'] == 3
        assert hide_request['updateDimensionProperties']['properties']['hiddenByUser'] is True
        
        # Verify merge request
        merge_request = merge_requests[0]
        assert merge_request['mergeCells']['range']['sheetId'] == sheet_id
        assert merge_request['mergeCells']['range']['startColumnIndex'] == 0
        assert merge_request['mergeCells']['range']['endColumnIndex'] == 2

    def test_is_parent_check_with_subchecks(self):
        """Test _is_parent_check_with_subchecks."""
        # Setup
        row = [CellData("C001", CellType.PLAIN), CellData("Test check", CellType.PLAIN)]
        
        # Execute
        result = self.manager._is_parent_check_with_subchecks(row)
        
        # Verify (currently returns False as noted in the code)
        assert result is False

    @patch('yaml2sheet.sheet_content_manager.logger')
    def test_add_sheet_content_requests_with_logging(self, mock_logger):
        """Test that appropriate logging occurs during sheet content processing."""
        # Setup
        requests = []
        sheet_id = 123
        sheet_name = "Test Sheet"
        
        sheet = SheetStructure("Test Sheet", 123)
        sheet.data = [
            [CellData("ID", CellType.PLAIN), CellData("Check", CellType.PLAIN)],
            [CellData("C001", CellType.PLAIN), CellData("Test check", CellType.PLAIN)]
        ]
        
        self.mock_spreadsheet_manager.get_sheet_grid_properties.return_value = {
            'rowCount': 1000,
            'columnCount': 26
        }
        self.mock_spreadsheet_manager.protected_ranges = {}
        
        with patch.object(self.manager.column_manager, 'get_column_widths', return_value=[100, 200]):
            with patch.object(self.manager.column_manager, 'has_generated_data', return_value=False):
                # Execute
                self.manager.add_sheet_content_requests(requests, sheet_id, sheet_name, sheet)
        
        # Verify debug logging was called
        assert mock_logger.debug.called

    @patch('yaml2sheet.sheet_content_manager.logger')
    def test_add_sheet_content_requests_error_logging(self, mock_logger):
        """Test error logging when sheet content processing fails."""
        # Setup
        requests = []
        sheet_id = 123
        sheet_name = "Test Sheet"
        sheet = SheetStructure("Test Sheet", 123)
        sheet.data = []
        
        # Mock to raise exception
        self.mock_spreadsheet_manager.get_sheet_grid_properties.side_effect = Exception("Test error")
        
        # Execute and expect exception
        with pytest.raises(Exception):
            self.manager.add_sheet_content_requests(requests, sheet_id, sheet_name, sheet)
        
        # Verify error was logged
        mock_logger.error.assert_called_once()
        assert "Error processing sheet content" in str(mock_logger.error.call_args)

    def test_integration_full_workflow(self):
        """Test complete workflow with all components."""
        # Setup
        requests = []
        sheet_id = 123
        sheet_name = "Integration Test Sheet"
        
        # Create comprehensive test data
        sheet = SheetStructure("Integration Test Sheet", 123)
        sheet.data = [
            [CellData("ID", CellType.PLAIN), CellData("Subcheck", CellType.PLAIN), CellData("Check", CellType.PLAIN)],
            [CellData("C001", CellType.PLAIN), CellData("", CellType.PLAIN), CellData("Parent check", CellType.PLAIN)],
            [CellData("C001-1", CellType.PLAIN), CellData("Sub1", CellType.PLAIN), CellData("Subcheck 1", CellType.PLAIN)],
            [CellData("C002", CellType.PLAIN), CellData("", CellType.PLAIN), CellData("Another check", CellType.PLAIN)]
        ]
        
        # Mock all dependencies
        self.mock_spreadsheet_manager.get_sheet_grid_properties.return_value = {
            'rowCount': 1000,
            'columnCount': 26
        }
        self.mock_spreadsheet_manager.protected_ranges = {123: [456]}
        
        with patch.object(self.manager.column_manager, 'get_column_widths', return_value=[100, 80, 300]):
            with patch.object(self.manager.column_manager, 'has_generated_data', return_value=True):
                with patch('yaml2sheet.sheet_content_manager.SheetFormatter') as mock_formatter_class:
                    mock_formatter = Mock()
                    mock_formatter_class.return_value = mock_formatter
                    mock_formatter.apply_basic_formatting.return_value = [{'format': 'basic'}]
                    mock_formatter.add_protection_settings.return_value = [{'protection': 'settings'}]
                    
                    # Execute
                    self.manager.add_sheet_content_requests(requests, sheet_id, sheet_name, sheet)
        
        # Verify comprehensive request generation
        assert len(requests) > 10  # Should have many different types of requests
        
        # Verify different types of requests are present
        request_types = set()
        for req in requests:
            request_types.update(req.keys())
        
        expected_types = {'deleteProtectedRange', 'updateCells', 'updateDimensionProperties'}
        assert expected_types.issubset(request_types)
