import pandas as pd
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Wczytanie danych z pliku CSV
df = pd.read_csv('Data/przykladowe_dane_potraw.csv')

# Definicja zmiennych rozmytych
smak = ctrl.Antecedent(np.arange(0, 11, 1), 'smak')
pikantnosc = ctrl.Antecedent(np.arange(0, 11, 1), 'pikantnosc')
konsystencja = ctrl.Antecedent(np.arange(0, 11, 1), 'konsystencja')
slodycz = ctrl.Antecedent(np.arange(0, 11, 1), 'slodycz')
przydatnosc = ctrl.Consequent(np.arange(0, 11, 1), 'przydatnosc')

# Definicja funkcji przynależności
smak.automf(5)
pikantnosc.automf(3)
konsystencja.automf(3)
slodycz.automf(3)

# Funkcje przynależności dla przydatności
przydatnosc['niskie'] = fuzz.trimf(przydatnosc.universe, [0, 0, 5])
przydatnosc['umiarkowane'] = fuzz.trimf(przydatnosc.universe, [4, 5, 6])
przydatnosc['wysokie'] = fuzz.trimf(przydatnosc.universe, [5, 10, 10])

# Definicja reguł
regula1 = ctrl.Rule(smak['good'] & pikantnosc['average'], przydatnosc['wysokie'])
regula2 = ctrl.Rule(smak['average'] & pikantnosc['poor'], przydatnosc['umiarkowane'])
regula3 = ctrl.Rule(konsystencja['poor'] | slodycz['average'], przydatnosc['niskie'])

# Tworzenie systemu kontrolnego
przydatnosc_system = ctrl.ControlSystem([regula1, regula2, regula3])

# Tworzenie symulatora systemu
przydatnosc_simulator = ctrl.ControlSystemSimulation(przydatnosc_system)

# Ocena przydatności dla każdej potrawy w zbiorze danych
wyniki = []
for i in range(len(df)):
    przydatnosc_simulator.input['smak'] = df.loc[i, 'Smak']
    przydatnosc_simulator.input['pikantnosc'] = df.loc[i, 'Pikantnosc']
    przydatnosc_simulator.input['konsystencja'] = df.loc[i, 'Konsystencja']
    przydatnosc_simulator.input['slodycz'] = df.loc[i, 'Slodycz']

    przydatnosc_simulator.compute()
    wynik = przydatnosc_simulator.output['przydatnosc']
    wyniki.append((df.loc[i, 'Potrawa'], wynik))

# Wyświetlenie wyników
for potrawa, ocena in wyniki:
    print(f"Potrawa: {potrawa}, Ocena przydatności: {ocena}")