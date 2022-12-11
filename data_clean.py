import pandas as pd
from pandas import DataFrame



data_samples = pd.read_csv("/Users/wangruoqi/Desktop/cov/covid19-kg-vis/data/samples.csv")

df1=DataFrame(index=['Id','START','STOP','PATIENT','ORGANIZATION','PROVIDER','PAYER','ENCOUNTERCLASS','CODE','DESCRIPTION','BASE_ENCOUNTER_COST','TOTAL_CLAIM_COST','PAYER_COVERAGE','REASONCODE','REASONDESCRIPTION']) 
encounters = pd.read_csv("/Users/wangruoqi/Desktop/cov/data/encounters.csv")
lst = list(data_samples['ENCOUNTER'])
for index, row in encounters.iterrows():
    if row['Id'] in lst:
        row = row.to_frame()
        df1 = pd.concat([df1, row.T],ignore_index=True)
df1.to_csv('encounters_clean.csv')


df2=DataFrame(index=['START','STOP','PATIENT','ENCOUNTER','CODE','DESCRIPTION']) 
allergies = pd.read_csv("/Users/wangruoqi/Desktop/cov/data/allergies.csv")
lst = list(data_samples['ENCOUNTER'])
for index, row in allergies.iterrows():
    if row['ENCOUNTER'] in lst:
        row = row.to_frame()
        df2 = pd.concat([df2, row.T],ignore_index=True)     
df2.to_csv('allergies_clean.csv')


df3=DataFrame(index=['START','STOP','PATIENT','ENCOUNTER','CODE','DESCRIPTION']) 
conditions = pd.read_csv("/Users/wangruoqi/Desktop/cov/data/conditions.csv")
lst = list(data_samples['ENCOUNTER'])
for index, row in conditions.iterrows():
    if row['ENCOUNTER'] in lst:
        row = row.to_frame()
        df3 = pd.concat([df3, row.T],ignore_index=True)
df3.to_csv('conditions_clean.csv')


df4=DataFrame(index=['START','STOP','PATIENT','PAYER','ENCOUNTER','CODE','DESCRIPTION','BASE_COST','PAYER_COVERAGE','DISPENSES','TOTALCOST','REASONCODE','REASONDESCRIPTION']) 
medications = pd.read_csv("/Users/wangruoqi/Desktop/cov/data/medications.csv")
lst = list(data_samples['ENCOUNTER'])
for index, row in medications.iterrows():
    if row['ENCOUNTER'] in lst:
        row = row.to_frame()
        df4 = pd.concat([df4, row.T],ignore_index=True)
df4.to_csv('medications_clean.csv')


df5=DataFrame(index=['DATA','PATIENT','ENCOUNTER','CODE','DESCRIPTION','BASE_COST','REASONCODE','REASONDESCRIPTION']) 
procedures = pd.read_csv("/Users/wangruoqi/Desktop/cov/data/procedures.csv")
lst = list(data_samples['ENCOUNTER'])
for index, row in procedures.iterrows():
    if row['ENCOUNTER'] in lst:
        row = row.to_frame()
        df5 = pd.concat([df5, row.T],ignore_index=True)
df5.to_csv('procedures_clean.csv')


df6=DataFrame(index=['Id','START','STOP','PATIENT','ENCOUNTER','CODE','DESCRIPTION','REASONCODE','REASONDESCRIPTION']) 
careplans = pd.read_csv("/Users/wangruoqi/Desktop/cov/data/careplans.csv")
lst = list(data_samples['ENCOUNTER'])
for index, row in careplans.iterrows():
    if row['ENCOUNTER'] in lst:
        row = row.to_frame()
        df6 = pd.concat([df6, row.T],ignore_index=True)
df6.to_csv('careplans_clean.csv')


