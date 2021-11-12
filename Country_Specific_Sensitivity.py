import numpy as np
import math as math
import lhs_python as lhs
from scipy import stats
import pandas as pd
import xlsxwriter

#%%
Countries = pd.read_csv(r'CSVforCode\Countries.csv')
ImpactParameterNames = pd.read_csv(r'CSVforCode\ImpactNames.csv')
CostParameterNames = pd.read_csv(r'CSVforCode\CostNames.csv')

Impacts = pd.read_csv(r'CSVforCode\TotalImpacts.csv')
Cost = pd.read_csv(r'CSVforCode\TotalCost.csv')

ImpactParameters = pd.read_csv(r'CSVforCode\GeneralUncertainParametersGHG.csv')
CostParameters = pd.read_csv(r'CSVforCode\GeneralUncertainParametersCost.csv')
PLR = pd.read_csv(r'CSVforCode\PLR.csv')
Waste = pd.read_csv(r'CSVforCode\Waste.csv')
Protein = pd.read_csv(r'CSVforCode\TotalProtein.csv')
Energy = pd.read_csv(r'CSVforCode\Energy.csv')
ConstructionWage = pd.read_csv(r'CSVforCode\ConstructionWage.csv')
MaintenanceWage = pd.read_csv(r'CSVforCode\MaintenanceWage.csv')
#%%

PImpacts = np.full((1000,40),0.0)
for j in range (0,40):
    IParameter = ImpactParameterNames['Parameter'][j]
    PImpacts[:,j] = ImpactParameters[IParameter]
    PCost = np.full((1000,51),0.0)
    for k in range (0,51):
        CParameter = CostParameterNames['Parameter'][k]
        PCost[:,k] = CostParameters[CParameter]
        rho_I_PImpacts = np.full((41,89),0.0)
        rho_C_PCost = np.full((52,89),0.0)
        rho_I_CS_Waste = np.full((1,89),0.0)
        rho_I_CS_Protein = np.full((1,89),0.0)
        rho_C_CS_Waste = np.full((1,89),0.0)
        rho_C_CS_Protein = np.full((1,89),0.0)
        rho_C_CS_PLR = np.full((1,89),0.0)
        rho_C_CS_Energy = np.full((1,89),0.0)
        rho_C_CS_ConstructionWage = np.full((1,89),0.0)
        rho_C_CS_MaintenanceWage = np.full((1,89),0.0)
        for i in range(0,89):
            Country = Countries['Country'][i]
            CS_Impacts = Impacts[Country]
            CS_Cost = Cost[Country]
            CS_PLR = PLR[Country]
            CS_Waste = Waste[Country]
            CS_Protein = Protein[Country]
            CS_Energy = Energy[Country]
            CS_ConstructionWage = ConstructionWage[Country]
            CS_MaintenanceWage = MaintenanceWage[Country]
            
            rho_I_PImpacts2, p_all = stats.spearmanr(PImpacts, CS_Impacts) 
            rho_I_PImpacts1 = rho_I_PImpacts2[ : , 40]
            rho_I_PImpacts[:,i] = rho_I_PImpacts1
            rho_I_CS_Waste[0,i], p_all = stats.spearmanr(CS_Waste, CS_Impacts)       
            rho_I_CS_Protein[0,i], p_all = stats.spearmanr(CS_Protein, CS_Impacts)       
            
            rho_C_PCost2, p_all = stats.spearmanr(PCost, CS_Cost)
            rho_C_PCost1 = rho_C_PCost2[ : , 51]
            rho_C_PCost[:,i] = rho_C_PCost1
            rho_C_CS_PLR[0,i], p_all = stats.spearmanr(CS_PLR, CS_Cost)       
            rho_C_CS_Waste[0,i], p_all = stats.spearmanr(CS_Waste, CS_Cost)       
            rho_C_CS_Protein[0,i], p_all = stats.spearmanr(CS_Protein, CS_Cost)       
            rho_C_CS_Energy[0,i], p_all = stats.spearmanr(CS_Energy, CS_Cost)       
            rho_C_CS_ConstructionWage[0,i], p_all = stats.spearmanr(CS_ConstructionWage, CS_Cost)       
            rho_C_CS_MaintenanceWage[0,i], p_all = stats.spearmanr(CS_MaintenanceWage, CS_Cost) 
            print(j,k,i)
