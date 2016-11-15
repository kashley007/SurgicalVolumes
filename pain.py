
#Find Pain Cases
def findPain(row):
    if((row['TotalProcedureCount'] > 0) and (row['TotalProcedureCount'] == row['PainProcedureCount'])):
        return 'Pain'
    elif((row['Location'] == 'RCH AMB SURG') and (row['TotalProcedureCount'] > row['PainProcedureCount']) and (row['PainProcedureCount'] > 0) ):
        return 'Both'
    else:
        return 'Non Pain'

def painfilter(df):
    df_pain = df.query('Service == "Pain"')
    return df_pain

#Find the number of Pain Procedures in Dataset
def countPainProcedure(row):
    painProcedureCount = 0
    painPro = row['Procedures'].lower()
    procedures = painPro.split("]")   

    for procedure in procedures:
        if('(pain)' in procedure):
            painProcedureCount = painProcedureCount + 1
    return painProcedureCount

