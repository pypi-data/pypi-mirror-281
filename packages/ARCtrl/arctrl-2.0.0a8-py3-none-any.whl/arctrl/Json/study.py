from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..fable_modules.fable_library.list import (try_find, FSharpList, choose, of_array, singleton, map as map_1, empty)
from ..fable_modules.fable_library.option import (default_arg, value as value_17, bind, map, default_arg_with)
from ..fable_modules.fable_library.result import FSharpResult_2
from ..fable_modules.fable_library.seq import is_empty
from ..fable_modules.fable_library.string_ import (replace, to_text, printf, to_fail)
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import (equals, get_enumerator, dispose, IEnumerable_1)
from ..fable_modules.thoth_json_core.decode import (object, IRequiredGetter, string, IOptionalGetter, IGetters, list_1 as list_1_2)
from ..fable_modules.thoth_json_core.encode import list_1 as list_1_1
from ..fable_modules.thoth_json_core.types import (Json, Decoder_1)
from ..fable_modules.thoth_json_python.decode import Decode_fromString
from ..fable_modules.thoth_json_python.encode import to_string
from ..Core.arc_types import (ArcAssay, ArcStudy)
from ..Core.comment import Comment
from ..Core.conversion import (ARCtrl_ArcTables__ArcTables_GetProcesses, ARCtrl_ArcTables__ArcTables_fromProcesses_Static_62A3309D, Person_setSourceAssayComment, Person_getSourceAssayIdentifiersFromComments, Person_removeSourceAssayComments)
from ..Core.Helper.collections_ import (ResizeArray_map, Option_fromValueWithDefault)
from ..Core.Helper.identifier import (Study_tryFileNameFromIdentifier, Study_tryIdentifierFromFileName, create_missing_identifier, Study_fileNameFromIdentifier)
from ..Core.ontology_annotation import OntologyAnnotation
from ..Core.person import Person
from ..Core.Process.factor import Factor
from ..Core.Process.material_attribute import MaterialAttribute
from ..Core.Process.process import Process
from ..Core.Process.process_sequence import (get_units, get_factors, get_characteristics, get_protocols)
from ..Core.Process.protocol import Protocol
from ..Core.publication import Publication
from ..Core.Table.arc_table import ArcTable
from ..Core.Table.arc_tables import ArcTables
from ..Core.Table.composite_cell import CompositeCell
from .assay import (Assay_ROCrate_encoder, Assay_ROCrate_decoder, Assay_ISAJson_encoder, Assay_ISAJson_decoder)
from .comment import (Comment_encoder, Comment_decoder, Comment_ROCrate_encoder, Comment_ROCrate_decoder, Comment_ISAJson_encoder, Comment_ISAJson_decoder)
from .context.rocrate.isa_study_context import context_jsonvalue
from .decode import (Decode_resizeArray, Decode_objectNoAdditionalProperties)
from .encode import (try_include, try_include_seq, try_include_list, default_spaces)
from .idtable import encode
from .ontology_annotation import (OntologyAnnotation_encoder, OntologyAnnotation_decoder, OntologyAnnotation_ROCrate_encoderDefinedTerm, OntologyAnnotation_ROCrate_decoderDefinedTerm, OntologyAnnotation_ISAJson_encoder, OntologyAnnotation_ISAJson_decoder)
from .person import (Person_encoder, Person_decoder, Person_ROCrate_encoder, Person_ROCrate_decoder, Person_ISAJson_encoder, Person_ISAJson_decoder)
from .Process.factor import Factor_ISAJson_encoder
from .Process.material_attribute import MaterialAttribute_ISAJson_encoder
from .Process.process import (Process_ROCrate_encoder, Process_ROCrate_decoder, Process_ISAJson_encoder, Process_ISAJson_decoder)
from .Process.protocol import Protocol_ISAJson_encoder
from .Process.study_materials import encoder as encoder_4
from .publication import (Publication_encoder, Publication_decoder, Publication_ROCrate_encoder, Publication_ROCrate_decoder, Publication_ISAJson_encoder, Publication_ISAJson_decoder)
from .Table.arc_table import (ArcTable_encoder, ArcTable_decoder, ArcTable_encoderCompressed, ArcTable_decoderCompressed)
from .Table.compression import (decode, encode as encode_1)

def Study_Helper_getAssayInformation(assays: FSharpList[ArcAssay] | None, study: ArcStudy) -> Array[ArcAssay]:
    if assays is not None:
        def f(assay_id: str, assays: Any=assays, study: Any=study) -> ArcAssay:
            def predicate(a: ArcAssay, assay_id: Any=assay_id) -> bool:
                return a.Identifier == assay_id

            return default_arg(try_find(predicate, value_17(assays)), ArcAssay.init(assay_id))

        return ResizeArray_map(f, study.RegisteredAssayIdentifiers)

    else: 
        return study.GetRegisteredAssaysOrIdentifier()



