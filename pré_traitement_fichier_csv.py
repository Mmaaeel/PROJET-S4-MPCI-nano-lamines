import csv


def get_lignes_début_exp(reader):
    compteur = 0
    test_indice = 0
    verbose = True
    ligne = 0
    liste_début = []
    for char in reader:
        ligne += 1
        if char != []:
            if '//' in char[0] and verbose:
                verbose = False
                compteur += 1
            if '//' in char[0] and not verbose:
                compteur += 1
                verbose = False
            if compteur == 5:
                test_indice += 1
                compteur = 0
                liste_début.append(ligne+2)
    return liste_début


def get_lignes_fin_exp(liste_début, reader):
    liste_f = []
    nbr_ligne = 0
    for ligne in reader:
        nbr_ligne += 1
    for element in liste_début[1:]:
        liste_f.append(element - 3)
    liste_f.append(nbr_ligne)
    return liste_f


def create_listes(nbr_exp, liste_col):
    dic_exp = {f"exp_{i+1}": {nom_col: [] for nom_col in liste_col}
               for i in range(nbr_exp)}
    return dic_exp


def remplir_liste(reader, ligne0, ligne_fin, dic_exp, c_exp, colonne):
    current_ligne = 0
    for row in reader:
        current_ligne += 1
        if ligne0 < current_ligne < ligne_fin-2:
            for i in range(len(colonne)):
                dic_exp[f"exp_{c_exp}"][colonne[i]].append(float(row[i+1]))


def get_nom_colonne(reader):
    liste_nom = []
    compteur_ligne = 0
    for ligne in reader:
        compteur_ligne += 1
        if compteur_ligne == 3:
            for char in ligne:
                liste_nom.append(char)
    return liste_nom[1:]


def csv_to_list(fichier):
    # entrée : chemin d'accès d'un fichier csv
    # sortie : dictionnaire contenant les données du fichier csv classer par
    # expérience et par colonne
    compteur_exp = 0

    with open(fichier) as csvfile:
        reader2 = csv.reader(csvfile, delimiter=';', quotechar='|')
        lignes_début_exp = get_lignes_début_exp(reader2)
    with open(fichier) as csvfile:
        reader3 = csv.reader(csvfile, delimiter=';', quotechar='|')
        lignes_fin_exp = get_lignes_fin_exp(lignes_début_exp, reader3)
    with open(fichier) as csvfile:
        reader4 = csv.reader(csvfile, delimiter=';', quotechar='|')
        liste_colonne = get_nom_colonne(reader4)
        nbr_exp = len(lignes_début_exp)
        dic_exp = create_listes(nbr_exp, liste_colonne)
        for c_exp in range(1, nbr_exp+1):
            compteur_exp += 1
            with open(fichier) as csvfile:
                reader = csv.reader(csvfile, delimiter=';', quotechar='|')
                remplir_liste(reader,
                              lignes_début_exp[compteur_exp-1],
                              lignes_fin_exp[compteur_exp-1], dic_exp, c_exp,
                              liste_colonne)
        return dic_exp
