from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...fable_modules.fable_library.list import (choose, of_array, singleton, FSharpList)
from ...fable_modules.fable_library.option import default_arg
from ...fable_modules.fable_library.result import FSharpResult_2
from ...fable_modules.fable_library.string_ import (replace, to_text, printf)
from ...fable_modules.fable_library.types import Array
from ...fable_modules.fable_library.util import equals
from ...fable_modules.thoth_json_core.decode import (object, IOptionalGetter, string, IGetters)
from ...fable_modules.thoth_json_core.encode import list_1 as list_1_1
from ...fable_modules.thoth_json_core.types import (Json, Decoder_1)
from ...fable_modules.thoth_json_python.decode import Decode_fromString
from ...fable_modules.thoth_json_python.encode import to_string
from ...Core.comment import Comment
from ...Core.data import Data
from ...Core.data_file import DataFile
from ...Core.uri import URIModule_toString
from ..comment import (Comment_encoder, Comment_decoder, Comment_ROCrate_encoder, Comment_ROCrate_decoder, Comment_ISAJson_encoder, Comment_ISAJson_decoder)
from ..context.rocrate.isa_data_context import context_jsonvalue
from ..decode import (Decode_uri, Decode_resizeArray, Decode_objectNoAdditionalProperties)
from ..encode import (try_include, try_include_seq, default_spaces)
from ..idtable import encode
from ..string_table import (encode_string, decode_string)
from .data_file import (DataFile_ISAJson_encoder, DataFile_ISAJson_decoder, DataFile_ROCrate_encoder, DataFile_ROCrate_decoder)

def Data_encoder(d: Data) -> Json:
    def chooser(tupled_arg: tuple[str, Json], d: Any=d) -> tuple[str, Json] | None:
        v: Json = tupled_arg[1]
        if equals(v, Json(3)):
            return None

        else: 
            return (tupled_arg[0], v)


    def _arrow1466(value: str, d: Any=d) -> Json:
        return Json(0, value)

    def _arrow1467(value_2: str, d: Any=d) -> Json:
        return Json(0, value_2)

    def _arrow1468(value_4: str, d: Any=d) -> Json:
        return Json(0, value_4)

    def _arrow1469(value_6: str, d: Any=d) -> Json:
        return Json(0, value_6)

    def _arrow1470(comment: Comment, d: Any=d) -> Json:
        return Comment_encoder(comment)

    return Json(5, choose(chooser, of_array([try_include("@id", _arrow1466, d.ID), try_include("name", _arrow1467, d.Name), try_include("dataType", DataFile_ISAJson_encoder, d.DataType), try_include("format", _arrow1468, d.Format), try_include("selectorFormat", _arrow1469, d.SelectorFormat), try_include_seq("comments", _arrow1470, d.Comments)])))


