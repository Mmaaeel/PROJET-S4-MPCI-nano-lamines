import numpy as np
import matplotlib.pyplot as plt


def determine_phase(exp):
    # entrée : dictionnaire d'une expérience
    # sortie : liste contenant les temps et les valeurs de forces par phase
    #         possibilité de modifier le return pour que ca renvoie le temps de début des phases

    value_phase_2 = []
    time_phase_2 = []

    value_phase_3 = []
    time_phase_3 = []

    value_phase_4 = []
    time_phase_4 = []

    in_phase_1 = True  # approche

    max_bruit = 0
    for index_value in range(min(8000, int(len(exp["Force A"])/4))):
        if exp["Force A"][index_value] > max_bruit:
            max_bruit = exp["Force A"][index_value]

    for index_value in range(len(exp["Force A"])):
        current_value = exp["Force A"][index_value]
        phase = exp["Phase"][index_value]

        if current_value > 2*max_bruit and in_phase_1:
            in_phase_1 = False

        if not in_phase_1 and phase < 3:
            value_phase_2.append(current_value)
            time_phase_2.append(exp["Time"][index_value])
            exp["Phase"][index_value] = 2

        if phase == 3:
            value_phase_3.append(current_value)
            time_phase_3.append(exp["Time"][index_value])

        if phase == 4:
            value_phase_4.append(current_value)
            time_phase_4.append(exp["Time"][index_value])

    return value_phase_2, time_phase_2, value_phase_3, time_phase_3, value_phase_4, time_phase_4
