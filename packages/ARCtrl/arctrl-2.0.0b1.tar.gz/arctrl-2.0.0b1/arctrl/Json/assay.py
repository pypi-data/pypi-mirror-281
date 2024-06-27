from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..fable_modules.fable_library.list import (choose, of_array, FSharpList, singleton, empty)
from ..fable_modules.fable_library.option import (default_arg, map, bind)
from ..fable_modules.fable_library.result import FSharpResult_2
from ..fable_modules.fable_library.string_ import (replace, to_text, printf, to_fail)
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import equals
from ..fable_modules.thoth_json_core.decode import (object, IRequiredGetter, string, IOptionalGetter, IGetters, list_1 as list_1_2, map as map_1)
from ..fable_modules.thoth_json_core.encode import list_1 as list_1_1
from ..fable_modules.thoth_json_core.types import (Json, Decoder_1)
from ..fable_modules.thoth_json_python.decode import Decode_fromString
from ..fable_modules.thoth_json_python.encode import to_string
from ..Core.arc_types import ArcAssay
from ..Core.comment import Comment
from ..Core.conversion import (ARCtrl_ArcTables__ArcTables_GetProcesses, ARCtrl_ArcTables__ArcTables_fromProcesses_Static_62A3309D, JsonTypes_composeTechnologyPlatform, JsonTypes_decomposeTechnologyPlatform)
from ..Core.data import Data
from ..Core.Helper.collections_ import Option_fromValueWithDefault
from ..Core.Helper.identifier import (Assay_fileNameFromIdentifier, create_missing_identifier, Assay_tryIdentifierFromFileName)
from ..Core.ontology_annotation import OntologyAnnotation
from ..Core.person import Person
from ..Core.Process.material_attribute import MaterialAttribute
from ..Core.Process.process import Process
from ..Core.Process.process_sequence import (get_data, get_units, get_characteristics)
from ..Core.Table.arc_table import ArcTable
from ..Core.Table.arc_tables import ArcTables
from ..Core.Table.composite_cell import CompositeCell
from .comment import (Comment_encoder, Comment_decoder, Comment_ROCrate_encoder, Comment_ROCrate_decoder, Comment_ISAJson_encoder, Comment_ISAJson_decoder)
from .context.rocrate.isa_assay_context import context_jsonvalue
from .decode import (Decode_resizeArray, Decode_objectNoAdditionalProperties)
from .encode import (try_include, try_include_seq, try_include_list, default_spaces)
from .idtable import encode
from .ontology_annotation import (OntologyAnnotation_encoder, OntologyAnnotation_decoder, OntologyAnnotation_ROCrate_encoderPropertyValue, OntologyAnnotation_ROCrate_encoderDefinedTerm, OntologyAnnotation_ROCrate_decoderPropertyValue, OntologyAnnotation_ROCrate_decoderDefinedTerm, OntologyAnnotation_ISAJson_encoder, OntologyAnnotation_ISAJson_decoder)
from .person import (Person_encoder, Person_decoder, Person_ROCrate_encoder, Person_ROCrate_decoder)
from .Process.assay_materials import encoder as encoder_3
from .Process.data import (Data_ROCrate_encoder, Data_ISAJson_encoder)
from .Process.material_attribute import MaterialAttribute_ISAJson_encoder
from .Process.process import (Process_ROCrate_encoder, Process_ROCrate_decoder, Process_ISAJson_encoder, Process_ISAJson_decoder)
from .Table.arc_table import (ArcTable_encoder, ArcTable_decoder, ArcTable_encoderCompressed, ArcTable_decoderCompressed)
from .Table.compression import (decode, encode as encode_1)

