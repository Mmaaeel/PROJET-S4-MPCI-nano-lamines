import numpy as np
import detection_phase as dp


def regression_linéaire(X, Y):
    coef = np.polyfit(X, Y, 1)
    poly1d_fn = np.poly1d(coef)
    regression = poly1d_fn(X)
    a = (regression[1]-regression[0])/(X[1]-X[0])
    b = regression[0] - a*X[0]
    return X, regression, a, b


def valeur_réelle_piezo(exp, déformation):
    # enlève la déformation de la machine au piezo
    for i in range(len(exp["Piezo X"])):
        exp["Piezo X"][i] -= déformation


def get_x_contact(exp):
    # donne la position du contact entre la pointe et le pilier
    for index in range(len(exp["Phase"])):
        if exp["Phase"][index] == 2:
            return index
    return len(exp["Phase"])-1


def calcul_déformation(exp, hauteur):
    # conversion piezo en déformation
    # retourne la défrmation en pourcentage
    piezo_contact = exp["Piezo X"][get_x_contact(exp)-1]
    déformation = []
    for i in exp["Piezo X"]:
        val = ((i - piezo_contact)*10**(-6)) / hauteur
        if val > 0:
            déformation.append(val*100)
        else:
            déformation.append(0)
    return déformation


def calcul_contrainte(exp, surface):
    # conversion de la force en contrainte
    contrainte = []
    for elt in exp["Force A"]:
        contrainte.append((elt*10**(-6))/surface)
    return contrainte


def calcul_hauteur_largeur(h, longueur, a):
    H = h / np.sin(a)
    L = longueur / np.cos(a)
    return H, L


def calcul_module_young(current_exp, contrainte, déformation):
    déformation_réelle = []
    for i in range(len(déformation)):
        déformation_réelle.append(déformation[i]/100)

    x_ini = 0
    for index in range(len(current_exp["Phase"])):
        if current_exp["Phase"][index] == 4 and x_ini == 0:
            x_ini = index

    x_deb_RegLin = x_ini
    x_fin_RegLin = 0
    for i in range(len(contrainte[x_ini:])):
        if contrainte[x_ini + i] > 0.7*contrainte[x_ini]:
            x_fin_RegLin = x_ini + i

    reg = regression_linéaire(
        déformation_réelle[x_deb_RegLin:x_fin_RegLin],
        contrainte[x_deb_RegLin:x_fin_RegLin])
    
    X_reg = reg[0]
    Y_reg = reg[1]
    module_youg = reg[2]
    for i in range(len(X_reg)):
        X_reg[i] = X_reg[i]*100
        
    return X_reg, Y_reg, module_youg, x_deb_RegLin, x_fin_RegLin


def calcul_all_module_young(dic_exp, surface_pilier, hauteur_pilier):
    somme_module_youg = 0
    dic_module_young = {}
    for i in range(len(dic_exp)):
        dp.determine_phase(dic_exp[f"exp_{i+1}"])
        contrainte = calcul_contrainte(
            dic_exp[f"exp_{i+1}"], surface_pilier)
        déformation = calcul_déformation(
            dic_exp[f"exp_{i+1}"], hauteur_pilier)
        res = calcul_module_young(
            dic_exp[f"exp_{i+1}"], contrainte, déformation)
        module_young = res[2]/10**9
        somme_module_youg += module_young
        dic_module_young[f"exp{i+1}"] = module_young
    print("moyenne module young = ", somme_module_youg/len(dic_exp))
    print("valeurs module young :", dic_module_young)
    return dic_module_young
