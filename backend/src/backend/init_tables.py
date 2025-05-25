import csv
import os
from add_request import add_from_row

def init_tables():
    #prendo il path del file "data.tsv"
    path_cartella=os.path.join(os.getcwd(), os.path.dirname(__file__))
    path=os.path.join(path_cartella, 'data.tsv')
    #apertura del file e inserimento delle righe nelle varie tabelle di mariadb
    with open(path, "r", encoding="utf8") as data:
        tsv_reader = csv.DictReader(data, delimiter="\t")
        for row in tsv_reader:
            out=add_from_row(row)
            #print(out)#questa print serve solo a vedere se si inizializza in modo corretto le tabelle
if __name__=="__main__":#DEBUG
    init_tables()