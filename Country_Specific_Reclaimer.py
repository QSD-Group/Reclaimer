import numpy as np
import math as math
import lhs_python as lhs
import pandas as pd
from scipy import stats
#%% Conversions
df1 = pd.read_csv(r'CSVforCode\CountryCode.csv')
df2 = pd.read_csv(r'CSVforCode\TCode.csv')
df3 = pd.read_csv(r'CSVforCode\LCI.csv')
#%%
m3_L= 1000
m_ft = 3.28084
M_mm = 1000
M_in = 39.37 
Years_Days = 365
Days_Hours = 24
Hours_Min = 60
Min_Sec = 60
Watts_HP = 745.7 
kW_W = 1000
m3_Gal = 264.172
Gal_L = 3.785
Hours_Sec = 3600
m_bar = 0.09804
L_Oz = 33.814
Watts_HP = 745.7
kg_g = 1000
#%% Assumed Parameter Distributions

nsamples = 1000

Daily_Flushes = lhs.lhs_uniform(1,7,nsamples) #flushes/user/day
Flush_Volume = lhs.lhs_uniform(6,10,nsamples) #L blackwater/flush
Membrane_Flux = lhs.lhs_uniform(114,171,nsamples) #L/m2*hr
Velocity_Crossflow = lhs.lhs_uniform(3.5,5.6,nsamples) #m/s
Pressure_Membrane = lhs.lhs_uniform(0,3.5,nsamples) #bar
Fill_Fraction_GAC_Column = lhs.lhs_uniform(.75,.85,nsamples) #% 
UF_GAC_N_P_Removal = lhs.lhs_uniform(0.3,0.5,nsamples) #%
Clinoptilolite_Cost = lhs.lhs_triangle(1.08*0.9,1.08,1.08*1.1,nsamples) #$/kg
Polonite_Cost = lhs.lhs_triangle(1.37*0.9,1.37,1.37*1.1,nsamples) #$/kg
Clinoptilolite_Capacity = lhs.lhs_triangle(10*.9,10,10*1.1,nsamples) #mg NH3/g
Polonite_Capacity = lhs.lhs_triangle(10*.9,10,10*1.1,nsamples) #mg PO4/g
N_Content_Protein=lhs.lhs_uniform(.13,.19,nsamples) #% nitrogen in protein
N_P_Excretion=lhs.lhs_uniform(.99,1,nsamples) #% intake nitrogen excreted in urine and feces
N_Urine = lhs.lhs_triangle(.86*.9,.86,.86*1.1,nsamples) #% excreted nitrogen in urine
P_Content_A_Protein = lhs.lhs_triangle(.004,0.022,0.048,nsamples) #%phosphorus in animal protein
P_Content_V_Protein = lhs.lhs_triangle(.002,0.011,0.032,nsamples) #%phosphorus in vegetal protein
P_Urine = lhs.lhs_triangle(.67*.9,.67,.67*1.1,nsamples) #% excreted phosphorus in urine
Seperation_Efficiency = lhs.lhs_uniform(0.8,0.9,nsamples) 
Density_GAC = lhs.lhs_uniform(400,500,nsamples) #kg/m3
#Lifetime_GAC = lhs.lhs_uniform(48,81,nsamples) #flushes/kg GAC
Lifetime_GAC = lhs.lhs_triangle(4500,9000,13500,nsamples) #L treated
Power_Required_Treatment_EC = lhs.lhs_uniform(5.6,6.4,nsamples) #Wh/L
Current_EC = lhs.lhs_triangle(4,4,8,nsamples) # A
Power_Stirrer = lhs.lhs_uniform(18,30,nsamples) #W
Flowrate_Discharge = lhs.lhs_uniform(8,16,nsamples) #L/min
Pump_UF_Lifetime = lhs.lhs_triangle(10*.75,10,10*1.25,nsamples) #years
Membrane_UF_Lifetime = lhs.lhs_triangle(3*.9,3,3*1.1,nsamples) #years
Switch_Lifetime = lhs.lhs_triangle(10*.75,10,10*1.25,nsamples) #years
Valve_UF_Lifetime = lhs.lhs_triangle(5*.5,5,5*1.5,nsamples) #years
Electrode_EC_Lifetime = lhs.lhs_triangle(2*.9,2,2*1.1,nsamples) #years
Stirrer_Lifetime = lhs.lhs_triangle(5*.5,5,5*1.5,nsamples) #years
U_Pump_Misc_Lifetime = lhs.lhs_triangle(10*.9,10,10*1.1,nsamples) #years
Discount_Rate = lhs.lhs_uniform(0.03,0.06,nsamples) #% 
U_Pump_UF = lhs.lhs_uniform(150,200,nsamples) #$
U_Membrane_UF = lhs.lhs_triangle(212*.9,212,212*1.1,nsamples) #$
U_Valve_UF = lhs.lhs_triangle(100.5*.9,100.5,100.5*1.1,nsamples) #$
U_Tank_UF = lhs.lhs_triangle(549.76*.9,549.76,549.76*1.1,nsamples) #$
U_Switch = lhs.lhs_triangle(110*.9,110,110*1.1,nsamples) #$
U_Column_GAC = lhs.lhs_triangle(16.19*.75,16.19,16.19*1.25,nsamples) #$/ft
U_Stirrer_EC = lhs.lhs_triangle(151.02*.9,151.02,151.02*1.1,nsamples)#$
U_Electrode_EC = lhs.lhs_triangle(99.45*.9,99.45,99.45*1.1,nsamples) #$
U_Pump_Misc = lhs.lhs_triangle(175*.9,175,175*1.1,nsamples) #$
US_Initial_Unit_Cost_UF = lhs.lhs_triangle(875.5*.9,875.5,875.5*1.1,nsamples)
InCountry_Initial_Unit_Cost_UF = lhs.lhs_triangle(601.31*.9,601.31,601.31*1.1,nsamples)
US_Initial_Unit_Cost_GAC = lhs.lhs_triangle(264.60*.9,264.60,264.60*1.1,nsamples)
InCountry_Initial_Unit_Cost_GAC = lhs.lhs_triangle(574.41*.9,574.41,574.41*1.1,nsamples)
US_Initial_Unit_Cost_EC = lhs.lhs_triangle(470.47*.9,470.47,470.47*1.1,nsamples)
InCountry_Initial_Unit_Cost_EC = lhs.lhs_triangle(247.43*.9,247.43,247.43*1.1,nsamples)
US_Initial_Unit_Cost_Controls = lhs.lhs_triangle(575.34*.9,575.34,575.34*1.1,nsamples)
InCountry_Initial_Unit_Cost_Controls = lhs.lhs_triangle(985.57*.9,985.57,985.57*1.1,nsamples)
US_Initial_Unit_Cost_Misc = lhs.lhs_triangle(387.78*.9,387.78,387.78*1.1,nsamples)
InCountry_Initial_Unit_Cost_Misc = lhs.lhs_triangle(1828.41*.9,1828.41,1828.41*1.1,nsamples)
U_Media_GAC = lhs.lhs_triangle(0.29,3,5,nsamples) #$/kg

E_Nuclear_Ozone = df3['Nuclear_Electricity'][0]
E_Hydro_Ozone = df3['Min_Hydro_Electricity'][0]
E_Geothermal_Ozone = df3['Geothermal_Electricity'][0]
E_Wind_Ozone = lhs.lhs_triangle((df3['Min_Wind_Electricity'][0]),(df3['Mid_Wind_Electricity'][0]),(df3['Max_Wind_Electricity'][0]),nsamples)
E_Solar_Ozone = lhs.lhs_uniform((df3['Min_Solar_Electricity'][0]),(df3['Max_Solar_Electricity'][0]),nsamples)
E_Waste_Ozone = df3['Waste_Electricity'][0]
E_Coal_Ozone = df3['Coal_Electricity'][0]
E_Oil_Ozone = df3['Oil_Electricity'][0]
E_Gas_Ozone = lhs.lhs_triangle((df3['Min_Gas_Electricity'][0]),(df3['Mid_Gas_Electricity'][0]),(df3['Max_Gas_Electricity'][0]),nsamples)

E_Nuclear_GHG = df3['Nuclear_Electricity'][1]
E_Hydro_GHG = lhs.lhs_uniform((df3['Min_Hydro_Electricity'][1]),(df3['Max_Hydro_Electricity'][1]),nsamples)
E_Geothermal_GHG = df3['Geothermal_Electricity'][1]
E_Wind_GHG = lhs.lhs_triangle((df3['Min_Wind_Electricity'][1]),(df3['Mid_Wind_Electricity'][1]),(df3['Max_Wind_Electricity'][1]),nsamples)
E_Solar_GHG = lhs.lhs_uniform((df3['Min_Solar_Electricity'][1]),(df3['Max_Solar_Electricity'][1]),nsamples)
E_Waste_GHG = df3['Waste_Electricity'][1]
E_Coal_GHG = df3['Coal_Electricity'][1]
E_Oil_GHG = df3['Oil_Electricity'][1]
E_Gas_GHG = lhs.lhs_triangle((df3['Min_Gas_Electricity'][1]),(df3['Mid_Gas_Electricity'][1]),(df3['Max_Gas_Electricity'][1]),nsamples)

E_Nuclear_Smog = df3['Nuclear_Electricity'][2]
E_Hydro_Smog = df3['Min_Hydro_Electricity'][2]
E_Geothermal_Smog = df3['Geothermal_Electricity'][2]
E_Wind_Smog = lhs.lhs_triangle((df3['Min_Wind_Electricity'][2]),(df3['Mid_Wind_Electricity'][2]),(df3['Max_Wind_Electricity'][2]),nsamples)
E_Solar_Smog = lhs.lhs_uniform((df3['Min_Solar_Electricity'][2]),(df3['Max_Solar_Electricity'][2]),nsamples)
E_Waste_Smog = df3['Waste_Electricity'][2]
E_Coal_Smog = df3['Coal_Electricity'][2]
E_Oil_Smog = df3['Oil_Electricity'][2]
E_Gas_Smog = lhs.lhs_triangle((df3['Min_Gas_Electricity'][2]),(df3['Mid_Gas_Electricity'][2]),(df3['Max_Gas_Electricity'][2]),nsamples)

E_Nuclear_Acid = df3['Nuclear_Electricity'][3]
E_Hydro_Acid = df3['Max_Hydro_Electricity'][3]
E_Geothermal_Acid = df3['Geothermal_Electricity'][3]
E_Wind_Acid = lhs.lhs_triangle((df3['Min_Wind_Electricity'][3]),(df3['Mid_Wind_Electricity'][3]),(df3['Max_Wind_Electricity'][3]),nsamples)
E_Solar_Acid = lhs.lhs_uniform((df3['Min_Solar_Electricity'][3]),(df3['Max_Solar_Electricity'][3]),nsamples)
E_Waste_Acid = df3['Waste_Electricity'][3]
E_Coal_Acid = df3['Coal_Electricity'][3]
E_Oil_Acid = df3['Oil_Electricity'][3]
E_Gas_Acid = lhs.lhs_triangle((df3['Min_Gas_Electricity'][3]),(df3['Mid_Gas_Electricity'][3]),(df3['Max_Gas_Electricity'][3]),nsamples)

