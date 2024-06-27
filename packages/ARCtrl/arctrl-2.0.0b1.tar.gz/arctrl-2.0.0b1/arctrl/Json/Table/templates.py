from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...fable_modules.fable_library.array_ import map
from ...fable_modules.fable_library.date import to_string as to_string_1
from ...fable_modules.fable_library.option import default_arg
from ...fable_modules.fable_library.result import FSharpResult_2
from ...fable_modules.fable_library.string_ import (to_fail, printf, to_text)
from ...fable_modules.fable_library.types import (to_string, Array)
from ...fable_modules.fable_library.util import to_enumerable
from ...fable_modules.thoth_json_core.decode import (and_then, succeed, string, object, IRequiredGetter, guid, IOptionalGetter, IGetters, datetime_local, array as array_1)
from ...fable_modules.thoth_json_core.types import (Json, Decoder_1)
from ...fable_modules.thoth_json_python.decode import Decode_fromString
from ...fable_modules.thoth_json_python.encode import to_string as to_string_2
from ...Core.ontology_annotation import OntologyAnnotation
from ...Core.person import Person
from ...Core.Table.arc_table import ArcTable
from ...Core.Table.composite_cell import CompositeCell
from ...Core.template import (Organisation, Template)
from ..decode import (Decode_resizeArray, Decode_datetime)
from ..encode import (try_include_seq, date_time, default_spaces)
from ..ontology_annotation import (OntologyAnnotation_encoder, OntologyAnnotation_decoder)
from ..person import (Person_encoder, Person_decoder)
from .arc_table import (ArcTable_encoder, ArcTable_decoder, ArcTable_encoderCompressed, ArcTable_decoderCompressed)
from .compression import (decode, encode)

def _arrow1713(arg: Organisation) -> Json:
    return Json(0, to_string(arg))


Template_Organisation_encoder: Callable[[Organisation], Json] = _arrow1713

def cb(text_value: str) -> Decoder_1[Organisation]:
    return succeed(Organisation.of_string(text_value))


Template_Organisation_decoder: Decoder_1[Organisation] = and_then(cb, string)

def Template_encoder(template: Template) -> Json:
    def _arrow1714(__unit: None=None, template: Any=template) -> str:
        copy_of_struct: str = template.Id
        return str(copy_of_struct)

    def _arrow1715(person: Person, template: Any=template) -> Json:
        return Person_encoder(person)

    def _arrow1716(oa: OntologyAnnotation, template: Any=template) -> Json:
        return OntologyAnnotation_encoder(oa)

    def _arrow1717(oa_1: OntologyAnnotation, template: Any=template) -> Json:
        return OntologyAnnotation_encoder(oa_1)

    return Json(5, to_enumerable([("id", Json(0, _arrow1714())), ("table", ArcTable_encoder(template.Table)), ("name", Json(0, template.Name)), ("description", Json(0, template.Description)), ("organisation", Template_Organisation_encoder(template.Organisation)), ("version", Json(0, template.Version)), try_include_seq("authors", _arrow1715, template.Authors), try_include_seq("endpoint_repositories", _arrow1716, template.EndpointRepositories), try_include_seq("tags", _arrow1717, template.Tags), ("last_updated", date_time(template.LastUpdated))]))