def Assay_encoder(assay: ArcAssay) -> Json:
    def chooser(tupled_arg: tuple[str, Json], assay: Any=assay) -> tuple[str, Json] | None:
        v: Json = tupled_arg[1]
        if equals(v, Json(3)):
            return None

        else: 
            return (tupled_arg[0], v)


    def _arrow1746(oa: OntologyAnnotation, assay: Any=assay) -> Json:
        return OntologyAnnotation_encoder(oa)

    def _arrow1747(oa_1: OntologyAnnotation, assay: Any=assay) -> Json:
        return OntologyAnnotation_encoder(oa_1)

    def _arrow1748(oa_2: OntologyAnnotation, assay: Any=assay) -> Json:
        return OntologyAnnotation_encoder(oa_2)

    def _arrow1749(table: ArcTable, assay: Any=assay) -> Json:
        return ArcTable_encoder(table)

    def _arrow1750(person: Person, assay: Any=assay) -> Json:
        return Person_encoder(person)

    def _arrow1751(comment: Comment, assay: Any=assay) -> Json:
        return Comment_encoder(comment)

    return Json(5, choose(chooser, of_array([("Identifier", Json(0, assay.Identifier)), try_include("MeasurementType", _arrow1746, assay.MeasurementType), try_include("TechnologyType", _arrow1747, assay.TechnologyType), try_include("TechnologyPlatform", _arrow1748, assay.TechnologyPlatform), try_include_seq("Tables", _arrow1749, assay.Tables), try_include_seq("Performers", _arrow1750, assay.Performers), try_include_seq("Comments", _arrow1751, assay.Comments)])))


def _arrow1759(get: IGetters) -> ArcAssay:
    def _arrow1752(__unit: None=None) -> str:
        object_arg: IRequiredGetter = get.Required
        return object_arg.Field("Identifier", string)

    def _arrow1753(__unit: None=None) -> OntologyAnnotation | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("MeasurementType", OntologyAnnotation_decoder)

    def _arrow1754(__unit: None=None) -> OntologyAnnotation | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("TechnologyType", OntologyAnnotation_decoder)

    def _arrow1755(__unit: None=None) -> OntologyAnnotation | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("TechnologyPlatform", OntologyAnnotation_decoder)

    def _arrow1756(__unit: None=None) -> Array[ArcTable] | None:
        arg_9: Decoder_1[Array[ArcTable]] = Decode_resizeArray(ArcTable_decoder)
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("Tables", arg_9)

    def _arrow1757(__unit: None=None) -> Array[Person] | None:
        arg_11: Decoder_1[Array[Person]] = Decode_resizeArray(Person_decoder)
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("Performers", arg_11)

    def _arrow1758(__unit: None=None) -> Array[Comment] | None:
        arg_13: Decoder_1[Array[Comment]] = Decode_resizeArray(Comment_decoder)
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("Comments", arg_13)

    return ArcAssay.create(_arrow1752(), _arrow1753(), _arrow1754(), _arrow1755(), _arrow1756(), None, _arrow1757(), _arrow1758())


Assay_decoder: Decoder_1[ArcAssay] = object(_arrow1759)

def Assay_encoderCompressed(string_table: Any, oa_table: Any, cell_table: Any, assay: ArcAssay) -> Json:
    def chooser(tupled_arg: tuple[str, Json], string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, assay: Any=assay) -> tuple[str, Json] | None:
        v: Json = tupled_arg[1]
        if equals(v, Json(3)):
            return None

        else: 
            return (tupled_arg[0], v)


    def _arrow1760(oa: OntologyAnnotation, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, assay: Any=assay) -> Json:
        return OntologyAnnotation_encoder(oa)

    def _arrow1761(oa_1: OntologyAnnotation, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, assay: Any=assay) -> Json:
        return OntologyAnnotation_encoder(oa_1)

    def _arrow1762(oa_2: OntologyAnnotation, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, assay: Any=assay) -> Json:
        return OntologyAnnotation_encoder(oa_2)

    def _arrow1763(table: ArcTable, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, assay: Any=assay) -> Json:
        return ArcTable_encoderCompressed(string_table, oa_table, cell_table, table)

    def _arrow1764(person: Person, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, assay: Any=assay) -> Json:
        return Person_encoder(person)

    def _arrow1765(comment: Comment, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, assay: Any=assay) -> Json:
        return Comment_encoder(comment)

    return Json(5, choose(chooser, of_array([("Identifier", Json(0, assay.Identifier)), try_include("MeasurementType", _arrow1760, assay.MeasurementType), try_include("TechnologyType", _arrow1761, assay.TechnologyType), try_include("TechnologyPlatform", _arrow1762, assay.TechnologyPlatform), try_include_seq("Tables", _arrow1763, assay.Tables), try_include_seq("Performers", _arrow1764, assay.Performers), try_include_seq("Comments", _arrow1765, assay.Comments)])))


