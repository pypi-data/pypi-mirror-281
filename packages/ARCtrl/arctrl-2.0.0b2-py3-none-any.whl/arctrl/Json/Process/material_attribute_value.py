from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...fable_modules.fable_library.list import (choose, of_array)
from ...fable_modules.fable_library.option import default_arg
from ...fable_modules.fable_library.result import FSharpResult_2
from ...fable_modules.fable_library.string_ import (to_text, printf)
from ...fable_modules.fable_library.util import equals
from ...fable_modules.thoth_json_core.decode import (object, IOptionalGetter, IGetters)
from ...fable_modules.thoth_json_core.types import (Json, Decoder_1)
from ...fable_modules.thoth_json_python.decode import Decode_fromString
from ...fable_modules.thoth_json_python.encode import to_string
from ...Core.ontology_annotation import OntologyAnnotation
from ...Core.Process.material_attribute import MaterialAttribute
from ...Core.Process.material_attribute_value import (MaterialAttributeValue, MaterialAttributeValue_createAsPV)
from ...Core.Process.value import Value as Value_1
from ..decode import Decode_uri
from ..encode import (try_include, default_spaces)
from ..idtable import encode
from ..ontology_annotation import (OntologyAnnotation_ISAJson_encoder, OntologyAnnotation_ISAJson_decoder)
from .material_attribute import (MaterialAttribute_ISAJson_encoder, MaterialAttribute_ISAJson_decoder)
from .property_value import (encoder, decoder as decoder_1, gen_id)
from .value import (Value_ISAJson_encoder, Value_ISAJson_decoder)

MaterialAttributeValue_ROCrate_encoder: Callable[[MaterialAttributeValue], Json] = encoder

MaterialAttributeValue_ROCrate_decoder: Decoder_1[MaterialAttributeValue] = decoder_1(MaterialAttributeValue_createAsPV)

def MaterialAttributeValue_ISAJson_genID(oa: MaterialAttributeValue) -> str:
    return gen_id(oa)


def MaterialAttributeValue_ISAJson_encoder(id_map: Any | None, oa: MaterialAttributeValue) -> Json:
    def f(oa_1: MaterialAttributeValue, id_map: Any=id_map, oa: Any=oa) -> Json:
        def chooser(tupled_arg: tuple[str, Json], oa_1: Any=oa_1) -> tuple[str, Json] | None:
            v: Json = tupled_arg[1]
            if equals(v, Json(3)):
                return None

            else: 
                return (tupled_arg[0], v)


        def _arrow1406(value: str, oa_1: Any=oa_1) -> Json:
            return Json(0, value)

        def _arrow1407(value_2: MaterialAttribute, oa_1: Any=oa_1) -> Json:
            return MaterialAttribute_ISAJson_encoder(id_map, value_2)

        def _arrow1408(value_3: Value_1, oa_1: Any=oa_1) -> Json:
            return Value_ISAJson_encoder(id_map, value_3)

        def _arrow1409(oa_3: OntologyAnnotation, oa_1: Any=oa_1) -> Json:
            return OntologyAnnotation_ISAJson_encoder(id_map, oa_3)

        return Json(5, choose(chooser, of_array([try_include("@id", _arrow1406, MaterialAttributeValue_ISAJson_genID(oa_1)), try_include("category", _arrow1407, oa_1.Category), try_include("value", _arrow1408, oa_1.Value), try_include("unit", _arrow1409, oa_1.Unit)])))

    if id_map is not None:
        def _arrow1410(oa_4: MaterialAttributeValue, id_map: Any=id_map, oa: Any=oa) -> str:
            return MaterialAttributeValue_ISAJson_genID(oa_4)

        return encode(_arrow1410, f, oa, id_map)

    else: 
        return f(oa)