def _arrow1728(get: IGetters) -> Template:
    def _arrow1718(__unit: None=None) -> str:
        object_arg: IRequiredGetter = get.Required
        return object_arg.Field("id", guid)

    def _arrow1719(__unit: None=None) -> ArcTable:
        object_arg_1: IRequiredGetter = get.Required
        return object_arg_1.Field("table", ArcTable_decoder)

    def _arrow1720(__unit: None=None) -> str:
        object_arg_2: IRequiredGetter = get.Required
        return object_arg_2.Field("name", string)

    def _arrow1721(__unit: None=None) -> str:
        object_arg_3: IRequiredGetter = get.Required
        return object_arg_3.Field("description", string)

    def _arrow1722(__unit: None=None) -> Organisation:
        object_arg_4: IRequiredGetter = get.Required
        return object_arg_4.Field("organisation", Template_Organisation_decoder)

    def _arrow1723(__unit: None=None) -> str:
        object_arg_5: IRequiredGetter = get.Required
        return object_arg_5.Field("version", string)

    def _arrow1724(__unit: None=None) -> Array[Person] | None:
        arg_13: Decoder_1[Array[Person]] = Decode_resizeArray(Person_decoder)
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("authors", arg_13)

    def _arrow1725(__unit: None=None) -> Array[OntologyAnnotation] | None:
        arg_15: Decoder_1[Array[OntologyAnnotation]] = Decode_resizeArray(OntologyAnnotation_decoder)
        object_arg_7: IOptionalGetter = get.Optional
        return object_arg_7.Field("endpoint_repositories", arg_15)

    def _arrow1726(__unit: None=None) -> Array[OntologyAnnotation] | None:
        arg_17: Decoder_1[Array[OntologyAnnotation]] = Decode_resizeArray(OntologyAnnotation_decoder)
        object_arg_8: IOptionalGetter = get.Optional
        return object_arg_8.Field("tags", arg_17)

    def _arrow1727(__unit: None=None) -> Any:
        object_arg_9: IRequiredGetter = get.Required
        return object_arg_9.Field("last_updated", Decode_datetime)

    return Template.create(_arrow1718(), _arrow1719(), _arrow1720(), _arrow1721(), _arrow1722(), _arrow1723(), _arrow1724(), _arrow1725(), _arrow1726(), _arrow1727())


Template_decoder: Decoder_1[Template] = object(_arrow1728)

def Template_encoderCompressed(string_table: Any, oa_table: Any, cell_table: Any, template: Template) -> Json:
    def _arrow1729(__unit: None=None, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, template: Any=template) -> str:
        copy_of_struct: str = template.Id
        return str(copy_of_struct)

    def _arrow1730(person: Person, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, template: Any=template) -> Json:
        return Person_encoder(person)

    def _arrow1731(oa: OntologyAnnotation, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, template: Any=template) -> Json:
        return OntologyAnnotation_encoder(oa)

    def _arrow1732(oa_1: OntologyAnnotation, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, template: Any=template) -> Json:
        return OntologyAnnotation_encoder(oa_1)

    return Json(5, to_enumerable([("id", Json(0, _arrow1729())), ("table", ArcTable_encoderCompressed(string_table, oa_table, cell_table, template.Table)), ("name", Json(0, template.Name)), ("description", Json(0, template.Description)), ("organisation", Template_Organisation_encoder(template.Organisation)), ("version", Json(0, template.Version)), try_include_seq("authors", _arrow1730, template.Authors), try_include_seq("endpoint_repositories", _arrow1731, template.EndpointRepositories), try_include_seq("tags", _arrow1732, template.Tags), ("last_updated", Json(0, to_string_1(template.LastUpdated, "O", {})))]))


def Template_decoderCompressed(string_table: Array[str], oa_table: Array[OntologyAnnotation], cell_table: Array[CompositeCell]) -> Decoder_1[Template]:
    def _arrow1743(get: IGetters, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table) -> Template:
        def _arrow1733(__unit: None=None) -> str:
            object_arg: IRequiredGetter = get.Required
            return object_arg.Field("id", guid)

        def _arrow1734(__unit: None=None) -> ArcTable:
            arg_3: Decoder_1[ArcTable] = ArcTable_decoderCompressed(string_table, oa_table, cell_table)
            object_arg_1: IRequiredGetter = get.Required
            return object_arg_1.Field("table", arg_3)

        def _arrow1735(__unit: None=None) -> str:
            object_arg_2: IRequiredGetter = get.Required
            return object_arg_2.Field("name", string)

        def _arrow1736(__unit: None=None) -> str:
            object_arg_3: IRequiredGetter = get.Required
            return object_arg_3.Field("description", string)

        def _arrow1737(__unit: None=None) -> Organisation:
            object_arg_4: IRequiredGetter = get.Required
            return object_arg_4.Field("organisation", Template_Organisation_decoder)

        def _arrow1738(__unit: None=None) -> str:
            object_arg_5: IRequiredGetter = get.Required
            return object_arg_5.Field("version", string)

        def _arrow1739(__unit: None=None) -> Array[Person] | None:
            arg_13: Decoder_1[Array[Person]] = Decode_resizeArray(Person_decoder)
            object_arg_6: IOptionalGetter = get.Optional
            return object_arg_6.Field("authors", arg_13)

        def _arrow1740(__unit: None=None) -> Array[OntologyAnnotation] | None:
            arg_15: Decoder_1[Array[OntologyAnnotation]] = Decode_resizeArray(OntologyAnnotation_decoder)
            object_arg_7: IOptionalGetter = get.Optional
            return object_arg_7.Field("endpoint_repositories", arg_15)

        def _arrow1741(__unit: None=None) -> Array[OntologyAnnotation] | None:
            arg_17: Decoder_1[Array[OntologyAnnotation]] = Decode_resizeArray(OntologyAnnotation_decoder)
            object_arg_8: IOptionalGetter = get.Optional
            return object_arg_8.Field("tags", arg_17)

        def _arrow1742(__unit: None=None) -> Any:
            object_arg_9: IRequiredGetter = get.Required
            return object_arg_9.Field("last_updated", datetime_local)

        return Template.create(_arrow1733(), _arrow1734(), _arrow1735(), _arrow1736(), _arrow1737(), _arrow1738(), _arrow1739(), _arrow1740(), _arrow1741(), _arrow1742())

    return object(_arrow1743)


