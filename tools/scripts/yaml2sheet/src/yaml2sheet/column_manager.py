from typing import List
import logging
from .config import COLUMNS, COLUMN_INFO

logger = logging.getLogger(__name__)


class ColumnManager:
    """Manages column-related operations for sheet generation"""

    def __init__(self, target_id: str):
        self.target_id = target_id

    def get_header_ids(self) -> List[str]:
        """Get column IDs for sheet

        Returns:
            List[str]: Column IDs
        """
        # Column groups in order
        id_headers = COLUMNS['idCols']
        generated_headers = COLUMNS[self.target_id]['generatedData']
        user_headers = COLUMNS['userEntered']
        plain_headers = [
            *COLUMNS['common']['plainData1'],
            *COLUMNS[self.target_id]['plainData1'],
            *COLUMNS['common']['plainData2'],
            *COLUMNS[self.target_id]['plainData2']
        ]
        link_headers = [
            *COLUMNS[self.target_id]['linkData'],
            *COLUMNS['common']['linkData']
        ]

        # All headers in order
        all_headers = [
            *id_headers,
            *generated_headers,
            *user_headers,
            *plain_headers,
            *link_headers
        ]

        return all_headers

    def get_header_names(self, lang: str) -> List[str]:
        """Get localized column header names for sheet

        Args:
            lang: Language code

        Returns:
            List[str]: Localized header names
        """
        all_headers = self.get_header_ids()

        # Get localized names
        return [
            COLUMN_INFO['name'].get(header, {}).get(lang, header)
            for header in all_headers
        ]

    def get_column_widths(self) -> List[int]:
        """Get list of column widths

        Returns:
            List[int]: List of column widths
        """
        headers = self.get_header_ids()
        return [
            COLUMN_INFO['width'].get(header, 100)
            for header in headers
        ]

    def has_generated_data(self) -> bool:
        """Check if target has generated data columns

        Returns:
            bool: True if target has generated data
        """
        return bool(COLUMNS[self.target_id]['generatedData'])

    def get_generated_data_column_count(self) -> int:
        """Get number of generated data columns

        Returns:
            int: Number of generated data columns
        """
        return len(COLUMNS[self.target_id]['generatedData'])

    def get_result_column_index(self) -> int:
        """Get index of result column

        Returns:
            int: Index of result column
        """
        # ID columns + generated data columns = result column index
        return (len(COLUMNS['idCols']) +
                len(COLUMNS[self.target_id]['generatedData']))
