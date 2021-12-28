# Predictive_Control_for_Thermal_comfort
This research aims to utilize building automation system and model predict control for human thermal comfort in office building.

In this case, we are fortunate to have a real commercial building as a study case in Taiwan.

We design a Model Predictive Control module for indoor thermal comfort and fan coil units (FCUs) management.

# Methodology
The methods, theories, and the workflow of this research will be demonstrated in the following sections.

## Model Predictive Control
MPC method is commonly used in the building automation field.

Through the existed Building Automation System (BAS) of the building, we are able to construct a data-driven MPC framework.

The framework comprises real-time data, predictive algorithm, optimizer, and automated controller.

Some of these components will introduce in the following sections.

(BTW, some of the details won't be elaborated because of the confidential protocol.)
<a href="url"><img src="https://github.com/JackyWeng526/Predictive_Control_for_Thermal_comfort/blob/main/docs/MPC_construction_for_Thermal_Comfort.png" align="middle" height="70%" width="70%" ></a>


## Input data
The data used in this module includes weather dataset from Central Weather Bureau and building dataset from BAS.

We used historical data for model training and applied the model with real-time data flow for predictive control.


### Taiwan micro-climate data
The weather data could be downloaded on the [CWB website](https://e-service.cwb.gov.tw/HistoryDataQuery/).

Or you can try the downloader in [Taiwan_Weather_Data](https://github.com/JackyWeng526/Taiwan_Weather_Data) repository on my GitHub.

The Taipei weather data of 2021 is showed below.

You can also gather the real-time data and the weather prediction through the [open-API](https://opendata.cwb.gov.tw/dist/opendata-swagger.html?urls.primaryName=openAPI#/%E9%A0%90%E5%A0%B1/get_v1_rest_datastore_F_D0047_069). (Maybe need registration.)
<a href="url"><img src="https://github.com/JackyWeng526/Predictive_Control_for_Thermal_comfort/blob/main/docs/Taiwan_weather_NewTaipeiCity.PNG" align="middle" height="70%" width="70%" ></a>
![Weather_Data](https://github.com/JackyWeng526/Predictive_Control_for_Thermal_comfort/blob/main/docs/Taiwan_weather_NewTaipeiCity.PNG)


### Building Dataset
Beside the weather data, there is building dataset containing the FCU and AHU operation records and CO2 concentration values.
<a href="url"><img src="https://github.com/JackyWeng526/Predictive_Control_for_Thermal_comfort/blob/main/docs/FCU_data.PNG" align="middle" height="70%" width="70%" ></a>
![FCU_data](https://github.com/JackyWeng526/Predictive_Control_for_Thermal_comfort/blob/main/docs/FCU_data.PNG)
<a href="url"><img src="https://github.com/JackyWeng526/Predictive_Control_for_Thermal_comfort/blob/main/docs/AHU_data.PNG" align="middle" height="70%" width="70%" ></a>
![AHU_data](https://github.com/JackyWeng526/Predictive_Control_for_Thermal_comfort/blob/main/docs/AHU_data.PNG)
<a href="url"><img src="https://github.com/JackyWeng526/Predictive_Control_for_Thermal_comfort/blob/main/docs/CO2_data.PNG" align="middle" height="70%" width="70%" ></a>
![CO2_data](https://github.com/JackyWeng526/Predictive_Control_for_Thermal_comfort/blob/main/docs/CO2_data.PNG)

Beside the dataset introduced above, we also have the control strategy and suggestion provided by the [physical model](https://github.com/JackyWeng526/Office_Data_Application).

The PET and setpoint temperature targets would both be part of the training dataset.
<a href="url"><img src="https://github.com/JackyWeng526/Predictive_Control_for_Thermal_comfort/blob/main/docs/PET_and_SP_Target_by_physical_model.PNG" align="middle" height="70%" width="70%" ></a>
![Target_data](https://github.com/JackyWeng526/Predictive_Control_for_Thermal_comfort/blob/main/docs/PET_and_SP_Target_by_physical_model.PNG)


## Optimizer and boundary conditions
To conduct MPC framework for HVAC and comfort control, we have the building environment and human comfort standard as our boundary conditions.


### Taiwanese indoor comfort range with adaptive model
By ASHRAE 55[[1]](https://en.wikipedia.org/wiki/ASHRAE_55) and local research[[2]](https://www.sciencedirect.com/science/article/abs/pii/S0306261912000967), we can have the Taiwanese adaptive comfort range.

The adaptive comfort range can help us easily determine the target of HVAC setpoint temperature.
<a href="url"><img src="https://github.com/JackyWeng526/Predictive_Control_for_Thermal_comfort/blob/main/docs/Taiwan_PET_adaptive_model.PNG" align="middle" height="70%" width="70%" ></a>
![Local_Comfort_Range](https://github.com/JackyWeng526/Predictive_Control_for_Thermal_comfort/blob/main/docs/Taiwan_PET_adaptive_model.PNG)


## Optimal SP Strategy from Predictive Algorithm and Automated Controller
### Automated Controller
This section will vary a lot with the corresponding case study.

Our controller is built by MQTT, AWS, and the existing BAS in the field, please refer to the [MQTT example](https://github.com/JackyWeng526/Support_AI_service_with_MQTT).

The privacy and security of the internet and IoT protocols are well-considered.

# Results of Model Predictions and Comfort Control 
## SP prediction
We used Neural Network for predictive algorithm construction, and the results are shown below.

The test data predictions performed: r<sup>2</sup> = 0.64; MAE = 0.04.
<a href="url"><img src="https://github.com/JackyWeng526/Predictive_Control_for_Thermal_comfort/blob/main/docs/NN_result_1.png" align="middle" height="70%" width="70%" ></a>
![NN_result_1](https://github.com/JackyWeng526/Predictive_Control_for_Thermal_comfort/blob/main/docs/NN_result_1.png)

While this predictive model only has to be precise at the time we need, we can use some schedule rules to optimize predictive strategy for such a special application.

For example, the FCUs will be shut down or turned to 25 <sup>o</sup>C at night and on weekends.

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
<a href="url"><img src="https://github.com/JackyWeng526/Predictive_Control_for_Thermal_comfort/blob/main/docs/NN_result_2.png" align="middle" height="70%" width="70%" ></a>
![NN_result_2](https://github.com/JackyWeng526/Predictive_Control_for_Thermal_comfort/blob/main/docs/NN_result_2.png)


## Indoor Thermal Comfort Control
There must be other synergy predictive models for PET or indoor temperature predictions to achieve the MPC framework in this subject for optimizer's responding.

However, the models' construction is very similar and we don't elaborate here.

In conclusion, we had the performance of the comfort control module on a certain floor as well as the employees' complaints to HVAC management.

After the module was imported, the indoor PET was almost well-controlled and the number of employees' complaints reduced apparently.

<a href="url"><img src="https://github.com/JackyWeng526/Predictive_Control_for_Thermal_comfort/blob/main/docs/Results.PNG" align="middle" height="70%" width="70%" ></a>
![Results](https://github.com/JackyWeng526/Predictive_Control_for_Thermal_comfort/blob/main/docs/Results.PNG)


## Authors
- [@Jacky Weng](https://github.com/JackyWeng526)

## Acknowledgement
The module here is just the sample, not the real one in the field.
