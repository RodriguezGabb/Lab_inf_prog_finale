from typing import List, Tuple
from pydantic import BaseModel

class AddPayload(BaseModel):
    '''this is the payload from the frontend for the add post request'''
    data_line:str
class AddValidation(BaseModel):
    '''this is the validation for the frontend for the add post request'''
    status:str

class SearchPayload(BaseModel):
    '''this is the payload from the frontend for the search post request'''
    question: str 
    model: str = "gemma3:1b-it-qat"

class ResultProprieties(BaseModel):
    '''those are the proprieties in ResultMicro'''
    property_name:str
    property_value:str
class ResultMicro(BaseModel):
    '''those are the result in ResultMacro '''
    item_type:str
    properties:List[ResultProprieties]
class ResultMacro(BaseModel):
    '''conatains ResultMicro'''
    sql:str
    sql_validation:str
    results:List[ResultMicro]=None

class SqlSearchPayload(BaseModel):
    '''this is the payload from the frontend for the sql_search post request'''
    sql_query:str

class ResultSqlSearch(BaseModel):
    '''this is the result for the sql_search post request'''
    sql_validation:str
    results:List[ResultMicro] = None

class Schema(BaseModel):
    table_name:str
    table_column:str


#builders

def result_macro_builder(sql_input:str,vali:str,MicroList:list[ResultMicro])->ResultMacro:
    return ResultMacro(sql=sql_input, sql_validation=vali, results=MicroList)


def result_micro_builder(sql_output:List[Tuple[str]], type:str)->list[ResultMicro]:
    '''makes the right data type for json from query'''
    result:List[ResultMicro]=[] 
    if sql_output:
        for item in sql_output:
            proprieties_list:List[ResultProprieties]=[]
            proprieties:ResultProprieties=ResultProprieties(property_name="name", property_value=item[0])
            proprieties_list.append(proprieties)
            result.append(ResultMicro(item_type=type,properties=proprieties_list))
        
    return result

def result_builder(sql_output:List[Tuple[str]],request_type:str,sql:str,vali:str)->ResultMacro:
    '''uses  result_micro_builder and result_macro_builder to make the element in only one call'''
    micro=result_micro_builder(sql_output,request_type)
    return result_macro_builder(sql,vali,micro)