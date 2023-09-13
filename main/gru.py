import sys, os

import numpy as np
import pandas as pd

sys.path.insert(1, "/home/winimoid/Documents/Projets/Prediction/")
# %%

from fr_utils.utils import *

# %% Hyper Parameters

look_back, look_ahead, neuron1, neuron2, neuron3, timestep = list(map(int, sys.argv[1:]))
validation_split = 0.8  # Percentage of train set from the whole dataset
# look_back = 100          # Number of timesteps that will be fed to the network in order to predict the future timesteps
# look_ahead = 20         # Number of timesteps to be predicted
# nb_epochs = 1000  # Number of iterations in the training phase
nb_epochs = 2

batch_size = 10  # Number of samples per gradient update
# neuron1 = 100
# neuron2 = 100
# neuron3 = 50

# delete_percentage est utilisé pour supprimer un pourcentage spécifique
# de valeurs aberrantes d'un ensemble de données. Les valeurs aberrantes sont des points
# de données qui sont significativement différents du reste des données.
# La suppression des valeurs aberrantes peut contribuer à améliorer la précision de
# l'analyse statistique.
# delete_percentage = {1: 4000, 60: 100}
delete_percentage = {1: 10, 60: 1}
y_preds = []
y_tests = []

# %%
path_result = "/home/winimoid/Documents/Projets/Prediction/results/gru/timestep_%d/lb=%d_la=%d_ne1=%d_ne2=%d_ne=%d/" % (
    timestep, look_back, look_ahead, neuron1, neuron2, neuron3)

if os.path.isdir("/home/winimoid/Documents/Projets/Prediction/results/gru") == 0:
    os.system("mkdir /home/winimoid/Documents/Projets/Prediction/results/gru")
if os.path.isdir("/home/winimoid/Documents/Projets/Prediction/results/gru/timestep_%d" % timestep) == 0:
    os.system("mkdir /home/winimoid/Documents/Projets/Prediction/results/gru/timestep_%d" % timestep)
if os.path.isdir(path_result) == 0:
    os.system("mkdir " + path_result)
else:
    # if len(glob(path_result + '*')) == 2:
    if len(glob(path_result + '*')) > 2:
        exit()
    else:
        os.system("rm " + path_result + "*")

# %%

series = read_data(path="/home/winimoid/Documents/Projets/Prediction/data/custom_fdata_Timestep_%d" % timestep)
times = range(len(series))
# plot_series(times, series, ylabel="Packets / minute", path="brute_data.png")

# %%
del_percentage = delete_percentage[timestep]
times, series = times[:-del_percentage], series[:-del_percentage]
# plot_series(times, series, ylabel="Packets / minute", path="splitted_data.png")

# %%

series_mean, series_std = series.mean(), series.std()
series = preprocessing.scale(series).reshape(len(series), 1)

train, test = train_test_split(series, validation_split)

train_x, train_y = create_datasets(train, look_back, look_ahead)
test_x, test_y = create_datasets(test, look_back, look_ahead)

# reshape the data to match Keras LSTM gate input [samples, time steps, features]
train_x = np.reshape(train_x, (train_x.shape[0], train_x.shape[1], 1))
train_y = np.reshape(train_y, (train_y.shape[0], train_y.shape[1], 1))

test_x = np.reshape(test_x, (test_x.shape[0], test_x.shape[1], 1))
test_y = np.reshape(test_y, (test_y.shape[0], test_y.shape[1], 1))

# %%

model = Sequential()
model.add(GRU(neuron1, input_dim=1))
model.add(RepeatVector(look_ahead))
model.add(GRU(neuron2, return_sequences=True))
model.add(GRU(neuron3, return_sequences=True))
model.add(GRU(neuron1, return_sequences=True))
model.add(GRU(neuron1, return_sequences=True))
model.add(TimeDistributed(Dense(1)))

model.compile(loss="mse", optimizer="rmsprop", metrics=["mape"])
model.summary()
# %%

history = model.fit(
    train_x,
    train_y,
    epochs=nb_epochs,
    batch_size=batch_size,
    callbacks=[EarlyStopping(monitor='val_loss', min_delta=0.0001, patience=3, verbose=2, mode='auto')],
    validation_split=0.1,
    verbose=2
)

# %%

pred_train = model.predict(train_x)
pred_test = model.predict(test_x)

pred_train = reverse_scale(pred_train, series_mean, series_std)
pred_test = reverse_scale(pred_test, series_mean, series_std)
test_y = reverse_scale(test_y, series_mean, series_std)
train_y = reverse_scale(train_y, series_mean, series_std)

errors = []
# for i in range(20):
for i in range(9):
    errors.append(mean_absolute_percentage(test_y[:, i, :], pred_test[:, i, :]))

# plot_4_errors(pred_test, test_y, errors[0], errors[3], errors[7], errors[15], path=path_result+"comparaison.png")

# la ligne ci dessous est custom
# plot_1_error(pred_test, test_y, errors[0], path=path_result+"comparaison.png")

# %%

columns = ["look_back", "look_ahead", "neuron1", "neuron2", "neuron3"] + ["MAPE: %d Step" % i for i in range(1, 21)]
values = [look_back, look_ahead, neuron1, neuron2, neuron3] + errors

dic_results = {column: value for column, value in zip(columns[:len(values)], values)}

# df = pd.DataFrame(columns=columns)
# df = df.append(dic_results, ignore_index=True) -> deprecated ?

# Les 3 lignes ci dessous sont totalement custom
create_columns = pd.DataFrame(columns=columns)
create_values = pd.DataFrame(dic_results, index=[0])
df = pd.concat([create_columns, create_values], ignore_index=True)

df.to_csv(path_result + "metrics_comparison.csv", index=False)

# %%
y_preds = [pred_train, pred_test]
y_tests = [train_y, test_y]

dic = {"pred": y_preds, "real": y_tests, "errors": errors}

path_file = path_result + "values.pickle"
with open(path_file, 'wb') as f:
    pickle.dump(dic, f, pickle.HIGHEST_PROTOCOL)


# Sauvegarde du modèle
if os.path.isdir("/home/winimoid/Documents/Projets/Prediction/model") == 0:
    os.system("mkdir /home/winimoid/Documents/Projets/Prediction/model")

model.save('/home/winimoid/Documents/Projets/Prediction/model/Network-Model.h5')
