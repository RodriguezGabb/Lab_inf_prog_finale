from typing import List
from src.backend.mariadb_manager import execute_query
from src.backend.school import Schema

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