E_Nuclear_Eutro = df3['Nuclear_Electricity'][4]
E_Hydro_Eutro = df3['Min_Hydro_Electricity'][4]
E_Geothermal_Eutro = df3['Geothermal_Electricity'][4]
E_Wind_Eutro = lhs.lhs_triangle((df3['Min_Wind_Electricity'][4]),(df3['Mid_Wind_Electricity'][4]),(df3['Max_Wind_Electricity'][4]),nsamples)
E_Solar_Eutro = lhs.lhs_uniform((df3['Min_Solar_Electricity'][4]),(df3['Max_Solar_Electricity'][4]),nsamples)
E_Waste_Eutro = df3['Waste_Electricity'][4]
E_Coal_Eutro = df3['Coal_Electricity'][4]
E_Oil_Eutro = df3['Oil_Electricity'][4]
E_Gas_Eutro = lhs.lhs_triangle((df3['Min_Gas_Electricity'][4]),(df3['Mid_Gas_Electricity'][4]),(df3['Max_Gas_Electricity'][4]),nsamples)

E_Nuclear_Carcin = df3['Nuclear_Electricity'][5]
E_Hydro_Carcin = df3['Min_Hydro_Electricity'][5]
E_Geothermal_Carcin = df3['Geothermal_Electricity'][5]
E_Wind_Carcin = lhs.lhs_triangle((df3['Mid_Wind_Electricity'][5]),(df3['Min_Wind_Electricity'][5]),(df3['Max_Wind_Electricity'][5]),nsamples)
E_Solar_Carcin = lhs.lhs_uniform((df3['Min_Solar_Electricity'][5]),(df3['Max_Solar_Electricity'][5]),nsamples)
E_Waste_Carcin = df3['Waste_Electricity'][5]
E_Coal_Carcin = df3['Coal_Electricity'][5]
E_Oil_Carcin = df3['Oil_Electricity'][5]
E_Gas_Carcin = lhs.lhs_triangle((df3['Min_Gas_Electricity'][5]),(df3['Max_Gas_Electricity'][5]),(df3['Mid_Gas_Electricity'][5]),nsamples)

E_Nuclear_NonCar = df3['Nuclear_Electricity'][6]
E_Hydro_NonCar = df3['Min_Hydro_Electricity'][6]
E_Geothermal_NonCar = df3['Geothermal_Electricity'][6]
E_Wind_NonCar = lhs.lhs_triangle((df3['Mid_Wind_Electricity'][6]),(df3['Min_Wind_Electricity'][6]),(df3['Max_Wind_Electricity'][6]),nsamples)
E_Solar_NonCar = lhs.lhs_uniform((df3['Min_Solar_Electricity'][6]),(df3['Max_Solar_Electricity'][6]),nsamples)
E_Waste_NonCar = df3['Waste_Electricity'][6]
E_Coal_NonCar = df3['Coal_Electricity'][6]
E_Oil_NonCar = df3['Oil_Electricity'][6]
E_Gas_NonCar = lhs.lhs_triangle((df3['Min_Gas_Electricity'][6]),(df3['Max_Gas_Electricity'][6]),(df3['Mid_Gas_Electricity'][6]),nsamples)

E_Nuclear_Resp = df3['Nuclear_Electricity'][7]
E_Hydro_Resp = df3['Min_Hydro_Electricity'][7]
E_Geothermal_Resp = df3['Geothermal_Electricity'][7]
E_Wind_Resp = lhs.lhs_triangle((df3['Mid_Wind_Electricity'][7]),(df3['Min_Wind_Electricity'][7]),(df3['Max_Wind_Electricity'][7]),nsamples)
E_Solar_Resp = lhs.lhs_uniform((df3['Min_Solar_Electricity'][7]),(df3['Max_Solar_Electricity'][7]),nsamples)
E_Waste_Resp = df3['Waste_Electricity'][7]
E_Coal_Resp = df3['Coal_Electricity'][7]
E_Oil_Resp = df3['Oil_Electricity'][7]
E_Gas_Resp = lhs.lhs_triangle((df3['Min_Gas_Electricity'][7]),(df3['Mid_Gas_Electricity'][7]),(df3['Max_Gas_Electricity'][7]),nsamples)

E_Nuclear_EcoTox = df3['Nuclear_Electricity'][8]
E_Hydro_EcoTox = df3['Min_Hydro_Electricity'][8]
E_Geothermal_EcoTox = df3['Geothermal_Electricity'][8]
E_Wind_EcoTox = lhs.lhs_triangle((df3['Mid_Wind_Electricity'][8]),(df3['Min_Wind_Electricity'][8]),(df3['Max_Wind_Electricity'][8]),nsamples)
E_Solar_EcoTox = lhs.lhs_uniform((df3['Min_Solar_Electricity'][8]),(df3['Max_Solar_Electricity'][8]),nsamples)
E_Waste_EcoTox = df3['Waste_Electricity'][8]
E_Coal_EcoTox = df3['Coal_Electricity'][8]
E_Oil_EcoTox = df3['Oil_Electricity'][8]
E_Gas_EcoTox = lhs.lhs_triangle((df3['Min_Gas_Electricity'][8]),(df3['Max_Gas_Electricity'][8]),(df3['Mid_Gas_Electricity'][8]),nsamples)

E_Nuclear_FFD = df3['Nuclear_Electricity'][9]
E_Hydro_FFD = df3['Min_Hydro_Electricity'][9]
E_Geothermal_FFD = df3['Geothermal_Electricity'][9]
E_Wind_FFD = lhs.lhs_triangle((df3['Min_Wind_Electricity'][9]),(df3['Mid_Wind_Electricity'][9]),(df3['Max_Wind_Electricity'][9]),nsamples)
E_Solar_FFD = lhs.lhs_uniform((df3['Min_Solar_Electricity'][9]),(df3['Max_Solar_Electricity'][9]),nsamples)
E_Waste_FFD = df3['Waste_Electricity'][9]
E_Coal_FFD = df3['Coal_Electricity'][9]
E_Oil_FFD = df3['Oil_Electricity'][9]
E_Gas_FFD = lhs.lhs_triangle((df3['Min_Gas_Electricity'][9]),(df3['Mid_Gas_Electricity'][9]),(df3['Max_Gas_Electricity'][9]),nsamples)

GAC_Ozone = lhs.lhs_uniform(1.24905E-07*0.9, 1.24905E-07*1.1,nsamples)
GAC_GHG = lhs.lhs_uniform(8.388648277*0.9,8.388648277*1.1,nsamples)
GAC_Smog = lhs.lhs_uniform(0.398574022*0.9,0.398574022*1.1,nsamples)
GAC_Acid = lhs.lhs_uniform(0.053673728*0.9,0.053673728*1.1,nsamples)
GAC_Eutro = lhs.lhs_uniform(0.038863552*0.9,0.038863552*1.1,nsamples)
GAC_Carcin = lhs.lhs_uniform(4.18201E-07*0.9,4.18201E-07*1.1,nsamples)
GAC_NonCar = lhs.lhs_uniform(1.50583E-06*0.9,1.50583E-06*1.1,nsamples)
GAC_Resp = lhs.lhs_uniform(0.004727252*0.9,0.004727252*1.1,nsamples)
GAC_EcoTox = lhs.lhs_uniform(39.62653812*0.9,39.62653812*1.1,nsamples)
GAC_FFD = lhs.lhs_uniform(2.948630375*0.9,2.948630375*1.1,nsamples)

Zeo_Ozone = lhs.lhs_uniform(5.84E-07*.9,5.84E-07*1.1,nsamples)
Zeo_GHG = lhs.lhs_uniform(1.778776771*0.9,1.778776771*1.1,nsamples)
Zeo_Smog = lhs.lhs_uniform(0.099907178*0.9,0.099907178*1.1,nsamples)
Zeo_Acid = lhs.lhs_uniform(0.010357385*0.9,0.010357385*1.1,nsamples)
Zeo_Eutro = lhs.lhs_uniform(7.82E-03*0.9,7.82E-03*1.1,nsamples)
Zeo_Carcin = lhs.lhs_uniform(7.82E-07*0.9,7.82E-07*1.1,nsamples)
Zeo_NonCar = lhs.lhs_uniform(1.10E-06*0.9,1.10E-06*1.1,nsamples)
Zeo_Resp = lhs.lhs_uniform(2.32E-03*0.9,2.32E-03*1.1,nsamples)
Zeo_EcoTox = lhs.lhs_uniform(46.12729017*0.9,46.12729017*1.1,nsamples)
Zeo_FFD = lhs.lhs_uniform(1.872453392*0.9,1.872453392*1.1,nsamples)

#%% Decision Variables
U = 20 #users
D = 4 #in
V = 5 #gal/batch
L = 20 #years
#%% Fixed Parameters
Membrane_Surface_Area = 0.07 #m2
Nominal_Internal_Diameter = 12.77 #mm
Area_Concentrate = ((math.pi/4)*(Nominal_Internal_Diameter)**2)*(1/M_mm)**2 #m2
Volume_GAC = 7.7 #L
Voltage_Discharge_Pump = 12 #V
Current_Discharge_Pump = 6 #A
Voltage_EC = 12 #V
#%% Equations
Results_SpearmansCoefCost = np.full((60,89),0.0)
Results_Cost_Total=np.full((1000,89),0.0)
Results_Cost_Initial=np.full((1000,89),0.0)
Results_Cost_OM=np.full((1000,89),0.0)
Results_Cost_Energy=np.full((1000,89),0.0)
#Results_Energy_Demand = np.full((1000,89),0.0)
Results_Cost_Percent_Initial=np.full((1000,89),0.0)
Results_Cost_Percent_OM=np.full((1000,89),0.0)
Results_Percent_Energy=np.full((1000,89),0.0)
Results_Percent_Materials= np.full((1000,89),0.0)
Results_Percent_Labor = np.full((1000,89),0.0)
Results_Percent_GAC_Media= np.full((1000,89),0.0)
Results_Percent_Zeolites = np.full((1000,89),0.0)
Results_E_Ozone = np.full((1000,89),0.0)
Results_E_GHG = np.full((1000,89),0.0)
Results_E_Smog = np.full((1000,89),0.0)
Results_E_Acid = np.full((1000,89),0.0)
Results_E_Eutro = np.full((1000,89),0.0)
Results_E_Carcin = np.full((1000,89),0.0)
Results_E_NonCar = np.full((1000,89),0.0)
Results_E_Resp = np.full((1000,89),0.0)
Results_E_EcoTox = np.full((1000,89),0.0)
Results_E_FFD = np.full((1000,89),0.0)
Results_Zeo_Ozone = np.full((1000,89),0.0)
Results_Zeo_GHG = np.full((1000,89),0.0)
Results_Zeo_Smog = np.full((1000,89),0.0)
Results_Zeo_Acid = np.full((1000,89),0.0)
Results_Zeo_Eutro = np.full((1000,89),0.0)
Results_Zeo_Carcin = np.full((1000,89),0.0)
Results_Zeo_NonCar = np.full((1000,89),0.0)
Results_Zeo_Resp = np.full((1000,89),0.0)
Results_Zeo_EcoTox = np.full((1000,89),0.0)
Results_Zeo_FFD = np.full((1000,89),0.0)
Results_E_CO2_Intensity = np.full((1000,89),0.0)
Results_Energy_Overall = np.full((1000,89),0.0)
Results_Zeo = np.full((1000,89),0.0)
Results_ModSpearmansCost = np.full((60,89),0.0)

