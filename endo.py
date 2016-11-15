#Find Endo Cases
def findEndo(row):
    if((row['TotalProcedureCount'] > 0) and (row['TotalProcedureCount'] == row['EndoProcedureCount'])):
        return 'Endo'
    elif((row['Location'] == 'CRMH MAIN OR') and (row['TotalProcedureCount'] > row['EndoProcedureCount']) and (row['EndoProcedureCount'] > 0)):
        return 'Both'
    else:
        return 'Non Endo'

def getEndoCases(df):
    df_endo = df.query('EndoCase == "Endo"')
    return df_endo

def countEndoProcedures(row):
    endoProcedureCount = 0
    endoPro = row['Procedures'].lower()
    procedures = endoPro.split("]")   
    for procedure in procedures:
        if('(endo)' in procedure):
            endoProcedureCount = endoProcedureCount + 1
        elif('(endo)' not in procedure):
                endoProcedureCount = endoPro.count('egd') + endoPro.count('ercp') + endoPro.count('colonoscopy') + endoPro.count('sigmoidoscopy') + endoPro.count('bronchoscopy')
    return endoProcedureCount