# %%
# Import packages
import pandas as pd
import numpy as np
import os
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import cufflinks as cf
cf.go_offline()

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.python.ops.gen_array_ops import size

from keras.layers.advanced_activations import LeakyReLU

from sklearn.metrics import mean_absolute_error as mae
from sklearn.metrics import mean_squared_error as mse
from sklearn.metrics import r2_score


BATH_PATH = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BATH_PATH, "..", "data")

# %%
# Read data
def get_PET_history(floor):
    path = os.path.join(data_path, F"PET_{floor}F_data-20210401_20210831.csv")
    PET_data = pd.read_csv(path)
    PET_data["Time"] = pd.to_datetime(PET_data["Time"])
    PET_data.sort_values(by="Time", inplace=True)
    PET_data.set_index("Time", inplace=True)
    PET_data = PET_data.loc[~PET_data.index.duplicated(keep="first")]
    return PET_data


def get_FCU_history(floor):
    path = os.path.join(data_path, F"FCU_{floor}F_data-20210201_20210831.csv")
    FCU_data = pd.read_csv(path)
    FCU_data["Time"] = pd.to_datetime(FCU_data["Time"])
    FCU_data.sort_values(by="Time", inplace=True)
    FCU_data.set_index("Time", inplace=True)
    FCU_data = FCU_data.loc[~FCU_data.index.duplicated(keep='first')]
    return FCU_data


def get_AHU_history(floor):
    path = os.path.join(data_path, F"AHU_{floor}F_data-20210201_20210831.csv")
    AHU_data = pd.read_csv(path)
    AHU_data["Time"] = pd.to_datetime(AHU_data["Time"])
    AHU_data.sort_values(by="Time", inplace=True)
    AHU_data.set_index("Time", inplace=True)
    AHU_data = AHU_data.loc[~AHU_data.index.duplicated(keep='first')]
    return AHU_data


def get_CO2_history(floor):
    path = os.path.join(data_path, F"CDS_{floor}F_data-20210201_20210831.csv")
    CDS_data = pd.read_csv(path)
    CDS_data["Time"] = pd.to_datetime(CDS_data["Time"])
    CDS_data.sort_values(by="Time", inplace=True)
    CDS_data.set_index("Time", inplace=True)
    if floor == 8:
        CDS_data = CDS_data.drop("CDS_108_8-CO2", axis=1) # deviation in this sensor data 
    CDS_data = CDS_data.loc[~CDS_data.index.duplicated(keep='first')]
    CDS_data["Floor_CO2_mean"] = CDS_data.mean(axis=1)
    return CDS_data.loc[:, ["Floor_CO2_mean"]]


def get_CWB_history():
    path = os.path.join(data_path, "CWB_data-20210201_20210831.csv")
    CWB_data = pd.read_csv(path)
    CWB_data["Time"] = pd.to_datetime(CWB_data["Time"])
    CWB_data.sort_values(by="Time", inplace=True)
    CWB_data.set_index("Time", inplace=True)
    CWB_data = CWB_data.loc[~CWB_data.index.duplicated(keep='first')]
    return CWB_data


def merge_data(floor):
    CWB_data = get_CWB_history()
    FCU_data = get_FCU_history(floor)
    AHU_data = get_AHU_history(floor)
    CDS_data = get_CO2_history(floor)
    PET_data = get_PET_history(floor)
    ALL_data = pd.concat([CWB_data, FCU_data, AHU_data, CDS_data, PET_data], axis=1, join="outer")
    # Drop insignificant or noisy variable 
    ALL_data = ALL_data.drop(["RH", "GloblRad", "PAH-OA_FLOW", "PAH-FAN_RUN_CMD", "PAH-DMP_POS", "PET_Target"], axis=1)
    return ALL_data.dropna()

floor = 8
display(merge_data(floor))
merge_data(floor).iplot()

# %%
# Create timeseries features (here is just the sample not the real structure in the field)
def get_train_feature(target, floor, future_step=1):
    # Preparing features (can also add some features if you'd like to try other models)
    data = merge_data(floor)
    
    # data.insert(loc=0, column="DoY", value=(data.index.dayofyear).values) # seems not significant
    data.insert(loc=1, column="Hour", value=(data.index.hour).values + (pd.Series(data.index).dt.minute).values/60)
    data.insert(loc=2, column="DoW", value=(data.index.dayofweek).values)
    data.insert(loc=3, column="HoW", value=(data["Hour"] + 24 * data.index.dayofweek).values)

    # features set (add lag features for future prediction: the [t-1] situation leads to [t] outcome)
    for col in data.loc[:, ~data.columns.str.contains(target)].columns:
        data.loc[:, F"{col}-lag"] = data.loc[:, col].shift(future_step)
    
    # target can also shift as lag features (but seems not significant)
    # data.loc[:, F"{target}-lag"] = data.loc[:, target].shift(future_step)

    return data.dropna()

