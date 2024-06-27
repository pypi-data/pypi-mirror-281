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
    def _arrow945(__unit: None=None, columns: Any=columns) -> IEnumerable_1[CompositeCell]:
        def _arrow944(i: int) -> CompositeCell:
            def mapping_1(c_1: Array[str]) -> str:
                return c_1[i]

            return pattern_input[1](map(mapping_1, columns, None))

        return map_1(_arrow944, range_big_int(1, 1, l - 1))

    cells: Array[CompositeCell] = to_array(delay(_arrow945))
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
        def _arrow951(__unit: None=None, column: Any=column) -> IEnumerable_1[str]:
            def _arrow950(__unit: None=None) -> IEnumerable_1[str]:
                def _arrow949(i: int) -> str:
                    return cells[i][0]

                return map_1(_arrow949, range_big_int(0, 1, len(column.Cells) - 1))

            return append(singleton(header[0]), delay(_arrow950))

        def _arrow954(__unit: None=None, column: Any=column) -> IEnumerable_1[str]:
            def _arrow953(__unit: None=None) -> IEnumerable_1[str]:
                def _arrow952(i_1: int) -> str:
                    return cells[i_1][1]

                return map_1(_arrow952, range_big_int(0, 1, len(column.Cells) - 1))

            return append(singleton(header[1]), delay(_arrow953))

        def _arrow957(__unit: None=None, column: Any=column) -> IEnumerable_1[str]:
            def _arrow956(__unit: None=None) -> IEnumerable_1[str]:
                def _arrow955(i_2: int) -> str:
                    return cells[i_2][2]

                return map_1(_arrow955, range_big_int(0, 1, len(column.Cells) - 1))

            return append(singleton(header[2]), delay(_arrow956))

        def _arrow960(__unit: None=None, column: Any=column) -> IEnumerable_1[str]:
            def _arrow959(__unit: None=None) -> IEnumerable_1[str]:
                def _arrow958(i_3: int) -> str:
                    return cells[i_3][3]

                return map_1(_arrow958, range_big_int(0, 1, len(column.Cells) - 1))

            return append(singleton(header[3]), delay(_arrow959))

        return of_array([to_list(delay(_arrow951)), to_list(delay(_arrow954)), to_list(delay(_arrow957)), to_list(delay(_arrow960))])

    elif is_term:
        def _arrow966(__unit: None=None, column: Any=column) -> IEnumerable_1[str]:
            def _arrow965(__unit: None=None) -> IEnumerable_1[str]:
                def _arrow964(i_4: int) -> str:
                    return cells[i_4][0]

                return map_1(_arrow964, range_big_int(0, 1, len(column.Cells) - 1))

            return append(singleton(header[0]), delay(_arrow965))

        def _arrow969(__unit: None=None, column: Any=column) -> IEnumerable_1[str]:
            def _arrow968(__unit: None=None) -> IEnumerable_1[str]:
                def _arrow967(i_5: int) -> str:
                    return cells[i_5][1]

                return map_1(_arrow967, range_big_int(0, 1, len(column.Cells) - 1))

            return append(singleton(header[1]), delay(_arrow968))

        def _arrow972(__unit: None=None, column: Any=column) -> IEnumerable_1[str]:
            def _arrow971(__unit: None=None) -> IEnumerable_1[str]:
                def _arrow970(i_6: int) -> str:
                    return cells[i_6][2]

                return map_1(_arrow970, range_big_int(0, 1, len(column.Cells) - 1))

            return append(singleton(header[2]), delay(_arrow971))

        return of_array([to_list(delay(_arrow966)), to_list(delay(_arrow969)), to_list(delay(_arrow972))])

    elif is_data:
        def predicate_1(c_1: CompositeCell, column: Any=column) -> bool:
            return c_1.AsData.Format is not None

        has_format: bool = exists(predicate_1, column.Cells)
        def predicate_2(c_2: CompositeCell, column: Any=column) -> bool:
            return c_2.AsData.SelectorFormat is not None

        has_selector_format: bool = exists(predicate_2, column.Cells)
        def _arrow984(__unit: None=None, column: Any=column) -> IEnumerable_1[FSharpList[str]]:
            def _arrow975(__unit: None=None) -> IEnumerable_1[str]:
                def _arrow974(__unit: None=None) -> IEnumerable_1[str]:
                    def _arrow973(i_7: int) -> str:
                        return cells[i_7][0]

                    return map_1(_arrow973, range_big_int(0, 1, len(column.Cells) - 1))

                return append(singleton(header[0]), delay(_arrow974))

            def _arrow983(__unit: None=None) -> IEnumerable_1[FSharpList[str]]:
                def _arrow978(__unit: None=None) -> IEnumerable_1[str]:
                    def _arrow977(__unit: None=None) -> IEnumerable_1[str]:
                        def _arrow976(i_8: int) -> str:
                            return cells[i_8][1]

                        return map_1(_arrow976, range_big_int(0, 1, len(column.Cells) - 1))

                    return append(singleton(header[1]), delay(_arrow977))

                def _arrow982(__unit: None=None) -> IEnumerable_1[FSharpList[str]]:
                    def _arrow981(__unit: None=None) -> IEnumerable_1[str]:
                        def _arrow980(__unit: None=None) -> IEnumerable_1[str]:
                            def _arrow979(i_9: int) -> str:
                                return cells[i_9][2]

                            return map_1(_arrow979, range_big_int(0, 1, len(column.Cells) - 1))

                        return append(singleton(header[2]), delay(_arrow980))

                    return singleton(to_list(delay(_arrow981))) if has_selector_format else empty()

                return append(singleton(to_list(delay(_arrow978))) if has_format else empty(), delay(_arrow982))

            return append(singleton(to_list(delay(_arrow975))), delay(_arrow983))

        return to_list(delay(_arrow984))

    else: 
        def _arrow987(__unit: None=None, column: Any=column) -> IEnumerable_1[str]:
            def _arrow986(__unit: None=None) -> IEnumerable_1[str]:
                def _arrow985(i_10: int) -> str:
                    return cells[i_10][0]

                return map_1(_arrow985, range_big_int(0, 1, len(column.Cells) - 1))

            return append(singleton(header[0]), delay(_arrow986))

        return singleton_1(to_list(delay(_arrow987)))



def to_fs_columns(column: CompositeColumn) -> FSharpList[FSharpList[FsCell]]:
    def mapping_1(c: FSharpList[str], column: Any=column) -> FSharpList[FsCell]:
        def mapping(s: str, c: Any=c) -> FsCell:
            return FsCell(s)

        return map_2(mapping, c)

    return map_2(mapping_1, to_string_cell_columns(column))


__all__ = ["fix_deprecated_ioheader", "from_string_cell_columns", "from_fs_columns", "to_string_cell_columns", "to_fs_columns"]

