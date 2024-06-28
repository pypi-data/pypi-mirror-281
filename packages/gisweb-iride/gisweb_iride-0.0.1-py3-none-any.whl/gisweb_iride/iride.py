
# type: ignore
from calendar import c
from typing import Any
from .schema import  IConfigProtocollo, IAmministrazione, IProtocolloResult, IDataProtocollo
import os, base64, uuid
import json
from datetime import datetime, date
from pydantic import BaseModel
from jinja2 import Environment, PackageLoader, select_autoescape
import time
import httpx
from bs4 import BeautifulSoup
import base64
import logging
from uuid import UUID

_logger = logging.getLogger('gisweb-iride')

env = Environment(
    loader=PackageLoader("gisweb_iride"),
    autoescape=select_autoescape()
)

class Protocollo:
    
    config: IConfigProtocollo
    DST:str | None
    
    def __init__(self, config:IConfigProtocollo):
        self.config = config

    
    
    def protocollaDocumento(self, data:IDataProtocollo, testXml:bool=False) -> str | IProtocolloResult:
        
        return self.serviceCall(Operazione="AAAAAAAAAAAAAA",xml="<pippo>pluto</pippo>")

        return IProtocolloResult(lngErrNumber=0, lngNumPG=123456, lngAnnoPG=2024)
    
    
 
    def parseResponse(self, xml:str):
        soup = BeautifulSoup(xml, 'xml') # memo xml tiene conto delle maiuscole lxml tutto minuscolo
        keys = ["IDPos","IDDeb","CodiceTipoDebito","Url","IdentificativoUnivocoVersamento","NumeroAvviso","TipoVersamento","StatoTecnicoPagamento",
                "EsitoRichiestaPagamento","ImportoTotaleRichiesta","ImportoTotalePagato","DataPagamento","DataAccredito","tipoIdentificativoUnivoco",
                "codiceIdentificativoUnivoco","Nome","Cognome","RagioneSociale","Localita","Provincia","Nazione","Email"]
        dz=dict()
        for key in keys:
            dz[key]=soup.find(key) and str(soup.find(key).string)

        return dz
    
  
    def serviceCall(self, Operazione:str, xml:str,  **kwargs):
        """
        chiamata base al servizio SOAP JPPA
        """
        import pdb;pdb.set_trace()
        config = self.config
        data_richiesta =  datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ') 

        template = env.get_template("serviceCall.xml")
        xml = template.render(
            content=xml, 
            codice_amministrazione = 'fff', 
            codice_aoo = 'gggggg',
            data = data_richiesta, 
        )
        headers = {'Content-type': 'text/xml; charset=utf-8'}  
        
        if kwargs.get("testXml"):
            return xml

        with httpx.Client() as client:
                        
            response = client.post(config.wsUrl, content=xml, headers=headers)
            soup = BeautifulSoup(response.text, 'xml')
            if soup.find('EsitoOperazione') and soup.find('DatiDettaglioRisposta'):
                if soup.find('EsitoOperazione').string == "OK":
                    return self.parseResponse(soup.find('DatiDettaglioRisposta').string)

                elif soup.find('EsitoOperazione').string == "ERROR":
                    try:
                        return {"esito":soup.find('EsitoOperazione').string, "errore":soup.find('Codice').string, "descrizione":soup.find('Descrizione').string}
                    except:
                        with open("./jppa_resp.xml", "a") as f:
                            f.write(response.text)

                    
            else:
                with open("./jppa_resp.xml", "a") as f:
                    f.write(response.text)
   
        return {"esito":"ERRORE NON GESTITO"}
    



        
         
  




