from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..fable_modules.fable_library.list import (choose, of_array)
from ..fable_modules.fable_library.result import FSharpResult_2
from ..fable_modules.fable_library.string_ import (replace, to_text, printf)
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import equals
from ..fable_modules.thoth_json_core.decode import (object, IOptionalGetter, string, IGetters)
from ..fable_modules.thoth_json_core.types import (Json, Decoder_1)
from ..fable_modules.thoth_json_python.decode import Decode_fromString
from ..fable_modules.thoth_json_python.encode import to_string
from ..Core.comment import Comment
from ..Core.ontology_source_reference import OntologySourceReference
from .comment import (Comment_encoder, Comment_decoder, Comment_ISAJson_encoder)
from .context.rocrate.isa_ontology_source_reference_context import context_jsonvalue
from .decode import (Decode_uri, Decode_resizeArray)
from .encode import (try_include, try_include_seq, default_spaces)

def OntologySourceReference_encoder(osr: OntologySourceReference) -> Json:
    def chooser(tupled_arg: tuple[str, Json], osr: Any=osr) -> tuple[str, Json] | None:
        v: Json = tupled_arg[1]
        if equals(v, Json(3)):
            return None

        else: 
            return (tupled_arg[0], v)


    def _arrow1163(value: str, osr: Any=osr) -> Json:
        return Json(0, value)

    def _arrow1164(value_2: str, osr: Any=osr) -> Json:
        return Json(0, value_2)

    def _arrow1165(value_4: str, osr: Any=osr) -> Json:
        return Json(0, value_4)

    def _arrow1166(value_6: str, osr: Any=osr) -> Json:
        return Json(0, value_6)

    def _arrow1167(comment: Comment, osr: Any=osr) -> Json:
        return Comment_encoder(comment)

    return Json(5, choose(chooser, of_array([try_include("description", _arrow1163, osr.Description), try_include("file", _arrow1164, osr.File), try_include("name", _arrow1165, osr.Name), try_include("version", _arrow1166, osr.Version), try_include_seq("comments", _arrow1167, osr.Comments)])))