# Scale data may get some help
def data_scale(dataset, scale_type="MinMax"):
    if scale_type =="MinMax":
        data_min = dataset.min()
        data_max = dataset.max()
        scaled_df = (dataset - data_min) / (data_max - data_min)
        pars = {"data_min": data_min, "data_max": data_max}
        return scaled_df, pars
    if scale_type =="normalize":
        data_mean = dataset.mean()
        data_std = dataset.std()
        normalized_df = (dataset - data_mean) / data_std
        pars = {"data_mean": data_mean, "data_std": data_std}
        return normalized_df, pars

# Split train, valid and test data
def generator(data, start, end):
    X = data.loc[start:end, ~data.columns.str.contains(target)]
    Y = data.loc[start:end, data.columns.str.contains(target)]
    return X, Y

floor = 8
target = "SP_Target"
future_step = 6 * 1 # timestep is 10 min, 6 timestep for 1 hr lag-feature

# data = get_train_feature(target, floor, future_step) # can also try training data without scaled
data = data_scale(get_train_feature(target, floor, future_step))[0]
pars = data_scale(get_train_feature(target, floor, future_step))[1]

# train data
start = "2021-04-01"
end = "2021-06-30"
_train = generator(data, start, end)
train_x = _train[0]
train_y = _train[1]

# valid data
start = "2021-05-31"
end = "2021-07-31"
_val = generator(data, start, end)
val_x = _val[0]
val_y = _val[1]

# test data
start = "2021-06-30"
end = "2021-08-31"
_test = generator(data, start, end)
test_x = _test[0]
test_y = _test[1]

# all data
start = "2021-04-01"
end = "2021-08-31"
_all = generator(data, start, end)
all_x = _all[0]
all_y = _all[1]

display(all_x)
display(all_y)

# %%
# Model train (the model here is one of the optimized sample)
model_summary = pd.DataFrame()
Epochs = 30
Batch = 6 * 24 * 7

tf.random.set_seed(221)
model = Sequential()
model.add(Dense(units=8, input_dim=train_x.shape[1], activation="relu"))
model.add(Dense(units=16, activation="selu"))
model.add(Dense(units=32, activation=LeakyReLU()))
model.add(Dense(units=16, activation="selu"))
model.add(Dense(units=8, activation="relu"))
model.add(Dense(units=1))

opt = keras.optimizers.Adam()
model.compile(loss="mae", optimizer=opt, metrics=["mse"])
model.fit(train_x, train_y, epochs=Epochs, batch_size=Batch, validation_data=(val_x, val_y))

y_pred = model.predict(test_x)
test_y["pred"] = y_pred[:, 0]
test_y[target] = test_y[target]
test_y["pred"] = test_y["pred"]

fig = go.Figure()
fig.add_trace(go.Scatter(name="real", x=test_y.index, y=test_y[target]))
fig.add_trace(go.Scatter(name="pred", x=test_y.index, y=test_y["pred"]))
fig.show()

test_y = test_y.dropna()

print("r2: ", round(r2_score(test_y[target], test_y["pred"]), 2))
print("MAE: ", round(mae(test_y[target], test_y["pred"]), 2))
print("RMSE: ", round(mse(test_y[target], test_y["pred"]), 2))

model.summary()


# %%
plot_df = test_y * (pars["data_max"][target] - pars["data_min"][target]) + pars["data_min"][target]
plot_df.iplot(title=F"{target}-real vs prediction")

# %%
# this model only have to be precise at the time we need
# for such a special application, here can use schedule rules to optimize predictive strategy
plot_df["pred"] = np.where(np.logical_or(plot_df.index.dayofweek>4, np.logical_or(plot_df.index.hour<7, plot_df.index.hour>21)), 25, plot_df["pred"])
plot_df.iplot(title=F"{target}-real vs prediction")

# the control strategy of HVAC Setpoint temperature assure the indoor thermal comfort
print("r2: ", round(r2_score(plot_df[target], plot_df["pred"]), 2))
print("MAE: ", round(mae(plot_df[target], plot_df["pred"]), 2))
print("RMSE: ", round(mse(plot_df[target], plot_df["pred"]), 2))
# %%
