import random
import mysql.connector as mysqlpy
import streamlit as st
import pandas as pd
#####################################################################
print("BASE DE DONNÉE ")#     BASE DE DONNÉE                        #
#####################################################################
#apelle de la base de donner mysql "binomotron"
db=mysqlpy.connect(
    host='127.0.0.1',
    port='3306',
    user='root',
    passwd='example',
    database='binomotron_save',
)

#selection de la colone "nom" de la table "eleve"
cursor = db.cursor()
cursor.execute("SELECT * FROM eleve")
test=pd.DataFrame(cursor.fetchall())
 
print(test)
    
