import endo

def totalProcedures(row):
    procedureCount = row['Procedures'].count(']')
    return procedureCount

def nonEndoProcedures(row):
    nonEndoPro = totalProcedures(row) - endo.countEndoProcedures(row)
    return nonEndoPro



def getMainDF(df):
    df_main = df.query('EndoCase == ["Non Endo", "Both"] and Room != "RMH-PACU ROOM" and Room != "RMH-O ROOM"')
    return df_main


#Give the case a patient Type based on value in the Class column making the patient Inpatient or Outpatient
def addPatientType(row):
    if row['Class'] == 'Hospital Ambulatory Surgery' or row['Class'] == 'Outpatient':
        return 'Outpatient'
    else:
        return 'Inpatient'

#Correct the Year column based on fical year starting in Oct. If month is greater than 9, return year + 1
def fiscalYear(row):
    if row['Month'] > 9:
        return row['Year'] + 1
    else:
        return row['Year']



def applyMonthYearFilter(df, month, year):
    monthYearFilter = df.query('LogStatus == ["Posted", "Complete"] and Month == @month and Year == @year')
    return monthYearFilter

def applyLocationFilter(df, loc):
    locationFilter = df.query('@loc in Location')   
    return locationFilter


