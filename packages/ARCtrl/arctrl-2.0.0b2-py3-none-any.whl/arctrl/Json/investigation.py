from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..fable_modules.fable_library.list import (choose, of_array, unzip, FSharpList, empty)
from ..fable_modules.fable_library.option import default_arg
from ..fable_modules.fable_library.result import FSharpResult_2
from ..fable_modules.fable_library.seq import (concat, map)
from ..fable_modules.fable_library.seq2 import distinct_by
from ..fable_modules.fable_library.string_ import (to_text, printf, to_fail)
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import (equals, string_hash)
from ..fable_modules.thoth_json_core.decode import (object, IRequiredGetter, string, IOptionalGetter, IGetters, list_1 as list_1_1)
from ..fable_modules.thoth_json_core.types import (Json, Decoder_1)
from ..fable_modules.thoth_json_python.decode import Decode_fromString
from ..fable_modules.thoth_json_python.encode import to_string
from ..Core.arc_types import (ArcAssay, ArcStudy, ArcInvestigation)
from ..Core.comment import Comment
from ..Core.Helper.identifier import create_missing_identifier
from ..Core.ontology_annotation import OntologyAnnotation
from ..Core.ontology_source_reference import OntologySourceReference
from ..Core.person import Person
from ..Core.publication import Publication
from ..Core.Table.composite_cell import CompositeCell
from .assay import (Assay_encoder, Assay_decoder, Assay_encoderCompressed, Assay_decoderCompressed)
from .comment import (Comment_encoder, Comment_decoder, Comment_ROCrate_encoder, Comment_ROCrate_decoder, Comment_ISAJson_encoder, Comment_ISAJson_decoder)
from .context.rocrate.isa_investigation_context import context_jsonvalue
from .context.rocrate.rocrate_context import (conforms_to_jsonvalue, context_jsonvalue as context_jsonvalue_1)
from .decode import (Decode_resizeArray, Decode_objectNoAdditionalProperties)
from .encode import (try_include, try_include_seq, default_spaces)
from .ontology_source_reference import (OntologySourceReference_encoder, OntologySourceReference_decoder, OntologySourceReference_ROCrate_encoder, OntologySourceReference_ROCrate_decoder, OntologySourceReference_ISAJson_encoder, OntologySourceReference_ISAJson_decoder)
from .person import (Person_encoder, Person_decoder, Person_ROCrate_encoder, Person_ROCrate_decoder, Person_ISAJson_encoder, Person_ISAJson_decoder)
from .publication import (Publication_encoder, Publication_decoder, Publication_ROCrate_encoder, Publication_ROCrate_decoder, Publication_ISAJson_encoder, Publication_ISAJson_decoder)
from .study import (Study_encoder, Study_decoder, Study_encoderCompressed, Study_decoderCompressed, Study_ROCrate_encoder, Study_ROCrate_decoder, Study_ISAJson_encoder, Study_ISAJson_decoder)
from .Table.compression import (decode, encode)

