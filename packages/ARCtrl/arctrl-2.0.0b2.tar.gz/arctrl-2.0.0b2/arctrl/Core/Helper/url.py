from collections.abc import Callable
from typing import Any
from ...fable_modules.fable_library.util import to_enumerable
from .collections_ import (Dictionary_ofSeq, Dictionary_tryFind)

def OntobeeParser(tsr: str, local_tan: str) -> str:
    return ((((("" + "http://purl.obolibrary.org/obo/") + "") + tsr) + "_") + local_tan) + ""


def BioregistryParser(tsr: str, local_tan: str) -> str:
    return ((((("" + "https://bioregistry.io/") + "") + tsr) + ":") + local_tan) + ""


def OntobeeDPBOParser(tsr: str, local_tan: str) -> str:
    return ((((("" + "http://purl.org/nfdi4plants/ontology/dpbo/") + "") + tsr) + "_") + local_tan) + ""


def MSParser(tsr: str, local_tan: str) -> str:
    return ((((("" + "https://www.ebi.ac.uk/ols4/ontologies/ms/classes/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252F") + "") + tsr) + "_") + local_tan) + ""


def POParser(tsr: str, local_tan: str) -> str:
    return ((((("" + "https://www.ebi.ac.uk/ols4/ontologies/po/classes/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252F") + "") + tsr) + "_") + local_tan) + ""


def ROParser(tsr: str, local_tan: str) -> str:
    return ((((("" + "https://www.ebi.ac.uk/ols4/ontologies/ro/classes/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252F") + "") + tsr) + "_") + local_tan) + ""


def _arrow299(tsr: str) -> Callable[[str], str]:
    def _arrow298(local_tan: str) -> str:
        return OntobeeDPBOParser(tsr, local_tan)

    return _arrow298


def _arrow301(tsr_1: str) -> Callable[[str], str]:
    def _arrow300(local_tan_1: str) -> str:
        return MSParser(tsr_1, local_tan_1)

    return _arrow300


def _arrow303(tsr_2: str) -> Callable[[str], str]:
    def _arrow302(local_tan_2: str) -> str:
        return POParser(tsr_2, local_tan_2)

    return _arrow302


def _arrow305(tsr_3: str) -> Callable[[str], str]:
    def _arrow304(local_tan_3: str) -> str:
        return ROParser(tsr_3, local_tan_3)

    return _arrow304


def _arrow307(tsr_4: str) -> Callable[[str], str]:
    def _arrow306(local_tan_4: str) -> str:
        return BioregistryParser(tsr_4, local_tan_4)

    return _arrow306


def _arrow309(tsr_5: str) -> Callable[[str], str]:
    def _arrow308(local_tan_5: str) -> str:
        return BioregistryParser(tsr_5, local_tan_5)

    return _arrow308


def _arrow311(tsr_6: str) -> Callable[[str], str]:
    def _arrow310(local_tan_6: str) -> str:
        return BioregistryParser(tsr_6, local_tan_6)

    return _arrow310


def _arrow313(tsr_7: str) -> Callable[[str], str]:
    def _arrow312(local_tan_7: str) -> str:
        return BioregistryParser(tsr_7, local_tan_7)

    return _arrow312


def _arrow315(tsr_8: str) -> Callable[[str], str]:
    def _arrow314(local_tan_8: str) -> str:
        return BioregistryParser(tsr_8, local_tan_8)

    return _arrow314


def _arrow317(tsr_9: str) -> Callable[[str], str]:
    def _arrow316(local_tan_9: str) -> str:
        return BioregistryParser(tsr_9, local_tan_9)

    return _arrow316


def _arrow319(tsr_10: str) -> Callable[[str], str]:
    def _arrow318(local_tan_10: str) -> str:
        return BioregistryParser(tsr_10, local_tan_10)

    return _arrow318


def _arrow321(tsr_11: str) -> Callable[[str], str]:
    def _arrow320(local_tan_11: str) -> str:
        return BioregistryParser(tsr_11, local_tan_11)

    return _arrow320


def _arrow323(tsr_12: str) -> Callable[[str], str]:
    def _arrow322(local_tan_12: str) -> str:
        return BioregistryParser(tsr_12, local_tan_12)

    return _arrow322


def _arrow325(tsr_13: str) -> Callable[[str], str]:
    def _arrow324(local_tan_13: str) -> str:
        return BioregistryParser(tsr_13, local_tan_13)

    return _arrow324


def _arrow327(tsr_14: str) -> Callable[[str], str]:
    def _arrow326(local_tan_14: str) -> str:
        return BioregistryParser(tsr_14, local_tan_14)

    return _arrow326


uri_parser_collection: Any = Dictionary_ofSeq(to_enumerable([("DPBO", _arrow299), ("MS", _arrow301), ("PO", _arrow303), ("RO", _arrow305), ("ENVO", _arrow307), ("CHEBI", _arrow309), ("GO", _arrow311), ("OBI", _arrow313), ("PATO", _arrow315), ("PECO", _arrow317), ("TO", _arrow319), ("UO", _arrow321), ("EFO", _arrow323), ("NCIT", _arrow325), ("OMP", _arrow327)]))

def create_oauri(tsr: str, local_tan: str) -> str:
    match_value: Callable[[str, str], str] | None = Dictionary_tryFind(tsr, uri_parser_collection)
    if match_value is None:
        return OntobeeParser(tsr, local_tan)

    else: 
        return match_value(tsr)(local_tan)



__all__ = ["OntobeeParser", "BioregistryParser", "OntobeeDPBOParser", "MSParser", "POParser", "ROParser", "uri_parser_collection", "create_oauri"]