def Study_encoder(study: ArcStudy) -> Json:
    def chooser(tupled_arg: tuple[str, Json], study: Any=study) -> tuple[str, Json] | None:
        v: Json = tupled_arg[1]
        if equals(v, Json(3)):
            return None

        else: 
            return (tupled_arg[0], v)


    def _arrow1803(value_1: str, study: Any=study) -> Json:
        return Json(0, value_1)

    def _arrow1804(value_3: str, study: Any=study) -> Json:
        return Json(0, value_3)

    def _arrow1805(value_5: str, study: Any=study) -> Json:
        return Json(0, value_5)

    def _arrow1806(value_7: str, study: Any=study) -> Json:
        return Json(0, value_7)

    def _arrow1807(oa: Publication, study: Any=study) -> Json:
        return Publication_encoder(oa)

    def _arrow1808(person: Person, study: Any=study) -> Json:
        return Person_encoder(person)

    def _arrow1809(oa_1: OntologyAnnotation, study: Any=study) -> Json:
        return OntologyAnnotation_encoder(oa_1)

    def _arrow1810(table: ArcTable, study: Any=study) -> Json:
        return ArcTable_encoder(table)

    def _arrow1811(value_9: str, study: Any=study) -> Json:
        return Json(0, value_9)

    def _arrow1812(comment: Comment, study: Any=study) -> Json:
        return Comment_encoder(comment)

    return Json(5, choose(chooser, of_array([("Identifier", Json(0, study.Identifier)), try_include("Title", _arrow1803, study.Title), try_include("Description", _arrow1804, study.Description), try_include("SubmissionDate", _arrow1805, study.SubmissionDate), try_include("PublicReleaseDate", _arrow1806, study.PublicReleaseDate), try_include_seq("Publications", _arrow1807, study.Publications), try_include_seq("Contacts", _arrow1808, study.Contacts), try_include_seq("StudyDesignDescriptors", _arrow1809, study.StudyDesignDescriptors), try_include_seq("Tables", _arrow1810, study.Tables), try_include_seq("RegisteredAssayIdentifiers", _arrow1811, study.RegisteredAssayIdentifiers), try_include_seq("Comments", _arrow1812, study.Comments)])))


