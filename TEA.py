import numpy as np
import math as math
import lhs_python as lhs
import pandas as pd
from scipy import stats
#%% Conversions
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

nsamples = 10000

Daily_Flushes = lhs.lhs_uniform(1,7,nsamples) #flushes/user/day
Flush_Volume = lhs.lhs_uniform(6,10,nsamples) #L blackwater/flush
Membrane_Flux = lhs.lhs_uniform(114,171,nsamples) #L/m2*hr
Velocity_Crossflow = lhs.lhs_uniform(3.5,5.6,nsamples) #m/s
Pressure_Membrane = lhs.lhs_uniform(0,3.5,nsamples) #bar
Fill_Fraction_GAC_Column = lhs.lhs_uniform(.75,.85,nsamples) #% 
UF_GAC_N_P_Removal = lhs.lhs_uniform(0.3,0.5,nsamples) #%
Clinoptilolite_Cost = lhs.lhs_uniform(1.08*0.9,1.08*1.1,nsamples) #$/kg
Polonite_Cost = lhs.lhs_uniform(1.37*0.9,1.37*1.1,nsamples) #$/kg
Clinoptilolite_Capacity = lhs.lhs_uniform(10*.9,10*1.1,nsamples) #mg NH3/g
Polonite_Capacity = lhs.lhs_uniform(10*.9,10*1.1,nsamples) #mg PO4/g
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
US_Initial_Unit_Cost_GAC = lhs.lhs_triangle(88.20*.9,88.20,88.2*1.1,nsamples)
InCountry_Initial_Unit_Cost_GAC = lhs.lhs_triangle(211.5*.9,211.5,211.5*1.1,nsamples)
US_Initial_Unit_Cost_EC = lhs.lhs_triangle(470.47*.9,470.47,470.47*1.1,nsamples)
InCountry_Initial_Unit_Cost_EC = lhs.lhs_triangle(247.43*.9,247.43,247.43*1.1,nsamples)
US_Initial_Unit_Cost_Controls = lhs.lhs_triangle(575.34*.9,575.34,575.34*1.1,nsamples)
InCountry_Initial_Unit_Cost_Controls = lhs.lhs_triangle(985.57*.9,985.57,985.57*1.1,nsamples)
US_Initial_Unit_Cost_Misc = lhs.lhs_triangle(387.78*.9,387.78,387.78*1.1,nsamples)
InCountry_Initial_Unit_Cost_Misc = lhs.lhs_triangle(1828.41*.9,1828.41,1828.41*1.1,nsamples)
U_Media_GAC = lhs.lhs_triangle(0.29,3,5,nsamples) #$/kg
Waste = lhs.lhs_triangle(0.001,0.125,0.25,nsamples)
Total_Protein=lhs.lhs_uniform(51.66,133.54,nsamples)
Total_Protein_A=lhs.lhs_uniform(7.69,37.06,nsamples)
Total_Protein_V=lhs.lhs_uniform(29.42,76.9,nsamples)
PLR = lhs.lhs_uniform(.206,1.63,nsamples)
U_Electricity=lhs.lhs_uniform(.02,.4,nsamples)
Monthly_Construction_Wage=lhs.lhs_triangle(27.01,3314,6655.2,nsamples) #$/month
Monthly_Maintenance_Wage=lhs.lhs_triangle(70.64,3738.63,7547.9,nsamples) #$/month
Income_Tax=lhs.lhs_uniform(0,0.35,nsamples)
Monthly_Work_Days = lhs.lhs_uniform(20,25,nsamples) #days/month
Construction_Time=lhs.lhs_uniform(2,4,nsamples) #days/toilet assembly
Maintenance_Frequency = lhs.lhs_uniform(1,2,nsamples) #times/year
Maintenance_Time = lhs.lhs_uniform(0.25,1,nsamples) #days/maintenance

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

