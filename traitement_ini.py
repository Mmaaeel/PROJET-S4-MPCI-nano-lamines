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


def remplir_liste(reader, ligne0, ligne_fin, index, phase, displacement, time,
                  Pos_X, Pos_Y, Pos_Z, Rot_A, Rot_B, Piezo_X, Force_A,
                  Force_B, Gripper, Voltage_A, Voltage_B, Temperature,
                  Sample_Displace):
    current_ligne = 0
    for row in reader:
        current_ligne += 1
        if ligne0 < current_ligne < ligne_fin-2:
            index.append(float(row[1]))
            phase.append(float(row[2]))
            displacement.append(float(row[3]))
            time.append(float(row[4]))
            Pos_X.append(float(row[5]))
            Pos_Y.append(float(row[6]))
            Pos_Z.append(float(row[7]))
            Rot_A.append(float(row[8]))
            Rot_B.append(float(row[9]))
            Piezo_X.append(float(row[10]))
            Force_A.append(float(row[11]))
            Force_B.append(row[12])
            Gripper.append(float(row[13]))
            Voltage_A.append(float(row[14]))
            Voltage_B.append(float(row[15]))
            Temperature.append(float(row[16]))
            Sample_Displace.append(float(row[17]))


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
        with open(fichier) as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='|')
            compteur_exp += 1
            remplir_liste(reader,
                          lignes_début_exp[compteur_exp-1],
                          lignes_fin_exp[compteur_exp-1],
                          dic_exp[f"exp_{c_exp}"]["Index"],
                          dic_exp[f"exp_{c_exp}"]["Phase"],
                          dic_exp[f"exp_{c_exp}"]["Displacement"],
                          dic_exp[f"exp_{c_exp}"]["Time"],
                          dic_exp[f"exp_{c_exp}"]["Pos X"],
                          dic_exp[f"exp_{c_exp}"]["Pos Y"],
                          dic_exp[f"exp_{c_exp}"]["Pos Z"],
                          dic_exp[f"exp_{c_exp}"]["Rot A"],
                          dic_exp[f"exp_{c_exp}"]["Rot B"],
                          dic_exp[f"exp_{c_exp}"]["Piezo X"],
                          dic_exp[f"exp_{c_exp}"]["Force A"],
                          dic_exp[f"exp_{c_exp}"]["Force B"],
                          dic_exp[f"exp_{c_exp}"]["Gripper"],
                          dic_exp[f"exp_{c_exp}"]["Voltage A"],
                          dic_exp[f"exp_{c_exp}"]["Voltage B"],
                          dic_exp[f"exp_{c_exp}"]["Temperature"],
                          dic_exp[f"exp_{c_exp}"]["Sample Displace"])
        return dic_exp

