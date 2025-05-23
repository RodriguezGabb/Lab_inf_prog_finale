import re
from typing import List, Tuple
from pydantic import BaseModel
from src.backend.mariadb_manager import execute_query

class Proprieta(BaseModel):
    property_name:str
    property_value:str
class Res(BaseModel):
    item_type:str
    properties:List[Proprieta]
class Schema(BaseModel):
    table_name:str
    table_column:str



def clean_input(inp:str)->str:
    '''ripulisce e corregge l'input per le querry sql'''
    if "'" in inp:
        inp=inp.replace("'","\\'")#controllo che impedisce di fare injection usando il carattere '
    return re.sub(r'[,.?]', '', inp)#togle . , e ? non desiderati

def crea_res(lista:List[Tuple[str]], type:str)->Res:
    '''funzione che crea il tipo di dato richiesto da jason per la comunicazione appartire del risultato delle querry sql'''
    res:List[Res]=[] #TODO chiedere a prof se va bene, oppure devo mettere tutte le collonne in propriety name e se devo farlo manualmente o usando BaseModel (probabilmente la seconda)
    for oggetto in lista:
        lista_proprita:List[Proprieta]=[]
        proprieta:Proprieta=Proprieta(property_name="name", property_value=oggetto[0])
        lista_proprita.append(proprieta)
        res.append(Res(item_type=type,properties=lista_proprita))
        
    return res


def get_film_da_anno(anno:int)->Res:
    '''seleziona tutti i film usciti in quel anno'''
    anno=clean_input(anno)
    try:
        anno=int(anno)
    except(ValueError):
        return f"Non è possibile filtrare tramite anno dato che l'input inserito \"{anno}\"non è numerico"
    lista_film=execute_query("SELECT titolo FROM movies WHERE anno=%d"%anno)
    if lista_film==None:
        return f"Errore nel recupero dei film dal anno \"{anno}\""
    res:Res=crea_res(lista_film,"film")
    return res

def get_regista_da_piattaforma(piattaforma:str)->Res:
    '''seleziona tutti i registi disponibili in tale piattaforma'''
    piattaforma=clean_input(piattaforma)

    lista_registi=execute_query("SELECT DISTINCT Registi.regista From Registi JOIN movies ON Registi.regista=movies.regista JOIN Piattaforme ON Piattaforme.titolo=movies.titolo WHERE piattaforma_1='%s' OR piattaforma_2='%s'"%(piattaforma,piattaforma))
    if lista_registi==None:
        return f"Errore nel recupero dei registi dalla piattaforma \"{piattaforma}\""
    res:Res=crea_res(lista_registi, "director")
    return res

def get_film_da_genere(genere:str)->Res:
    '''seleziona tutti i film di tale genenre'''
    genere=clean_input(genere)

    lista_film=execute_query("SELECT titolo FROM movies WHERE genere='%s'"%genere)
    if lista_film==None:
        return f"Errore nel recupero dei film del genere \"{genere}\""
    res:Res=crea_res(lista_film,"film")
    return res

def get_film_da_eta_regista(eta_input:str)->Res:
    '''seleziona tutti i film dove il regista a quel eta'''
    eta=clean_input(eta_input)
    eta=(re.search(r'\d+',eta))#recupera solo il valore numerico
    try:
        if not eta:
            return f"Non è possibile filtrare tramite età dato che l'input inserito \"{eta_input}\" non ha un valore numerico"
        eta=int(eta.group())
    except(ValueError):
        return f"Non è possibile filtrare tramite età dato che l'input inserito \"{eta_input}\" non ha un valore numerico"
    
    lista_film=execute_query("SELECT titolo FROM movies CROSS JOIN Registi ON movies.regista=Registi.regista WHERE eta>=%d" %eta)
    if lista_film==None:
        return f"Errore nel recupero dei film creati da autori con \"{eta}\" o superiore"
    res:Res=crea_res(lista_film,"film")
    return res

def get_registi_con_piu_film(num_film:str)->Res:
    '''seleziona tutti i registi con più di un film o se specificato più di un numero (numerico)'''
    num_clean=clean_input(num_film)
    num=(re.search(r'\d+',num_clean))#recupera solo il valore numerico
    if num:
        num=int(num.group())
        lista_registi=execute_query("SELECT regista FROM movies GROUP BY regista HAVING COUNT(regista)>%d ;"%num)
        if lista_registi==None:
            return f"Errore nel recupero dei registi con più di {num} film"
    else:
        lista_registi=execute_query("SELECT regista FROM movies GROUP BY regista HAVING COUNT(regista)>1 ;")
        if lista_registi==None:
            return f"Errore nel recupero dei registi con più di un film"
    
    res:Res=crea_res(lista_registi, "director")
    return res

def get_collone_tabella(tabella:str)->List[Tuple]:
    '''Restituisce una lista di tutte le collonne della tabbella chiesta'''
    res= execute_query("SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA`='esonero' AND `TABLE_NAME`='%s';"%tabella)
    if res==None:
        return f"Errore nel recupero delle collone della tabella \"{tabella}\""
    return res

def schema_summary()->List[Schema]:
        '''Restituisce lo schema delle varie tabelle'''
        res:List[Schema]=[]
        tabelle=execute_query("SHOW TABLES")
        for tab in tabelle:#tab sta per tabella ma per non confondere i due per una lettera di differenza 
            nome_tabella=tab[0]
            colonne=execute_query("SHOW COLUMNS FROM %s" % nome_tabella)
            for col in colonne:
                nome_collonna=col[0]
                agg=Schema(table_name=nome_tabella,table_column=nome_collonna)
                res.append(agg)
        return res