Required_User_Fee_Overall=np.full([10000,1], 0.0)
Required_User_Fee_Initial_Overall=np.full([10000,1], 0.0)
Required_User_Fee_OM_Overall=np.full([10000,1], 0.0)
Required_User_Fee_Energy_Overall=np.full([10000,1], 0.0)
N_Removal_Cost=np.full([10000,1], 0.0)
P_Removal_Cost=np.full([10000,1], 0.0)
Initial_Unit_Cost_Overall=np.full([10000,1], 0.0)
Replacement_Cost_Overall=np.full([10000,1], 0.0)
Energy_Cost_Overall=np.full([10000,1], 0.0)
Labor_Construction_Cost_Overall=np.full([10000,1], 0.0)
Operation_Maintenance_Cost_Overall=np.full([10000,1], 0.0)
Media_GAC=np.full([10000,1], 0.0)

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
    N_Removal_Cost[j,0] = N_Concentration*(1-UF_GAC_N_P_Removal[j,0])*(Clinoptilolite_Cost[j,0]/Clinoptilolite_Capacity[j,0])*(Years_Days) #$/year
    P_Removal_Cost[j,0] = P_Concentration*(1-UF_GAC_N_P_Removal[j,0])*(Polonite_Cost[j,0]/Polonite_Capacity[j,0])*(Years_Days) #$/year
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
    Initial_Unit_Cost_GAC = US_Initial_Unit_Cost_GAC[j,0]+((InCountry_Initial_Unit_Cost_GAC[j,0]+(U_Column_GAC[j,0]*Length_GAC_Column))*PLR[j,0])
    Media_GAC[j,0] = (Annual_GAC_Required*U_Media_GAC[j,0]) #$/year
    Media_Cost_GAC = (Annual_GAC_Required*U_Media_GAC[j,0])+N_Removal_Cost[j,0]+P_Removal_Cost[j,0] #$/year
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
    Initial_Unit_Cost_Overall[j,0] = Initial_Unit_Cost_UF+Initial_Unit_Cost_GAC+Initial_Unit_Cost_EC+Initial_Unit_Cost_Misc+Initial_Unit_Cost_Controls #$
    Replacement_Cost_Overall[j,0] = Replacement_Cost_UF+Replacement_Cost_EC+Replacement_Cost_Misc #$/year
    Energy_Cost_Overall[j,0] = (Energy_Annual_UF+Energy_Annual_EC+Energy_Annual_Misc+Energy_Annual_Controls)*U_Electricity[j,0] #$/year
    Daily_Construction_Wage=Monthly_Construction_Wage[j,0]/Monthly_Work_Days[j,0] #$/day
    Labor_Construction_Cost_Overall[j,0] = Daily_Construction_Wage*Construction_Time[j,0] #$
    Initial_Construction_Cost_Overall = (Initial_Unit_Cost_Overall[j,0])+Labor_Construction_Cost_Overall[j,0] #$
    Daily_Maintenance_Wage=Monthly_Maintenance_Wage[j,0]/Monthly_Work_Days[j,0]
    Operation_Maintenance_Cost_Overall[j,0] = Daily_Maintenance_Wage*Maintenance_Frequency[j,0]*Maintenance_Time[j,0]#$/year
    Ongoing_Cost_Overall = Energy_Cost_Overall[j,0]+Media_Cost_GAC+Operation_Maintenance_Cost_Overall[j,0]+Replacement_Cost_Overall[j,0] #$/year   
    Depreciation_Cost_Overall = Depreciation_Cost_UF+Depreciation_Cost_GAC+Depreciation_Cost_EC+Depreciation_Cost_Misc+Depreciation_Cost_Controls #$/year
    Cost_Overall = 0
    Profits_Overall = 0
    Prelim_Present_OM_Replacement_Cost_Overall = 0
    Present_Energy_Cost_Overall = 0
    Present_Depreciation_Cost_Overall = 0
    p = 1
    while p <= L:
        Required_User_Fee_newterm_Cost_Overall = (1/((1+Discount_Rate[j,0])**p))*(((Ongoing_Cost_Overall+Depreciation_Cost_Overall)*(1-Income_Tax[j,0]))-Depreciation_Cost_Overall)
        Required_User_Fee_newterm_Profits_Overall = (1/((1+Discount_Rate[j,0])**p))*365*U*(1-Income_Tax[j,0])
        Cost_Overall = Cost_Overall+Required_User_Fee_newterm_Cost_Overall
        Profits_Overall = Profits_Overall+Required_User_Fee_newterm_Profits_Overall
        Prelim_Present_OM_Replacement_newterm_Cost_Overall = (1/((1+Discount_Rate[j,0])**p))*((Operation_Maintenance_Cost_Overall[j,0]+Replacement_Cost_Overall[j,0]+Media_Cost_GAC)*(1-Income_Tax[j,0]))
        Prelim_Present_OM_Replacement_Cost_Overall = Prelim_Present_OM_Replacement_Cost_Overall+Prelim_Present_OM_Replacement_newterm_Cost_Overall
        Present_Energy_newterm_Cost_Overall = (1/((1+Discount_Rate[j,0])**p))*(Energy_Cost_Overall[j,0]*(1-Income_Tax[j,0]))
        Present_Energy_Cost_Overall = Present_Energy_Cost_Overall+Present_Energy_newterm_Cost_Overall
        Present_Depreciation_newterm_Cost_Overall = (1/((1+Discount_Rate[j,0])**p))*(((Depreciation_Cost_Overall)*(1-Income_Tax[j,0]))-Depreciation_Cost_Overall)
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
    print (j)
           