Results_PLR = np.full((1000,89),0.0)
Results_Waste = np.full((1000,89),0.0)
Results_Total_Protein = np.full((1000,89),0.0)
Results_U_Energy = np.full((1000,89),0.0)
Results_Monthly_Construction_Wage = np.full((1000,89),0.0)
Results_Monthly_Maintenance_Wage = np.full((1000,89),0.0)

Impacts_GAC_Ozone = np.full((1000,1),0.0)
Impacts_GAC_GHG = np.full((1000,1),0.0)
Impacts_GAC_Smog = np.full((1000,1),0.0)
Impacts_GAC_Acid = np.full((1000,1),0.0)
Impacts_GAC_Eutro = np.full((1000,1),0.0)
Impacts_GAC_Carcin = np.full((1000,1),0.0)
Impacts_GAC_NonCar = np.full((1000,1),0.0)
Impacts_GAC_Resp = np.full((1000,1),0.0)
Impacts_GAC_EcoTox = np.full((1000,1),0.0)
Impacts_GAC_FFD = np.full((1000,1),0.0)



Country = []

allCountriesRes = []
allCountriesCoefCost = []

for i in range(0,89):
    #SpearmansCoefCost = np.full((60,1),0.0)
    Required_User_Fee_Overall = np.full((1000,1),0.0)
    Required_User_Fee_Initial_Overall = np.full((1000,1),0.0)
    Required_User_Fee_OM_Overall = np.full((1000,1),0.0)
    Required_User_Fee_Energy_Overall = np.full((1000,1),0.0)
    #Energy_Demand = np.full((1000,1)0.0)
    Percent_Initial = np.full((1000,1),0.0)
    Percent_OM = np.full((1000,1),0.0)
    Percent_Energy = np.full((1000,1),0.0)
    Percent_Materials= np.full((1000,1),0.0)
    Percent_Labor = np.full((1000,1),0.0)
    Percent_GAC_Media= np.full((1000,1),0.0)
    Percent_Zeolites = np.full((1000,1),0.0)
    E_Impacts_Ozone = np.full((1000,1),0.0)
    E_Impacts_GHG = np.full((1000,1),0.0)
    E_Impacts_Smog = np.full((1000,1),0.0)
    E_Impacts_Acid = np.full((1000,1),0.0)
    E_Impacts_Eutro = np.full((1000,1),0.0)
    E_Impacts_Carcin = np.full((1000,1),0.0)
    E_Impacts_NonCar = np.full((1000,1),0.0)
    E_Impacts_Resp = np.full((1000,1),0.0)
    E_Impacts_EcoTox = np.full((1000,1),0.0)
    E_Impacts_FFD = np.full((1000,1),0.0)
    Impacts_Zeo_Ozone = np.full((1000,1),0.0)
    Impacts_Zeo_GHG = np.full((1000,1),0.0)
    Impacts_Zeo_Smog = np.full((1000,1),0.0)
    Impacts_Zeo_Acid = np.full((1000,1),0.0)
    Impacts_Zeo_Eutro = np.full((1000,1),0.0)
    Impacts_Zeo_Carcin = np.full((1000,1),0.0)
    Impacts_Zeo_NonCar = np.full((1000,1),0.0)
    Impacts_Zeo_Resp = np.full((1000,1),0.0)
    Impacts_Zeo_EcoTox = np.full((1000,1),0.0)
    Impacts_Zeo_FFD = np.full((1000,1),0.0)
    E_CO2_Intensity = np.full((1000,1),0.0)
    Energy_Overall = np.full((1000,1),0.0)
    Zeolite_Total = np.full((1000,1),0.0)
    
    #CS_PLR = np.full((1000,1),0.0)
    #CS_Waste = np.full((1000,1),0.0)
    #CS_Total_Protein = np.full((1000,1),0.0)
    #CS_U_Energy = np.full((1000,1),0.0)
    #CS_Monthly_Construction_Wage = np.full((1000,1),0.0)
    #CS_Monthly_Maintenance_Wage = np.full((1000,1),0.0)
    
    Total_Protein=lhs.lhs_triangle(df1.Nitrogen[i]*.9, df1.Nitrogen[i],df1.Nitrogen[i]*1.1,nsamples)
    #CS_Total_Protein[i,0] = Total_Protein
    Total_Protein_A=lhs.lhs_triangle(df1.Panimal[i]*.9,df1.Panimal[i],df1.Panimal[i]*1.1,nsamples)
    Total_Protein_V=lhs.lhs_triangle(df1.Pvegetal[i]*.9,df1.Pvegetal[i],df1.Pvegetal[i]*1.1,nsamples)
    Waste = lhs.lhs_triangle(df1.NMin[i],df1.NMid[i],df1.NMax[i], nsamples)
    #CS_Waste[i,0] = Waste
    PLR = lhs.lhs_triangle(df1.PLR[i]*0.9,df1.PLR[i], df1.PLR[i]*1.1, nsamples)
    #CS_PLR[i,0] = PLR
    U_Energy=lhs.lhs_triangle(df1.Energy[i]*0.9, df1.Energy[i], df1.Energy[i]*1.1, nsamples)
    #CS_U_Energy[i,0] = U_Energy
    Monthly_Construction_Wage=lhs.lhs_triangle(df1.ConstructionLabor[i]*0.9,df1.ConstructionLabor[i],df1.ConstructionLabor[i]*1.1,nsamples) #$/month
    #CS_Monthly_Construction_Wage[i,0] = Monthly_Construction_Wage
    Monthly_Maintenance_Wage=lhs.lhs_triangle(df1.OMLabor[i]*0.9,df1.OMLabor[i],df1.OMLabor[i]*1.1,nsamples) #$/month
    #CS_Monthly_Maintenance_Wage[i,0] = Monthly_Maintenance_Wage
    Income_Tax=df1.Tax[i]
    E_Per_Nuclear=df1.Nuclear[i]
    E_Per_Hydro=df1.Hydro[i]
    E_Per_Geo=df1.Geo[i]
    E_Per_Wind=df1.Wind[i]
    E_Per_Solar=df1.Solar[i]
    E_Per_Waste=df1.Bio[i]
    E_Per_Coal=df1.Oil[i]
    E_Per_Oil=df1.Coal[i]
    E_Per_Gas=df1.Gas[i]
    Country.append(df1.Country[i])

    for j in range(0, nsamples):
        Flowrate_Users = U*Daily_Flushes[j,0]*Flush_Volume[j,0]*(1/Days_Hours) #L/hr
        Flowrate_Permeate = Flowrate_Users #assume continuous pumping
        Required_Membrane_Area = Flowrate_Permeate/Membrane_Flux[j,0] #m2
        Membranes_Required = math.ceil(Required_Membrane_Area/Membrane_Surface_Area) #units
        Flowrate_Permeate_Membrane = Flowrate_Permeate/Membranes_Required #L/hr/membrane
        Flowrate_Concentrate_Membrane = Velocity_Crossflow[j,0]*Area_Concentrate*m3_L*Hours_Sec #L/hr
        Flowrate_Feed = ((Flowrate_Permeate_Membrane+Flowrate_Concentrate_Membrane)*Membranes_Required)/m3_L #m3/hr
        Head = ((-4.346*Flowrate_Feed)+40.8)*m_bar #bar
        Pump_Power = 0.5 #horsepower
        if Head <= Pressure_Membrane[j,0]:
            Head = ((-5.588*Flowrate_Feed)+53.6)*m_bar #bar
            Pump_Power = 0.75 #horsepower
            if Head <= Pressure_Membrane[j,0]:
                Head = ((-5.588*Flowrate_Feed)+58.8)*m_bar #bar
                Pump_Power = 1.0 #horsepower
        Time_Daily_Pump = (Daily_Flushes[j,0]*Flush_Volume[j,0]*U)/(Flowrate_Permeate) #hours/day
        Energy_Annual_UF = Pump_Power*Time_Daily_Pump*Years_Days*Watts_HP*(1/kW_W) #kWh/year
        Area_GAC_Column = (math.pi/4)*((D)**2)
        Volume_GAC_Column = Volume_GAC/Fill_Fraction_GAC_Column[j,0] #L
        Length_GAC_Column = ((Volume_GAC_Column/Area_GAC_Column)*((M_in)**2)*m_ft)/m3_L #ft
        Mass_GAC_Total = (Volume_GAC*(Density_GAC[j,0]))/m3_L #kg
        Replacement_Period_GAC = (Lifetime_GAC[j,0]/Flowrate_Users)*(1/Days_Hours)*(1/Years_Days) #yr
        Annual_GAC_Required = Mass_GAC_Total/Replacement_Period_GAC #kg/year
        N_Feces = 1-N_Urine[j,0]
        P_Feces = 1-P_Urine[j,0]
        N_Concentration = (Total_Protein[j,0]*N_Content_Protein[j,0]*(1-Waste[j,0])*N_P_Excretion[j,0])*(N_Urine[j,0]+((1-Seperation_Efficiency[j,0])*N_Feces)) #g/person/day
        P_Concentration = (((Total_Protein_A[j,0]*P_Content_A_Protein[j,0])+(Total_Protein_V[j,0]*P_Content_V_Protein[j,0]))*(1-Waste[j,0])*N_P_Excretion[j,0])*(P_Urine[j,0]+((1-Seperation_Efficiency[j,0])*P_Feces)) #g/person/day
        Clinop = N_Concentration*(1-UF_GAC_N_P_Removal[j,0])*(1/Clinoptilolite_Capacity[j,0])*(Years_Days) #kg/year
        Polonite = P_Concentration*(1-UF_GAC_N_P_Removal[j,0])*(1/Polonite_Capacity[j,0])*(Years_Days) #kg/year
        Zeolite_Total[j,0] = Clinop+Polonite
        N_Removal_Cost = N_Concentration*(1-UF_GAC_N_P_Removal[j,0])*(Clinoptilolite_Cost[j,0]/Clinoptilolite_Capacity[j,0])*(Years_Days) #$/year
        P_Removal_Cost = P_Concentration*(1-UF_GAC_N_P_Removal[j,0])*(Polonite_Cost[j,0]/Polonite_Capacity[j,0])*(Years_Days) #$/year
        Batch_Daily_EC = (U*Daily_Flushes[j,0]*Flush_Volume[j,0])/(V*Gal_L) #Batches/Day
        Time_Batch_EC = (Power_Required_Treatment_EC[j,0]*V*Gal_L)/(Voltage_EC*Current_EC[j,0]) #hours/batch
        Time_Daily_EC = Time_Batch_EC*Batch_Daily_EC #hours/day
        Energy_EC_Treatment = Current_EC[j,0]*Voltage_EC*Time_Daily_EC*(1/kW_W)*(Years_Days) #kWh/year
        Energy_Annual_Stirrer = Power_Stirrer[j,0]*Time_Daily_EC*(1/kW_W)*(Years_Days) #kWh/year
        Energy_Annual_EC = Energy_EC_Treatment+Energy_Annual_Stirrer #kWh/year
        Time_Batch_Discharge = (V*Gal_L)/Flowrate_Discharge[j,0] #min/batch
        Time_Daily_Discharge = Time_Batch_Discharge*Batch_Daily_EC*(1/Hours_Min) #hours/day
        Energy_Annual_Misc = Voltage_Discharge_Pump*Current_Discharge_Pump*Time_Daily_Discharge*(1/kW_W)*(Years_Days) #kWh/year
        Initial_Unit_Cost_UF = US_Initial_Unit_Cost_UF[j,0]+(InCountry_Initial_Unit_Cost_UF[j,0]*PLR[j,0])
        U_Pump_UF_Replacement = U_Pump_UF[j,0]*((L/Pump_UF_Lifetime[j,0])-1)
        if (U_Pump_UF_Replacement+U_Pump_UF[j,0]) <= U_Pump_UF[j,0]:
            U_Pump_UF_Replacement = 0
        U_Membrane_UF_Replacement = U_Membrane_UF[j,0]*Membranes_Required*((L/Membrane_UF_Lifetime[j,0])-1)
        if (U_Membrane_UF_Replacement+U_Membrane_UF[j,0]*Membranes_Required) <= U_Membrane_UF[j,0]:
            U_Membrane_UF_Replacement = 0
        U_Switch_Replacement = U_Switch[j,0]*3*((L/Switch_Lifetime[j,0])-1)
        if (U_Switch_Replacement+(U_Switch[j,0]*3)) <= U_Switch[j,0]*3:
            U_Switch_Replacement = 0
        U_Valve_UF_Replacement = U_Valve_UF[j,0]*((L/Valve_UF_Lifetime[j,0])-1)
        if (U_Valve_UF_Replacement+U_Valve_UF[j,0]) <= U_Valve_UF[j,0]:
            U_Valve_UF_Replacement = 0
        Replacement_Cost_UF = (U_Pump_UF_Replacement+(U_Membrane_UF_Replacement)+U_Switch_Replacement+U_Valve_UF_Replacement)/L #$/year
        Depreciation_Cost_UF = ((Initial_Unit_Cost_UF-U_Pump_UF[j,0]-U_Membrane_UF[j,0]-(U_Switch[j,0]*3)-U_Valve_UF[j,0])/L)+(U_Pump_UF[j,0]/Pump_UF_Lifetime[j,0])+(U_Membrane_UF[j,0]/Membrane_UF_Lifetime[j,0])+((U_Switch[j,0]*3)/Switch_Lifetime[j,0])+(U_Valve_UF[j,0]/Valve_UF_Lifetime[j,0])
        Initial_Unit_Cost_GAC = US_Initial_Unit_Cost_GAC[i,0]+((InCountry_Initial_Unit_Cost_GAC[i,0]+(Length_GAC_Column*U_Column_GAC[i,0]))*PLR[i,0])
        Media_Cost_GAC = (Annual_GAC_Required*U_Media_GAC[j,0])+N_Removal_Cost+P_Removal_Cost #$/year
        GAC_Cost = (Annual_GAC_Required*U_Media_GAC[j,0])
        Zeolites_Cost = N_Removal_Cost+P_Removal_Cost
        Depreciation_Cost_GAC = Initial_Unit_Cost_GAC/L #$/year
        Initial_Unit_Cost_EC = US_Initial_Unit_Cost_EC[j,0]+(InCountry_Initial_Unit_Cost_EC[j,0]*PLR[j,0])
        U_Electrode_EC_Replacement = U_Electrode_EC[j,0]*((L/Electrode_EC_Lifetime[j,0])-1)
        if (U_Electrode_EC_Replacement+U_Electrode_EC[j,0]) <= U_Electrode_EC[j,0]:
            U_Electrode_EC_Replacement = 0
        U_Stirrer_EC_Replacement = U_Stirrer_EC[j,0]*((L/Stirrer_Lifetime[j,0])-1)
        if (U_Stirrer_EC_Replacement+U_Stirrer_EC[j,0]) <= U_Stirrer_EC[j,0]:
            U_Stirrer_EC_Replacement = 0
        U_Switch_Replacement = U_Switch[j,0]*2*((L/Switch_Lifetime[j,0])-1)
        if (U_Switch_Replacement+(U_Switch[j,0]*2)) <= U_Switch[j,0]*2:
            U_Switch_Replacement = 0
        Replacement_Cost_EC = (U_Electrode_EC_Replacement+U_Stirrer_EC_Replacement+U_Switch_Replacement)/L #/year
        Depreciation_Cost_EC = ((Initial_Unit_Cost_EC-U_Electrode_EC[j,0]-U_Stirrer_EC[j,0]-(U_Switch[j,0]*2))/L)+(U_Electrode_EC[j,0]/Electrode_EC_Lifetime[j,0])+(U_Stirrer_EC[j,0]/Stirrer_Lifetime[j,0])+((U_Switch[j,0]*2)/Switch_Lifetime[j,0]) #$/year
        Initial_Unit_Cost_Misc = US_Initial_Unit_Cost_Misc[j,0]+(InCountry_Initial_Unit_Cost_Misc[j,0]*PLR[j,0])
        U_Pump_Misc_Replacement = U_Pump_Misc[j,0]*((L/U_Pump_Misc_Lifetime[j,0])-1)
        if (U_Pump_Misc_Replacement+U_Pump_Misc[j,0]) <= U_Pump_Misc[j,0]:
            U_Pump_Misc_Replacement = 0
        Replacement_Cost_Misc = (U_Pump_Misc_Replacement)/L #/year
        Depreciation_Cost_Misc = Initial_Unit_Cost_Misc/L #$/year
        Initial_Unit_Cost_Controls = US_Initial_Unit_Cost_Controls[j,0]+(InCountry_Initial_Unit_Cost_Controls[j,0]*PLR[j,0])
        Energy_Annual_Controls = ((25*24*365)/1000) #kWh/yr
        Depreciation_Cost_Controls = Initial_Unit_Cost_Controls/L #$/year
        Initial_Unit_Cost_Overall = Initial_Unit_Cost_UF+Initial_Unit_Cost_GAC+Initial_Unit_Cost_EC+Initial_Unit_Cost_Misc+Initial_Unit_Cost_Controls #$
        Replacement_Cost_Overall = Replacement_Cost_UF+Replacement_Cost_EC+Replacement_Cost_Misc #$/year
        Material_Cost_Overall = Replacement_Cost_Overall+Initial_Unit_Cost_Overall
        Energy_Overall[j,0] = Energy_Annual_UF+Energy_Annual_EC+Energy_Annual_Misc+Energy_Annual_Controls #kWh/year
        Energy_Cost_Overall = Energy_Overall[j,0]*U_Energy[j,0] #$/year
        Monthly_Work_Days = lhs.lhs_uniform(20,25,nsamples) #days/month
        Daily_Construction_Wage=Monthly_Construction_Wage[j,0]/Monthly_Work_Days[j,0] #$/day
        Construction_Time=lhs.lhs_uniform(2,4,nsamples) #days/toilet assembly
        Labor_Construction_Cost_Overall = Daily_Construction_Wage*Construction_Time[j,0] #$
        Initial_Construction_Cost_Overall = (Initial_Unit_Cost_Overall)+Labor_Construction_Cost_Overall #$
        Daily_Maintenance_Wage=Monthly_Maintenance_Wage[j,0]/Monthly_Work_Days[j,0]
        Maintenance_Frequency = lhs.lhs_uniform(1,2,nsamples) #times/year
        Maintenance_Time = lhs.lhs_uniform(0.25,1,nsamples) #days/maintenance
        Operation_Maintenance_Cost_Overall = Daily_Maintenance_Wage*Maintenance_Frequency[j,0]*Maintenance_Time[j,0]#$/year
        Labor_Cost_Overall = Operation_Maintenance_Cost_Overall+Labor_Construction_Cost_Overall
        Ongoing_Cost_Overall = Energy_Cost_Overall+Media_Cost_GAC+Operation_Maintenance_Cost_Overall+Replacement_Cost_Overall #$/year   
        Depreciation_Cost_Overall = Depreciation_Cost_UF+Depreciation_Cost_GAC+Depreciation_Cost_EC+Depreciation_Cost_Misc+Depreciation_Cost_Controls #$/year
        Cost_Overall = 0
        Profits_Overall = 0
        Prelim_Present_OM_Replacement_Cost_Overall = 0
        Present_Energy_Cost_Overall = 0
        Present_Depreciation_Cost_Overall = 0
        p = 1
        while p <= L:
            Required_User_Fee_newterm_Cost_Overall = (1/((1+Discount_Rate[j,0])**p))*(((Ongoing_Cost_Overall+Depreciation_Cost_Overall)*(1-Income_Tax))-Depreciation_Cost_Overall)
            Required_User_Fee_newterm_Profits_Overall = (1/((1+Discount_Rate[j,0])**p))*365*U*(1-Income_Tax)
            Cost_Overall = Cost_Overall+Required_User_Fee_newterm_Cost_Overall
            Profits_Overall = Profits_Overall+Required_User_Fee_newterm_Profits_Overall
            Prelim_Present_OM_Replacement_newterm_Cost_Overall = (1/((1+Discount_Rate[j,0])**p))*((Operation_Maintenance_Cost_Overall+Replacement_Cost_Overall+Media_Cost_GAC)*(1-Income_Tax))
            Prelim_Present_OM_Replacement_Cost_Overall = Prelim_Present_OM_Replacement_Cost_Overall+Prelim_Present_OM_Replacement_newterm_Cost_Overall
            Present_Energy_newterm_Cost_Overall = (1/((1+Discount_Rate[j,0])**p))*(Energy_Cost_Overall*(1-Income_Tax))
            Present_Energy_Cost_Overall = Present_Energy_Cost_Overall+Present_Energy_newterm_Cost_Overall
            Present_Depreciation_newterm_Cost_Overall = (1/((1+Discount_Rate[j,0])**p))*(((Depreciation_Cost_Overall)*(1-Income_Tax))-Depreciation_Cost_Overall)
            Present_Depreciation_Cost_Overall = Present_Depreciation_Cost_Overall+Present_Depreciation_newterm_Cost_Overall
            p = p+1
        Prelim_Present_Initial_OM_Cost_Overall = Initial_Construction_Cost_Overall+Prelim_Present_OM_Replacement_Cost_Overall
        Depreciation_Portion_Initial_Construction_Cost_Overall = Initial_Construction_Cost_Overall/Prelim_Present_Initial_OM_Cost_Overall
        Depreciation_Portion_OM_Replacement_Cost_Overall = Prelim_Present_OM_Replacement_Cost_Overall/Prelim_Present_Initial_OM_Cost_Overall
        Present_Initial_Construction_Cost_Overall = Initial_Construction_Cost_Overall+(Present_Depreciation_Cost_Overall*Depreciation_Portion_Initial_Construction_Cost_Overall)
        Present_OM_Replacement_Cost_Overall = Prelim_Present_OM_Replacement_Cost_Overall+(Present_Depreciation_Cost_Overall*Depreciation_Portion_OM_Replacement_Cost_Overall)
        Present_Total_Cost_Overall = Present_Initial_Construction_Cost_Overall+Present_OM_Replacement_Cost_Overall+Present_Energy_Cost_Overall
        Portion_Initial_Construction_Cost_Overall = Present_Initial_Construction_Cost_Overall/Present_Total_Cost_Overall
        Portion_OM_Replacement_Cost_Overall = Present_OM_Replacement_Cost_Overall/Present_Total_Cost_Overall
        Portion_Energy_Cost_Overall = Present_Energy_Cost_Overall/Present_Total_Cost_Overall
        Required_User_Fee_Overall[j,0] = (Initial_Construction_Cost_Overall+Cost_Overall)/Profits_Overall #$/user/year
        Required_User_Fee_Initial_Overall[j,0]=Required_User_Fee_Overall[j,0]*Portion_Initial_Construction_Cost_Overall
        Required_User_Fee_OM_Overall[j,0]=Required_User_Fee_Overall[j,0]*Portion_OM_Replacement_Cost_Overall
        Required_User_Fee_Energy_Overall[j,0]=Required_User_Fee_Overall[j,0]*Portion_Energy_Cost_Overall
        Percent_Initial[j,0]=Required_User_Fee_Initial_Overall[j,0]/Required_User_Fee_Overall[j,0]
        Percent_OM[j,0]=Required_User_Fee_OM_Overall[j,0]/Required_User_Fee_Overall[j,0]
        Percent_Energy[j,0]=Required_User_Fee_Energy_Overall[j,0]/Required_User_Fee_Overall[j,0]
        Percent_Materials[j,0] = ((Initial_Unit_Cost_Overall/Initial_Construction_Cost_Overall)*Percent_Initial[j,0])+((Replacement_Cost_Overall/(Replacement_Cost_Overall+Operation_Maintenance_Cost_Overall+Media_Cost_GAC))*Percent_OM[j,0])
        Percent_Labor[j,0] = ((Labor_Construction_Cost_Overall/Initial_Construction_Cost_Overall)*Percent_Initial[j,0])+((Operation_Maintenance_Cost_Overall/(Replacement_Cost_Overall+Operation_Maintenance_Cost_Overall+Media_Cost_GAC))*Percent_OM[j,0])
        Percent_GAC_Media[j,0] = ((Annual_GAC_Required*U_Media_GAC[j,0])/(Replacement_Cost_Overall+Operation_Maintenance_Cost_Overall+Media_Cost_GAC))*Percent_OM[j,0]
        Percent_Zeolites[j,0] = ((N_Removal_Cost+P_Removal_Cost)/(Replacement_Cost_Overall+Operation_Maintenance_Cost_Overall+Media_Cost_GAC))*Percent_OM[j,0]
        E_Impacts_Ozone[j,0] = ((Energy_Overall[j,0]*E_Per_Nuclear*E_Nuclear_Ozone)+(Energy_Overall[j,0]*E_Per_Hydro*E_Hydro_Ozone)+(Energy_Overall[j,0]*E_Per_Geo*E_Geothermal_Ozone)+(Energy_Overall[j,0]*E_Per_Wind*E_Wind_Ozone[j,0])+(Energy_Overall[j,0]*E_Per_Solar*E_Solar_Ozone[j,0])+(Energy_Overall[j,0]*E_Per_Waste*E_Waste_Ozone)+(Energy_Overall[j,0]*E_Per_Coal*E_Coal_Ozone)+(Energy_Overall[j,0]*E_Per_Oil*E_Oil_Ozone)+(Energy_Overall[j,0]*E_Per_Gas*E_Gas_Ozone[j,0]))/(U*Years_Days)
        E_Impacts_GHG[j,0] = ((Energy_Overall[j,0]*E_Per_Nuclear*E_Nuclear_GHG)+(Energy_Overall[j,0]*E_Per_Hydro*E_Hydro_GHG[j,0])+(Energy_Overall[j,0]*E_Per_Geo*E_Geothermal_GHG)+(Energy_Overall[j,0]*E_Per_Wind*E_Wind_GHG[j,0])+(Energy_Overall[j,0]*E_Per_Solar*E_Solar_GHG[j,0])+(Energy_Overall[j,0]*E_Per_Waste*E_Waste_GHG)+(Energy_Overall[j,0]*E_Per_Coal*E_Coal_GHG)+(Energy_Overall[j,0]*E_Per_Oil*E_Oil_GHG)+(Energy_Overall[j,0]*E_Per_Gas*E_Gas_GHG[j,0]))/(U*Years_Days)
        E_Impacts_Smog[j,0] = ((Energy_Overall[j,0]*E_Per_Nuclear*E_Nuclear_Smog)+(Energy_Overall[j,0]*E_Per_Hydro*E_Hydro_Smog)+(Energy_Overall[j,0]*E_Per_Geo*E_Geothermal_Smog)+(Energy_Overall[j,0]*E_Per_Wind*E_Wind_Smog[j,0])+(Energy_Overall[j,0]*E_Per_Solar*E_Solar_Smog[j,0])+(Energy_Overall[j,0]*E_Per_Waste*E_Waste_Smog)+(Energy_Overall[j,0]*E_Per_Coal*E_Coal_Smog)+(Energy_Overall[j,0]*E_Per_Oil*E_Oil_Smog)+(Energy_Overall[j,0]*E_Per_Gas*E_Gas_Smog[j,0]))/(U*Years_Days)
        E_Impacts_Acid[j,0] = ((Energy_Overall[j,0]*E_Per_Nuclear*E_Nuclear_Acid)+(Energy_Overall[j,0]*E_Per_Hydro*E_Hydro_Acid)+(Energy_Overall[j,0]*E_Per_Geo*E_Geothermal_Acid)+(Energy_Overall[j,0]*E_Per_Wind*E_Wind_Acid[j,0])+(Energy_Overall[j,0]*E_Per_Solar*E_Solar_Acid[j,0])+(Energy_Overall[j,0]*E_Per_Waste*E_Waste_Acid)+(Energy_Overall[j,0]*E_Per_Coal*E_Coal_Acid)+(Energy_Overall[j,0]*E_Per_Oil*E_Oil_Acid)+(Energy_Overall[j,0]*E_Per_Gas*E_Gas_Acid[j,0]))/(U*Years_Days)
        E_Impacts_Eutro[j,0] = ((Energy_Overall[j,0]*E_Per_Nuclear*E_Nuclear_Eutro)+(Energy_Overall[j,0]*E_Per_Hydro*E_Hydro_Eutro)+(Energy_Overall[j,0]*E_Per_Geo*E_Geothermal_Eutro)+(Energy_Overall[j,0]*E_Per_Wind*E_Wind_Eutro[j,0])+(Energy_Overall[j,0]*E_Per_Solar*E_Solar_Eutro[j,0])+(Energy_Overall[j,0]*E_Per_Waste*E_Waste_Eutro)+(Energy_Overall[j,0]*E_Per_Coal*E_Coal_Eutro)+(Energy_Overall[j,0]*E_Per_Oil*E_Oil_Eutro)+(Energy_Overall[j,0]*E_Per_Gas*E_Gas_Eutro[j,0]))/(U*Years_Days)
        E_Impacts_Carcin[j,0] = ((Energy_Overall[j,0]*E_Per_Nuclear*E_Nuclear_Carcin)+(Energy_Overall[j,0]*E_Per_Hydro*E_Hydro_Carcin)+(Energy_Overall[j,0]*E_Per_Geo*E_Geothermal_Carcin)+(Energy_Overall[j,0]*E_Per_Wind*E_Wind_Carcin[j,0])+(Energy_Overall[j,0]*E_Per_Solar*E_Solar_Carcin[j,0])+(Energy_Overall[j,0]*E_Per_Waste*E_Waste_Carcin)+(Energy_Overall[j,0]*E_Per_Coal*E_Coal_Carcin)+(Energy_Overall[j,0]*E_Per_Oil*E_Oil_Carcin)+(Energy_Overall[j,0]*E_Per_Gas*E_Gas_Carcin[j,0]))/(U*Years_Days)
        E_Impacts_NonCar[j,0] = ((Energy_Overall[j,0]*E_Per_Nuclear*E_Nuclear_NonCar)+(Energy_Overall[j,0]*E_Per_Hydro*E_Hydro_NonCar)+(Energy_Overall[j,0]*E_Per_Geo*E_Geothermal_NonCar)+(Energy_Overall[j,0]*E_Per_Wind*E_Wind_NonCar[j,0])+(Energy_Overall[j,0]*E_Per_Solar*E_Solar_NonCar[j,0])+(Energy_Overall[j,0]*E_Per_Waste*E_Waste_NonCar)+(Energy_Overall[j,0]*E_Per_Coal*E_Coal_NonCar)+(Energy_Overall[j,0]*E_Per_Oil*E_Oil_NonCar)+(Energy_Overall[j,0]*E_Per_Gas*E_Gas_NonCar[j,0]))/(U*Years_Days)
        E_Impacts_Resp[j,0] = ((Energy_Overall[j,0]*E_Per_Nuclear*E_Nuclear_Resp)+(Energy_Overall[j,0]*E_Per_Hydro*E_Hydro_Resp)+(Energy_Overall[j,0]*E_Per_Geo*E_Geothermal_Resp)+(Energy_Overall[j,0]*E_Per_Wind*E_Wind_Resp[j,0])+(Energy_Overall[j,0]*E_Per_Solar*E_Solar_Resp[j,0])+(Energy_Overall[j,0]*E_Per_Waste*E_Waste_Resp)+(Energy_Overall[j,0]*E_Per_Coal*E_Coal_Resp)+(Energy_Overall[j,0]*E_Per_Oil*E_Oil_Resp)+(Energy_Overall[j,0]*E_Per_Gas*E_Gas_Resp[j,0]))/(U*Years_Days)
        E_Impacts_EcoTox[j,0] = ((Energy_Overall[j,0]*E_Per_Nuclear*E_Nuclear_EcoTox)+(Energy_Overall[j,0]*E_Per_Hydro*E_Hydro_EcoTox)+(Energy_Overall[j,0]*E_Per_Geo*E_Geothermal_EcoTox)+(Energy_Overall[j,0]*E_Per_Wind*E_Wind_EcoTox[j,0])+(Energy_Overall[j,0]*E_Per_Solar*E_Solar_EcoTox[j,0])+(Energy_Overall[j,0]*E_Per_Waste*E_Waste_EcoTox)+(Energy_Overall[j,0]*E_Per_Coal*E_Coal_EcoTox)+(Energy_Overall[j,0]*E_Per_Oil*E_Oil_EcoTox)+(Energy_Overall[j,0]*E_Per_Gas*E_Gas_EcoTox[j,0]))/(U*Years_Days)
        E_Impacts_FFD[j,0] = ((Energy_Overall[j,0]*E_Per_Nuclear*E_Nuclear_FFD)+(Energy_Overall[j,0]*E_Per_Hydro*E_Hydro_FFD)+(Energy_Overall[j,0]*E_Per_Geo*E_Geothermal_FFD)+(Energy_Overall[j,0]*E_Per_Wind*E_Wind_FFD[j,0])+(Energy_Overall[j,0]*E_Per_Solar*E_Solar_FFD[j,0])+(Energy_Overall[j,0]*E_Per_Waste*E_Waste_FFD)+(Energy_Overall[j,0]*E_Per_Coal*E_Coal_FFD)+(Energy_Overall[j,0]*E_Per_Oil*E_Oil_FFD)+(Energy_Overall[j,0]*E_Per_Gas*E_Gas_FFD[j,0]))/(U*Years_Days)
        
        E_CO2_Intensity[j,0] = E_Impacts_GHG[j,0]/(Energy_Overall[j,0]/(U*Years_Days))
        
        Impacts_GAC_Ozone[j,0] = ((Annual_GAC_Required*GAC_Ozone[j,0]))/(U*Years_Days)
        Impacts_GAC_GHG[j,0] = ((Annual_GAC_Required*GAC_GHG[j,0]))/(U*Years_Days)
        Impacts_GAC_Smog[j,0] = ((Annual_GAC_Required*GAC_Smog[j,0]))/(U*Years_Days)
        Impacts_GAC_Acid[j,0] = ((Annual_GAC_Required*GAC_Acid[j,0]))/(U*Years_Days)
        Impacts_GAC_Eutro[j,0] = ((Annual_GAC_Required*GAC_Eutro[j,0]))/(U*Years_Days)
        Impacts_GAC_Carcin[j,0] = ((Annual_GAC_Required*GAC_Carcin[j,0]))/(U*Years_Days)
        Impacts_GAC_NonCar[j,0] = ((Annual_GAC_Required*GAC_NonCar[j,0]))/(U*Years_Days)
        Impacts_GAC_Resp[j,0] = ((Annual_GAC_Required*GAC_Resp[j,0]))/(U*Years_Days)
        Impacts_GAC_EcoTox[j,0] = ((Annual_GAC_Required*GAC_EcoTox[j,0]))/(U*Years_Days)
        Impacts_GAC_FFD[j,0] = ((Annual_GAC_Required*GAC_FFD[j,0]))/(U*Years_Days)
        
        Impacts_Zeo_Ozone[j,0] = ((Zeolite_Total[j,0]*Zeo_Ozone[i,0]))/(U*Years_Days)
        Impacts_Zeo_GHG[j,0] = ((Zeolite_Total[j,0]*Zeo_GHG[i,0]))/(U*Years_Days)
        Impacts_Zeo_Smog[j,0] = ((Zeolite_Total[j,0]*Zeo_Smog[i,0]))/(U*Years_Days)
        Impacts_Zeo_Acid[j,0] = ((Zeolite_Total[j,0]*Zeo_Acid[i,0]))/(U*Years_Days)
        Impacts_Zeo_Eutro[j,0] = ((Zeolite_Total[j,0]*Zeo_Eutro[i,0]))/(U*Years_Days)
        Impacts_Zeo_Carcin[j,0] = ((Zeolite_Total[j,0]*Zeo_Carcin[i,0]))/(U*Years_Days)
        Impacts_Zeo_NonCar[j,0] = ((Zeolite_Total[j,0]*Zeo_NonCar[i,0]))/(U*Years_Days)
        Impacts_Zeo_Resp[j,0] = ((Zeolite_Total[j,0]*Zeo_Resp[i,0]))/(U*Years_Days)
        Impacts_Zeo_EcoTox[j,0] = ((Zeolite_Total[j,0]*Zeo_EcoTox[i,0]))/(U*Years_Days)
        Impacts_Zeo_FFD[j,0] = ((Zeolite_Total[j,0]*Zeo_FFD[i,0]))/(U*Years_Days)
        
    Assumed_Parameters_Cost = np.concatenate((Daily_Flushes, Flush_Volume, Membrane_Flux, Velocity_Crossflow, Pressure_Membrane, Fill_Fraction_GAC_Column, UF_GAC_N_P_Removal, Clinoptilolite_Cost, Polonite_Cost, Clinoptilolite_Capacity, Polonite_Capacity, N_Content_Protein, N_P_Excretion, N_Urine, P_Content_A_Protein, P_Content_V_Protein, P_Urine, Seperation_Efficiency, Density_GAC, Lifetime_GAC, Power_Required_Treatment_EC, Current_EC, Power_Stirrer, Flowrate_Discharge, Pump_UF_Lifetime, Membrane_UF_Lifetime, Switch_Lifetime, Valve_UF_Lifetime, Electrode_EC_Lifetime, Stirrer_Lifetime, U_Pump_Misc_Lifetime, Discount_Rate, U_Pump_UF, U_Membrane_UF, U_Valve_UF, U_Tank_UF, U_Switch, U_Column_GAC, U_Stirrer_EC, U_Electrode_EC, U_Pump_Misc, US_Initial_Unit_Cost_UF, InCountry_Initial_Unit_Cost_UF, US_Initial_Unit_Cost_GAC, InCountry_Initial_Unit_Cost_GAC, US_Initial_Unit_Cost_EC, InCountry_Initial_Unit_Cost_EC, US_Initial_Unit_Cost_Controls, InCountry_Initial_Unit_Cost_Controls, US_Initial_Unit_Cost_Misc, InCountry_Initial_Unit_Cost_Misc, U_Media_GAC, Total_Protein, Waste, PLR, U_Energy, Monthly_Construction_Wage, Monthly_Maintenance_Wage, Monthly_Work_Days), axis=1)
    rho_all, p_all = stats.spearmanr(Assumed_Parameters_Cost, Required_User_Fee_Overall)       
    SpearmansCost = pd.DataFrame(rho_all, columns = ['Daily_Flushes', 'Flush_Volume', 'Membrane_Flux', 'Velocity_Crossflow', 'Pressure_Membrane', 'Fill_Fraction_GAC_Column', 'UF_GAC_N_P_Removal', 'Clinoptilolite_Cost', 'Polonite_Cost', 'Clinoptilolite_Capacity', 'Polonite_Capacity', 'N_Content_Protein', 'N_P_Excretion', 'N_Urine', 'P_Content_A_Protein', 'P_Content_V_Protein', 'P_Urine', 'Seperation_Efficiency', 'Density_GAC', 'Lifetime_GAC', 'Power_Required_Treatment_EC', 'Current_EC', 'Power_Stirrer', 'Flowrate_Discharge', 'Pump_UF_Lifetime', 'Membrane_UF_Lifetime', 'Switch_Lifetime', 'Valve_UF_Lifetime', 'Electrode_EC_Lifetime', 'Stirrer_Lifetime', 'U_Pump_Misc_Lifetime', 'Discount_Rate', 'U_Pump_UF', 'U_Membrane_UF', 'U_Valve_UF', 'U_Tank_UF', 'U_Switch', 'U_Column_GAC', 'U_Stirrer_EC', 'U_Electrode_EC', 'U_Pump_Misc', 'US_Initial_Unit_Cost_UF', 'InCountry_Initial_Unit_Cost_UF', 'US_Initial_Unit_Cost_GAC', 'InCountry_Initial_Unit_Cost_GAC', 'US_Initial_Unit_Cost_EC', 'InCountry_Initial_Unit_Cost_EC', 'US_Initial_Unit_Cost_Controls', 'InCountry_Initial_Unit_Cost_Controls', 'US_Initial_Unit_Cost_Misc', 'InCountry_Initial_Unit_Cost_Misc', 'U_Media_GAC', 'Total_Protein', 'Waste', 'PLR', 'U_Energy', 'Monthly_Construction_Wage', 'Monthly_Maintenance_Wage', 'Monthly_Work_Days', 'Required_User_Fee_Overall'], index = ['Daily_Flushes', 'Flush_Volume', 'Membrane_Flux', 'Velocity_Crossflow', 'Pressure_Membrane', 'Fill_Fraction_GAC_Column', 'UF_GAC_N_P_Removal', 'Clinoptilolite_Cost', 'Polonite_Cost', 'Clinoptilolite_Capacity', 'Polonite_Capacity', 'N_Content_Protein', 'N_P_Excretion', 'N_Urine', 'P_Content_A_Protein', 'P_Content_V_Protein', 'P_Urine', 'Seperation_Efficiency', 'Density_GAC', 'Lifetime_GAC', 'Power_Required_Treatment_EC', 'Current_EC', 'Power_Stirrer', 'Flowrate_Discharge', 'Pump_UF_Lifetime', 'Membrane_UF_Lifetime', 'Switch_Lifetime', 'Valve_UF_Lifetime', 'Electrode_EC_Lifetime', 'Stirrer_Lifetime', 'U_Pump_Misc_Lifetime', 'Discount_Rate', 'U_Pump_UF', 'U_Membrane_UF', 'U_Valve_UF', 'U_Tank_UF', 'U_Switch', 'U_Column_GAC', 'U_Stirrer_EC', 'U_Electrode_EC', 'U_Pump_Misc', 'US_Initial_Unit_Cost_UF', 'InCountry_Initial_Unit_Cost_UF', 'US_Initial_Unit_Cost_GAC', 'InCountry_Initial_Unit_Cost_GAC', 'US_Initial_Unit_Cost_EC', 'InCountry_Initial_Unit_Cost_EC', 'US_Initial_Unit_Cost_Controls', 'InCountry_Initial_Unit_Cost_Controls', 'US_Initial_Unit_Cost_Misc', 'InCountry_Initial_Unit_Cost_Misc', 'U_Media_GAC', 'Total_Protein', 'Waste', 'PLR', 'U_Energy', 'Monthly_Construction_Wage', 'Monthly_Maintenance_Wage', 'Monthly_Work_Days', 'Required_User_Fee_Overall'])
    SpearmansCoefCost = SpearmansCost['Required_User_Fee_Overall']
    #modSpearmansCost = SpearmansCost.drop(['Required_User_Fee_Overall'])
    #SpearmansCoefCost = modSpearmansCost['Required_User_Fee_Overall']
    
    Results_Energy_Overall[:,i] = Energy_Overall[:,0]
    Results_Cost_Total[:,i] = Required_User_Fee_Overall[:,0]
    Results_Cost_Initial[:,i] = Required_User_Fee_Initial_Overall[:,0]
    Results_Cost_OM[:,i] = Required_User_Fee_OM_Overall[:,0]
    Results_Cost_Energy[:,i] = Required_User_Fee_Energy_Overall[:,0]
    Results_Cost_Percent_Initial[:,i] = Percent_Initial[:,0]
    Results_Cost_Percent_OM[:,i] =Percent_OM[:,0]
    Results_Percent_Energy[:,i] = Percent_Energy[:,0]
    Results_Percent_Materials[:,i] = Percent_Materials[:,0]
    Results_Percent_Labor[:,i] = Percent_Labor[:,0]
    Results_Percent_GAC_Media[:,i] = Percent_GAC_Media[:,0]
    Results_Percent_Zeolites[:,i] = Percent_Zeolites[:,0]
    Results_E_Ozone[:,i] = E_Impacts_Ozone[:,0]
    Results_E_GHG[:,i] = E_Impacts_GHG[:,0]
    Results_E_Smog[:,i] = E_Impacts_Smog[:,0]
    Results_E_Acid[:,i] = E_Impacts_Acid[:,0]
    Results_E_Eutro[:,i] = E_Impacts_Eutro[:,0]
    Results_E_Carcin[:,i] = E_Impacts_Carcin[:,0]
    Results_E_NonCar[:,i] = E_Impacts_NonCar[:,0]
    Results_E_Resp[:,i] = E_Impacts_Resp[:,0]
    Results_E_EcoTox[:,i] = E_Impacts_EcoTox[:,0]
    Results_E_FFD[:,i] = E_Impacts_FFD[:,0]
    Results_Zeo_Ozone[:,i] = Impacts_Zeo_Ozone[:,0]
    Results_Zeo_GHG[:,i] = Impacts_Zeo_GHG[:,0]
    Results_Zeo_Smog[:,i] = Impacts_Zeo_Smog[:,0]
    Results_Zeo_Acid[:,i] = Impacts_Zeo_Acid[:,0]
    Results_Zeo_Eutro[:,i] = Impacts_Zeo_Eutro[:,0]
    Results_Zeo_Carcin[:,i] = Impacts_Zeo_Carcin[:,0]
    Results_Zeo_NonCar[:,i] = Impacts_Zeo_NonCar[:,0]
    Results_Zeo_Resp[:,i] = Impacts_Zeo_Resp[:,0]
    Results_Zeo_EcoTox[:,i] = Impacts_Zeo_EcoTox[:,0]
    Results_Zeo_FFD[:,i] = Impacts_Zeo_FFD[:,0]
    Results_E_CO2_Intensity[:,i] = E_CO2_Intensity[:,0]
    #Results_Energy_Demand[:,i] = Energy_Demand[:,0]
    #Results_SpearmansCoefCost[:,i] = SpearmansCoefCost[:,0]
    
    Results_PLR[:,i] = PLR[:,0]
    Results_Waste[:,i] = Waste[:,0]
    Results_Total_Protein[:,i] = Total_Protein[:,0]
    Results_U_Energy[:,i] = U_Energy[:,0]
    Results_Monthly_Construction_Wage[:,i] = Monthly_Construction_Wage[:,0]
    Results_Monthly_Maintenance_Wage[:,i] = Monthly_Maintenance_Wage[:,0] 
    
    print(i,j)

