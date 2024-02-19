import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# lire le fichier csv
df = pd.read_csv('9810000202-sanssymbole-mod.csv', delimiter=';', decimal=',', thousands=' ',
                 usecols=(0, 1, 2, 3, 11))

# On renomme pour manipuler
df.columns = ['Nom', 'Type', 'Pop21', 'Pop16', 'Km2']

# Les espaces delimites les milliers, on les enleve
for col in ['Pop21', 'Pop16']:
    df[col] = df[col].apply(lambda x: x.replace(' ', ''))

# Les ".."  correspondent a des valeurs non fournies, on les remplace par des NaN
df = df.replace('..', np.nan)

# On convertit finalement en float
for col in ['Pop21', 'Pop16']:
    df[col] = df[col].astype(float)

# On sauvegarde pour ne plus souffrir :D
df.to_csv('Census_2016_2021.csv')

# Dataframe regroupant toutes les municipalités
df_municipalites = df[df['Type'] == 'MÉ']

# Obtenir le nombre de municipalités
nombre_municipalite = len(df_municipalites['Type'])
print(f'Le nombre de municipalités est:  {nombre_municipalite}. \n')

# Calcul de la population moyenne
population_moyenne_2016 = df_municipalites['Pop16'].mean()
print(f'La population moyenne des municipalité en 2016 est: {int(population_moyenne_2016)} personnes. \n')

population_moyenne_2021 = df_municipalites['Pop21'].mean()
print(f'La population moyenne des municipalité en 2021 est: {int(population_moyenne_2021)} personnes. \n')

# Calcul du pourcentage du taux d'accroissement entre 2016 et 2021
df_municipalites['Accroissement'] = ((df_municipalites['Pop21'] - df_municipalites['Pop16'])
                                     / df_municipalites['Pop16'] * 100)

# Tracé du taux d'accroissement en fonction de la population de 2021
fig = plt.figure(figsize=(20, 5))
plt.rcParams['font.size'] = 14
plt.rcParams['figure.autolayout'] = True  # s'assure que tout rentre dans la figure
plt.rcParams['figure.dpi'] = 100
plt.scatter(df_municipalites['Pop21'], df_municipalites['Accroissement'], label="Taux d'accroissement", color='b', s=8)
plt.xlabel('Population des municipalités en 2021')
plt.ylabel("Taux d'accroissement en %")
plt.legend()
plt.grid()
plt.title("Taux d'accroissement de la population de 2016 à 2021 en fonction de la population en 2021")
plt.savefig('taux_accroissement_2016_2021.png')
plt.savefig('taux_accroissement_2016_2021.pdf')
plt.close()


# Classement des municipalités selon leur municipalité\
def classer_municipalites_population(population):
    if population < 2000:
        return 1
    elif 2000 <= population < 10000:
        return 2
    elif 10000 <= population < 25000:
        return 3
    elif 25000 <= population < 100000:
        return 4
    elif population >= 100000:
        return 5


df_municipalites['Classement'] = df_municipalites['Pop21'].apply(classer_municipalites_population)

# Tracé d'un diagramme du classement des municipalités
nombre_classement = np.array([len(df_municipalites[df_municipalites['Classement'] == 1]),
                              len(df_municipalites[df_municipalites['Classement'] == 2]),
                              len(df_municipalites[df_municipalites['Classement'] == 3]),
                              len(df_municipalites[df_municipalites['Classement'] == 4]),
                              len(df_municipalites[df_municipalites['Classement'] == 5])])

classement = ('inférieure à 2000', 'entre 2000 et 9999', 'entre 10000 et 24999', 'entre 25000 et 99999', '100000 +')

plt.figure(figsize=(20, 5))
plt.rcParams['font.size'] = 14
plt.rcParams['figure.autolayout'] = True  # s'assure que tout rentre dans la figure
plt.rcParams['figure.dpi'] = 100
plt.barh(np.arange(1, 6), nombre_classement, align='center')
ax = plt.gca()
ax.set_yticks(np.arange(1, 6), labels=classement)
ax.set_xlabel('Nombre de municipalités')
ax.set_title('Classement du nombre de municipalité dans les catégories de population')
plt.savefig('classement_municipalites.png')
plt.savefig('classement_municipalites.pdf')
plt.close()
