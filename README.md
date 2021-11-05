# Predictive_Control_for_Thermal_comfort
This repository aims to utilize building automation system and model predict control for human thermal comfort in office building.

In this case, we are fortunate to have a real commercial building as a study case in Taiwan.

We design a Model Predictive Control module for indoor thermal comfort and fan coil units (FCUs) management.


## Model Predictive Control
MPC method is commonly used in the building automation field.

Through the existed Building Automation System (BAS) of the building, we are able to construct a data-driven MPC framework.

The framework comprises real-time data, predictive algorithm, optimizer, and automated controller.

Some of these components will introduce in the following sections.

(BTW, some of the details won't be elaborated because of the confidential protocol.)
![Model_Predictive_Control](https://github.com/JackyWeng526/Predictive_Control_for_Thermal_comfort/blob/main/docs/MPC_construction_for_Thermal_Comfort.png)


## Input data
The data used in this module includes weather dataset from Central Weather Bureau and building dataset from BAS.

We used historical data for model training and applied the model with real-time data flow for predictive control.

### Taiwan micro-climate data
The weather data could be downloaded on the [CWB website](https://e-service.cwb.gov.tw/HistoryDataQuery/).

Or you can try the downloader in [Taiwan_Weather_Data](https://github.com/JackyWeng526/Taiwan_Weather_Data) repository on my GitHub.

The Taipei weather data of 2021 is showed below.

You can also gather the real-time data and the weather prediction through the [open-API](https://opendata.cwb.gov.tw/dist/opendata-swagger.html?urls.primaryName=openAPI#/%E9%A0%90%E5%A0%B1/get_v1_rest_datastore_F_D0047_069). (Maybe need registration.)
![Weather_Data](https://github.com/JackyWeng526/Predictive_Control_for_Thermal_comfort/blob/main/docs/Taiwan_weather_NewTaipeiCity.PNG)

### Building Dataset
Beside the weather data, there is building dataset containing the FCU and AHU operation records and CO2 concentration values.
![FCU_data](https://github.com/JackyWeng526/Predictive_Control_for_Thermal_comfort/blob/main/docs/FCU_data.PNG)
![AHU_data](https://github.com/JackyWeng526/Predictive_Control_for_Thermal_comfort/blob/main/docs/AHU_data.PNG)
![CO2_data](https://github.com/JackyWeng526/Predictive_Control_for_Thermal_comfort/blob/main/docs/CO2_data.PNG)

Beside the dataset introduced above, we also have the control strategy and suggestion provided by the [physical model](https://github.com/JackyWeng526/Office_Data_Application).

The PET and setpoint temperature targets would both be part of the training dataset.
![Target_data](https://github.com/JackyWeng526/Predictive_Control_for_Thermal_comfort/blob/main/docs/PET_and_SP_Target_by_physical_model.PNG)

## Optimizer and boundary conditions
To conduct MPC framework for HVAC and comfort control, we have the building environment and human comfort standard as our boundary conditions.

### Taiwanese indoor comfort range with adaptive model
By ASHRAE 55[[1]](https://en.wikipedia.org/wiki/ASHRAE_55) and local research[[2]](https://www.sciencedirect.com/science/article/abs/pii/S0306261912000967), we can have the Taiwanese adaptive comfort range.

The adaptive comfort range can help us easily determine the target of HVAC setpoint temperature.
![Local_Comfort_Range](https://github.com/JackyWeng526/Predictive_Control_for_Thermal_comfort/blob/main/docs/Taiwan_PET_adaptive_model.PNG)

## Optimal SP Strategy and Automated Controller
### SP prediction
We used Neural Network for predictive algorithm construction, and the results are shown below.

The test data predictions performed: r<sup>2</sup> = 0.64; MAE = 0.04.
![NN_result_1](https://github.com/JackyWeng526/Predictive_Control_for_Thermal_comfort/blob/main/docs/NN_result_1.png)

While this predictive model only has to be precise at the time we need, we can use some schedule rules to optimize predictive strategy for such a special application.

For example, the FCUs will be shut down or turned to 25 <sup>o</sup>C at night as well as on weekends.

So, the strategy could be adjusted (r<sup>2</sup> = 0.84; MAE = 0.13) before being packaged and transmitted to the controller. 

```bash
plot_df["pred"] = np.where(
    np.logical_or(
        plot_df.index.dayofweek>4, 
    np.logical_or(
        plot_df.index.hour<7, 
        plot_df.index.hour>21)), 
    25, plot_df["pred"])
```

![NN_result_2](https://github.com/JackyWeng526/Predictive_Control_for_Thermal_comfort/blob/main/docs/NN_result_2.png)



## Indoor Thermal Comfort Control
![PET_before_after](https://github.com/JackyWeng526/Predictive_Control_for_Thermal_comfort/blob/main/docs/control_before_after.PNG)


### Prediction


## Results 
![Results](https://github.com/JackyWeng526/Predictive_Control_for_Thermal_comfort/blob/main/docs/Results.PNG)