#%%
#allCountriesRes.append(SpearmansCost)
#allCountriesCoefCost.append(SpearmansCoefCost)
#allCountriesCoefEmissions.append(SpearmansCoefEmissions)

#dfallcountriesres = pd.DataFrame(allCountriesRes, index = Country)
#dfallcountriescoefcost = pd.DataFrame(allCountriesCoefCost, index = Country)
#writer = pd.ExcelWriter(r'C:\Users\Owner\Dropbox\_Andrus-Guest_Shared\Research\Results\spearmans.xlsx', engine = 'xlsxwriter')
#export_excel = dfallcountriesres.to_excel(writer, sheet_name = 'I am the cutest Becca')
#export_excel = dfallcountriescoefcost.to_excel(writer, sheet_name = 'Cost')
#export_excel = dfallcountriescoefemissions.to_excel(writer, sheet_name = 'Emissions')
#writer.save()
#%%

Results_Ozone=np.full((1000,246),0.0)
Results_GHG=np.full((1000,246),0.0)
Results_Smog=np.full((1000,246),0.0)
Results_Acid=np.full((1000,246),0.0)
Results_Eutro=np.full((1000,246),0.0)
Results_Carcin=np.full((1000,246),0.0)
Results_NonCar=np.full((1000,246),0.0)
Results_Resp=np.full((1000,246),0.0)
Results_EcoTox=np.full((1000,246),0.0)
Results_FFD=np.full((1000,246),0.0)
BOM = []
        
