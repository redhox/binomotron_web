import random
import mysql.connector as mysqlpy
from datetime import datetime
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
    database='binomotron',
)

#selection de la colone "nom" de la table "eleve"
mycursor = db.cursor()

def nouveau_projet(mycursor):
    print(" nouveau projet")
        
    #information de la table "eleve"
    mycursor.execute("SELECT id_eleve FROM eleve")
    idresult = mycursor.fetchall()
    mycursor.execute("SELECT prenom FROM eleve")
    prenom_result = mycursor.fetchall()
    mycursor.execute("SELECT nom FROM eleve")
    nom_result = mycursor.fetchall()
    mycursor.execute("SELECT mail FROM eleve")
    mail_result = mycursor.fetchall()

    liste_d_eleve=[]


    for i in range(0,len(idresult)):
        for z in prenom_result[i]:#boucle des mail
            prenom=""
            for ligne_prenom in z:
                for element in ligne_prenom:
                    prenom=prenom+element
        for z in nom_result[i]:#boucle des mail
            nom=""
            for ligne_nom in z:
                for element in ligne_nom:
                    nom=nom+element
                
        for z in mail_result[i]:#boucle des mail
            mail=""
            for ligne_mail in z:
                for element in ligne_mail:
                    mail=mail+element
                
        listinfo=[i,prenom,nom,mail]
        liste_d_eleve.append(listinfo)



#####################################################################
#                           #INTERACTION PROJET                     #
#####################################################################

    date_de_debut=""
    date_de_fin=""
    nom_projet =input("nom du projet:"or"projet test")


    while True:
        try:
            date_saisie = input('Entrez la  date de debut du projet(JJ/MM/AAAA): ')
            if date_saisie == "":
                date_saisie = "12/12/1212"
            date_objet = datetime.strptime(date_saisie, '%d/%m/%Y')
            date_formatee_debut = date_objet.strftime('%Y-%m-%d')
        except ValueError:
            print("Invalid date")
        else:
            break

    del date_objet

    while True:
        try:
            date_saisie = input('Entrez la  date de fin du projet(JJ/MM/AAAA): ')
            if date_saisie == "":
                date_saisie = "12/12/1212"
            date_objet = datetime.strptime(date_saisie, '%d/%m/%Y')
            date_formatee_fin = date_objet.strftime('%Y-%m-%d')
        except ValueError:
            print("Invalid date")
        else:
            break

    requeteprojet = '''INSERT INTO Projet (id_projet,libelle,date_debut,date_fin) VALUES (%s,%s,%s,%s)'''

    valeursdatedebut = (date_formatee_debut)
    valeursdatefin= (date_formatee_fin)



    mycursor.execute('''SELECT id_projet FROM Projet ORDER BY id_projet DESC LIMIT 1''')
    id_projet= mycursor.fetchall()
    print(id_projet,"idprojet")
    if id_projet == []:
        id_projet_tlup = 1
    else:
        for z in id_projet:
                id_projet_tlup=""
                for ligne_projet in z:
                    print(" ligne ",ligne_projet," z ",z)
                    id_projet_tlup=ligne_projet+1
                print(id_projet_tlup,"id_projet_tlup")

# Validation des changements
#db.commit()
    print(id_projet_tlup,"id_projet_tlup2")
#####################################################################
#                       # LISTE ALEATOIRE                           #
#####################################################################

    print("\n\n")# passage de ligne pour la lisibilité dans le terminal
    liste_R =[] #liste qui acceuilra les nom de façon random
    L = len(liste_d_eleve)
    print("nombre d'eleve total",L)

    #################### boucle de creation d'une liste random
    for i in range(0,L):
        R = random.randrange(0, L-i)
        liste_R.append(liste_d_eleve[R])
        del(liste_d_eleve[R])