def Assay_decoderCompressed(string_table: Array[str], oa_table: Array[OntologyAnnotation], cell_table: Array[CompositeCell]) -> Decoder_1[ArcAssay]:
    def _arrow1773(get: IGetters, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table) -> ArcAssay:
        def _arrow1766(__unit: None=None) -> str:
            object_arg: IRequiredGetter = get.Required
            return object_arg.Field("Identifier", string)

        def _arrow1767(__unit: None=None) -> OntologyAnnotation | None:
            object_arg_1: IOptionalGetter = get.Optional
            return object_arg_1.Field("MeasurementType", OntologyAnnotation_decoder)

        def _arrow1768(__unit: None=None) -> OntologyAnnotation | None:
            object_arg_2: IOptionalGetter = get.Optional
            return object_arg_2.Field("TechnologyType", OntologyAnnotation_decoder)

        def _arrow1769(__unit: None=None) -> OntologyAnnotation | None:
            object_arg_3: IOptionalGetter = get.Optional
            return object_arg_3.Field("TechnologyPlatform", OntologyAnnotation_decoder)

        def _arrow1770(__unit: None=None) -> Array[ArcTable] | None:
            arg_9: Decoder_1[Array[ArcTable]] = Decode_resizeArray(ArcTable_decoderCompressed(string_table, oa_table, cell_table))
            object_arg_4: IOptionalGetter = get.Optional
            return object_arg_4.Field("Tables", arg_9)

        def _arrow1771(__unit: None=None) -> Array[Person] | None:
            arg_11: Decoder_1[Array[Person]] = Decode_resizeArray(Person_decoder)
            object_arg_5: IOptionalGetter = get.Optional
            return object_arg_5.Field("Performers", arg_11)

        def _arrow1772(__unit: None=None) -> Array[Comment] | None:
            arg_13: Decoder_1[Array[Comment]] = Decode_resizeArray(Comment_decoder)
            object_arg_6: IOptionalGetter = get.Optional
            return object_arg_6.Field("Comments", arg_13)

        return ArcAssay.create(_arrow1766(), _arrow1767(), _arrow1768(), _arrow1769(), _arrow1770(), None, _arrow1771(), _arrow1772())

    return object(_arrow1773)


def Assay_ROCrate_genID(a: ArcAssay) -> str:
    match_value: str = a.Identifier
    if match_value == "":
        return "#EmptyAssay"

    else: 
        return ("#assay/" + replace(match_value, " ", "_")) + ""