for k in range(0,246):
    Unit_Process=df2.Unit_Process[k]
    Size = df2.Size[k]
    Min = df2.Min[k]
    Max = df2.Max[k]
    Ozone = df3[Unit_Process][0]
    Ozone = lhs.lhs_uniform((Ozone*Size*Min)/(U*L*Years_Days),(Ozone*Size*Max)/(U*L*Years_Days),nsamples)
    BOM.append(df2.BOM[k])
    Results_Ozone[:,k]=Ozone[:,0]
    GHG = df3[Unit_Process][1]
    GHG = lhs.lhs_uniform((GHG*Size*Min)/(U*L*Years_Days),(GHG*Size*Max)/(U*L*Years_Days),nsamples)
    Results_GHG[:,k]=GHG[:,0]
    Smog = df3[Unit_Process][2]
    Smog = lhs.lhs_uniform((Smog*Size*Min)/(U*L*Years_Days),(Smog*Size*Max)/(U*L*Years_Days),nsamples)
    Results_Smog[:,k]=Smog[:,0]
    Acid = df3[Unit_Process][3]
    Acid = lhs.lhs_uniform((Acid*Size*Min)/(U*L*Years_Days),(Acid*Size*Max)/(U*L*Years_Days),nsamples)
    Results_Acid[:,k]=Acid[:,0]
    Eutro = df3[Unit_Process][4]
    Eutro = lhs.lhs_uniform((Eutro*Size*Min)/(U*L*Years_Days),(Eutro*Size*Max)/(U*L*Years_Days),nsamples)
    Results_Eutro[:,k]=Eutro[:,0]
    Carcin = df3[Unit_Process][5]
    Carcin = lhs.lhs_uniform((Carcin*Size*Min)/(U*L*Years_Days),(Carcin*Size*Max)/(U*L*Years_Days),nsamples)
    Results_Carcin[:,k]=Carcin[:,0]
    NonCar = df3[Unit_Process][6]
    NonCar = lhs.lhs_uniform((NonCar*Size*Min)/(U*L*Years_Days),(NonCar*Size*Max)/(U*L*Years_Days),nsamples)
    Results_NonCar[:,k]=NonCar[:,0]
    Resp = df3[Unit_Process][7]
    Resp = lhs.lhs_uniform((Resp*Size*Min)/(U*L*Years_Days),(Resp*Size*Max)/(U*L*Years_Days),nsamples)
    Results_Resp[:,k]=Resp[:,0]
    EcoTox = df3[Unit_Process][8]
    EcoTox = lhs.lhs_uniform((EcoTox*Size*Min)/(U*L*Years_Days),(EcoTox*Size*Max)/(U*L*Years_Days),nsamples)
    Results_EcoTox[:,k]=Ozone[:,0]
    FFD = df3[Unit_Process][9]
    FFD = lhs.lhs_uniform((FFD*Size*Min)/(U*L*Years_Days),(FFD*Size*Max)/(U*L*Years_Days),nsamples)
    Results_FFD[:,k]=FFD[:,0]
    