#%%
#Assumed_Parameters = np.concatenate((Daily_Flushes, Flush_Volume, Membrane_Flux, Velocity_Crossflow, Pressure_Membrane, Fill_Fraction_GAC_Column, UF_GAC_N_P_Removal, Clinoptilolite_Cost, Polonite_Cost, Clinoptilolite_Capacity, Polonite_Capacity, N_Content_Protein, N_P_Excretion, N_Urine, P_Content_A_Protein, P_Content_V_Protein, P_Urine, Seperation_Efficiency, Lifetime_GAC, Power_Required_Treatment_EC, Current_EC, Power_Stirrer, Flowrate_Discharge, Pump_UF_Lifetime, Membrane_UF_Lifetime, Switch_Lifetime, Valve_UF_Lifetime, Electrode_EC_Lifetime, Stirrer_Lifetime, U_Pump_Misc_Lifetime, Discount_Rate, U_Pump_UF, U_Membrane_UF, U_Valve_UF, U_Tank_UF, U_Switch, U_Column_GAC, U_Stirrer_EC, U_Electrode_EC, U_Pump_Misc, US_Initial_Unit_Cost_UF, InCountry_Initial_Unit_Cost_UF, US_Initial_Unit_Cost_GAC, InCountry_Initial_Unit_Cost_GAC, US_Initial_Unit_Cost_EC, InCountry_Initial_Unit_Cost_EC, US_Initial_Unit_Cost_Controls, InCountry_Initial_Unit_Cost_Controls, US_Initial_Unit_Cost_Misc, InCountry_Initial_Unit_Cost_Misc, U_Media_GAC, Waste, Total_Protein, Total_Protein_A, Total_Protein_V, PLR, U_Electricity, Monthly_Construction_Wage, Monthly_Maintenance_Wage, Income_Tax, Monthly_Work_Days, Construction_Time, Maintenance_Frequency, Maintenance_Time), axis=1)
Assumed_Parameters = np.concatenate((N_Removal_Cost, P_Removal_Cost, Initial_Unit_Cost_Overall, Replacement_Cost_Overall, Energy_Cost_Overall, Labor_Construction_Cost_Overall, Operation_Maintenance_Cost_Overall, Media_GAC), axis =1)
Outputs = Required_User_Fee_Overall