def Assay_ROCrate_encoder(study_name: str | None, a: ArcAssay) -> Json:
    file_name: str = Assay_fileNameFromIdentifier(a.Identifier)
    processes: FSharpList[Process] = ARCtrl_ArcTables__ArcTables_GetProcesses(a)
    data_files: FSharpList[Data] = get_data(processes)
    def chooser(tupled_arg: tuple[str, Json], study_name: Any=study_name, a: Any=a) -> tuple[str, Json] | None:
        v: Json = tupled_arg[1]
        if equals(v, Json(3)):
            return None

        else: 
            return (tupled_arg[0], v)


    def _arrow1774(oa: OntologyAnnotation, study_name: Any=study_name, a: Any=a) -> Json:
        return OntologyAnnotation_ROCrate_encoderPropertyValue(oa)

    def _arrow1775(oa_1: OntologyAnnotation, study_name: Any=study_name, a: Any=a) -> Json:
        return OntologyAnnotation_ROCrate_encoderDefinedTerm(oa_1)

    def _arrow1776(oa_2: OntologyAnnotation, study_name: Any=study_name, a: Any=a) -> Json:
        return OntologyAnnotation_ROCrate_encoderDefinedTerm(oa_2)

    def _arrow1777(oa_3: Person, study_name: Any=study_name, a: Any=a) -> Json:
        return Person_ROCrate_encoder(oa_3)

    def _arrow1778(oa_4: Data, study_name: Any=study_name, a: Any=a) -> Json:
        return Data_ROCrate_encoder(oa_4)

    def _arrow1780(__unit: None=None, study_name: Any=study_name, a: Any=a) -> Callable[[Process], Json]:
        assay_name: str | None = a.Identifier
        def _arrow1779(oa_5: Process) -> Json:
            return Process_ROCrate_encoder(study_name, assay_name, oa_5)

        return _arrow1779

    def _arrow1781(comment: Comment, study_name: Any=study_name, a: Any=a) -> Json:
        return Comment_ROCrate_encoder(comment)

    return Json(5, choose(chooser, of_array([("@id", Json(0, Assay_ROCrate_genID(a))), ("@type", list_1_1(singleton(Json(0, "Assay")))), ("additionalType", Json(0, "Assay")), ("identifier", Json(0, a.Identifier)), ("filename", Json(0, file_name)), try_include("measurementType", _arrow1774, a.MeasurementType), try_include("technologyType", _arrow1775, a.TechnologyType), try_include("technologyPlatform", _arrow1776, a.TechnologyPlatform), try_include_seq("performers", _arrow1777, a.Performers), try_include_list("dataFiles", _arrow1778, data_files), try_include_list("processSequence", _arrow1780(), processes), try_include_seq("comments", _arrow1781, a.Comments), ("@context", context_jsonvalue)])))