def _arrow1824(get: IGetters) -> ArcStudy:
    def _arrow1813(__unit: None=None) -> str:
        object_arg: IRequiredGetter = get.Required
        return object_arg.Field("Identifier", string)

    def _arrow1814(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("Title", string)

    def _arrow1815(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("Description", string)

    def _arrow1816(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("SubmissionDate", string)

    def _arrow1817(__unit: None=None) -> str | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("PublicReleaseDate", string)

    def _arrow1818(__unit: None=None) -> Array[Publication] | None:
        arg_11: Decoder_1[Array[Publication]] = Decode_resizeArray(Publication_decoder)
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("Publications", arg_11)

    def _arrow1819(__unit: None=None) -> Array[Person] | None:
        arg_13: Decoder_1[Array[Person]] = Decode_resizeArray(Person_decoder)
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("Contacts", arg_13)

    def _arrow1820(__unit: None=None) -> Array[OntologyAnnotation] | None:
        arg_15: Decoder_1[Array[OntologyAnnotation]] = Decode_resizeArray(OntologyAnnotation_decoder)
        object_arg_7: IOptionalGetter = get.Optional
        return object_arg_7.Field("StudyDesignDescriptors", arg_15)

    def _arrow1821(__unit: None=None) -> Array[ArcTable] | None:
        arg_17: Decoder_1[Array[ArcTable]] = Decode_resizeArray(ArcTable_decoder)
        object_arg_8: IOptionalGetter = get.Optional
        return object_arg_8.Field("Tables", arg_17)

    def _arrow1822(__unit: None=None) -> Array[str] | None:
        arg_19: Decoder_1[Array[str]] = Decode_resizeArray(string)
        object_arg_9: IOptionalGetter = get.Optional
        return object_arg_9.Field("RegisteredAssayIdentifiers", arg_19)

    def _arrow1823(__unit: None=None) -> Array[Comment] | None:
        arg_21: Decoder_1[Array[Comment]] = Decode_resizeArray(Comment_decoder)
        object_arg_10: IOptionalGetter = get.Optional
        return object_arg_10.Field("Comments", arg_21)

    return ArcStudy(_arrow1813(), _arrow1814(), _arrow1815(), _arrow1816(), _arrow1817(), _arrow1818(), _arrow1819(), _arrow1820(), _arrow1821(), None, _arrow1822(), _arrow1823())


Study_decoder: Decoder_1[ArcStudy] = object(_arrow1824)

def Study_encoderCompressed(string_table: Any, oa_table: Any, cell_table: Any, study: ArcStudy) -> Json:
    def chooser(tupled_arg: tuple[str, Json], string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, study: Any=study) -> tuple[str, Json] | None:
        v: Json = tupled_arg[1]
        if equals(v, Json(3)):
            return None

        else: 
            return (tupled_arg[0], v)


    def _arrow1825(value_1: str, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, study: Any=study) -> Json:
        return Json(0, value_1)

    def _arrow1826(value_3: str, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, study: Any=study) -> Json:
        return Json(0, value_3)

    def _arrow1827(value_5: str, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, study: Any=study) -> Json:
        return Json(0, value_5)

    def _arrow1828(value_7: str, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, study: Any=study) -> Json:
        return Json(0, value_7)

    def _arrow1829(oa: Publication, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, study: Any=study) -> Json:
        return Publication_encoder(oa)

    def _arrow1830(person: Person, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, study: Any=study) -> Json:
        return Person_encoder(person)

    def _arrow1831(oa_1: OntologyAnnotation, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, study: Any=study) -> Json:
        return OntologyAnnotation_encoder(oa_1)

    def _arrow1832(table: ArcTable, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, study: Any=study) -> Json:
        return ArcTable_encoderCompressed(string_table, oa_table, cell_table, table)

    def _arrow1833(value_9: str, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, study: Any=study) -> Json:
        return Json(0, value_9)

    def _arrow1834(comment: Comment, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, study: Any=study) -> Json:
        return Comment_encoder(comment)

    return Json(5, choose(chooser, of_array([("Identifier", Json(0, study.Identifier)), try_include("Title", _arrow1825, study.Title), try_include("Description", _arrow1826, study.Description), try_include("SubmissionDate", _arrow1827, study.SubmissionDate), try_include("PublicReleaseDate", _arrow1828, study.PublicReleaseDate), try_include_seq("Publications", _arrow1829, study.Publications), try_include_seq("Contacts", _arrow1830, study.Contacts), try_include_seq("StudyDesignDescriptors", _arrow1831, study.StudyDesignDescriptors), try_include_seq("Tables", _arrow1832, study.Tables), try_include_seq("RegisteredAssayIdentifiers", _arrow1833, study.RegisteredAssayIdentifiers), try_include_seq("Comments", _arrow1834, study.Comments)])))


def Study_decoderCompressed(string_table: Array[str], oa_table: Array[OntologyAnnotation], cell_table: Array[CompositeCell]) -> Decoder_1[ArcStudy]:
    def _arrow1846(get: IGetters, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table) -> ArcStudy:
        def _arrow1835(__unit: None=None) -> str:
            object_arg: IRequiredGetter = get.Required
            return object_arg.Field("Identifier", string)

        def _arrow1836(__unit: None=None) -> str | None:
            object_arg_1: IOptionalGetter = get.Optional
            return object_arg_1.Field("Title", string)

        def _arrow1837(__unit: None=None) -> str | None:
            object_arg_2: IOptionalGetter = get.Optional
            return object_arg_2.Field("Description", string)

        def _arrow1838(__unit: None=None) -> str | None:
            object_arg_3: IOptionalGetter = get.Optional
            return object_arg_3.Field("SubmissionDate", string)

        def _arrow1839(__unit: None=None) -> str | None:
            object_arg_4: IOptionalGetter = get.Optional
            return object_arg_4.Field("PublicReleaseDate", string)

        def _arrow1840(__unit: None=None) -> Array[Publication] | None:
            arg_11: Decoder_1[Array[Publication]] = Decode_resizeArray(Publication_decoder)
            object_arg_5: IOptionalGetter = get.Optional
            return object_arg_5.Field("Publications", arg_11)

        def _arrow1841(__unit: None=None) -> Array[Person] | None:
            arg_13: Decoder_1[Array[Person]] = Decode_resizeArray(Person_decoder)
            object_arg_6: IOptionalGetter = get.Optional
            return object_arg_6.Field("Contacts", arg_13)

        def _arrow1842(__unit: None=None) -> Array[OntologyAnnotation] | None:
            arg_15: Decoder_1[Array[OntologyAnnotation]] = Decode_resizeArray(OntologyAnnotation_decoder)
            object_arg_7: IOptionalGetter = get.Optional
            return object_arg_7.Field("StudyDesignDescriptors", arg_15)

        def _arrow1843(__unit: None=None) -> Array[ArcTable] | None:
            arg_17: Decoder_1[Array[ArcTable]] = Decode_resizeArray(ArcTable_decoderCompressed(string_table, oa_table, cell_table))
            object_arg_8: IOptionalGetter = get.Optional
            return object_arg_8.Field("Tables", arg_17)

        def _arrow1844(__unit: None=None) -> Array[str] | None:
            arg_19: Decoder_1[Array[str]] = Decode_resizeArray(string)
            object_arg_9: IOptionalGetter = get.Optional
            return object_arg_9.Field("RegisteredAssayIdentifiers", arg_19)

        def _arrow1845(__unit: None=None) -> Array[Comment] | None:
            arg_21: Decoder_1[Array[Comment]] = Decode_resizeArray(Comment_decoder)
            object_arg_10: IOptionalGetter = get.Optional
            return object_arg_10.Field("Comments", arg_21)

        return ArcStudy(_arrow1835(), _arrow1836(), _arrow1837(), _arrow1838(), _arrow1839(), _arrow1840(), _arrow1841(), _arrow1842(), _arrow1843(), None, _arrow1844(), _arrow1845())

    return object(_arrow1846)


def Study_ROCrate_genID(a: ArcStudy) -> str:
    match_value: str = a.Identifier
    if match_value == "":
        return "#EmptyStudy"

    else: 
        return ("#study/" + replace(match_value, " ", "_")) + ""



def Study_ROCrate_encoder(assays: FSharpList[ArcAssay] | None, s: ArcStudy) -> Json:
    file_name: str | None = Study_tryFileNameFromIdentifier(s.Identifier)
    processes: FSharpList[Process] = ARCtrl_ArcTables__ArcTables_GetProcesses(s)
    assays_1: Array[ArcAssay] = Study_Helper_getAssayInformation(assays, s)
    def chooser(tupled_arg: tuple[str, Json], assays: Any=assays, s: Any=s) -> tuple[str, Json] | None:
        v: Json = tupled_arg[1]
        if equals(v, Json(3)):
            return None

        else: 
            return (tupled_arg[0], v)


    def _arrow1848(value_4: str, assays: Any=assays, s: Any=s) -> Json:
        return Json(0, value_4)

    def _arrow1850(value_6: str, assays: Any=assays, s: Any=s) -> Json:
        return Json(0, value_6)

    def _arrow1851(value_8: str, assays: Any=assays, s: Any=s) -> Json:
        return Json(0, value_8)

    def _arrow1853(oa: OntologyAnnotation, assays: Any=assays, s: Any=s) -> Json:
        return OntologyAnnotation_ROCrate_encoderDefinedTerm(oa)

    def _arrow1854(value_10: str, assays: Any=assays, s: Any=s) -> Json:
        return Json(0, value_10)

    def _arrow1855(value_12: str, assays: Any=assays, s: Any=s) -> Json:
        return Json(0, value_12)

    def _arrow1856(oa_1: Publication, assays: Any=assays, s: Any=s) -> Json:
        return Publication_ROCrate_encoder(oa_1)

    def _arrow1857(oa_2: Person, assays: Any=assays, s: Any=s) -> Json:
        return Person_ROCrate_encoder(oa_2)

    def _arrow1859(__unit: None=None, assays: Any=assays, s: Any=s) -> Callable[[Process], Json]:
        study_name: str | None = s.Identifier
        def _arrow1858(oa_3: Process) -> Json:
            return Process_ROCrate_encoder(study_name, None, oa_3)

        return _arrow1858

    def _arrow1861(__unit: None=None, assays: Any=assays, s: Any=s) -> Callable[[ArcAssay], Json]:
        study_name_1: str | None = s.Identifier
        def _arrow1860(a_1: ArcAssay) -> Json:
            return Assay_ROCrate_encoder(study_name_1, a_1)

        return _arrow1860

    def _arrow1862(comment: Comment, assays: Any=assays, s: Any=s) -> Json:
        return Comment_ROCrate_encoder(comment)

    return Json(5, choose(chooser, of_array([("@id", Json(0, Study_ROCrate_genID(s))), ("@type", list_1_1(singleton(Json(0, "Study")))), ("additionalType", Json(0, "Study")), ("identifier", Json(0, s.Identifier)), try_include("filename", _arrow1848, file_name), try_include("title", _arrow1850, s.Title), try_include("description", _arrow1851, s.Description), try_include_seq("studyDesignDescriptors", _arrow1853, s.StudyDesignDescriptors), try_include("submissionDate", _arrow1854, s.SubmissionDate), try_include("publicReleaseDate", _arrow1855, s.PublicReleaseDate), try_include_seq("publications", _arrow1856, s.Publications), try_include_seq("people", _arrow1857, s.Contacts), try_include_list("processSequence", _arrow1859(), processes), try_include_seq("assays", _arrow1861(), assays_1), try_include_seq("comments", _arrow1862, s.Comments), ("@context", context_jsonvalue)])))


def _arrow1874(get: IGetters) -> tuple[ArcStudy, FSharpList[ArcAssay]]:
    def _arrow1863(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("filename", string)

    identifier: str = default_arg(bind(Study_tryIdentifierFromFileName, _arrow1863()), create_missing_identifier())
    assays: FSharpList[ArcAssay] | None
    arg_3: Decoder_1[FSharpList[ArcAssay]] = list_1_2(Assay_ROCrate_decoder)
    object_arg_1: IOptionalGetter = get.Optional
    assays = object_arg_1.Field("assays", arg_3)
    def mapping_1(arg_4: FSharpList[ArcAssay]) -> Array[str]:
        def mapping(a: ArcAssay, arg_4: Any=arg_4) -> str:
            return a.Identifier

        return list(map_1(mapping, arg_4))

    assay_identifiers: Array[str] | None = map(mapping_1, assays)
    def mapping_2(ps: FSharpList[Process]) -> Array[ArcTable]:
        return ARCtrl_ArcTables__ArcTables_fromProcesses_Static_62A3309D(ps).Tables

    def _arrow1864(__unit: None=None) -> FSharpList[Process] | None:
        arg_6: Decoder_1[FSharpList[Process]] = list_1_2(Process_ROCrate_decoder)
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("processSequence", arg_6)

    tables: Array[ArcTable] | None = map(mapping_2, _arrow1864())
    def _arrow1866(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("title", string)

    def _arrow1867(__unit: None=None) -> str | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("description", string)

    def _arrow1868(__unit: None=None) -> str | None:
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("submissionDate", string)

    def _arrow1869(__unit: None=None) -> str | None:
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("publicReleaseDate", string)

    def _arrow1870(__unit: None=None) -> Array[Publication] | None:
        arg_16: Decoder_1[Array[Publication]] = Decode_resizeArray(Publication_ROCrate_decoder)
        object_arg_7: IOptionalGetter = get.Optional
        return object_arg_7.Field("publications", arg_16)

    def _arrow1871(__unit: None=None) -> Array[Person] | None:
        arg_18: Decoder_1[Array[Person]] = Decode_resizeArray(Person_ROCrate_decoder)
        object_arg_8: IOptionalGetter = get.Optional
        return object_arg_8.Field("people", arg_18)

    def _arrow1872(__unit: None=None) -> Array[OntologyAnnotation] | None:
        arg_20: Decoder_1[Array[OntologyAnnotation]] = Decode_resizeArray(OntologyAnnotation_ROCrate_decoderDefinedTerm)
        object_arg_9: IOptionalGetter = get.Optional
        return object_arg_9.Field("studyDesignDescriptors", arg_20)

    def _arrow1873(__unit: None=None) -> Array[Comment] | None:
        arg_22: Decoder_1[Array[Comment]] = Decode_resizeArray(Comment_ROCrate_decoder)
        object_arg_10: IOptionalGetter = get.Optional
        return object_arg_10.Field("comments", arg_22)

    return (ArcStudy(identifier, _arrow1866(), _arrow1867(), _arrow1868(), _arrow1869(), _arrow1870(), _arrow1871(), _arrow1872(), tables, None, assay_identifiers, _arrow1873()), default_arg(assays, empty()))


Study_ROCrate_decoder: Decoder_1[tuple[ArcStudy, FSharpList[ArcAssay]]] = object(_arrow1874)

def Study_ISAJson_encoder(id_map: Any | None, assays: FSharpList[ArcAssay] | None, s: ArcStudy) -> Json:
    def f(s_1: ArcStudy, id_map: Any=id_map, assays: Any=assays, s: Any=s) -> Json:
        study: ArcStudy = s_1.Copy(True)
        file_name: str = Study_fileNameFromIdentifier(study.Identifier)
        assays_1: Array[ArcAssay]
        n: Array[ArcAssay] = []
        enumerator: Any = get_enumerator(Study_Helper_getAssayInformation(assays, study))
        try: 
            while enumerator.System_Collections_IEnumerator_MoveNext():
                a: ArcAssay = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                assay: ArcAssay = a.Copy()
                enumerator_1: Any = get_enumerator(assay.Performers)
                try: 
                    while enumerator_1.System_Collections_IEnumerator_MoveNext():
                        person_1: Person = Person_setSourceAssayComment(enumerator_1.System_Collections_Generic_IEnumerator_1_get_Current(), assay.Identifier)
                        (study.Contacts.append(person_1))

                finally: 
                    dispose(enumerator_1)

                assay.Performers = []
                (n.append(assay))

        finally: 
            dispose(enumerator)

        assays_1 = n
        processes: FSharpList[Process] = ARCtrl_ArcTables__ArcTables_GetProcesses(study)
        def encoder(oa: OntologyAnnotation, s_1: Any=s_1) -> Json:
            return OntologyAnnotation_ISAJson_encoder(id_map, oa)

        encoded_units: tuple[str, Json] = try_include_list("unitCategories", encoder, get_units(processes))
        def encoder_1(value_1: Factor, s_1: Any=s_1) -> Json:
            return Factor_ISAJson_encoder(id_map, value_1)

        encoded_factors: tuple[str, Json] = try_include_list("factors", encoder_1, get_factors(processes))
        def encoder_2(value_3: MaterialAttribute, s_1: Any=s_1) -> Json:
            return MaterialAttribute_ISAJson_encoder(id_map, value_3)

        encoded_characteristics: tuple[str, Json] = try_include_list("characteristicCategories", encoder_2, get_characteristics(processes))
        def _arrow1875(ps: FSharpList[Process], s_1: Any=s_1) -> Json:
            return encoder_4(id_map, ps)

        encoded_materials: tuple[str, Json] = try_include("materials", _arrow1875, Option_fromValueWithDefault(empty(), processes))
        encoded_protocols: tuple[str, Json]
        value_5: FSharpList[Protocol] = get_protocols(processes)
        def _arrow1877(__unit: None=None, s_1: Any=s_1) -> Callable[[Protocol], Json]:
            study_name: str | None = s_1.Identifier
            def _arrow1876(oa_1: Protocol) -> Json:
                return Protocol_ISAJson_encoder(study_name, None, None, id_map, oa_1)

            return _arrow1876

        encoded_protocols = try_include_list("protocols", _arrow1877(), value_5)
        def chooser(tupled_arg: tuple[str, Json], s_1: Any=s_1) -> tuple[str, Json] | None:
            v: Json = tupled_arg[1]
            if equals(v, Json(3)):
                return None

            else: 
                return (tupled_arg[0], v)


        def _arrow1878(value_9: str, s_1: Any=s_1) -> Json:
            return Json(0, value_9)

        def _arrow1879(value_11: str, s_1: Any=s_1) -> Json:
            return Json(0, value_11)

        def _arrow1880(value_13: str, s_1: Any=s_1) -> Json:
            return Json(0, value_13)

        def _arrow1881(value_15: str, s_1: Any=s_1) -> Json:
            return Json(0, value_15)

        def _arrow1882(oa_2: Publication, s_1: Any=s_1) -> Json:
            return Publication_ISAJson_encoder(id_map, oa_2)

        def _arrow1883(person_2: Person, s_1: Any=s_1) -> Json:
            return Person_ISAJson_encoder(id_map, person_2)

        def _arrow1884(oa_3: OntologyAnnotation, s_1: Any=s_1) -> Json:
            return OntologyAnnotation_ISAJson_encoder(id_map, oa_3)

        def _arrow1886(__unit: None=None, s_1: Any=s_1) -> Callable[[Process], Json]:
            study_name_1: str | None = s_1.Identifier
            def _arrow1885(oa_4: Process) -> Json:
                return Process_ISAJson_encoder(study_name_1, None, id_map, oa_4)

            return _arrow1885

        def _arrow1888(__unit: None=None, s_1: Any=s_1) -> Callable[[ArcAssay], Json]:
            study_name_2: str | None = s_1.Identifier
            def _arrow1887(a_2: ArcAssay) -> Json:
                return Assay_ISAJson_encoder(study_name_2, id_map, a_2)

            return _arrow1887

        def _arrow1889(comment: Comment, s_1: Any=s_1) -> Json:
            return Comment_ISAJson_encoder(id_map, comment)

        return Json(5, choose(chooser, of_array([("@id", Json(0, Study_ROCrate_genID(study))), ("filename", Json(0, file_name)), ("identifier", Json(0, study.Identifier)), try_include("title", _arrow1878, study.Title), try_include("description", _arrow1879, study.Description), try_include("submissionDate", _arrow1880, study.SubmissionDate), try_include("publicReleaseDate", _arrow1881, study.PublicReleaseDate), try_include_seq("publications", _arrow1882, study.Publications), try_include_seq("people", _arrow1883, study.Contacts), try_include_seq("studyDesignDescriptors", _arrow1884, study.StudyDesignDescriptors), encoded_protocols, encoded_materials, try_include_list("processSequence", _arrow1886(), processes), try_include_seq("assays", _arrow1888(), assays_1), encoded_factors, encoded_characteristics, encoded_units, try_include_seq("comments", _arrow1889, study.Comments)])))

    if id_map is not None:
        def _arrow1890(s_2: ArcStudy, id_map: Any=id_map, assays: Any=assays, s: Any=s) -> str:
            return Study_ROCrate_genID(s_2)

        return encode(_arrow1890, f, s, id_map)

    else: 
        return f(s)



Study_ISAJson_allowedFields: FSharpList[str] = of_array(["@id", "filename", "identifier", "title", "description", "submissionDate", "publicReleaseDate", "publications", "people", "studyDesignDescriptors", "protocols", "materials", "assays", "factors", "characteristicCategories", "unitCategories", "processSequence", "comments", "@type", "@context"])

def _arrow1901(get: IGetters) -> tuple[ArcStudy, FSharpList[ArcAssay]]:
    def _arrow1891(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("identifier", string)

    def def_thunk(__unit: None=None) -> str:
        def _arrow1892(__unit: None=None) -> str | None:
            object_arg_1: IOptionalGetter = get.Optional
            return object_arg_1.Field("filename", string)

        return default_arg(bind(Study_tryIdentifierFromFileName, _arrow1892()), create_missing_identifier())

    identifier: str = default_arg_with(_arrow1891(), def_thunk)
    def mapping(arg_6: FSharpList[Process]) -> Array[ArcTable]:
        a: ArcTables = ARCtrl_ArcTables__ArcTables_fromProcesses_Static_62A3309D(arg_6)
        return a.Tables

    def _arrow1893(__unit: None=None) -> FSharpList[Process] | None:
        arg_5: Decoder_1[FSharpList[Process]] = list_1_2(Process_ISAJson_decoder)
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("processSequence", arg_5)

    tables: Array[ArcTable] | None = map(mapping, _arrow1893())
    assays: FSharpList[ArcAssay] | None
    arg_8: Decoder_1[FSharpList[ArcAssay]] = list_1_2(Assay_ISAJson_decoder)
    object_arg_3: IOptionalGetter = get.Optional
    assays = object_arg_3.Field("assays", arg_8)
    persons_raw: Array[Person] | None
    arg_10: Decoder_1[Array[Person]] = Decode_resizeArray(Person_ISAJson_decoder)
    object_arg_4: IOptionalGetter = get.Optional
    persons_raw = object_arg_4.Field("people", arg_10)
    persons: Array[Person] = []
    if persons_raw is not None:
        enumerator: Any = get_enumerator(value_17(persons_raw))
        try: 
            while enumerator.System_Collections_IEnumerator_MoveNext():
                person: Person = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                source_assays: IEnumerable_1[str] = Person_getSourceAssayIdentifiersFromComments(person)
                with get_enumerator(source_assays) as enumerator_1:
                    while enumerator_1.System_Collections_IEnumerator_MoveNext():
                        assay_identifier: str = enumerator_1.System_Collections_Generic_IEnumerator_1_get_Current()
                        with get_enumerator(value_17(assays)) as enumerator_2:
                            while enumerator_2.System_Collections_IEnumerator_MoveNext():
                                assay: ArcAssay = enumerator_2.System_Collections_Generic_IEnumerator_1_get_Current()
                                if assay.Identifier == assay_identifier:
                                    (assay.Performers.append(person))

                person.Comments = Person_removeSourceAssayComments(person)
                if is_empty(source_assays):
                    (persons.append(person))


        finally: 
            dispose(enumerator)


    def mapping_2(arg_11: FSharpList[ArcAssay]) -> Array[str]:
        def mapping_1(a_1: ArcAssay, arg_11: Any=arg_11) -> str:
            return a_1.Identifier

        return list(map_1(mapping_1, arg_11))

    assay_identifiers: Array[str] | None = map(mapping_2, assays)
    def _arrow1894(__unit: None=None) -> str | None:
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("title", string)

    def _arrow1895(__unit: None=None) -> str | None:
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("description", string)

    def _arrow1896(__unit: None=None) -> str | None:
        object_arg_7: IOptionalGetter = get.Optional
        return object_arg_7.Field("submissionDate", string)

    def _arrow1897(__unit: None=None) -> str | None:
        object_arg_8: IOptionalGetter = get.Optional
        return object_arg_8.Field("publicReleaseDate", string)

    def _arrow1898(__unit: None=None) -> Array[Publication] | None:
        arg_21: Decoder_1[Array[Publication]] = Decode_resizeArray(Publication_ISAJson_decoder)
        object_arg_9: IOptionalGetter = get.Optional
        return object_arg_9.Field("publications", arg_21)

    def _arrow1899(__unit: None=None) -> Array[OntologyAnnotation] | None:
        arg_23: Decoder_1[Array[OntologyAnnotation]] = Decode_resizeArray(OntologyAnnotation_ISAJson_decoder)
        object_arg_10: IOptionalGetter = get.Optional
        return object_arg_10.Field("studyDesignDescriptors", arg_23)

    def _arrow1900(__unit: None=None) -> Array[Comment] | None:
        arg_25: Decoder_1[Array[Comment]] = Decode_resizeArray(Comment_ISAJson_decoder)
        object_arg_11: IOptionalGetter = get.Optional
        return object_arg_11.Field("comments", arg_25)

    return (ArcStudy(identifier, _arrow1894(), _arrow1895(), _arrow1896(), _arrow1897(), _arrow1898(), None if (len(persons) == 0) else persons, _arrow1899(), tables, None, assay_identifiers, _arrow1900()), default_arg(assays, empty()))


Study_ISAJson_decoder: Decoder_1[tuple[ArcStudy, FSharpList[ArcAssay]]] = Decode_objectNoAdditionalProperties(Study_ISAJson_allowedFields, _arrow1901)

def ARCtrl_ArcStudy__ArcStudy_fromJsonString_Static_Z721C83C5(s: str) -> ArcStudy:
    match_value: FSharpResult_2[ArcStudy, str] = Decode_fromString(Study_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_ArcStudy__ArcStudy_toJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[ArcStudy], str]:
    def _arrow1902(obj: ArcStudy, spaces: Any=spaces) -> str:
        value: Json = Study_encoder(obj)
        return to_string(default_spaces(spaces), value)

    return _arrow1902


def ARCtrl_ArcStudy__ArcStudy_ToJsonString_71136F3F(this: ArcStudy, spaces: int | None=None) -> str:
    return ARCtrl_ArcStudy__ArcStudy_toJsonString_Static_71136F3F(spaces)(this)


def ARCtrl_ArcStudy__ArcStudy_fromCompressedJsonString_Static_Z721C83C5(s: str) -> ArcStudy:
    try: 
        match_value: FSharpResult_2[ArcStudy, str] = Decode_fromString(decode(Study_decoderCompressed), s)
        if match_value.tag == 1:
            raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

        else: 
            return match_value.fields[0]


    except Exception as e_1:
        arg_1: str = str(e_1)
        return to_fail(printf("Error. Unable to parse json string to ArcStudy: %s"))(arg_1)



def ARCtrl_ArcStudy__ArcStudy_toCompressedJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[ArcStudy], str]:
    def _arrow1903(obj: ArcStudy, spaces: Any=spaces) -> str:
        return to_string(default_arg(spaces, 0), encode_1(Study_encoderCompressed, obj))

    return _arrow1903


def ARCtrl_ArcStudy__ArcStudy_ToCompressedJsonString_71136F3F(this: ArcStudy, spaces: int | None=None) -> str:
    return ARCtrl_ArcStudy__ArcStudy_toCompressedJsonString_Static_71136F3F(spaces)(this)


def ARCtrl_ArcStudy__ArcStudy_fromROCrateJsonString_Static_Z721C83C5(s: str) -> tuple[ArcStudy, FSharpList[ArcAssay]]:
    match_value: FSharpResult_2[tuple[ArcStudy, FSharpList[ArcAssay]], str] = Decode_fromString(Study_ROCrate_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_ArcStudy__ArcStudy_toROCrateJsonString_Static_3BA23086(assays: FSharpList[ArcAssay] | None=None, spaces: int | None=None) -> Callable[[ArcStudy], str]:
    def _arrow1904(obj: ArcStudy, assays: Any=assays, spaces: Any=spaces) -> str:
        value: Json = Study_ROCrate_encoder(assays, obj)
        return to_string(default_spaces(spaces), value)

    return _arrow1904


def ARCtrl_ArcStudy__ArcStudy_ToROCrateJsonString_3BA23086(this: ArcStudy, assays: FSharpList[ArcAssay] | None=None, spaces: int | None=None) -> str:
    return ARCtrl_ArcStudy__ArcStudy_toROCrateJsonString_Static_3BA23086(assays, spaces)(this)


def ARCtrl_ArcStudy__ArcStudy_fromISAJsonString_Static_Z721C83C5(s: str) -> tuple[ArcStudy, FSharpList[ArcAssay]]:
    match_value: FSharpResult_2[tuple[ArcStudy, FSharpList[ArcAssay]], str] = Decode_fromString(Study_ISAJson_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_ArcStudy__ArcStudy_toISAJsonString_Static_Z3FD920F1(assays: FSharpList[ArcAssay] | None=None, spaces: int | None=None, use_idreferencing: bool | None=None) -> Callable[[ArcStudy], str]:
    id_map: Any | None = dict([]) if default_arg(use_idreferencing, False) else None
    def _arrow1905(obj: ArcStudy, assays: Any=assays, spaces: Any=spaces, use_idreferencing: Any=use_idreferencing) -> str:
        value: Json = Study_ISAJson_encoder(id_map, assays, obj)
        return to_string(default_spaces(spaces), value)

    return _arrow1905


def ARCtrl_ArcStudy__ArcStudy_ToISAJsonString_Z3FD920F1(this: ArcStudy, assays: FSharpList[ArcAssay] | None=None, spaces: int | None=None, use_idreferencing: bool | None=None) -> str:
    return ARCtrl_ArcStudy__ArcStudy_toISAJsonString_Static_Z3FD920F1(assays, spaces, use_idreferencing)(this)


__all__ = ["Study_Helper_getAssayInformation", "Study_encoder", "Study_decoder", "Study_encoderCompressed", "Study_decoderCompressed", "Study_ROCrate_genID", "Study_ROCrate_encoder", "Study_ROCrate_decoder", "Study_ISAJson_encoder", "Study_ISAJson_allowedFields", "Study_ISAJson_decoder", "ARCtrl_ArcStudy__ArcStudy_fromJsonString_Static_Z721C83C5", "ARCtrl_ArcStudy__ArcStudy_toJsonString_Static_71136F3F", "ARCtrl_ArcStudy__ArcStudy_ToJsonString_71136F3F", "ARCtrl_ArcStudy__ArcStudy_fromCompressedJsonString_Static_Z721C83C5", "ARCtrl_ArcStudy__ArcStudy_toCompressedJsonString_Static_71136F3F", "ARCtrl_ArcStudy__ArcStudy_ToCompressedJsonString_71136F3F", "ARCtrl_ArcStudy__ArcStudy_fromROCrateJsonString_Static_Z721C83C5", "ARCtrl_ArcStudy__ArcStudy_toROCrateJsonString_Static_3BA23086", "ARCtrl_ArcStudy__ArcStudy_ToROCrateJsonString_3BA23086", "ARCtrl_ArcStudy__ArcStudy_fromISAJsonString_Static_Z721C83C5", "ARCtrl_ArcStudy__ArcStudy_toISAJsonString_Static_Z3FD920F1", "ARCtrl_ArcStudy__ArcStudy_ToISAJsonString_Z3FD920F1"]