def Templates_encoder(templates: Array[Template]) -> Json:
    def mapping(template: Template, templates: Any=templates) -> Json:
        return Template_encoder(template)

    return Json(6, map(mapping, templates, None))


Templates_decoder: Decoder_1[Array[Template]] = array_1(Template_decoder)

def Templates_fromJsonString(json_string: str) -> Array[Template]:
    try: 
        match_value: FSharpResult_2[Array[Template], str] = Decode_fromString(Templates_decoder, json_string)
        if match_value.tag == 1:
            raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

        else: 
            return match_value.fields[0]


    except Exception as exn:
        return to_fail(printf("Error. Given json string cannot be parsed to Templates map: %A"))(exn)



def Templates_toJsonString(spaces: int, templates: Array[Template]) -> str:
    return to_string_2(spaces, Templates_encoder(templates))


def ARCtrl_Template__Template_fromJsonString_Static_Z721C83C5(json_string: str) -> Template:
    try: 
        match_value: FSharpResult_2[Template, str] = Decode_fromString(Template_decoder, json_string)
        if match_value.tag == 1:
            raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

        else: 
            return match_value.fields[0]


    except Exception as exn:
        return to_fail(printf("Error. Given json string cannot be parsed to Template: %A"))(exn)



def ARCtrl_Template__Template_toJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[Template], str]:
    def _arrow1744(template: Template, spaces: Any=spaces) -> str:
        return to_string_2(default_spaces(spaces), Template_encoder(template))

    return _arrow1744


def ARCtrl_Template__Template_toJsonString_71136F3F(this: Template, spaces: int | None=None) -> str:
    return ARCtrl_Template__Template_toJsonString_Static_71136F3F(spaces)(this)


def ARCtrl_Template__Template_fromCompressedJsonString_Static_Z721C83C5(s: str) -> Template:
    try: 
        match_value: FSharpResult_2[Template, str] = Decode_fromString(decode(Template_decoderCompressed), s)
        if match_value.tag == 1:
            raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

        else: 
            return match_value.fields[0]


    except Exception as e_1:
        arg_1: str = str(e_1)
        return to_fail(printf("Error. Unable to parse json string to ArcStudy: %s"))(arg_1)



def ARCtrl_Template__Template_toCompressedJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[Template], str]:
    def _arrow1745(obj: Template, spaces: Any=spaces) -> str:
        return to_string_2(default_arg(spaces, 0), encode(Template_encoderCompressed, obj))

    return _arrow1745


def ARCtrl_Template__Template_toCompressedJsonString_71136F3F(this: Template, spaces: int | None=None) -> str:
    return ARCtrl_Template__Template_toCompressedJsonString_Static_71136F3F(spaces)(this)


__all__ = ["Template_Organisation_encoder", "Template_Organisation_decoder", "Template_encoder", "Template_decoder", "Template_encoderCompressed", "Template_decoderCompressed", "Templates_encoder", "Templates_decoder", "Templates_fromJsonString", "Templates_toJsonString", "ARCtrl_Template__Template_fromJsonString_Static_Z721C83C5", "ARCtrl_Template__Template_toJsonString_Static_71136F3F", "ARCtrl_Template__Template_toJsonString_71136F3F", "ARCtrl_Template__Template_fromCompressedJsonString_Static_Z721C83C5", "ARCtrl_Template__Template_toCompressedJsonString_Static_71136F3F", "ARCtrl_Template__Template_toCompressedJsonString_71136F3F"]

