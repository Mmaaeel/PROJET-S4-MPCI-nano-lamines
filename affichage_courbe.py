import matplotlib.pyplot as plt


def plot_Piezo_Time(exp):
    plt.figure(figsize=(6, 4))
    plt.title("Piezo_X en fonction du temps")
    plt.plot(exp["Time"], exp["Piezo X"])

    plt.xlabel("Time")
    plt.ylabel("Piezo X")

    plt.show()


def plot_ForceA_Time(exp):
    plt.figure(figsize=(6, 4))
    plt.title("Force A en fonction du temps")

    plt.xlabel("Temps")
    plt.ylabel("Force A")

    plt.plot(exp["Time"], exp["Force A"])

    plt.show()


def plot_ForceA_Piezo(exp):
    plt.figure(figsize=(6, 4))
    plt.title("Force A en fonction du piezo")

    plt.xlabel("Piezo X")
    plt.ylabel("Force A")

    plt.plot(exp["Piezo X"], exp["Force A"])

    plt.show()


def mise_a_zero(dic, grandeur):
    # ramène à la meme valeur initiale toutes les expériences initiales
    # "grandeur" correspond à la liste du dictionnaire qui est modifié (ex: Temps)
    for num_exp in range(1, len(dic)+1):
        begining = dic[f"exp_{num_exp}"][grandeur][0]
        L = dic[f"exp_{num_exp}"][grandeur]
        for j in range(len(L)):
            L[j] = L[j]-begining
    return dic


def plot_all_expériences(dic_exp, nom_liste_x, nom_liste_y):

    new_dic = mise_a_zero(dic_exp, nom_liste_x)
    for i in range(1, len(dic_exp)+1):
        plt.plot(new_dic[f"exp_{i}"][nom_liste_x],
                 new_dic[f"exp_{i}"][nom_liste_y], label=f"expérience {i}")

    # plt.title(f"{nom_liste_y} en fonction du {nom_liste_x}")
    plt.xlabel(nom_liste_x)
    plt.ylabel(nom_liste_y)

    plt.grid()

    plt.legend()

    plt.show()
