import csv
import os
from src.backend.add_request import add_from_row

def init_tables():
    '''take the data from the data.tsv file and preapare it to be insert in the database'''
    #this finds the data.tsv path
    path_cartella=os.path.join(os.getcwd(), os.path.dirname(__file__))
    path=os.path.join(path_cartella, 'data.tsv')
    #open file and insert data into tables
    with open(path, "r", encoding="utf8") as data:
        tsv_reader = csv.DictReader(data, delimiter="\t")
        for row in tsv_reader:
            add_from_row(row)

