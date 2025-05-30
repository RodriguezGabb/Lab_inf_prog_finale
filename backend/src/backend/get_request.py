import re
from typing import List, Tuple
from pydantic import BaseModel
from src.backend.mariadb_manager import execute_query
#crea_res=class_maker get_film_da_anno=get_film_from_year get_regista_da_piattaforma=get_director_from_platform get_film_da_genere=get_film_from_genre
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
    '''fixes input for query'''
    if "'" in inp:
        inp=inp.replace("'","\\'")#prevents sql injections
    return re.sub(r'[,.?]', '', inp)#removes . and ?

def class_maker(input:List[Tuple[str]], type:str)->List[Res]:
    '''makes the right data type for json from query'''
    res:List[Res]=[] 
    for item in input:
        propertyList:List[Proprieta]=[]
        proprieta:Proprieta=Proprieta(property_name="name", property_value=item[0])
        propertyList.append(proprieta)
        res.append(Res(item_type=type,properties=propertyList))
        
    return res


def get_film_from_year(year:int)->Res:
    '''all film released in year'''
    year=clean_input(year)
    try:
        year=int(year)
    except(ValueError):
        return f"\"{year}\"is not a number"
    list_film=execute_query("SELECT title FROM movies WHERE anno=%d"%year)
    if list_film==None:
        return f"error in finding film fron year \"{year}\""
    res:Res=class_maker(list_film,"film")
    return res

def get_director_from_platform(platform:str)->Res:
    '''find all directors from given platform'''
    platform=clean_input(platform)

    director_list=execute_query("SELECT DISTINCT directors.director FROM directors JOIN movies ON directors.director=movies.director JOIN platforms ON platforms.titolo=movies.titolo WHERE platform1='%s' OR platform2='%s'"%(platform,platform))
    if director_list==None:
        return f"error in finding the directors from given platform \"{platform}\""
    res:Res=class_maker(director_list, "director")
    return res

def get_film_from_genre(genre:str)->Res:
    '''seleziona tutti i film di tale genenre'''
    genre=clean_input(genre)

    list_film=execute_query("SELECT titolo FROM movies WHERE genre='%s'"%genre)
    if list_film==None:
        return f"error in finding film from the genre \"{genre}\""
    res:Res=class_maker(list_film,"film")
    return res

def get_film_with_director_age(age_input:str)->Res:
    '''all film where the director is at least age years old'''
    age=clean_input(age_input)
    age=(re.search(r'\d+',age))#grabs the number
    try:
        if not age:
            return f"the input:\"{age_input}\" is not a number"
        age=int(age.group())
    except(ValueError):
        return f"the input:\"{age_input}\" is not a number"
    
    list_film=execute_query("SELECT titolo FROM movies CROSS JOIN directors ON movies.director=directors.director WHERE age>=%d" %age)
    if list_film==None:
        return f"error in finding the film made by a director old at least \"{age}\" years"
    res:Res=class_maker(list_film,"film")
    return res

def get_director_with_more_film(num_film:str)->Res:
    '''select all director with more then num_film film'''
    num_clean=clean_input(num_film)
    num=(re.search(r'\d+',num_clean))#grabs the number in the request
    if num:
        num=int(num.group())
        director_list=execute_query("SELECT director FROM movies GROUP BY director HAVING COUNT(director)>%d ;"%num)
        if director_list==None:
            return f"error in finding director with more then {num} film"
    else:
        director_list=execute_query("SELECT director FROM movies GROUP BY director HAVING COUNT(director)>1 ;")
        if director_list==None:
            return f"error in finding the directors with more then a film"
    
    res:Res=class_maker(director_list, "director")
    return res

def get_all_columns(tabella:str)->List[Tuple]:
    '''returns list of all columns in tab'''
    res= execute_query("SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA`='esame' AND `TABLE_NAME`='%s';"%tabella)
    if res==None:
        return f"error in grabbing the columns in the table \"{tabella}\""
    return res

def schema_summary()->List[Schema]:
        '''return the schema of the tables'''
        res:List[Schema]=[]
        tabelle=execute_query("SHOW TABLES")
        for tab in tabelle: 
            name_table=tab[0]
            columns=execute_query("SHOW COLUMNS FROM %s" % name_table)
            for col in columns:
                name_column=col[0]
                agg=Schema(table_name=name_table, table_column=name_column)
                res.append(agg)
        return res