dfozone = pd.DataFrame(Results_Ozone, columns = BOM)
dfghg = pd.DataFrame(Results_GHG, columns = BOM)
dfsmog = pd.DataFrame(Results_Smog, columns = BOM)
dfacid = pd.DataFrame(Results_Acid, columns = BOM)
dfeutro = pd.DataFrame(Results_Eutro, columns = BOM)
dfcarcin = pd.DataFrame(Results_Carcin, columns = BOM)
dfnoncar = pd.DataFrame(Results_NonCar, columns = BOM)
dfresp = pd.DataFrame(Results_Resp, columns = BOM)
dfecotox = pd.DataFrame(Results_EcoTox, columns = BOM)
dfffd = pd.DataFrame(Results_FFD, columns = BOM) 

#%%
dfcost = pd.DataFrame(Results_Cost_Total, columns = Country)    
dfcostinitial = pd.DataFrame(Results_Cost_Initial, columns = Country)    
dfcostOM = pd.DataFrame(Results_Cost_OM, columns = Country)    
dfcostenergy = pd.DataFrame(Results_Cost_Energy, columns = Country)    
dfcostperinitial = pd.DataFrame(Results_Cost_Percent_Initial, columns = Country) 
dfcostperOM = pd.DataFrame(Results_Cost_Percent_OM, columns = Country) 
dfcostperenergy = pd.DataFrame(Results_Percent_Energy, columns = Country) 
dfcostpermaterials = pd.DataFrame(Results_Percent_Materials, columns = Country) 
dfcostperlabor = pd.DataFrame(Results_Percent_Labor, columns = Country) 
dfcostpergac = pd.DataFrame(Results_Percent_GAC_Media, columns = Country) 
dfcostperzeolites = pd.DataFrame(Results_Percent_Zeolites, columns = Country)
#dfenergydemand = pd.DataFrame(Results_Energy_Demand, columns = Country)
dfeozone =  pd.DataFrame(Results_E_Ozone, columns = Country)
dfeghg =  pd.DataFrame(Results_E_GHG, columns = Country)
dfesmog =  pd.DataFrame(Results_E_Smog, columns = Country)
dfeacid =  pd.DataFrame(Results_E_Acid, columns = Country)
dfeeutro =  pd.DataFrame(Results_E_Eutro, columns = Country)
dfecarcin =  pd.DataFrame(Results_E_Carcin, columns = Country)
dfenoncar =  pd.DataFrame(Results_E_NonCar, columns = Country)
dferesp =  pd.DataFrame(Results_E_Resp, columns = Country)
dfeecotox =  pd.DataFrame(Results_E_EcoTox, columns = Country)
dfeffd =  pd.DataFrame(Results_E_FFD, columns = Country)
dfzeoozone =  pd.DataFrame(Results_Zeo_Ozone, columns = Country)
dfzeoghg =  pd.DataFrame(Results_Zeo_GHG, columns = Country)
dfzeosmog =  pd.DataFrame(Results_Zeo_Smog, columns = Country)
dfzeoacid =  pd.DataFrame(Results_Zeo_Acid, columns = Country)
dfzeoeutro =  pd.DataFrame(Results_Zeo_Eutro, columns = Country)
dfzeocarcin =  pd.DataFrame(Results_Zeo_Carcin, columns = Country)
dfzeononcar =  pd.DataFrame(Results_Zeo_NonCar, columns = Country)
dfzeoresp =  pd.DataFrame(Results_Zeo_Resp, columns = Country)
dfzeoecotox =  pd.DataFrame(Results_Zeo_EcoTox, columns = Country)
dfzeoffd =  pd.DataFrame(Results_Zeo_FFD, columns = Country)
dfgacozone =  pd.DataFrame(Impacts_GAC_Ozone)
dfgacghg =  pd.DataFrame(Impacts_GAC_GHG)
dfgacsmog =  pd.DataFrame(Impacts_GAC_Smog)
dfgacacid =  pd.DataFrame(Impacts_GAC_Acid)
dfgaceutro =  pd.DataFrame(Impacts_GAC_Eutro)
dfgaccarcin =  pd.DataFrame(Impacts_GAC_Carcin)
dfgacnoncar =  pd.DataFrame(Impacts_GAC_NonCar)
dfgacresp =  pd.DataFrame(Impacts_GAC_Resp)
dfgacecotox =  pd.DataFrame(Impacts_GAC_EcoTox)
dfgacffd =  pd.DataFrame(Impacts_GAC_FFD)
dfco2intensity = pd.DataFrame(Results_E_CO2_Intensity, columns = Country)
dfPLR = pd.DataFrame(Results_PLR, columns = Country)
dfWaste = pd.DataFrame(Results_Waste, columns = Country)
dfTotal_Protein = pd.DataFrame(Results_Total_Protein, columns = Country)
dfU_Energy = pd.DataFrame(Results_U_Energy, columns = Country)
dfMonthly_Construction_Wage = pd.DataFrame(Results_Monthly_Construction_Wage, columns = Country)
dfMonthly_Maintenance_Wage = pd.DataFrame(Results_Monthly_Maintenance_Wage, columns = Country)
#%%
writer = pd.ExcelWriter(r'Results\TEAResults.xlsx', engine = 'xlsxwriter')
export_excel = dfcost.to_excel(writer, sheet_name = 'Total')
export_excel = dfcostperinitial.to_excel(writer, sheet_name = 'Capital+Constr')
export_excel = dfcostperOM.to_excel(writer, sheet_name = 'OM+Replacement')
export_excel = dfcostperenergy.to_excel(writer, sheet_name = 'Energy')
export_excel = dfcostpermaterials.to_excel(writer, sheet_name = 'Materials')
export_excel = dfcostperlabor.to_excel(writer, sheet_name = 'Labor')
export_excel = dfcostpergac.to_excel(writer, sheet_name = 'GAC')
export_excel = dfcostperzeolites.to_excel(writer, sheet_name = 'Zeolites')