def _arrow1789(get: IGetters) -> ArcAssay:
    def _arrow1782(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("identifier", string)

    identifier: str = default_arg(_arrow1782(), create_missing_identifier())
    def mapping(arg_4: FSharpList[Process]) -> Array[ArcTable]:
        a: ArcTables = ARCtrl_ArcTables__ArcTables_fromProcesses_Static_62A3309D(arg_4)
        return a.Tables

    def _arrow1783(__unit: None=None) -> FSharpList[Process] | None:
        arg_3: Decoder_1[FSharpList[Process]] = list_1_2(Process_ROCrate_decoder)
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("processSequence", arg_3)

    tables: Array[ArcTable] | None = map(mapping, _arrow1783())
    def _arrow1784(__unit: None=None) -> OntologyAnnotation | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("measurementType", OntologyAnnotation_ROCrate_decoderPropertyValue)

    def _arrow1785(__unit: None=None) -> OntologyAnnotation | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("technologyType", OntologyAnnotation_ROCrate_decoderDefinedTerm)

    def _arrow1786(__unit: None=None) -> OntologyAnnotation | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("technologyPlatform", OntologyAnnotation_ROCrate_decoderDefinedTerm)

    def _arrow1787(__unit: None=None) -> Array[Person] | None:
        arg_12: Decoder_1[Array[Person]] = Decode_resizeArray(Person_ROCrate_decoder)
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("performers", arg_12)

    def _arrow1788(__unit: None=None) -> Array[Comment] | None:
        arg_14: Decoder_1[Array[Comment]] = Decode_resizeArray(Comment_ROCrate_decoder)
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("comments", arg_14)

    return ArcAssay(identifier, _arrow1784(), _arrow1785(), _arrow1786(), tables, None, _arrow1787(), _arrow1788())


Assay_ROCrate_decoder: Decoder_1[ArcAssay] = object(_arrow1789)

def Assay_ISAJson_encoder(study_name: str | None, id_map: Any | None, a: ArcAssay) -> Json:
    def f(a_1: ArcAssay, study_name: Any=study_name, id_map: Any=id_map, a: Any=a) -> Json:
        file_name: str = Assay_fileNameFromIdentifier(a_1.Identifier)
        processes: FSharpList[Process] = ARCtrl_ArcTables__ArcTables_GetProcesses(a_1)
        def encoder(oa: OntologyAnnotation, a_1: Any=a_1) -> Json:
            return OntologyAnnotation_ISAJson_encoder(id_map, oa)

        encoded_units: tuple[str, Json] = try_include_list("unitCategories", encoder, get_units(processes))
        def encoder_1(value_1: MaterialAttribute, a_1: Any=a_1) -> Json:
            return MaterialAttribute_ISAJson_encoder(id_map, value_1)

        encoded_characteristics: tuple[str, Json] = try_include_list("characteristicCategories", encoder_1, get_characteristics(processes))
        def _arrow1790(ps: FSharpList[Process], a_1: Any=a_1) -> Json:
            return encoder_3(id_map, ps)

        encoded_materials: tuple[str, Json] = try_include("materials", _arrow1790, Option_fromValueWithDefault(empty(), processes))
        def encoder_2(oa_1: Data, a_1: Any=a_1) -> Json:
            return Data_ISAJson_encoder(id_map, oa_1)

        encoced_data_files: tuple[str, Json] = try_include_list("dataFiles", encoder_2, get_data(processes))
        units: FSharpList[OntologyAnnotation] = get_units(processes)
        def chooser(tupled_arg: tuple[str, Json], a_1: Any=a_1) -> tuple[str, Json] | None:
            v: Json = tupled_arg[1]
            if equals(v, Json(3)):
                return None

            else: 
                return (tupled_arg[0], v)


        def _arrow1791(value_5: str, a_1: Any=a_1) -> Json:
            return Json(0, value_5)

        def _arrow1792(oa_2: OntologyAnnotation, a_1: Any=a_1) -> Json:
            return OntologyAnnotation_ISAJson_encoder(id_map, oa_2)

        def _arrow1793(oa_3: OntologyAnnotation, a_1: Any=a_1) -> Json:
            return OntologyAnnotation_ISAJson_encoder(id_map, oa_3)

        def _arrow1794(value_7: str, a_1: Any=a_1) -> Json:
            return Json(0, value_7)

        def mapping(tp: OntologyAnnotation, a_1: Any=a_1) -> str:
            return JsonTypes_composeTechnologyPlatform(tp)

        def _arrow1796(__unit: None=None, a_1: Any=a_1) -> Callable[[Process], Json]:
            assay_name: str | None = a_1.Identifier
            def _arrow1795(oa_4: Process) -> Json:
                return Process_ISAJson_encoder(study_name, assay_name, id_map, oa_4)

            return _arrow1795

        def _arrow1797(comment: Comment, a_1: Any=a_1) -> Json:
            return Comment_ISAJson_encoder(id_map, comment)

        return Json(5, choose(chooser, of_array([("filename", Json(0, file_name)), try_include("@id", _arrow1791, Assay_ROCrate_genID(a_1)), try_include("measurementType", _arrow1792, a_1.MeasurementType), try_include("technologyType", _arrow1793, a_1.TechnologyType), try_include("technologyPlatform", _arrow1794, map(mapping, a_1.TechnologyPlatform)), encoced_data_files, encoded_materials, encoded_characteristics, encoded_units, try_include_list("processSequence", _arrow1796(), processes), try_include_seq("comments", _arrow1797, a_1.Comments)])))

    if id_map is not None:
        def _arrow1798(a_2: ArcAssay, study_name: Any=study_name, id_map: Any=id_map, a: Any=a) -> str:
            return Assay_ROCrate_genID(a_2)

        return encode(_arrow1798, f, a, id_map)

    else: 
        return f(a)



Assay_ISAJson_allowedFields: FSharpList[str] = of_array(["@id", "filename", "measurementType", "technologyType", "technologyPlatform", "dataFiles", "materials", "characteristicCategories", "unitCategories", "processSequence", "comments", "@type", "@context"])

def _arrow1805(get: IGetters) -> ArcAssay:
    def _arrow1799(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("filename", string)

    identifier: str = default_arg(bind(Assay_tryIdentifierFromFileName, _arrow1799()), create_missing_identifier())
    def mapping(arg_4: FSharpList[Process]) -> Array[ArcTable]:
        a: ArcTables = ARCtrl_ArcTables__ArcTables_fromProcesses_Static_62A3309D(arg_4)
        return a.Tables

    def _arrow1800(__unit: None=None) -> FSharpList[Process] | None:
        arg_3: Decoder_1[FSharpList[Process]] = list_1_2(Process_ISAJson_decoder)
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("processSequence", arg_3)

    tables: Array[ArcTable] | None = map(mapping, _arrow1800())
    def _arrow1801(__unit: None=None) -> OntologyAnnotation | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("measurementType", OntologyAnnotation_ISAJson_decoder)

    def _arrow1802(__unit: None=None) -> OntologyAnnotation | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("technologyType", OntologyAnnotation_ISAJson_decoder)

    def _arrow1803(__unit: None=None) -> OntologyAnnotation | None:
        arg_10: Decoder_1[OntologyAnnotation] = map_1(JsonTypes_decomposeTechnologyPlatform, string)
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("technologyPlatform", arg_10)

    def _arrow1804(__unit: None=None) -> Array[Comment] | None:
        arg_12: Decoder_1[Array[Comment]] = Decode_resizeArray(Comment_ISAJson_decoder)
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("comments", arg_12)

    return ArcAssay(identifier, _arrow1801(), _arrow1802(), _arrow1803(), tables, None, None, _arrow1804())


Assay_ISAJson_decoder: Decoder_1[ArcAssay] = Decode_objectNoAdditionalProperties(Assay_ISAJson_allowedFields, _arrow1805)

def ARCtrl_ArcAssay__ArcAssay_fromJsonString_Static_Z721C83C5(s: str) -> ArcAssay:
    match_value: FSharpResult_2[ArcAssay, str] = Decode_fromString(Assay_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_ArcAssay__ArcAssay_toJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[ArcAssay], str]:
    def _arrow1806(obj: ArcAssay, spaces: Any=spaces) -> str:
        value: Json = Assay_encoder(obj)
        return to_string(default_spaces(spaces), value)

    return _arrow1806


def ARCtrl_ArcAssay__ArcAssay_ToJsonString_71136F3F(this: ArcAssay, spaces: int | None=None) -> str:
    return ARCtrl_ArcAssay__ArcAssay_toJsonString_Static_71136F3F(spaces)(this)


def ARCtrl_ArcAssay__ArcAssay_fromCompressedJsonString_Static_Z721C83C5(s: str) -> ArcAssay:
    try: 
        match_value: FSharpResult_2[ArcAssay, str] = Decode_fromString(decode(Assay_decoderCompressed), s)
        if match_value.tag == 1:
            raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

        else: 
            return match_value.fields[0]


    except Exception as e_1:
        arg_1: str = str(e_1)
        return to_fail(printf("Error. Unable to parse json string to ArcStudy: %s"))(arg_1)



def ARCtrl_ArcAssay__ArcAssay_toCompressedJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[ArcAssay], str]:
    def _arrow1807(obj: ArcAssay, spaces: Any=spaces) -> str:
        return to_string(default_arg(spaces, 0), encode_1(Assay_encoderCompressed, obj))

    return _arrow1807


def ARCtrl_ArcAssay__ArcAssay_ToCompressedJsonString_71136F3F(this: ArcAssay, spaces: int | None=None) -> str:
    return ARCtrl_ArcAssay__ArcAssay_toCompressedJsonString_Static_71136F3F(spaces)(this)


def ARCtrl_ArcAssay__ArcAssay_fromROCrateJsonString_Static_Z721C83C5(s: str) -> ArcAssay:
    match_value: FSharpResult_2[ArcAssay, str] = Decode_fromString(Assay_ROCrate_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_ArcAssay__ArcAssay_toROCrateJsonString_Static_5CABCA47(study_name: str | None=None, spaces: int | None=None) -> Callable[[ArcAssay], str]:
    def _arrow1808(obj: ArcAssay, study_name: Any=study_name, spaces: Any=spaces) -> str:
        value: Json = Assay_ROCrate_encoder(study_name, obj)
        return to_string(default_spaces(spaces), value)

    return _arrow1808


def ARCtrl_ArcAssay__ArcAssay_ToROCrateJsonString_5CABCA47(this: ArcAssay, study_name: str | None=None, spaces: int | None=None) -> str:
    return ARCtrl_ArcAssay__ArcAssay_toROCrateJsonString_Static_5CABCA47(study_name, spaces)(this)


def ARCtrl_ArcAssay__ArcAssay_toISAJsonString_Static_Z3B036AA(spaces: int | None=None, use_idreferencing: bool | None=None) -> Callable[[ArcAssay], str]:
    id_map: Any | None = dict([]) if default_arg(use_idreferencing, False) else None
    def _arrow1809(obj: ArcAssay, spaces: Any=spaces, use_idreferencing: Any=use_idreferencing) -> str:
        value: Json = Assay_ISAJson_encoder(None, id_map, obj)
        return to_string(default_spaces(spaces), value)

    return _arrow1809


def ARCtrl_ArcAssay__ArcAssay_fromISAJsonString_Static_Z721C83C5(s: str) -> ArcAssay:
    match_value: FSharpResult_2[ArcAssay, str] = Decode_fromString(Assay_ISAJson_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_ArcAssay__ArcAssay_ToISAJsonString_Z3B036AA(this: ArcAssay, spaces: int | None=None, use_idreferencing: bool | None=None) -> str:
    return ARCtrl_ArcAssay__ArcAssay_toISAJsonString_Static_Z3B036AA(spaces, use_idreferencing)(this)


__all__ = ["Assay_encoder", "Assay_decoder", "Assay_encoderCompressed", "Assay_decoderCompressed", "Assay_ROCrate_genID", "Assay_ROCrate_encoder", "Assay_ROCrate_decoder", "Assay_ISAJson_encoder", "Assay_ISAJson_allowedFields", "Assay_ISAJson_decoder", "ARCtrl_ArcAssay__ArcAssay_fromJsonString_Static_Z721C83C5", "ARCtrl_ArcAssay__ArcAssay_toJsonString_Static_71136F3F", "ARCtrl_ArcAssay__ArcAssay_ToJsonString_71136F3F", "ARCtrl_ArcAssay__ArcAssay_fromCompressedJsonString_Static_Z721C83C5", "ARCtrl_ArcAssay__ArcAssay_toCompressedJsonString_Static_71136F3F", "ARCtrl_ArcAssay__ArcAssay_ToCompressedJsonString_71136F3F", "ARCtrl_ArcAssay__ArcAssay_fromROCrateJsonString_Static_Z721C83C5", "ARCtrl_ArcAssay__ArcAssay_toROCrateJsonString_Static_5CABCA47", "ARCtrl_ArcAssay__ArcAssay_ToROCrateJsonString_5CABCA47", "ARCtrl_ArcAssay__ArcAssay_toISAJsonString_Static_Z3B036AA", "ARCtrl_ArcAssay__ArcAssay_fromISAJsonString_Static_Z721C83C5", "ARCtrl_ArcAssay__ArcAssay_ToISAJsonString_Z3B036AA"]

