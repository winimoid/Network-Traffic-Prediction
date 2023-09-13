import matplotlib.pyplot as plt
from keras.models import load_model

from fr_utils.utils import *


look_back, look_ahead, timestep = list(map(int, sys.argv[1:]))

# Charge le modèle sauvegardé
modele_charge = load_model('/home/winimoid/Documents/Projets/Prediction/model/Network-Model.h5')

# Utilise le modèle pour faire des prédictions ou effectuer d'autres tâches
# Par exemple :
# predictions = modele_charge.predict(donnees)

series = read_data(path="/home/winimoid/Documents/Projets/Prediction/data/custom_fdata_Timestep_%d" % timestep)
times = range(len(series))
# plot_series(times, series, ylabel="Packets / minute", path="brute_data.png")

# %%
# del_percentage = delete_percentage[timestep]
# times, series = times[:-del_percentage], series[:-del_percentage]
# plot_series(times, series, ylabel="Packets / minute", path="splitted_data.png")

# %%

series_mean, series_std = series.mean(), series.std()
series = preprocessing.scale(series).reshape(len(series), 1)

test_x, test_y = create_datasets(series, look_back, look_ahead)

# reshape the data to match Keras LSTM gate input [samples, time steps, features]

test_x = np.reshape(test_x, (test_x.shape[0], test_x.shape[1], 1))
test_y = np.reshape(test_y, (test_y.shape[0], test_y.shape[1], 1))

# Predictions du modèle
predictions = modele_charge.predict(test_x)


# Affichage
# Supposons que 'valeurs_reelles' contient les vraies valeurs cibles
# et 'predictions' contient les prédictions de ton modèle

# Crée un graphique de dispersion des valeurs réelles par rapport aux prédictions
#plt.figure(figsize=(8, 8))
# plt.scatter(valeurs_reelles, predictions, s=50, alpha=0.5)  # s est la taille des points, alpha est la transparence
# plt.scatter(predictions, predictions, s=50, alpha=0.5)

predictions_x = range(len(predictions[1]))
print(series.shape)
print(predictions.shape)
print(predictions_x)

#plt.plot(predictions_x, predictions[1])

# Ajoute des labels aux axes et un titre
#plt.xlabel('Valeurs Réelles')
#plt.ylabel('Prédictions')
#plt.title('Graphique de Dispersion des Prédictions')

# Affiche le graphique
#plt.show()





# Nombre d'échantillons
num_samples = predictions.shape[0]

# Créez un graphique
plt.figure(figsize=(8, 4))

total = []
# Affichez les courbes des échantillons bout à bout
for i in range(num_samples):
    for j in range(predictions[i].shape[0]):
        total.append(predictions[i][j])
print(total)
#exit(0)

plt.plot(total, label=f'Échantillon tot', linestyle='-')

plt.xlabel('Pas de Temps')
plt.ylabel('Valeur Prédite')
plt.title('Prédictions pour Tous les Échantillons (Bout à Bout)')
plt.legend()
plt.grid(True)

plt.show()  # Affichez le graphique avec les courbes des échantillons bout à bout
