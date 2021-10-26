# Predictive_Control_for_Thermal_comfort
This repository aims to utilize building automation system and model predict control for human thermal comfort in office building.

In this case, we were fortunate to have a real commercial building as a study case in Taiwan.

We designed a Model Predictive Control module for indoor thermal comfort and fan coil units (FCUs) management.


## Model Predictive Control
MPC method is commonly used in the building automation field.

Through the existed Building Automation System (BAS) of the building, we are able to construct a data-driven MPC workframe.

The workframe connects real-time data, predictive algorithm, optimizer, and automated controller.

Some of these components will introduce in the following sections.
![Model_Predictive_Control](https://github.com/JackyWeng526/Predictive_Control_for_Thermal_comfort/blob/main/docs/MPC_construction_for_Thermal_Comfort.png)


## Real-time data
The real-time data used in this module includes weather dataset from Central Weather Bureau and building dataset from BAS.

### Taiwan micro-climate
The weather data could be downloaded on the [CWB website](https://e-service.cwb.gov.tw/HistoryDataQuery/).

Or you can try the downloader in [Taiwan_Weather_Data](https://github.com/JackyWeng526/Taiwan_Weather_Data) repository on my GitHub.

The Taipei weather data of 2021 is showed below.
![Weather_Data](https://github.com/JackyWeng526/Predictive_Control_for_Thermal_comfort/blob/main/docs/Taiwan_weather_NewTaipeiCity.PNG)

### Taiwanese indoor comfort range with adaptive model
By ASHRAE 55[1](https://en.wikipedia.org/wiki/ASHRAE_55) and local research[2](https://www.sciencedirect.com/science/article/abs/pii/S0306261912000967), we can have the Taiwanese adaptive comfort range.
![Local_Comfort_Range](https://github.com/JackyWeng526/Predictive_Control_for_Thermal_comfort/blob/main/docs/Taiwan_PET_adaptive_model.PNG)
The adaptive comfort range can help us easily set the target of HVAC setpoint temperature.

### Building Dataset
The building dataset contains not only the FCU operation record but also AHU operation record and CO2 concentration.
![FCU_data](https://github.com/JackyWeng526/Predictive_Control_for_Thermal_comfort/blob/main/docs/FCU_data.PNG)
![AHU_data](https://github.com/JackyWeng526/Predictive_Control_for_Thermal_comfort/blob/main/docs/AHU_data.PNG)
![CO2_data](https://github.com/JackyWeng526/Predictive_Control_for_Thermal_comfort/blob/main/docs/CO2_data.PNG)

## Indoor Thermal Comfort Control
![PET_before_after](https://github.com/JackyWeng526/Predictive_Control_for_Thermal_comfort/blob/main/docs/control_before_after.PNG)


## Results 
![Results](https://github.com/JackyWeng526/Predictive_Control_for_Thermal_comfort/blob/main/docs/Results.PNG)