def _arrow1477(get: IGetters) -> Data:
    def _arrow1471(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("@id", Decode_uri)

    def _arrow1472(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("name", string)

    def _arrow1473(__unit: None=None) -> DataFile | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("dataType", DataFile_ISAJson_decoder)

    def _arrow1474(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("format", string)

    def _arrow1475(__unit: None=None) -> str | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("selectorFormat", Decode_uri)

    def _arrow1476(__unit: None=None) -> Array[Comment] | None:
        arg_11: Decoder_1[Array[Comment]] = Decode_resizeArray(Comment_decoder)
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("comments", arg_11)

    return Data(_arrow1471(), _arrow1472(), _arrow1473(), _arrow1474(), _arrow1475(), _arrow1476())


Data_decoder: Decoder_1[Data] = object(_arrow1477)

def Data_compressedEncoder(string_table: Any, d: Data) -> Json:
    def chooser(tupled_arg: tuple[str, Json], string_table: Any=string_table, d: Any=d) -> tuple[str, Json] | None:
        v: Json = tupled_arg[1]
        if equals(v, Json(3)):
            return None

        else: 
            return (tupled_arg[0], v)


    def _arrow1480(s: str, string_table: Any=string_table, d: Any=d) -> Json:
        return encode_string(string_table, s)

    def _arrow1481(s_1: str, string_table: Any=string_table, d: Any=d) -> Json:
        return encode_string(string_table, s_1)

    def _arrow1482(s_2: str, string_table: Any=string_table, d: Any=d) -> Json:
        return encode_string(string_table, s_2)

    def _arrow1483(s_3: str, string_table: Any=string_table, d: Any=d) -> Json:
        return encode_string(string_table, s_3)

    def _arrow1485(comment: Comment, string_table: Any=string_table, d: Any=d) -> Json:
        return Comment_encoder(comment)

    return Json(5, choose(chooser, of_array([try_include("i", _arrow1480, d.ID), try_include("n", _arrow1481, d.Name), try_include("d", DataFile_ISAJson_encoder, d.DataType), try_include("f", _arrow1482, d.Format), try_include("s", _arrow1483, d.SelectorFormat), try_include_seq("c", _arrow1485, d.Comments)])))


def Data_compressedDecoder(string_table: Array[str]) -> Decoder_1[Data]:
    def _arrow1502(get: IGetters, string_table: Any=string_table) -> Data:
        def _arrow1491(__unit: None=None) -> str | None:
            arg_1: Decoder_1[str] = decode_string(string_table)
            object_arg: IOptionalGetter = get.Optional
            return object_arg.Field("i", arg_1)

        def _arrow1494(__unit: None=None) -> str | None:
            arg_3: Decoder_1[str] = decode_string(string_table)
            object_arg_1: IOptionalGetter = get.Optional
            return object_arg_1.Field("n", arg_3)

        def _arrow1495(__unit: None=None) -> DataFile | None:
            object_arg_2: IOptionalGetter = get.Optional
            return object_arg_2.Field("d", DataFile_ISAJson_decoder)

        def _arrow1497(__unit: None=None) -> str | None:
            arg_7: Decoder_1[str] = decode_string(string_table)
            object_arg_3: IOptionalGetter = get.Optional
            return object_arg_3.Field("f", arg_7)

        def _arrow1498(__unit: None=None) -> str | None:
            arg_9: Decoder_1[str] = decode_string(string_table)
            object_arg_4: IOptionalGetter = get.Optional
            return object_arg_4.Field("s", arg_9)

        def _arrow1500(__unit: None=None) -> Array[Comment] | None:
            arg_11: Decoder_1[Array[Comment]] = Decode_resizeArray(Comment_decoder)
            object_arg_5: IOptionalGetter = get.Optional
            return object_arg_5.Field("c", arg_11)

        return Data(_arrow1491(), _arrow1494(), _arrow1495(), _arrow1497(), _arrow1498(), _arrow1500())

    return object(_arrow1502)


def Data_ROCrate_genID(d: Data) -> str:
    match_value: str | None = d.ID
    if match_value is None:
        match_value_1: str | None = d.Name
        if match_value_1 is None:
            return "#EmptyData"

        else: 
            return replace(match_value_1, " ", "_")


    else: 
        return URIModule_toString(match_value)



def Data_ROCrate_encoder(oa: Data) -> Json:
    def chooser(tupled_arg: tuple[str, Json], oa: Any=oa) -> tuple[str, Json] | None:
        v: Json = tupled_arg[1]
        if equals(v, Json(3)):
            return None

        else: 
            return (tupled_arg[0], v)


    def _arrow1505(value_2: str, oa: Any=oa) -> Json:
        return Json(0, value_2)

    def _arrow1507(value_4: DataFile, oa: Any=oa) -> Json:
        return DataFile_ROCrate_encoder(value_4)

    def _arrow1508(value_5: str, oa: Any=oa) -> Json:
        return Json(0, value_5)

    def _arrow1509(value_7: str, oa: Any=oa) -> Json:
        return Json(0, value_7)

    def _arrow1510(comment: Comment, oa: Any=oa) -> Json:
        return Comment_ROCrate_encoder(comment)

    return Json(5, choose(chooser, of_array([("@id", Json(0, Data_ROCrate_genID(oa))), ("@type", list_1_1(singleton(Json(0, "Data")))), try_include("name", _arrow1505, oa.Name), try_include("type", _arrow1507, oa.DataType), try_include("encodingFormat", _arrow1508, oa.Format), try_include("usageInfo", _arrow1509, oa.SelectorFormat), try_include_seq("comments", _arrow1510, oa.Comments), ("@context", context_jsonvalue)])))


def _arrow1518(get: IGetters) -> Data:
    def _arrow1512(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("@id", Decode_uri)

    def _arrow1513(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("name", string)

    def _arrow1514(__unit: None=None) -> DataFile | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("type", DataFile_ROCrate_decoder)

    def _arrow1515(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("encodingFormat", string)

    def _arrow1516(__unit: None=None) -> str | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("usageInfo", Decode_uri)

    def _arrow1517(__unit: None=None) -> Array[Comment] | None:
        arg_11: Decoder_1[Array[Comment]] = Decode_resizeArray(Comment_ROCrate_decoder)
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("comments", arg_11)

    return Data(_arrow1512(), _arrow1513(), _arrow1514(), _arrow1515(), _arrow1516(), _arrow1517())


Data_ROCrate_decoder: Decoder_1[Data] = object(_arrow1518)

def Data_ISAJson_encoder(id_map: Any | None, oa: Data) -> Json:
    def f(oa_1: Data, id_map: Any=id_map, oa: Any=oa) -> Json:
        def chooser(tupled_arg: tuple[str, Json], oa_1: Any=oa_1) -> tuple[str, Json] | None:
            v: Json = tupled_arg[1]
            if equals(v, Json(3)):
                return None

            else: 
                return (tupled_arg[0], v)


        def _arrow1520(value: str, oa_1: Any=oa_1) -> Json:
            return Json(0, value)

        def _arrow1521(value_2: str, oa_1: Any=oa_1) -> Json:
            return Json(0, value_2)

        def _arrow1522(comment: Comment, oa_1: Any=oa_1) -> Json:
            return Comment_ISAJson_encoder(id_map, comment)

        return Json(5, choose(chooser, of_array([try_include("@id", _arrow1520, Data_ROCrate_genID(oa_1)), try_include("name", _arrow1521, oa_1.Name), try_include("type", DataFile_ISAJson_encoder, oa_1.DataType), try_include_seq("comments", _arrow1522, oa_1.Comments)])))

    if id_map is not None:
        def _arrow1523(d_1: Data, id_map: Any=id_map, oa: Any=oa) -> str:
            return Data_ROCrate_genID(d_1)

        return encode(_arrow1523, f, oa, id_map)

    else: 
        return f(oa)



Data_ISAJson_allowedFields: FSharpList[str] = of_array(["@id", "name", "type", "comments", "@type", "@context"])

def _arrow1528(get: IGetters) -> Data:
    def _arrow1524(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("@id", Decode_uri)

    def _arrow1525(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("name", string)

    def _arrow1526(__unit: None=None) -> DataFile | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("type", DataFile_ISAJson_decoder)

    def _arrow1527(__unit: None=None) -> Array[Comment] | None:
        arg_7: Decoder_1[Array[Comment]] = Decode_resizeArray(Comment_ISAJson_decoder)
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("comments", arg_7)

    return Data(_arrow1524(), _arrow1525(), _arrow1526(), None, None, _arrow1527())


Data_ISAJson_decoder: Decoder_1[Data] = Decode_objectNoAdditionalProperties(Data_ISAJson_allowedFields, _arrow1528)

def ARCtrl_Data__Data_fromISAJsonString_Static_Z721C83C5(s: str) -> Data:
    match_value: FSharpResult_2[Data, str] = Decode_fromString(Data_ISAJson_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_Data__Data_toISAJsonString_Static_Z3B036AA(spaces: int | None=None, use_idreferencing: bool | None=None) -> Callable[[Data], str]:
    id_map: Any | None = dict([]) if default_arg(use_idreferencing, False) else None
    def _arrow1529(f: Data, spaces: Any=spaces, use_idreferencing: Any=use_idreferencing) -> str:
        value_1: Json = Data_ISAJson_encoder(id_map, f)
        return to_string(default_spaces(spaces), value_1)

    return _arrow1529


def ARCtrl_Data__Data_toISAJsonString_Z3B036AA(this: Data, spaces: int | None=None, use_idreferencing: bool | None=None) -> str:
    return ARCtrl_Data__Data_toISAJsonString_Static_Z3B036AA(spaces, use_idreferencing)(this)


def ARCtrl_Data__Data_fromROCrateJsonString_Static_Z721C83C5(s: str) -> Data:
    match_value: FSharpResult_2[Data, str] = Decode_fromString(Data_ROCrate_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_Data__Data_toROCrateJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[Data], str]:
    def _arrow1530(f: Data, spaces: Any=spaces) -> str:
        value: Json = Data_ROCrate_encoder(f)
        return to_string(default_spaces(spaces), value)

    return _arrow1530


def ARCtrl_Data__Data_toROCrateJsonString_71136F3F(this: Data, spaces: int | None=None) -> str:
    return ARCtrl_Data__Data_toROCrateJsonString_Static_71136F3F(spaces)(this)


__all__ = ["Data_encoder", "Data_decoder", "Data_compressedEncoder", "Data_compressedDecoder", "Data_ROCrate_genID", "Data_ROCrate_encoder", "Data_ROCrate_decoder", "Data_ISAJson_encoder", "Data_ISAJson_allowedFields", "Data_ISAJson_decoder", "ARCtrl_Data__Data_fromISAJsonString_Static_Z721C83C5", "ARCtrl_Data__Data_toISAJsonString_Static_Z3B036AA", "ARCtrl_Data__Data_toISAJsonString_Z3B036AA", "ARCtrl_Data__Data_fromROCrateJsonString_Static_Z721C83C5", "ARCtrl_Data__Data_toROCrateJsonString_Static_71136F3F", "ARCtrl_Data__Data_toROCrateJsonString_71136F3F"]

