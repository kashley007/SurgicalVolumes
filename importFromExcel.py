import pandas as pd
import numpy as np
import sys
import dfManip
import endo
import pain

#Read in the Volumes Data, Change Date column to DateTime Object, add Month and year column to DataFrame
def getDataFromExcel(args):
    if(args.file):
        df = pd.read_excel(args.file)
        df['Date'] = pd.to_datetime(df['Date'])
        df['Month'] = pd.to_numeric(df['Date'].dt.month)
        df['Year'] = pd.to_numeric(df['Date'].dt.year)
        df['Year'] = df.apply(lambda row: dfManip.fiscalYear(row), axis=1)
        df['Type'] = df.apply(lambda row: dfManip.addPatientType(row), axis=1)
        df['Procedures'] = df['Procedures'].apply(str)
        df['NonEndoProcedureCount'] = df.apply(lambda row: dfManip.nonEndoProcedures(row), axis=1)
        df['EndoProcedureCount'] = df.apply(lambda row: endo.countEndoProcedures(row), axis=1)
        df['TotalProcedureCount'] = df.apply(lambda row: dfManip.totalProcedures(row), axis=1)
        df['EndoCase'] = df.apply(lambda row: endo.findEndo(row), axis=1)
        df['PainProcedureCount'] = df.apply(lambda row: pain.countPainProcedure(row), axis=1)
        df['PainCase'] = df.apply(lambda row: pain.findPain(row), axis=1)
        df.to_html('VolumesData.html')
        df.to_csv('VolumesData.csv')
        
        return df
    else:
        print("Import file is require") 
        sys.exit() 