def Investigation_encoder(inv: ArcInvestigation) -> Json:
    def chooser(tupled_arg: tuple[str, Json], inv: Any=inv) -> tuple[str, Json] | None:
        v: Json = tupled_arg[1]
        if equals(v, Json(3)):
            return None

        else: 
            return (tupled_arg[0], v)


    def _arrow1952(value_1: str, inv: Any=inv) -> Json:
        return Json(0, value_1)

    def _arrow1953(value_3: str, inv: Any=inv) -> Json:
        return Json(0, value_3)

    def _arrow1954(value_5: str, inv: Any=inv) -> Json:
        return Json(0, value_5)

    def _arrow1955(value_7: str, inv: Any=inv) -> Json:
        return Json(0, value_7)

    def _arrow1956(osr: OntologySourceReference, inv: Any=inv) -> Json:
        return OntologySourceReference_encoder(osr)

    def _arrow1957(oa: Publication, inv: Any=inv) -> Json:
        return Publication_encoder(oa)

    def _arrow1958(person: Person, inv: Any=inv) -> Json:
        return Person_encoder(person)

    def _arrow1959(assay: ArcAssay, inv: Any=inv) -> Json:
        return Assay_encoder(assay)

    def _arrow1960(study: ArcStudy, inv: Any=inv) -> Json:
        return Study_encoder(study)

    def _arrow1961(value_9: str, inv: Any=inv) -> Json:
        return Json(0, value_9)

    def _arrow1962(comment: Comment, inv: Any=inv) -> Json:
        return Comment_encoder(comment)

    return Json(5, choose(chooser, of_array([("Identifier", Json(0, inv.Identifier)), try_include("Title", _arrow1952, inv.Title), try_include("Description", _arrow1953, inv.Description), try_include("SubmissionDate", _arrow1954, inv.SubmissionDate), try_include("PublicReleaseDate", _arrow1955, inv.PublicReleaseDate), try_include_seq("OntologySourceReferences", _arrow1956, inv.OntologySourceReferences), try_include_seq("Publications", _arrow1957, inv.Publications), try_include_seq("Contacts", _arrow1958, inv.Contacts), try_include_seq("Assays", _arrow1959, inv.Assays), try_include_seq("Studies", _arrow1960, inv.Studies), try_include_seq("RegisteredStudyIdentifiers", _arrow1961, inv.RegisteredStudyIdentifiers), try_include_seq("Comments", _arrow1962, inv.Comments)])))