writer.save()
#%%
writer = pd.ExcelWriter(r'LCAResults.xlsx', engine = 'xlsxwriter')
export_excel = dfeghg.to_excel(writer, sheet_name = 'Energy')
export_excel = dfzeoghg.to_excel(writer, sheet_name = 'Zeolites')
export_excel = dfgacghg.to_excel(writer, sheet_name = 'GAC')
export_excel = dfghg.to_excel(writer, sheet_name = 'Materials')
export_excel = dfco2intensity.to_excel(writer, sheet_name = 'CO2Intensity')

#export_excel = dfeozone.to_excel(writer, sheet_name = 'GHG')
#export_excel = dfesmog.to_excel(writer, sheet_name = 'Smog')
#export_excel = dfeacid.to_excel(writer, sheet_name = 'Acid')
#export_excel = dfeeutro.to_excel(writer, sheet_name = 'Eutro')
#export_excel = dfecarcin.to_excel(writer, sheet_name = 'Carcin')
#export_excel = dfenoncar.to_excel(writer, sheet_name = 'NonCar')
#export_excel = dferesp.to_excel(writer, sheet_name = 'Resp')
#export_excel = dfeecotox.to_excel(writer, sheet_name = 'EcoTox')
#export_excel = dfeffd.to_excel(writer, sheet_name = 'FFD')