def _arrow1415(get: IGetters) -> MaterialAttributeValue:
    def _arrow1411(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("@id", Decode_uri)

    def _arrow1412(__unit: None=None) -> MaterialAttribute | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("category", MaterialAttribute_ISAJson_decoder)

    def _arrow1413(__unit: None=None) -> Value_1 | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("value", Value_ISAJson_decoder)

    def _arrow1414(__unit: None=None) -> OntologyAnnotation | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("unit", OntologyAnnotation_ISAJson_decoder)

    return MaterialAttributeValue(_arrow1411(), _arrow1412(), _arrow1413(), _arrow1414())


MaterialAttributeValue_ISAJson_decoder: Decoder_1[MaterialAttributeValue] = object(_arrow1415)

def ARCtrl_Process_MaterialAttributeValue__MaterialAttributeValue_fromISAJsonString_Static_Z721C83C5(s: str) -> MaterialAttributeValue:
    match_value: FSharpResult_2[MaterialAttributeValue, str] = Decode_fromString(MaterialAttributeValue_ISAJson_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_Process_MaterialAttributeValue__MaterialAttributeValue_toISAJsonString_Static_Z3B036AA(spaces: int | None=None, use_idreferencing: bool | None=None) -> Callable[[MaterialAttributeValue], str]:
    id_map: Any | None = dict([]) if default_arg(use_idreferencing, False) else None
    def _arrow1416(f: MaterialAttributeValue, spaces: Any=spaces, use_idreferencing: Any=use_idreferencing) -> str:
        value: Json = MaterialAttributeValue_ISAJson_encoder(id_map, f)
        return to_string(default_spaces(spaces), value)

    return _arrow1416


def ARCtrl_Process_MaterialAttributeValue__MaterialAttributeValue_ToISAJsonString_Z3B036AA(this: MaterialAttributeValue, spaces: int | None=None, use_idreferencing: bool | None=None) -> str:
    return ARCtrl_Process_MaterialAttributeValue__MaterialAttributeValue_toISAJsonString_Static_Z3B036AA(spaces, use_idreferencing)(this)


def ARCtrl_Process_MaterialAttributeValue__MaterialAttributeValue_fromROCrateJsonString_Static_Z721C83C5(s: str) -> MaterialAttributeValue:
    match_value: FSharpResult_2[MaterialAttributeValue, str] = Decode_fromString(MaterialAttributeValue_ROCrate_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_Process_MaterialAttributeValue__MaterialAttributeValue_toROCrateJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[MaterialAttributeValue], str]:
    def _arrow1417(f: MaterialAttributeValue, spaces: Any=spaces) -> str:
        value: Json = MaterialAttributeValue_ROCrate_encoder(f)
        return to_string(default_spaces(spaces), value)

    return _arrow1417


def ARCtrl_Process_MaterialAttributeValue__MaterialAttributeValue_ToROCrateJsonString_71136F3F(this: MaterialAttributeValue, spaces: int | None=None) -> str:
    return ARCtrl_Process_MaterialAttributeValue__MaterialAttributeValue_toROCrateJsonString_Static_71136F3F(spaces)(this)


__all__ = ["MaterialAttributeValue_ROCrate_encoder", "MaterialAttributeValue_ROCrate_decoder", "MaterialAttributeValue_ISAJson_genID", "MaterialAttributeValue_ISAJson_encoder", "MaterialAttributeValue_ISAJson_decoder", "ARCtrl_Process_MaterialAttributeValue__MaterialAttributeValue_fromISAJsonString_Static_Z721C83C5", "ARCtrl_Process_MaterialAttributeValue__MaterialAttributeValue_toISAJsonString_Static_Z3B036AA", "ARCtrl_Process_MaterialAttributeValue__MaterialAttributeValue_ToISAJsonString_Z3B036AA", "ARCtrl_Process_MaterialAttributeValue__MaterialAttributeValue_fromROCrateJsonString_Static_Z721C83C5", "ARCtrl_Process_MaterialAttributeValue__MaterialAttributeValue_toROCrateJsonString_Static_71136F3F", "ARCtrl_Process_MaterialAttributeValue__MaterialAttributeValue_ToROCrateJsonString_71136F3F"]