def _arrow1975(get: IGetters) -> ArcInvestigation:
    def _arrow1963(__unit: None=None) -> str:
        object_arg: IRequiredGetter = get.Required
        return object_arg.Field("Identifier", string)

    def _arrow1964(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("Title", string)

    def _arrow1965(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("Description", string)

    def _arrow1966(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("SubmissionDate", string)

    def _arrow1967(__unit: None=None) -> str | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("PublicReleaseDate", string)

    def _arrow1968(__unit: None=None) -> Array[OntologySourceReference] | None:
        arg_11: Decoder_1[Array[OntologySourceReference]] = Decode_resizeArray(OntologySourceReference_decoder)
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("OntologySourceReferences", arg_11)

    def _arrow1969(__unit: None=None) -> Array[Publication] | None:
        arg_13: Decoder_1[Array[Publication]] = Decode_resizeArray(Publication_decoder)
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("Publications", arg_13)

    def _arrow1970(__unit: None=None) -> Array[Person] | None:
        arg_15: Decoder_1[Array[Person]] = Decode_resizeArray(Person_decoder)
        object_arg_7: IOptionalGetter = get.Optional
        return object_arg_7.Field("Contacts", arg_15)

    def _arrow1971(__unit: None=None) -> Array[ArcAssay] | None:
        arg_17: Decoder_1[Array[ArcAssay]] = Decode_resizeArray(Assay_decoder)
        object_arg_8: IOptionalGetter = get.Optional
        return object_arg_8.Field("Assays", arg_17)

    def _arrow1972(__unit: None=None) -> Array[ArcStudy] | None:
        arg_19: Decoder_1[Array[ArcStudy]] = Decode_resizeArray(Study_decoder)
        object_arg_9: IOptionalGetter = get.Optional
        return object_arg_9.Field("Studies", arg_19)

    def _arrow1973(__unit: None=None) -> Array[str] | None:
        arg_21: Decoder_1[Array[str]] = Decode_resizeArray(string)
        object_arg_10: IOptionalGetter = get.Optional
        return object_arg_10.Field("RegisteredStudyIdentifiers", arg_21)

    def _arrow1974(__unit: None=None) -> Array[Comment] | None:
        arg_23: Decoder_1[Array[Comment]] = Decode_resizeArray(Comment_decoder)
        object_arg_11: IOptionalGetter = get.Optional
        return object_arg_11.Field("Comments", arg_23)

    return ArcInvestigation(_arrow1963(), _arrow1964(), _arrow1965(), _arrow1966(), _arrow1967(), _arrow1968(), _arrow1969(), _arrow1970(), _arrow1971(), _arrow1972(), _arrow1973(), _arrow1974())


Investigation_decoder: Decoder_1[ArcInvestigation] = object(_arrow1975)

def Investigation_encoderCompressed(string_table: Any, oa_table: Any, cell_table: Any, inv: ArcInvestigation) -> Json:
    def chooser(tupled_arg: tuple[str, Json], string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> tuple[str, Json] | None:
        v: Json = tupled_arg[1]
        if equals(v, Json(3)):
            return None

        else: 
            return (tupled_arg[0], v)


    def _arrow1976(value_1: str, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> Json:
        return Json(0, value_1)

    def _arrow1977(value_3: str, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> Json:
        return Json(0, value_3)

    def _arrow1978(value_5: str, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> Json:
        return Json(0, value_5)

    def _arrow1979(value_7: str, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> Json:
        return Json(0, value_7)

    def _arrow1980(osr: OntologySourceReference, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> Json:
        return OntologySourceReference_encoder(osr)

    def _arrow1981(oa: Publication, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> Json:
        return Publication_encoder(oa)

    def _arrow1982(person: Person, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> Json:
        return Person_encoder(person)

    def _arrow1983(assay: ArcAssay, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> Json:
        return Assay_encoderCompressed(string_table, oa_table, cell_table, assay)

    def _arrow1984(study: ArcStudy, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> Json:
        return Study_encoderCompressed(string_table, oa_table, cell_table, study)

    def _arrow1985(value_9: str, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> Json:
        return Json(0, value_9)

    def _arrow1986(comment: Comment, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> Json:
        return Comment_encoder(comment)

    return Json(5, choose(chooser, of_array([("Identifier", Json(0, inv.Identifier)), try_include("Title", _arrow1976, inv.Title), try_include("Description", _arrow1977, inv.Description), try_include("SubmissionDate", _arrow1978, inv.SubmissionDate), try_include("PublicReleaseDate", _arrow1979, inv.PublicReleaseDate), try_include_seq("OntologySourceReferences", _arrow1980, inv.OntologySourceReferences), try_include_seq("Publications", _arrow1981, inv.Publications), try_include_seq("Contacts", _arrow1982, inv.Contacts), try_include_seq("Assays", _arrow1983, inv.Assays), try_include_seq("Studies", _arrow1984, inv.Studies), try_include_seq("RegisteredStudyIdentifiers", _arrow1985, inv.RegisteredStudyIdentifiers), try_include_seq("Comments", _arrow1986, inv.Comments)])))


def Investigation_decoderCompressed(string_table: Array[str], oa_table: Array[OntologyAnnotation], cell_table: Array[CompositeCell]) -> Decoder_1[ArcInvestigation]:
    def _arrow1999(get: IGetters, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table) -> ArcInvestigation:
        def _arrow1987(__unit: None=None) -> str:
            object_arg: IRequiredGetter = get.Required
            return object_arg.Field("Identifier", string)

        def _arrow1988(__unit: None=None) -> str | None:
            object_arg_1: IOptionalGetter = get.Optional
            return object_arg_1.Field("Title", string)

        def _arrow1989(__unit: None=None) -> str | None:
            object_arg_2: IOptionalGetter = get.Optional
            return object_arg_2.Field("Description", string)

        def _arrow1990(__unit: None=None) -> str | None:
            object_arg_3: IOptionalGetter = get.Optional
            return object_arg_3.Field("SubmissionDate", string)

        def _arrow1991(__unit: None=None) -> str | None:
            object_arg_4: IOptionalGetter = get.Optional
            return object_arg_4.Field("PublicReleaseDate", string)

        def _arrow1992(__unit: None=None) -> Array[OntologySourceReference] | None:
            arg_11: Decoder_1[Array[OntologySourceReference]] = Decode_resizeArray(OntologySourceReference_decoder)
            object_arg_5: IOptionalGetter = get.Optional
            return object_arg_5.Field("OntologySourceReferences", arg_11)

        def _arrow1993(__unit: None=None) -> Array[Publication] | None:
            arg_13: Decoder_1[Array[Publication]] = Decode_resizeArray(Publication_decoder)
            object_arg_6: IOptionalGetter = get.Optional
            return object_arg_6.Field("Publications", arg_13)

        def _arrow1994(__unit: None=None) -> Array[Person] | None:
            arg_15: Decoder_1[Array[Person]] = Decode_resizeArray(Person_decoder)
            object_arg_7: IOptionalGetter = get.Optional
            return object_arg_7.Field("Contacts", arg_15)

        def _arrow1995(__unit: None=None) -> Array[ArcAssay] | None:
            arg_17: Decoder_1[Array[ArcAssay]] = Decode_resizeArray(Assay_decoderCompressed(string_table, oa_table, cell_table))
            object_arg_8: IOptionalGetter = get.Optional
            return object_arg_8.Field("Assays", arg_17)

        def _arrow1996(__unit: None=None) -> Array[ArcStudy] | None:
            arg_19: Decoder_1[Array[ArcStudy]] = Decode_resizeArray(Study_decoderCompressed(string_table, oa_table, cell_table))
            object_arg_9: IOptionalGetter = get.Optional
            return object_arg_9.Field("Studies", arg_19)

        def _arrow1997(__unit: None=None) -> Array[str] | None:
            arg_21: Decoder_1[Array[str]] = Decode_resizeArray(string)
            object_arg_10: IOptionalGetter = get.Optional
            return object_arg_10.Field("RegisteredStudyIdentifiers", arg_21)

        def _arrow1998(__unit: None=None) -> Array[Comment] | None:
            arg_23: Decoder_1[Array[Comment]] = Decode_resizeArray(Comment_decoder)
            object_arg_11: IOptionalGetter = get.Optional
            return object_arg_11.Field("Comments", arg_23)

        return ArcInvestigation(_arrow1987(), _arrow1988(), _arrow1989(), _arrow1990(), _arrow1991(), _arrow1992(), _arrow1993(), _arrow1994(), _arrow1995(), _arrow1996(), _arrow1997(), _arrow1998())

    return object(_arrow1999)


def Investigation_ROCrate_genID(i: ArcInvestigation) -> str:
    return "./"


def Investigation_ROCrate_encoder(oa: ArcInvestigation) -> Json:
    def chooser(tupled_arg: tuple[str, Json], oa: Any=oa) -> tuple[str, Json] | None:
        v: Json = tupled_arg[1]
        if equals(v, Json(3)):
            return None

        else: 
            return (tupled_arg[0], v)


    def _arrow2000(value_5: str, oa: Any=oa) -> Json:
        return Json(0, value_5)

    def _arrow2001(value_7: str, oa: Any=oa) -> Json:
        return Json(0, value_7)

    def _arrow2002(value_9: str, oa: Any=oa) -> Json:
        return Json(0, value_9)

    def _arrow2003(value_11: str, oa: Any=oa) -> Json:
        return Json(0, value_11)

    def _arrow2004(osr: OntologySourceReference, oa: Any=oa) -> Json:
        return OntologySourceReference_ROCrate_encoder(osr)

    def _arrow2005(oa_1: Publication, oa: Any=oa) -> Json:
        return Publication_ROCrate_encoder(oa_1)

    def _arrow2006(oa_2: Person, oa: Any=oa) -> Json:
        return Person_ROCrate_encoder(oa_2)

    def _arrow2007(s: ArcStudy, oa: Any=oa) -> Json:
        return Study_ROCrate_encoder(None, s)

    def _arrow2008(comment: Comment, oa: Any=oa) -> Json:
        return Comment_ROCrate_encoder(comment)

    return Json(5, choose(chooser, of_array([("@id", Json(0, Investigation_ROCrate_genID(oa))), ("@type", Json(0, "Investigation")), ("additionalType", Json(0, "Investigation")), ("identifier", Json(0, oa.Identifier)), ("filename", Json(0, ArcInvestigation.FileName())), try_include("title", _arrow2000, oa.Title), try_include("description", _arrow2001, oa.Description), try_include("submissionDate", _arrow2002, oa.SubmissionDate), try_include("publicReleaseDate", _arrow2003, oa.PublicReleaseDate), try_include_seq("ontologySourceReferences", _arrow2004, oa.OntologySourceReferences), try_include_seq("publications", _arrow2005, oa.Publications), try_include_seq("people", _arrow2006, oa.Contacts), try_include_seq("studies", _arrow2007, oa.Studies), try_include_seq("comments", _arrow2008, oa.Comments), ("@context", context_jsonvalue)])))


def _arrow2021(get: IGetters) -> ArcInvestigation:
    identifier: str
    match_value: str | None
    object_arg: IOptionalGetter = get.Optional
    match_value = object_arg.Field("identifier", string)
    identifier = create_missing_identifier() if (match_value is None) else match_value
    def _arrow2009(__unit: None=None) -> FSharpList[tuple[ArcStudy, FSharpList[ArcAssay]]] | None:
        arg_3: Decoder_1[FSharpList[tuple[ArcStudy, FSharpList[ArcAssay]]]] = list_1_1(Study_ROCrate_decoder)
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("studies", arg_3)

    pattern_input: tuple[FSharpList[ArcStudy], FSharpList[FSharpList[ArcAssay]]] = unzip(default_arg(_arrow2009(), empty()))
    studies_raw: FSharpList[ArcStudy] = pattern_input[0]
    def projection(a: ArcAssay) -> str:
        return a.Identifier

    class ObjectExpr2011:
        @property
        def Equals(self) -> Callable[[str, str], bool]:
            def _arrow2010(x: str, y: str) -> bool:
                return x == y

            return _arrow2010

        @property
        def GetHashCode(self) -> Callable[[str], int]:
            return string_hash

    assays: Array[ArcAssay] = list(distinct_by(projection, concat(pattern_input[1]), ObjectExpr2011()))
    studies: Array[ArcStudy] = list(studies_raw)
    def mapping(a_1: ArcStudy) -> str:
        return a_1.Identifier

    study_identifiers: Array[str] = list(map(mapping, studies_raw))
    def _arrow2012(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("title", string)

    def _arrow2013(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("description", string)

    def _arrow2014(__unit: None=None) -> str | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("submissionDate", string)

    def _arrow2015(__unit: None=None) -> str | None:
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("publicReleaseDate", string)

    def _arrow2016(__unit: None=None) -> Array[OntologySourceReference] | None:
        arg_13: Decoder_1[Array[OntologySourceReference]] = Decode_resizeArray(OntologySourceReference_ROCrate_decoder)
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("ontologySourceReferences", arg_13)

    def _arrow2018(__unit: None=None) -> Array[Publication] | None:
        arg_15: Decoder_1[Array[Publication]] = Decode_resizeArray(Publication_ROCrate_decoder)
        object_arg_7: IOptionalGetter = get.Optional
        return object_arg_7.Field("publications", arg_15)

    def _arrow2019(__unit: None=None) -> Array[Person] | None:
        arg_17: Decoder_1[Array[Person]] = Decode_resizeArray(Person_ROCrate_decoder)
        object_arg_8: IOptionalGetter = get.Optional
        return object_arg_8.Field("people", arg_17)

    def _arrow2020(__unit: None=None) -> Array[Comment] | None:
        arg_19: Decoder_1[Array[Comment]] = Decode_resizeArray(Comment_ROCrate_decoder)
        object_arg_9: IOptionalGetter = get.Optional
        return object_arg_9.Field("comments", arg_19)

    return ArcInvestigation(identifier, _arrow2012(), _arrow2013(), _arrow2014(), _arrow2015(), _arrow2016(), _arrow2018(), _arrow2019(), assays, studies, study_identifiers, _arrow2020())


Investigation_ROCrate_decoder: Decoder_1[ArcInvestigation] = object(_arrow2021)

def Investigation_ROCrate_encodeRoCrate(oa: ArcInvestigation) -> Json:
    def chooser(tupled_arg: tuple[str, Json], oa: Any=oa) -> tuple[str, Json] | None:
        v: Json = tupled_arg[1]
        if equals(v, Json(3)):
            return None

        else: 
            return (tupled_arg[0], v)


    def _arrow2023(value: str, oa: Any=oa) -> Json:
        return Json(0, value)

    def _arrow2024(value_2: str, oa: Any=oa) -> Json:
        return Json(0, value_2)

    def _arrow2025(oa_1: ArcInvestigation, oa: Any=oa) -> Json:
        return Investigation_ROCrate_encoder(oa_1)

    return Json(5, choose(chooser, of_array([try_include("@type", _arrow2023, "CreativeWork"), try_include("@id", _arrow2024, "ro-crate-metadata.json"), try_include("about", _arrow2025, oa), ("conformsTo", conforms_to_jsonvalue), ("@context", context_jsonvalue_1)])))


Investigation_ISAJson_allowedFields: FSharpList[str] = of_array(["@id", "filename", "identifier", "title", "description", "submissionDate", "publicReleaseDate", "ontologySourceReferences", "publications", "people", "studies", "comments", "@type", "@context"])

def Investigation_ISAJson_encoder(id_map: Any | None, inv: ArcInvestigation) -> Json:
    def chooser(tupled_arg: tuple[str, Json], id_map: Any=id_map, inv: Any=inv) -> tuple[str, Json] | None:
        v: Json = tupled_arg[1]
        if equals(v, Json(3)):
            return None

        else: 
            return (tupled_arg[0], v)


    def _arrow2030(value_3: str, id_map: Any=id_map, inv: Any=inv) -> Json:
        return Json(0, value_3)

    def _arrow2031(value_5: str, id_map: Any=id_map, inv: Any=inv) -> Json:
        return Json(0, value_5)

    def _arrow2032(value_7: str, id_map: Any=id_map, inv: Any=inv) -> Json:
        return Json(0, value_7)

    def _arrow2033(value_9: str, id_map: Any=id_map, inv: Any=inv) -> Json:
        return Json(0, value_9)

    def _arrow2034(osr: OntologySourceReference, id_map: Any=id_map, inv: Any=inv) -> Json:
        return OntologySourceReference_ISAJson_encoder(id_map, osr)

    def _arrow2035(oa: Publication, id_map: Any=id_map, inv: Any=inv) -> Json:
        return Publication_ISAJson_encoder(id_map, oa)

    def _arrow2036(person: Person, id_map: Any=id_map, inv: Any=inv) -> Json:
        return Person_ISAJson_encoder(id_map, person)

    def _arrow2037(s: ArcStudy, id_map: Any=id_map, inv: Any=inv) -> Json:
        return Study_ISAJson_encoder(id_map, None, s)

    def _arrow2038(comment: Comment, id_map: Any=id_map, inv: Any=inv) -> Json:
        return Comment_ISAJson_encoder(id_map, comment)

    return Json(5, choose(chooser, of_array([("@id", Json(0, Investigation_ROCrate_genID(inv))), ("filename", Json(0, ArcInvestigation.FileName())), ("identifier", Json(0, inv.Identifier)), try_include("title", _arrow2030, inv.Title), try_include("description", _arrow2031, inv.Description), try_include("submissionDate", _arrow2032, inv.SubmissionDate), try_include("publicReleaseDate", _arrow2033, inv.PublicReleaseDate), try_include_seq("ontologySourceReferences", _arrow2034, inv.OntologySourceReferences), try_include_seq("publications", _arrow2035, inv.Publications), try_include_seq("people", _arrow2036, inv.Contacts), try_include_seq("studies", _arrow2037, inv.Studies), try_include_seq("comments", _arrow2038, inv.Comments)])))


def _arrow2050(get: IGetters) -> ArcInvestigation:
    identifer: str
    match_value: str | None
    object_arg: IOptionalGetter = get.Optional
    match_value = object_arg.Field("identifier", string)
    identifer = create_missing_identifier() if (match_value is None) else match_value
    def _arrow2039(__unit: None=None) -> FSharpList[tuple[ArcStudy, FSharpList[ArcAssay]]] | None:
        arg_3: Decoder_1[FSharpList[tuple[ArcStudy, FSharpList[ArcAssay]]]] = list_1_1(Study_ISAJson_decoder)
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("studies", arg_3)

    pattern_input: tuple[FSharpList[ArcStudy], FSharpList[FSharpList[ArcAssay]]] = unzip(default_arg(_arrow2039(), empty()))
    studies_raw: FSharpList[ArcStudy] = pattern_input[0]
    def projection(a: ArcAssay) -> str:
        return a.Identifier

    class ObjectExpr2041:
        @property
        def Equals(self) -> Callable[[str, str], bool]:
            def _arrow2040(x: str, y: str) -> bool:
                return x == y

            return _arrow2040

        @property
        def GetHashCode(self) -> Callable[[str], int]:
            return string_hash

    assays: Array[ArcAssay] = list(distinct_by(projection, concat(pattern_input[1]), ObjectExpr2041()))
    studies: Array[ArcStudy] = list(studies_raw)
    def mapping(a_1: ArcStudy) -> str:
        return a_1.Identifier

    study_identifiers: Array[str] = list(map(mapping, studies_raw))
    def _arrow2042(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("title", string)

    def _arrow2043(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("description", string)

    def _arrow2044(__unit: None=None) -> str | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("submissionDate", string)

    def _arrow2045(__unit: None=None) -> str | None:
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("publicReleaseDate", string)

    def _arrow2046(__unit: None=None) -> Array[OntologySourceReference] | None:
        arg_13: Decoder_1[Array[OntologySourceReference]] = Decode_resizeArray(OntologySourceReference_ISAJson_decoder)
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("ontologySourceReferences", arg_13)

    def _arrow2047(__unit: None=None) -> Array[Publication] | None:
        arg_15: Decoder_1[Array[Publication]] = Decode_resizeArray(Publication_ISAJson_decoder)
        object_arg_7: IOptionalGetter = get.Optional
        return object_arg_7.Field("publications", arg_15)

    def _arrow2048(__unit: None=None) -> Array[Person] | None:
        arg_17: Decoder_1[Array[Person]] = Decode_resizeArray(Person_ISAJson_decoder)
        object_arg_8: IOptionalGetter = get.Optional
        return object_arg_8.Field("people", arg_17)

    def _arrow2049(__unit: None=None) -> Array[Comment] | None:
        arg_19: Decoder_1[Array[Comment]] = Decode_resizeArray(Comment_ISAJson_decoder)
        object_arg_9: IOptionalGetter = get.Optional
        return object_arg_9.Field("comments", arg_19)

    return ArcInvestigation(identifer, _arrow2042(), _arrow2043(), _arrow2044(), _arrow2045(), _arrow2046(), _arrow2047(), _arrow2048(), assays, studies, study_identifiers, _arrow2049())


Investigation_ISAJson_decoder: Decoder_1[ArcInvestigation] = Decode_objectNoAdditionalProperties(Investigation_ISAJson_allowedFields, _arrow2050)

def ARCtrl_ArcInvestigation__ArcInvestigation_fromJsonString_Static_Z721C83C5(s: str) -> ArcInvestigation:
    match_value: FSharpResult_2[ArcInvestigation, str] = Decode_fromString(Investigation_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_ArcInvestigation__ArcInvestigation_toJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[ArcInvestigation], str]:
    def _arrow2051(obj: ArcInvestigation, spaces: Any=spaces) -> str:
        value: Json = Investigation_encoder(obj)
        return to_string(default_spaces(spaces), value)

    return _arrow2051


def ARCtrl_ArcInvestigation__ArcInvestigation_ToJsonString_71136F3F(this: ArcInvestigation, spaces: int | None=None) -> str:
    return ARCtrl_ArcInvestigation__ArcInvestigation_toJsonString_Static_71136F3F(spaces)(this)


def ARCtrl_ArcInvestigation__ArcInvestigation_fromCompressedJsonString_Static_Z721C83C5(s: str) -> ArcInvestigation:
    try: 
        match_value: FSharpResult_2[ArcInvestigation, str] = Decode_fromString(decode(Investigation_decoderCompressed), s)
        if match_value.tag == 1:
            raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

        else: 
            return match_value.fields[0]


    except Exception as e_1:
        arg_1: str = str(e_1)
        return to_fail(printf("Error. Unable to parse json string to ArcStudy: %s"))(arg_1)



def ARCtrl_ArcInvestigation__ArcInvestigation_toCompressedJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[ArcInvestigation], str]:
    def _arrow2052(obj: ArcInvestigation, spaces: Any=spaces) -> str:
        return to_string(default_arg(spaces, 0), encode(Investigation_encoderCompressed, obj))

    return _arrow2052


def ARCtrl_ArcInvestigation__ArcInvestigation_ToCompressedJsonString_71136F3F(this: ArcInvestigation, spaces: int | None=None) -> str:
    return ARCtrl_ArcInvestigation__ArcInvestigation_toCompressedJsonString_Static_71136F3F(spaces)(this)


def ARCtrl_ArcInvestigation__ArcInvestigation_fromROCrateJsonString_Static_Z721C83C5(s: str) -> ArcInvestigation:
    match_value: FSharpResult_2[ArcInvestigation, str] = Decode_fromString(Investigation_ROCrate_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_ArcInvestigation__ArcInvestigation_toROCrateJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[ArcInvestigation], str]:
    def _arrow2053(obj: ArcInvestigation, spaces: Any=spaces) -> str:
        value: Json = Investigation_ROCrate_encoder(obj)
        return to_string(default_spaces(spaces), value)

    return _arrow2053


def ARCtrl_ArcInvestigation__ArcInvestigation_ToROCrateJsonString_71136F3F(this: ArcInvestigation, spaces: int | None=None) -> str:
    return ARCtrl_ArcInvestigation__ArcInvestigation_toROCrateJsonString_Static_71136F3F(spaces)(this)


def ARCtrl_ArcInvestigation__ArcInvestigation_toISAJsonString_Static_Z3B036AA(spaces: int | None=None, use_idreferencing: bool | None=None) -> Callable[[ArcInvestigation], str]:
    id_map: Any | None = dict([]) if default_arg(use_idreferencing, False) else None
    def _arrow2054(obj: ArcInvestigation, spaces: Any=spaces, use_idreferencing: Any=use_idreferencing) -> str:
        value: Json = Investigation_ISAJson_encoder(id_map, obj)
        return to_string(default_spaces(spaces), value)

    return _arrow2054


def ARCtrl_ArcInvestigation__ArcInvestigation_fromISAJsonString_Static_Z721C83C5(s: str) -> ArcInvestigation:
    match_value: FSharpResult_2[ArcInvestigation, str] = Decode_fromString(Investigation_ISAJson_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_ArcInvestigation__ArcInvestigation_ToISAJsonString_Z3B036AA(this: ArcInvestigation, spaces: int | None=None, use_idreferencing: bool | None=None) -> str:
    return ARCtrl_ArcInvestigation__ArcInvestigation_toISAJsonString_Static_Z3B036AA(spaces, use_idreferencing)(this)


__all__ = ["Investigation_encoder", "Investigation_decoder", "Investigation_encoderCompressed", "Investigation_decoderCompressed", "Investigation_ROCrate_genID", "Investigation_ROCrate_encoder", "Investigation_ROCrate_decoder", "Investigation_ROCrate_encodeRoCrate", "Investigation_ISAJson_allowedFields", "Investigation_ISAJson_encoder", "Investigation_ISAJson_decoder", "ARCtrl_ArcInvestigation__ArcInvestigation_fromJsonString_Static_Z721C83C5", "ARCtrl_ArcInvestigation__ArcInvestigation_toJsonString_Static_71136F3F", "ARCtrl_ArcInvestigation__ArcInvestigation_ToJsonString_71136F3F", "ARCtrl_ArcInvestigation__ArcInvestigation_fromCompressedJsonString_Static_Z721C83C5", "ARCtrl_ArcInvestigation__ArcInvestigation_toCompressedJsonString_Static_71136F3F", "ARCtrl_ArcInvestigation__ArcInvestigation_ToCompressedJsonString_71136F3F", "ARCtrl_ArcInvestigation__ArcInvestigation_fromROCrateJsonString_Static_Z721C83C5", "ARCtrl_ArcInvestigation__ArcInvestigation_toROCrateJsonString_Static_71136F3F", "ARCtrl_ArcInvestigation__ArcInvestigation_ToROCrateJsonString_71136F3F", "ARCtrl_ArcInvestigation__ArcInvestigation_toISAJsonString_Static_Z3B036AA", "ARCtrl_ArcInvestigation__ArcInvestigation_fromISAJsonString_Static_Z721C83C5", "ARCtrl_ArcInvestigation__ArcInvestigation_ToISAJsonString_Z3B036AA"]

