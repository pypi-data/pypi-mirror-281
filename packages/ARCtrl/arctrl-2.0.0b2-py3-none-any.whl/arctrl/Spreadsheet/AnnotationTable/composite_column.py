from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...fable_modules.fable_library.array_ import (skip, map)
from ...fable_modules.fable_library.list import (of_array, FSharpList, singleton as singleton_1, map as map_2)
from ...fable_modules.fable_library.range import range_big_int
from ...fable_modules.fable_library.seq import (to_array, delay, map as map_1, exists, to_list, append, singleton, empty)
from ...fable_modules.fable_library.types import (Array, to_string)
from ...fable_modules.fable_library.util import IEnumerable_1
from ...fable_modules.fs_spreadsheet.Cells.fs_cell import FsCell
from ...fable_modules.fs_spreadsheet.fs_column import FsColumn
from ...Core.Table.composite_cell import CompositeCell
from ...Core.Table.composite_column import CompositeColumn
from ...Core.Table.composite_header import (IOType, CompositeHeader)
from .composite_cell import to_string_cells as to_string_cells_1
from .composite_header import (from_string_cells, to_string_cells)

def fix_deprecated_ioheader(string_cell_col: Array[str]) -> Array[str]:
    if len(string_cell_col) == 0:
        raise Exception("Can\'t fix IOHeader Invalid column, neither header nor values given")

    values: Array[str] = skip(1, string_cell_col, None)
    match_value: IOType = IOType.of_string(string_cell_col[0])
    if match_value.tag == 4:
        return string_cell_col

    elif match_value.tag == 0:
        string_cell_col[0] = to_string(CompositeHeader(11, IOType(0)))
        return string_cell_col

    else: 
        string_cell_col[0] = to_string(CompositeHeader(12, match_value))
        return string_cell_col



def from_string_cell_columns(columns: Array[Array[str]]) -> CompositeColumn:
    def mapping(c: Array[str], columns: Any=columns) -> str:
        return c[0]

    pattern_input: tuple[CompositeHeader, Callable[[Array[str]], CompositeCell]] = from_string_cells(map(mapping, columns, None))
    l: int = len(columns[0]) or 0
    def _arrow967(__unit: None=None, columns: Any=columns) -> IEnumerable_1[CompositeCell]:
        def _arrow966(i: int) -> CompositeCell:
            def mapping_1(c_1: Array[str]) -> str:
                return c_1[i]

            return pattern_input[1](map(mapping_1, columns, None))

        return map_1(_arrow966, range_big_int(1, 1, l - 1))

    cells: Array[CompositeCell] = to_array(delay(_arrow967))
    return CompositeColumn.create(pattern_input[0], cells)


def from_fs_columns(columns: Array[FsColumn]) -> CompositeColumn:
    def mapping_1(c: FsColumn, columns: Any=columns) -> Array[str]:
        c.ToDenseColumn()
        def mapping(c_1: FsCell, c: Any=c) -> str:
            return c_1.ValueAsString()

        return map(mapping, to_array(c.Cells), None)

    return from_string_cell_columns(map(mapping_1, columns, None))


