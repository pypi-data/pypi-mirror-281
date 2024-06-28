from typing import Any

from pydantic import BaseModel, EmailStr, Json
from uuid import UUID

from enum import Enum

class IAzioneEnum(str, Enum):
    ESEGUI = "ESEGUI"
    CARICO = "CARICO"
    
class ISmistamentoEnum(str, Enum):
    CONOSCENZA = "CONOSCENZA"
    COMPETENZA = "COMPETENZA"

class IAmministrazione(BaseModel):
    Denominazione: str
    CodiceAOO: str
    CodiceEnte: str
    IndirizzoTelematico: EmailStr

class IConfigProtocollo(BaseModel):
    wsUrl: str
    wsUser: str
    wsEnte: str
    wsPassword: str
    amministrazione: IAmministrazione
    
    
class BaseRet(BaseModel):
    lngErrNumber: int = 0
    strErrString: str = ''

class ILoginRet(BaseRet):
    strDST: str | None
    
class IProtocolloResult(BaseRet):
    lngNumPG: int = 0
    lngAnnoPG: int = 0
    strDataPG: str = ''
    lngDocID: int = 0


class IAllegato(BaseModel):
    pass

class IDocumento(BaseModel):
    id: int | None
    descrizione: str
    tipo: str
    nome: str
    content: Any
    size: int
    mimetype: str
    ext: str

class IFascicolo(BaseModel):
    numero: str
    anno:str
    
class IParametro(BaseModel):
    nome: str
    valore: str




class ISoggettoProtocollo(BaseModel):
    IndirizzoTelematico: str
    Denominazione: str | None = None
    Nome: str | None = None
    Cognome: str | None = None
    TitoloDitta: str | None = None
    CodiceFiscaleDitta: str | None = None
    IndirizzoTelematicoDitta: str | None = None
    TipoMittente: str | None = None
    CodiceFiscale: str
    Titolo: str | None = None
    
#### da rinominare in gisweb.ads

class IDataProtocollo(BaseModel):
    Soggetti: list[ISoggettoProtocollo] = [
        ISoggettoProtocollo(
            IndirizzoTelematico = "rstarnini@inwind.it",
            Denominazione = "Ditta ACME",
            Nome = "Mario",
            Cognome = "Rossi",
            TitoloDitta = "Amministatore",
            CodiceFiscaleDitta = "01533090997",
            IndirizzoTelematicoDitta = "ditta@prova.it",
            TipoMittente = "G",
            CodiceFiscale = "RSSMRA84C01D969H",
            Titolo = "Richiedente"
        )]
    Flusso: str = "E"
    Oggetto: str = "Prova protocollo"
    Titolario: str = "06-01"
    UO: str =  "2.5.1"
    Fascicolo: IFascicolo = IFascicolo(numero='1', anno="2024")
    Parametri: list[IParametro] = [
        IParametro(nome="uo", valore="4.3"), 
        IParametro(nome="tipoSmistamento", valore="COMPETENZA"), #CONOSCENZA/COMPETENZA
        IParametro(nome="azione", valore="ESEGUI"), 
        IParametro(nome="smistamento", valore="4.3@@CONOSCENZA"),
        IParametro(nome="smistamento", valore="0.1@@CONOSCENZA"),
        IParametro(nome="smistamento", valore="0.2@@CONOSCENZA"),
        IParametro(nome="smistamento", valore="0.3@@CONOSCENZA")
    ]
    TipoDocumento: str = "WSTS"
    Principale: str = "documento_riepilogo"
    Allegati: list[str] = ["allegati_osservazione"]
    
