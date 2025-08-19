from typing import Dict, List
import logging
from .cell_data import CellData, CellType
from .condition_formatter import ConditionFormatter
from .config import CHECK_RESULTS, FINAL_CHECK_RESULTS, COLUMNS
from .utils import l10n_string

logger = logging.getLogger(__name__)


class RowDataBuilder:
    """Builds row data for sheet generation"""

    def __init__(self, current_lang: str, current_target: str):
        self.current_lang = current_lang
        self.current_target = current_target

    def prepare_row_data(
        self,
        check: Dict,
        target_id: str,
        lang: str,
        id_to_row: Dict[str, int]
    ) -> List[CellData]:
        """Prepare data for a single row

        Args:
            check: Check data to process
            target_id: Target identifier
            lang: Language code
            id_to_row: Mapping of IDs to row numbers

        Returns:
            List[CellData]: List of prepared cell data
        """
        row_data = []

        # Add ID columns
        self._add_id_columns(check, row_data)

        # Add generated data if needed
        if COLUMNS[target_id]['generatedData']:
            self._add_generated_data(check, target_id, lang, row_data,
                                     id_to_row)

        # Add user entry columns
        self._add_user_entry_columns(check, target_id, lang, row_data)

        # Add plain data columns
        self._add_plain_data_columns(check, target_id, lang, row_data)

        # Add link columns
        self._add_link_columns(check, target_id, lang, row_data)

        return row_data

    def _add_id_columns(self, check: Dict, row_data: List[CellData]) -> None:
        """Add ID columns to row

        Args:
            check: Check data
            row_data: Row data to append to
        """
        for header in COLUMNS['idCols']:
            row_data.append(CellData(
                value=check[header],
                type=CellType.PLAIN,
                formatting={'numberFormat': {'type': 'TEXT',
                                             'pattern': '0000'}}
            ))

    def _add_generated_data(
        self,
        check: Dict,
        target_id: str,
        lang: str,
        row_data: List[CellData],
        id_to_row: Dict[str, int]
    ) -> None:
        """Add generated data columns to row

        Args:
            check: Check data
            target_id: Target identifier
            lang: Language code
            row_data: Row data to append to
            id_to_row: ID to row mapping
        """
        is_subcheck = check.get('isSubcheck', False)

        formatter = ConditionFormatter(CHECK_RESULTS, FINAL_CHECK_RESULTS,
                                       target_id)

        if check.get('conditions'):
            for condition in check['conditions']:
                if condition['target'] == target_id:
                    formula = formatter.get_condition_formula(condition,
                                                              id_to_row, lang)

                    if not is_subcheck:
                        # Parent check
                        # Calculate column for calculatedResult
                        # (second generatedData column)
                        calc_col = chr(ord('A') + len(COLUMNS['idCols']) + 1)
                        ref_col = f'{calc_col}{id_to_row[check["id"]]}'
                        row_data.extend([
                            CellData(
                                value=f'=IF({ref_col}="","'
                                      f'{CHECK_RESULTS["unchecked"][lang]}",'
                                      f'{ref_col})',
                                type=CellType.FORMULA,
                                protection=True
                            ),
                            CellData(
                                value=formula,
                                type=CellType.FORMULA,
                                protection=True
                            )
                        ])
                    else:
                        # Subcheck
                        calc_col = chr(ord('A') + len(COLUMNS['idCols']) + 1)
                        parent_id = check['id'].split('-')[0]
                        parent_row = id_to_row[parent_id]
                        row_data.extend([
                            CellData(value="", type=CellType.PLAIN,
                                     protection=True),
                            CellData(
                                value=f'={calc_col}{parent_row}',
                                type=CellType.FORMULA,
                                protection=True
                            )
                        ])
                    return

        # Simple check case
        if not is_subcheck:
            # Calculate column positions
            calc_col = chr(ord('A') + len(COLUMNS['idCols']) + 1)
            result_col = chr(ord('A') + len(COLUMNS['idCols']) +
                             len(COLUMNS[target_id]['generatedData']))
            result_cell = f'{result_col}{id_to_row[check["id"]]}'
            calc_cell = f'{calc_col}{id_to_row[check["id"]]}'
            row_data.extend([
                CellData(
                    value=f'=IF(${calc_cell}="","'
                          f'{CHECK_RESULTS["unchecked"][lang]}",'
                          f'${calc_cell})',
                    type=CellType.FORMULA,
                    protection=True
                ),
                CellData(
                    value=(
                        f'=IF(${result_cell}="'
                        f'{CHECK_RESULTS["unchecked"][lang]}", "", '
                        f'IF(TO_TEXT(${result_cell})="'
                        f'{CHECK_RESULTS["pass"][lang]}", '
                        f'"{FINAL_CHECK_RESULTS["pass"][lang]}", '
                        f'"{FINAL_CHECK_RESULTS["fail"][lang]}"))'
                    ),
                    type=CellType.FORMULA,
                    protection=True
                )
            ])
        else:
            # Calculate column for calculatedResult
            calc_col = chr(ord('A') + len(COLUMNS['idCols']) + 1)
            parent_id = check['id'].split('-')[0]
            parent_row = id_to_row[parent_id]
            row_data.extend([
                CellData(value="", type=CellType.PLAIN, protection=True),
                CellData(
                    value=f'={calc_col}{parent_row}',
                    type=CellType.FORMULA,
                    protection=True
                )
            ])

    def _add_user_entry_columns(
        self,
        check: Dict,
        target_id: str,
        lang: str,
        row_data: List[CellData]
    ) -> None:
        """Add user entry columns to row

        Args:
            check: Check data
            target_id: Target identifier
            lang: Language code
            row_data: Row data to append to
        """
        validation_dict = (CHECK_RESULTS if COLUMNS[target_id]['generatedData']
                           else FINAL_CHECK_RESULTS)
        validation_values = [validation_dict[key][lang]
                             for key in validation_dict.keys()]
        validation_rule = {
            'condition': {
                'type': 'ONE_OF_LIST',
                'values': [{'userEnteredValue': val}
                           for val in validation_values]
            },
            'strict': True,
            'showCustomUi': True
        }

        is_subcheck = check.get('isSubcheck', False)
        has_subchecks = (
            not is_subcheck and
            check.get('subchecks') and
            target_id in check['subchecks'] and
            check['subchecks'][target_id].get('count', 0) > 1
        )

        for header in COLUMNS['userEntered']:
            if header == 'result':
                if has_subchecks:
                    row_data.append(CellData(
                        value="",
                        type=CellType.PLAIN,
                        protection=True,
                        formatting={'backgroundColor': {'red': 0.9,
                                                        'green': 0.9,
                                                        'blue': 0.9}}
                    ))
                else:
                    row_data.append(CellData(
                        value=validation_dict['unchecked'][lang],
                        type=CellType.PLAIN,
                        validation=validation_rule
                    ))
            else:
                row_data.append(CellData(value='', type=CellType.PLAIN))

    def _add_plain_data_columns(
        self,
        check: Dict,
        target_id: str,
        lang: str,
        row_data: List[CellData]
    ) -> None:
        """Add plain data columns to row

        Args:
            check: Check data
            target_id: Target identifier
            lang: Language code
            row_data: Row data to append to
        """
        plain_headers = [
            *COLUMNS['common']['plainData1'],
            *COLUMNS[target_id]['plainData1'],
            *COLUMNS['common']['plainData2'],
            *COLUMNS[target_id]['plainData2']
        ]

        for header in plain_headers:
            value = check.get(header, '')
            if isinstance(value, dict) and {'ja', 'en'}.intersection(
                    value.keys()):
                value = l10n_string(value, lang)
            row_data.append(CellData(
                value=value or '',
                type=CellType.PLAIN
            ))

    def _add_link_columns(
        self,
        check: Dict,
        target_id: str,
        lang: str,
        row_data: List[CellData]
    ) -> None:
        """Add link columns to row

        Args:
            check: Check data
            target_id: Target identifier
            lang: Language code
            row_data: Row data to append to
        """
        link_headers = [
            *COLUMNS[target_id]['linkData'],
            *COLUMNS['common']['linkData']
        ]

        for header in link_headers:
            links = check.get(header, [])
            if links:
                row_data.append(self._create_rich_text_cell(links, lang))
            else:
                row_data.append(CellData(value='', type=CellType.PLAIN))

    def _create_rich_text_cell(self, links: List[Dict],
                               lang: str) -> CellData:
        """Create rich text cell with formatted links

        Args:
            links: List of link data
            lang: Language code

        Returns:
            CellData: Formatted cell data
        """
        text_parts = []
        format_runs = []
        current_index = 0

        for i, link in enumerate(links):
            if i > 0:
                text_parts.append("\n")
                current_index += 1

            link_text = link['text'][lang]
            text_parts.append(link_text)

            url = link['url'][lang]
            # Check if URL is relative and needs base_url
            if url.startswith('/'):
                from freee_a11y_gl import settings as GL
                base_url = GL.get('base_url', '')
                url = base_url.rstrip('/') + url

            format_runs.append({
                'startIndex': current_index,
                'format': {
                    'link': {'uri': url},
                    'foregroundColor': {'red': 0.06, 'green': 0.47,
                                        'blue': 0.82},
                    'underline': True
                }
            })
            current_index += len(link_text)

        return CellData(
            value={'text': ''.join(text_parts), 'format_runs': format_runs},
            type=CellType.RICH_TEXT
        )