writer.save()

#%%
GHG_Uncertainty_Parameters = np.concatenate((Daily_Flushes, Flush_Volume, Membrane_Flux, Velocity_Crossflow, Pressure_Membrane, Fill_Fraction_GAC_Column, UF_GAC_N_P_Removal, Clinoptilolite_Capacity, Polonite_Capacity, N_Content_Protein, N_P_Excretion, N_Urine, P_Content_A_Protein, P_Content_V_Protein, P_Urine, Seperation_Efficiency, Density_GAC, Lifetime_GAC, Power_Required_Treatment_EC, Current_EC, Power_Stirrer, Flowrate_Discharge, Pump_UF_Lifetime, Membrane_UF_Lifetime, Switch_Lifetime, Valve_UF_Lifetime, Electrode_EC_Lifetime, Stirrer_Lifetime, U_Pump_Misc_Lifetime, Zeo_GHG, GAC_GHG, E_Hydro_GHG, E_Wind_GHG, E_Solar_GHG, E_Gas_GHG), axis = 1)
Cost_Uncertainty_Parameters =  np.concatenate((Daily_Flushes, Flush_Volume, Membrane_Flux, Velocity_Crossflow, Pressure_Membrane, Fill_Fraction_GAC_Column, UF_GAC_N_P_Removal, Clinoptilolite_Cost, Polonite_Cost, Clinoptilolite_Capacity, Polonite_Capacity, N_Content_Protein, N_P_Excretion, N_Urine, P_Content_A_Protein, P_Content_V_Protein, P_Urine, Seperation_Efficiency, Density_GAC, Lifetime_GAC, Power_Required_Treatment_EC, Current_EC, Power_Stirrer, Flowrate_Discharge, Pump_UF_Lifetime, Membrane_UF_Lifetime, Switch_Lifetime, Valve_UF_Lifetime, Electrode_EC_Lifetime, Stirrer_Lifetime, U_Pump_Misc_Lifetime, Discount_Rate, U_Pump_UF, U_Valve_UF, U_Tank_UF, U_Switch, US_Initial_Unit_Cost_UF, InCountry_Initial_Unit_Cost_UF, US_Initial_Unit_Cost_GAC, InCountry_Initial_Unit_Cost_GAC, U_Stirrer_EC, U_Electrode_EC, US_Initial_Unit_Cost_EC, InCountry_Initial_Unit_Cost_EC, US_Initial_Unit_Cost_Controls, InCountry_Initial_Unit_Cost_Controls, U_Pump_Misc, US_Initial_Unit_Cost_Misc, InCountry_Initial_Unit_Cost_Misc, U_Media_GAC, Monthly_Work_Days, Construction_Time, Maintenance_Frequency, Maintenance_Time), axis = 1)

#%%
GHG_Headings = ["Daily_Flushes","Flush_Volume","Membrane_Flux","Velocity_Crossflow","Pressure_Membrane","Fill_Fraction_GAC_Column","UF_GAC_N_P_Removal","Clinoptilolite_Capacity","Polonite_Capacity","N_Content_Protein","N_P_Excretion","N_Urine","P_Content_A_Protein","P_Content_V_Protein","P_Urine","Seperation_Efficiency","Density_GAC","Lifetime_GAC","Power_Required_Treatment_EC","Current_EC","Power_Stirrer","Flowrate_Discharge","Pump_UF_Lifetime","Membrane_UF_Lifetime","Switch_Lifetime","Valve_UF_Lifetime","Electrode_EC_Lifetime","Stirrer_Lifetime","U_Pump_Misc_Lifetime","Zeo_GHG","GAC_GHG","E_Hydro_GHG","E_Wind_GHG","E_Solar_GHG","E_Gas_GHG"]
Cost_Headings = ["Daily_Flushes","Flush_Volume","Membrane_Flux","Velocity_Crossflow","Pressure_Membrane","Fill_Fraction_GAC_Column","UF_GAC_N_P_Removal","Clinoptilolite_Cost","Polonite_Cost","Clinoptilolite_Capacity","Polonite_Capacity","N_Content_Protein","N_P_Excretion","N_Urine","P_Content_A_Protein","P_Content_V_Protein","P_Urine","Seperation_Efficiency","Density_GAC","Lifetime_GAC","Power_Required_Treatment_EC","Current_EC","Power_Stirrer","Flowrate_Discharge","Pump_UF_Lifetime","Membrane_UF_Lifetime","Switch_Lifetime","Valve_UF_Lifetime","Electrode_EC_Lifetime","Stirrer_Lifetime","U_Pump_Misc_Lifetime","Discount_Rate","U_Pump_UF","U_Valve_UF","U_Tank_UF","U_Switch","US_Initial_Unit_Cost_UF","InCountry_Initial_Unit_Cost_UF","US_Initial_Unit_Cost_GAC","InCountry_Initial_Unit_Cost_GAC","U_Stirrer_EC","U_Electrode_EC","US_Initial_Unit_Cost_EC","InCountry_Initial_Unit_Cost_EC","US_Initial_Unit_Cost_Controls","InCountry_Initial_Unit_Cost_Controls","U_Pump_Misc","US_Initial_Unit_Cost_Misc","InCountry_Initial_Unit_Cost_Misc","U_Media_GAC","Monthly_Work_Days","Construction_Time","Maintenance_Frequency","Maintenance_Time"]
#%%
dfGHG_Uncertainty_Parameters = pd.DataFrame(GHG_Uncertainty_Parameters, columns = GHG_Headings)
dfCost_Uncertainty_Parameters = pd.DataFrame(Cost_Uncertainty_Parameters, columns = Cost_Headings)
#%%

writer = pd.ExcelWriter(r'Results\UncertainParameters.xlsx', engine = 'xlsxwriter')
export_excel = dfGHG_Uncertainty_Parameters.to_excel(writer, sheet_name = 'GHG Parameters')
export_excel = dfCost_Uncertainty_Parameters.to_excel(writer, sheet_name = 'Cost Parameters')

writer.save()

#%%
writer = pd.ExcelWriter(r'Results\CSUncertainParameters.xlsx', engine = 'xlsxwriter')

export_excel = dfPLR.to_excel(writer, sheet_name = 'PLR')
export_excel = dfWaste.to_excel(writer, sheet_name = 'Waste')
export_excel = dfTotal_Protein.to_excel(writer, sheet_name = 'Total_Protein')
export_excel = dfU_Energy.to_excel(writer, sheet_name = 'Energy')
export_excel = dfMonthly_Construction_Wage.to_excel(writer, sheet_name = 'Construction Wage')
export_excel = dfMonthly_Maintenance_Wage.to_excel(writer, sheet_name = 'Maintenance Wage')

writer.save()