def _arrow1173(get: IGetters) -> OntologySourceReference:
    def _arrow1168(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("description", Decode_uri)

    def _arrow1169(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("file", string)

    def _arrow1170(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("name", string)

    def _arrow1171(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("version", string)

    def _arrow1172(__unit: None=None) -> Array[Comment] | None:
        arg_9: Decoder_1[Array[Comment]] = Decode_resizeArray(Comment_decoder)
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("comments", arg_9)

    return OntologySourceReference(_arrow1168(), _arrow1169(), _arrow1170(), _arrow1171(), _arrow1172())


OntologySourceReference_decoder: Decoder_1[OntologySourceReference] = object(_arrow1173)

def OntologySourceReference_ROCrate_genID(o: OntologySourceReference) -> str:
    match_value: str | None = o.File
    if match_value is None:
        match_value_1: str | None = o.Name
        if match_value_1 is None:
            return "#DummyOntologySourceRef"

        else: 
            return "#OntologySourceRef_" + replace(match_value_1, " ", "_")


    else: 
        return match_value



def OntologySourceReference_ROCrate_encoder(osr: OntologySourceReference) -> Json:
    def chooser(tupled_arg: tuple[str, Json], osr: Any=osr) -> tuple[str, Json] | None:
        v: Json = tupled_arg[1]
        if equals(v, Json(3)):
            return None

        else: 
            return (tupled_arg[0], v)


    def _arrow1174(value_2: str, osr: Any=osr) -> Json:
        return Json(0, value_2)

    def _arrow1175(value_4: str, osr: Any=osr) -> Json:
        return Json(0, value_4)

    def _arrow1176(value_6: str, osr: Any=osr) -> Json:
        return Json(0, value_6)

    def _arrow1177(value_8: str, osr: Any=osr) -> Json:
        return Json(0, value_8)

    def _arrow1178(comment: Comment, osr: Any=osr) -> Json:
        return Comment_encoder(comment)

    return Json(5, choose(chooser, of_array([("@id", Json(0, OntologySourceReference_ROCrate_genID(osr))), ("@type", Json(0, "OntologySourceReference")), try_include("description", _arrow1174, osr.Description), try_include("file", _arrow1175, osr.File), try_include("name", _arrow1176, osr.Name), try_include("version", _arrow1177, osr.Version), try_include_seq("comments", _arrow1178, osr.Comments), ("@context", context_jsonvalue)])))


def _arrow1184(get: IGetters) -> OntologySourceReference:
    def _arrow1179(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("description", Decode_uri)

    def _arrow1180(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("file", string)

    def _arrow1181(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("name", string)

    def _arrow1182(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("version", string)

    def _arrow1183(__unit: None=None) -> Array[Comment] | None:
        arg_9: Decoder_1[Array[Comment]] = Decode_resizeArray(Comment_decoder)
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("comments", arg_9)

    return OntologySourceReference(_arrow1179(), _arrow1180(), _arrow1181(), _arrow1182(), _arrow1183())


OntologySourceReference_ROCrate_decoder: Decoder_1[OntologySourceReference] = object(_arrow1184)

def OntologySourceReference_ISAJson_encoder(id_map: Any | None, osr: OntologySourceReference) -> Json:
    def chooser(tupled_arg: tuple[str, Json], id_map: Any=id_map, osr: Any=osr) -> tuple[str, Json] | None:
        v: Json = tupled_arg[1]
        if equals(v, Json(3)):
            return None

        else: 
            return (tupled_arg[0], v)


    def _arrow1186(value: str, id_map: Any=id_map, osr: Any=osr) -> Json:
        return Json(0, value)

    def _arrow1187(value_2: str, id_map: Any=id_map, osr: Any=osr) -> Json:
        return Json(0, value_2)

    def _arrow1188(value_4: str, id_map: Any=id_map, osr: Any=osr) -> Json:
        return Json(0, value_4)

    def _arrow1189(value_6: str, id_map: Any=id_map, osr: Any=osr) -> Json:
        return Json(0, value_6)

    def _arrow1190(comment: Comment, id_map: Any=id_map, osr: Any=osr) -> Json:
        return Comment_ISAJson_encoder(id_map, comment)

    return Json(5, choose(chooser, of_array([try_include("description", _arrow1186, osr.Description), try_include("file", _arrow1187, osr.File), try_include("name", _arrow1188, osr.Name), try_include("version", _arrow1189, osr.Version), try_include_seq("comments", _arrow1190, osr.Comments)])))


OntologySourceReference_ISAJson_decoder: Decoder_1[OntologySourceReference] = OntologySourceReference_decoder

def ARCtrl_OntologySourceReference__OntologySourceReference_fromJsonString_Static_Z721C83C5(s: str) -> OntologySourceReference:
    match_value: FSharpResult_2[OntologySourceReference, str] = Decode_fromString(OntologySourceReference_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_OntologySourceReference__OntologySourceReference_toJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[OntologySourceReference], str]:
    def _arrow1191(obj: OntologySourceReference, spaces: Any=spaces) -> str:
        value: Json = OntologySourceReference_encoder(obj)
        return to_string(default_spaces(spaces), value)

    return _arrow1191


def ARCtrl_OntologySourceReference__OntologySourceReference_ToJsonString_71136F3F(this: OntologySourceReference, spaces: int | None=None) -> str:
    return ARCtrl_OntologySourceReference__OntologySourceReference_toJsonString_Static_71136F3F(spaces)(this)


def ARCtrl_OntologySourceReference__OntologySourceReference_fromROCrateJsonString_Static_Z721C83C5(s: str) -> OntologySourceReference:
    match_value: FSharpResult_2[OntologySourceReference, str] = Decode_fromString(OntologySourceReference_ROCrate_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_OntologySourceReference__OntologySourceReference_toROCrateJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[OntologySourceReference], str]:
    def _arrow1192(obj: OntologySourceReference, spaces: Any=spaces) -> str:
        value: Json = OntologySourceReference_ROCrate_encoder(obj)
        return to_string(default_spaces(spaces), value)

    return _arrow1192


def ARCtrl_OntologySourceReference__OntologySourceReference_ToROCrateJsonString_71136F3F(this: OntologySourceReference, spaces: int | None=None) -> str:
    return ARCtrl_OntologySourceReference__OntologySourceReference_toROCrateJsonString_Static_71136F3F(spaces)(this)


def ARCtrl_OntologySourceReference__OntologySourceReference_fromISAJsonString_Static_Z721C83C5(s: str) -> OntologySourceReference:
    match_value: FSharpResult_2[OntologySourceReference, str] = Decode_fromString(OntologySourceReference_ISAJson_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_OntologySourceReference__OntologySourceReference_toISAJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[OntologySourceReference], str]:
    def _arrow1193(obj: OntologySourceReference, spaces: Any=spaces) -> str:
        value: Json = OntologySourceReference_ISAJson_encoder(None, obj)
        return to_string(default_spaces(spaces), value)

    return _arrow1193


def ARCtrl_OntologySourceReference__OntologySourceReference_ToISAJsonString_71136F3F(this: OntologySourceReference, spaces: int | None=None) -> str:
    return ARCtrl_OntologySourceReference__OntologySourceReference_toISAJsonString_Static_71136F3F(spaces)(this)


__all__ = ["OntologySourceReference_encoder", "OntologySourceReference_decoder", "OntologySourceReference_ROCrate_genID", "OntologySourceReference_ROCrate_encoder", "OntologySourceReference_ROCrate_decoder", "OntologySourceReference_ISAJson_encoder", "OntologySourceReference_ISAJson_decoder", "ARCtrl_OntologySourceReference__OntologySourceReference_fromJsonString_Static_Z721C83C5", "ARCtrl_OntologySourceReference__OntologySourceReference_toJsonString_Static_71136F3F", "ARCtrl_OntologySourceReference__OntologySourceReference_ToJsonString_71136F3F", "ARCtrl_OntologySourceReference__OntologySourceReference_fromROCrateJsonString_Static_Z721C83C5", "ARCtrl_OntologySourceReference__OntologySourceReference_toROCrateJsonString_Static_71136F3F", "ARCtrl_OntologySourceReference__OntologySourceReference_ToROCrateJsonString_71136F3F", "ARCtrl_OntologySourceReference__OntologySourceReference_fromISAJsonString_Static_Z721C83C5", "ARCtrl_OntologySourceReference__OntologySourceReference_toISAJsonString_Static_71136F3F", "ARCtrl_OntologySourceReference__OntologySourceReference_ToISAJsonString_71136F3F"]

