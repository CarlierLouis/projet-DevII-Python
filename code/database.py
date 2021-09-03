import mysql
from mysql import connector


cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='infos')
cursor = cnx.cursor()


def creation_table_Profils():
    """
    Fonction de création de la table des profils dans la db

    PRE:-
    POST:-
    """
    cursor.execute("CREATE TABLE Profils (id int primary key not null auto_increment,"
                   "pseudo varchar(255), xp int(255), argent int(255), objet1 int(255), objet2 int(255),"
                   " objet3 int(255)")


def remplir_table_Profils(pseudo, xp, argent):
    """
    Fonction pour ajouter de nouveau joueur dans la db

    PRE:
        type(pseudo) == str
        type(xp) == int
        type(argent) == int
    POST:-
    """
    sql = "INSERT INTO Profils (pseudo, xp, argent) VALUES (%s, %s, %s)"
    value = (pseudo, xp, argent)
    cursor.execute(sql, value)
    cnx.commit()


def recuperer_infos_joueurs():
    """
    Fonction récupérant les données des joueurs présentes dans la db

    PRE:-
    POST: return list
    """
    infos_joueurs = []
    cursor.execute("SELECT pseudo, xp, argent FROM Profils")
    for i in cursor.fetchall():
        infos_joueurs.append(i)
    # Transformtion du tuple en liste
    liste = [x for elem in infos_joueurs for x in elem]
    j = 0
    liste2 = []
    # Transformation de la liste simple en liste avec sous-listes
    while j < len(liste) - 2:
        liste3 = [liste[j], liste[j + 1], liste[j + 2]]
        liste2.append(liste3)
        j += 3
    # Tri décroissant en fonction de l'xp du joueur
    liste_finale = sorted(liste2, key=lambda a: a[1], reverse=False)
    return liste_finale


def recuperer_pseudos_joueurs():
    """
    Fonction de récupération des pseudos des joueurs présents dans la db

    PRE:-
    POST: return list
    """
    infos_joueurs = []
    cursor.execute("SELECT pseudo, xp, argent FROM Profils")
    for i in cursor.fetchall():
        infos_joueurs.append(i)
    # Transformtion du tuple en liste
    liste = [x for elem in infos_joueurs for x in elem]
    j = 0
    liste2 = []
    pseudos = []
    # Transformation de la liste simple en liste avec sous-listes
    while j < len(liste) - 2:
        liste3 = [liste[j], liste[j + 1], liste[j + 2]]
        liste2.append(liste3)
        j += 3
    for i in liste2:
        pseudos.append(i[0])
    return pseudos


def ajout_xp(xp, argent, pseudo):
    """
    Fonction d'ajout d'xp et d'argent dans la db en fonction du pseudo

    PRE:
        type(pseudo) == str
        type(xp) == int
        type(argent) == int
    POST:-
    """
    sql = "UPDATE Profils SET xp = xp + %s, argent = argent + %s WHERE pseudo = %s"
    value = (xp, argent, pseudo)
    cursor.execute(sql, value)
    cnx.commit()


def payement(argent, pseudo):
    """
    Fonction de retrait d'argent dans la db après l'achat d'un objet dans la boutique en fonction du pseudo

    PRE:
        type(pseudo) == str
        type(argent) == int
    POST:-
    """
    sql = "UPDATE Profils Set argent = argent - %s WHERE pseudo = %s"
    value = (argent, pseudo)
    cursor.execute(sql, value)
    cnx.commit()


def ajout_objet1(objet1, pseudo):
    """
        Fonction d'ajout de l'objet1 dans la db en fonction du pseudo (1 si le joueur posséde l'objet)

        PRE:
            type(pseudo) == str
            type(objet1) == int
        POST:-
        """
    sql = "UPDATE Profils Set objet1 = %s WHERE pseudo = %s"
    value = (objet1, pseudo)
    cursor.execute(sql, value)
    cnx.commit()


def ajout_objet2(objet2, pseudo):
    """
        Fonction d'ajout de l'objet2 dans la db en fonction du pseudo (1 si le joueur posséde l'objet)

        PRE:
            type(pseudo) == str
            type(objet2) == int
        POST:-
        """
    sql = "UPDATE Profils Set objet2 = %s WHERE pseudo = %s"
    value = (objet2, pseudo)
    cursor.execute(sql, value)
    cnx.commit()


def ajout_objet3(objet3, pseudo):
    """
        Fonction d'ajout de l'objet2 dans la db en fonction du pseudo (1 si le joueur posséde l'objet)

        PRE:
            type(pseudo) == str
            type(objet3) == int
        POST:-
        """
    sql = "UPDATE Profils Set objet3 = %s WHERE pseudo = %s"
    value = (objet3, pseudo)
    cursor.execute(sql, value)
    cnx.commit()


def info_objet1():
    """
        Fonction de récupération du "status" de l'objet1 pour chaque joueur

        PRE:-
        POST: return list
        """
    infos_objet1 = []
    cursor.execute("SELECT pseudo, objet1 FROM Profils")
    for i in cursor.fetchall():
        infos_objet1.append(i)
    liste = [x for elem in infos_objet1 for x in elem]
    return liste


def info_objet2():
    """
        Fonction de récupération du "status" de l'objet2 pour chaque joueur

        PRE:-
        POST: return list
        """
    infos_objet2 = []
    cursor.execute("SELECT pseudo, objet2 FROM Profils")
    for i in cursor.fetchall():
        infos_objet2.append(i)
    liste = [x for elem in infos_objet2 for x in elem]
    return liste


def info_objet3():
    """
        Fonction de récupération du "status" de l'objet3 pour chaque joueur

        PRE:-
        POST: return list
        """
    infos_objet3 = []
    cursor.execute("SELECT pseudo, objet3 FROM Profils")
    for i in cursor.fetchall():
        infos_objet3.append(i)
    liste = [x for elem in infos_objet3 for x in elem]
    return liste


def supp_objet1(objet1, pseudo):
    """
        Fonction de retrait de l'objet1 dans la db en fonction du pseudo

        PRE:
            type(pseudo) == str
        POST:-
        """
    sql = "UPDATE Profils Set objet1 = %s WHERE pseudo = %s"
    value = (objet1, pseudo)
    cursor.execute(sql, value)
    cnx.commit()


def supp_objet2(objet2, pseudo):
    """
        Fonction de retrait de l'objet2 dans la db en fonction du pseudo

        PRE:
            type(pseudo) == str
        POST:-
        """
    sql = "UPDATE Profils Set objet2 = %s WHERE pseudo = %s"
    value = (objet2, pseudo)
    cursor.execute(sql, value)
    cnx.commit()


def supp_objet3(objet3, pseudo):
    """
        Fonction de retrait de l'objet3 dans la db en fonction du pseudo

        PRE:
            type(pseudo) == str
        POST:-
        """
    sql = "UPDATE Profils Set objet3 = %s WHERE pseudo = %s"
    value = (objet3, pseudo)
    cursor.execute(sql, value)
    cnx.commit()