def to_string_cell_columns(column: CompositeColumn) -> FSharpList[FSharpList[str]]:
    def predicate(c: CompositeCell, column: Any=column) -> bool:
        return c.is_unitized

    has_unit: bool = exists(predicate, column.Cells)
    is_term: bool = column.Header.IsTermColumn
    is_data: bool = column.Header.IsDataColumn
    header: Array[str] = to_string_cells(has_unit, column.Header)
    def mapping(cell: CompositeCell, column: Any=column) -> Array[str]:
        return to_string_cells_1(is_term, has_unit, cell)

    cells: Array[Array[str]] = map(mapping, column.Cells, None)
    if has_unit:
        def _arrow973(__unit: None=None, column: Any=column) -> IEnumerable_1[str]:
            def _arrow972(__unit: None=None) -> IEnumerable_1[str]:
                def _arrow971(i: int) -> str:
                    return cells[i][0]

                return map_1(_arrow971, range_big_int(0, 1, len(column.Cells) - 1))

            return append(singleton(header[0]), delay(_arrow972))

        def _arrow976(__unit: None=None, column: Any=column) -> IEnumerable_1[str]:
            def _arrow975(__unit: None=None) -> IEnumerable_1[str]:
                def _arrow974(i_1: int) -> str:
                    return cells[i_1][1]

                return map_1(_arrow974, range_big_int(0, 1, len(column.Cells) - 1))

            return append(singleton(header[1]), delay(_arrow975))

        def _arrow979(__unit: None=None, column: Any=column) -> IEnumerable_1[str]:
            def _arrow978(__unit: None=None) -> IEnumerable_1[str]:
                def _arrow977(i_2: int) -> str:
                    return cells[i_2][2]

                return map_1(_arrow977, range_big_int(0, 1, len(column.Cells) - 1))

            return append(singleton(header[2]), delay(_arrow978))

        def _arrow982(__unit: None=None, column: Any=column) -> IEnumerable_1[str]:
            def _arrow981(__unit: None=None) -> IEnumerable_1[str]:
                def _arrow980(i_3: int) -> str:
                    return cells[i_3][3]

                return map_1(_arrow980, range_big_int(0, 1, len(column.Cells) - 1))

            return append(singleton(header[3]), delay(_arrow981))

        return of_array([to_list(delay(_arrow973)), to_list(delay(_arrow976)), to_list(delay(_arrow979)), to_list(delay(_arrow982))])

    elif is_term:
        def _arrow988(__unit: None=None, column: Any=column) -> IEnumerable_1[str]:
            def _arrow987(__unit: None=None) -> IEnumerable_1[str]:
                def _arrow986(i_4: int) -> str:
                    return cells[i_4][0]

                return map_1(_arrow986, range_big_int(0, 1, len(column.Cells) - 1))

            return append(singleton(header[0]), delay(_arrow987))

        def _arrow991(__unit: None=None, column: Any=column) -> IEnumerable_1[str]:
            def _arrow990(__unit: None=None) -> IEnumerable_1[str]:
                def _arrow989(i_5: int) -> str:
                    return cells[i_5][1]

                return map_1(_arrow989, range_big_int(0, 1, len(column.Cells) - 1))

            return append(singleton(header[1]), delay(_arrow990))

        def _arrow994(__unit: None=None, column: Any=column) -> IEnumerable_1[str]:
            def _arrow993(__unit: None=None) -> IEnumerable_1[str]:
                def _arrow992(i_6: int) -> str:
                    return cells[i_6][2]

                return map_1(_arrow992, range_big_int(0, 1, len(column.Cells) - 1))

            return append(singleton(header[2]), delay(_arrow993))

        return of_array([to_list(delay(_arrow988)), to_list(delay(_arrow991)), to_list(delay(_arrow994))])

    elif is_data:
        def predicate_1(c_1: CompositeCell, column: Any=column) -> bool:
            return c_1.AsData.Format is not None

        has_format: bool = exists(predicate_1, column.Cells)
        def predicate_2(c_2: CompositeCell, column: Any=column) -> bool:
            return c_2.AsData.SelectorFormat is not None

        has_selector_format: bool = exists(predicate_2, column.Cells)
        def _arrow1006(__unit: None=None, column: Any=column) -> IEnumerable_1[FSharpList[str]]:
            def _arrow997(__unit: None=None) -> IEnumerable_1[str]:
                def _arrow996(__unit: None=None) -> IEnumerable_1[str]:
                    def _arrow995(i_7: int) -> str:
                        return cells[i_7][0]

                    return map_1(_arrow995, range_big_int(0, 1, len(column.Cells) - 1))

                return append(singleton(header[0]), delay(_arrow996))

            def _arrow1005(__unit: None=None) -> IEnumerable_1[FSharpList[str]]:
                def _arrow1000(__unit: None=None) -> IEnumerable_1[str]:
                    def _arrow999(__unit: None=None) -> IEnumerable_1[str]:
                        def _arrow998(i_8: int) -> str:
                            return cells[i_8][1]

                        return map_1(_arrow998, range_big_int(0, 1, len(column.Cells) - 1))

                    return append(singleton(header[1]), delay(_arrow999))

                def _arrow1004(__unit: None=None) -> IEnumerable_1[FSharpList[str]]:
                    def _arrow1003(__unit: None=None) -> IEnumerable_1[str]:
                        def _arrow1002(__unit: None=None) -> IEnumerable_1[str]:
                            def _arrow1001(i_9: int) -> str:
                                return cells[i_9][2]

                            return map_1(_arrow1001, range_big_int(0, 1, len(column.Cells) - 1))

                        return append(singleton(header[2]), delay(_arrow1002))

                    return singleton(to_list(delay(_arrow1003))) if has_selector_format else empty()

                return append(singleton(to_list(delay(_arrow1000))) if has_format else empty(), delay(_arrow1004))

            return append(singleton(to_list(delay(_arrow997))), delay(_arrow1005))

        return to_list(delay(_arrow1006))

    else: 
        def _arrow1009(__unit: None=None, column: Any=column) -> IEnumerable_1[str]:
            def _arrow1008(__unit: None=None) -> IEnumerable_1[str]:
                def _arrow1007(i_10: int) -> str:
                    return cells[i_10][0]

                return map_1(_arrow1007, range_big_int(0, 1, len(column.Cells) - 1))

            return append(singleton(header[0]), delay(_arrow1008))

        return singleton_1(to_list(delay(_arrow1009)))



def to_fs_columns(column: CompositeColumn) -> FSharpList[FSharpList[FsCell]]:
    def mapping_1(c: FSharpList[str], column: Any=column) -> FSharpList[FsCell]:
        def mapping(s: str, c: Any=c) -> FsCell:
            return FsCell(s)

        return map_2(mapping, c)

    return map_2(mapping_1, to_string_cell_columns(column))


__all__ = ["fix_deprecated_ioheader", "from_string_cell_columns", "from_fs_columns", "to_string_cell_columns", "to_fs_columns"]