#####################################################################
#                  #      GROUPEMENT DES ELEVE                      #
#####################################################################
#recuperation de la derniere id de la table Groupes
    requete = '''SELECT id_groupe FROM Groupes ORDER BY id_groupe DESC LIMIT 1'''
    mycursor.execute(requete)
    derniere_ligne = mycursor.fetchone()
    print("nombre de bdd existante ",derniere_ligne)
    if derniere_ligne == None:
        nombre_de_groupe_bdd = -1
    else:
        for element in derniere_ligne:
            nombre_de_groupe_bdd=element
    N =int(input("nombre de d'eleve par groupe?(2):") or"2")
    nombre_de_groupe = int(L//N)
    print("nombre de group",nombre_de_groupe_bdd,"\n")
    suplement = L%N #modulo du nombre d'eleve par groupe 
    ngroupe = 0 #nombre de groupe pour l'afichage
    #incrementation des nombre_de_groupe dans la bdd
    for i in range(1,nombre_de_groupe+1):
        requete = '''INSERT INTO Groupes (libelle) VALUES (%s)'''
        valeurs = (i,)
        mycursor.execute("SET FOREIGN_KEY_CHECKS=0;")
        mycursor.execute(requete, valeurs)
        requeteprojetgroupe = "INSERT INTO projet_groupe ( id_projet,id_groupe) VALUES (%s,%s)"
        mycursor.execute(requeteprojetgroupe,( id_projet_tlup,nombre_de_groupe_bdd+i))
    db.commit()
    if (suplement!=int):#si il y a un modulo(les groupe seront pas remplie) il lancera la prochaine boucle a 0+modulo
        e=suplement
    else:
        e=0
    nombre_de_groupe_bdd=nombre_de_groupe_bdd+1
    if suplement < nombre_de_groupe :
        for i in range(e,L,N):
            ngroupe=ngroupe+1
            print(ngroupe)#numero de groupe
                    

            for y in range(0,N):
                print(" ",liste_R[i+y][1])
                bdd_eleve=liste_R[i+y][0]                
                bdd_projet=id_projet_tlup
                print(bdd_eleve," ",ngroupe," ",bdd_projet)
                requeteelevegroupe = "INSERT INTO eleve_groupe ( id_eleve,id_groupe) VALUES (%s,%s)"
                mycursor.execute(requeteelevegroupe,( bdd_eleve,nombre_de_groupe_bdd))

                #mycursor.execute(requeteeleve)

            if suplement >= 1:#rajout des eleve suplementaire
                print(" ",liste_R[suplement][0])
                bdd_eleve = liste_R[suplement-1][0]          
                mycursor.execute(requeteelevegroupe,( bdd_eleve,nombre_de_groupe_bdd))
                
                suplement = suplement - 1
            nombre_de_groupe_bdd=nombre_de_groupe_bdd+1
            print("\n")

    else:
        ngroupe=ngroupe+1
        print("groupe_",ngroupe)
        
        bdd_projet=id_projet_tlup
        nombre_de_groupe_bdd=nombre_de_groupe_bdd+1 
        for i in range(0,suplement):
            print(" ",liste_R[i][0])
            bdd_eleve = liste_R[i][0]
            #requeteeleve = "INSERT INTO App_Groupe ( id_eleve,id_groupe,id_projet) VALUES (%s,%s,%s)"
            #mycursor.execute(requeteeleve,( bdd_eleve,bdd_group,bdd_projet))
                            
            mycursor.execute(requeteelevegroupe,( bdd_eleve,nombre_de_groupe_bdd))

        print("\n")
        
        for i in range(e,L,N): 
            ngroupe=ngroupe
            print("groupe_",ngroupe)
            
            for y in range(0,N):
                print(" ",liste_R[i+y][0])
                bdd_eleve=liste_R[i+y][0]
                mycursor.execute(requeteelevegroupe,( bdd_eleve,nombre_de_groupe_bdd))
            nombre_de_groupe_bdd=nombre_de_groupe_bdd+1

            print("\n")
    print(id_projet_tlup,"idprojettlup")
    mycursor.execute(requeteprojet, (id_projet_tlup,nom_projet, valeursdatedebut, valeursdatefin))


def aficher_projet(mycursor,suite_logique):
    print("aficher les Projets")
    
    requete = '''SELECT id_projet FROM Projet ORDER BY id_projet DESC LIMIT 1'''
    mycursor.execute(requete)
    derniere_ligne = mycursor.fetchone()
    if derniere_ligne==None:
        print("pas de projet!")
    else:
        print(" dernier projet",derniere_ligne)

        mycursor.execute("SELECT * FROM projet_groupe")
        id_projet_groupe = mycursor.fetchall()
        mycursor.execute("SELECT * FROM eleve_groupe")
        id_eleve_groupe = mycursor.fetchall()
        mycursor.execute("SELECT * FROM eleve")
        eleve = mycursor.fetchall()

        if suite_logique!=True:
            projet=int(input("selectioné le projet(par defaut le dernier):")or id_projet_groupe[-1][0])
        else:
            projet=id_projet_groupe[-1][0]
        print("\n Projet n: ",projet,"\n")

        liste_des_groupes=[]

        i=1

        for id_projet,id_groupe in id_projet_groupe:

            if id_projet == projet:
                print("groupe",i)
                if i == 1:
                    premier_groupe=id_groupe
                i=i+1
                
                for id_eleve,element in id_eleve_groupe:
                    if element == id_groupe:
                        print("       :",eleve[id_eleve][1])
        demande=True
        while demande==True:
            info=input("\nvoir un groupe de plus pres ? :")
            if info == "":
                demande=False
            else:
                info = int(info)
                info=info-1
                
                for id_projet,id_groupe in id_projet_groupe:
                    if id_projet == projet and id_groupe == premier_groupe+info:
                        print("\n groupe",info+1)
                        i=i+1
                        for id_eleve,element in id_eleve_groupe:
                            if element == id_groupe:
                                print("\n")
                                for y in range (len(eleve[id_eleve])):
                                    if y != 0:
                                        
                                        print(eleve[id_eleve][y])

cursor = db.cursor()
cursor.execute('SELECT id_projet FROM Projet ORDER BY id_projet DESC LIMIT 1')
id_groupe = cursor.fetchall()
# Step 7: Convert the retrieved rows into a DataFrame using `pd.DataFrame`
df_groupe = pd.DataFrame(id_groupe)
mycursor.execute("SELECT * FROM Projet")
df_projet = pd.DataFrame(cursor.fetchall())
mycursor.execute("SELECT * FROM projet_groupe")
df_projet_groupe = pd.DataFrame(cursor.fetchall())
mycursor.execute("SELECT * FROM eleve_groupe")
df_eleve_groupe = pd.DataFrame(cursor.fetchall())
mycursor.execute("SELECT * FROM eleve")
df_eleve = pd.DataFrame(cursor.fetchall())

id_dernier_projet= value = df_projet.iloc[-1, 0]
print('dernierprojet= ',id_dernier_projet,", nom= ",df_projet.iloc[-1, 1])
st.title(f"binomotron: {df_projet.iloc[-1, 1]}")
filtered_df_groupe = df_projet_groupe[df_projet_groupe[0] == df_projet.iloc[-1, 0]]
print(filtered_df_groupe[1].values)
i=1
#merged_df = pd.merge(df_eleve_groupe, df_eleve, left_on=0, right_on=0, how='left')
#print(merged_df)
for element in (filtered_df_groupe[1].values):
    st.title(f"Groupe: {i}")
    i=i+1
    print('i=',i)
    
    filtered_df_eleve = df_eleve_groupe[df_eleve_groupe[1] == element]
    print('id eleve',filtered_df_eleve)
    
    merged_df = pd.merge(filtered_df_eleve, df_eleve, left_on=0, right_on=0, how='left')
    print(merged_df)
    df_test=pd.DataFrame(merged_df)
    st.dataframe(df_test)
    

db.commit()
mycursor.execute("SET FOREIGN_KEY_CHECKS=0;")