rho_all, p_all = stats.spearmanr(Assumed_Parameters, Outputs)
Spearmans = pd.DataFrame(rho_all, index = ['N_Removal_Cost', 'P_Removal_Cost', 'Initial_Unit_Cost_Overall', 'Replacement_Cost_Overall', 'Energy_Cost_Overall', 'Labor_Construction_Cost_Overall', 'Operation_Maintenance_Cost_Overall', 'Media_GAC', 'Required_User_Fee_Overall'], columns = ['N_Removal_Cost', 'P_Removal_Cost', 'Initial_Unit_Cost_Overall', 'Replacement_Cost_Overall', 'Energy_Cost_Overall', 'Labor_Construction_Cost_Overall', 'Operation_Maintenance_Cost_Overall', 'Media_GAC', 'Required_User_Fee_Overall'])
#Spearmans = pd.DataFrame(rho_all, index = ['Daily_Flushes', 'Flush_Volume', 'Membrane_Flux', 'Velocity_Crossflow', 'Pressure_Membrane', 'Fill_Fraction_GAC_Column', 'UF_GAC_N_P_Removal', 'Clinoptilolite_Cost', 'Polonite_Cost', 'Clinoptilolite_Capacity', 'Polonite_Capacity', 'N_Content_Protein', 'N_P_Excretion', 'N_Urine', 'P_Content_A_Protein', 'P_Content_V_Protein', 'P_Urine', 'Seperation_Efficiency', 'Lifetime_GAC', 'Power_Required_Treatment_EC', 'Current_EC', 'Power_Stirrer', 'Flowrate_Discharge', 'Pump_UF_Lifetime', 'Membrane_UF_Lifetime', 'Switch_Lifetime', 'Valve_UF_Lifetime', 'Electrode_EC_Lifetime', 'Stirrer_Lifetime', 'U_Pump_Misc_Lifetime', 'Discount_Rate', 'U_Pump_UF', 'U_Membrane_UF', 'U_Valve_UF', 'U_Tank_UF', 'U_Switch', 'U_Column_GAC', 'U_Stirrer_EC', 'U_Electrode_EC', 'U_Pump_Misc', 'US_Initial_Unit_Cost_UF', 'InCountry_Initial_Unit_Cost_UF', 'US_Initial_Unit_Cost_GAC', 'InCountry_Initial_Unit_Cost_GAC', 'US_Initial_Unit_Cost_EC', 'InCountry_Initial_Unit_Cost_EC', 'US_Initial_Unit_Cost_Controls', 'InCountry_Initial_Unit_Cost_Controls', 'US_Initial_Unit_Cost_Misc', 'InCountry_Initial_Unit_Cost_Misc', 'U_Media_GAC', 'Waste', 'Total_Protein', 'Total_Protein_A', 'Total_Protein_V', 'PLR', 'U_Electricity', 'Monthly_Construction_Wage', 'Monthly_Maintenance_Wage', 'Income_Tax', 'Monthly_Work_Days', 'Construction_Time', 'Maintenance_Frequency', 'Maintenance_Time', 'Required_User_Fee_Overall'], columns = ['Daily_Flushes', 'Flush_Volume', 'Membrane_Flux', 'Velocity_Crossflow', 'Pressure_Membrane', 'Fill_Fraction_GAC_Column', 'UF_GAC_N_P_Removal', 'Clinoptilolite_Cost', 'Polonite_Cost', 'Clinoptilolite_Capacity', 'Polonite_Capacity', 'N_Content_Protein', 'N_P_Excretion', 'N_Urine', 'P_Content_A_Protein', 'P_Content_V_Protein', 'P_Urine', 'Seperation_Efficiency', 'Lifetime_GAC', 'Power_Required_Treatment_EC', 'Current_EC', 'Power_Stirrer', 'Flowrate_Discharge', 'Pump_UF_Lifetime', 'Membrane_UF_Lifetime', 'Switch_Lifetime', 'Valve_UF_Lifetime', 'Electrode_EC_Lifetime', 'Stirrer_Lifetime', 'U_Pump_Misc_Lifetime', 'Discount_Rate', 'U_Pump_UF', 'U_Membrane_UF', 'U_Valve_UF', 'U_Tank_UF', 'U_Switch', 'U_Column_GAC', 'U_Stirrer_EC', 'U_Electrode_EC', 'U_Pump_Misc', 'US_Initial_Unit_Cost_UF', 'InCountry_Initial_Unit_Cost_UF', 'US_Initial_Unit_Cost_GAC', 'InCountry_Initial_Unit_Cost_GAC', 'US_Initial_Unit_Cost_EC', 'InCountry_Initial_Unit_Cost_EC', 'US_Initial_Unit_Cost_Controls', 'InCountry_Initial_Unit_Cost_Controls', 'US_Initial_Unit_Cost_Misc', 'InCountry_Initial_Unit_Cost_Misc', 'U_Media_GAC', 'Waste', 'Total_Protein', 'Total_Protein_A', 'Total_Protein_V', 'PLR', 'U_Electricity', 'Monthly_Construction_Wage', 'Monthly_Maintenance_Wage', 'Income_Tax', 'Monthly_Work_Days', 'Construction_Time', 'Maintenance_Frequency', 'Maintenance_Time', 'Required_User_Fee_Overall'] )
#%%
df1 = Spearmans[('Required_User_Fee_Overall')]

#%%
writer = pd.ExcelWriter(r'Results\SpearmansRefinedTEA.xlsx', engine = 'xlsxwriter')
export_excel = df1.to_excel(writer)

writer.save()