"""
This module will import an excel file and create
a pandas Dataframe with appended customized columns.
"""
import sys
import pandas as pd
import df_manip
import endo
import pain

#Read in the Volumes Data, Change Date column to DateTime Object, add Month and year column to DataFrame
def get_excel_data(args):
    """
    Get data from excel file and create pandas dataframe
    """
    if args.file:
        df = pd.read_excel(args.file)
        df['Date'] = pd.to_datetime(df['Date'])
        df['Month'] = pd.to_numeric(df['Date'].dt.month)
        df['Year'] = pd.to_numeric(df['Date'].dt.year)
        df['Year'] = df.apply(lambda row: df_manip.fiscal_year(row), axis=1)
        df['Type'] = df.apply(lambda row: df_manip.add_patient_type(row), axis=1)
        df['Procedures'] = df['Procedures'].apply(str)
        df['NonEndoProcedureCount'] = df.apply(lambda row: df_manip.non_endo_procedures(row), axis=1)
        df['EndoProcedureCount'] = df.apply(lambda row: endo.count_endo_procedures(row), axis=1)
        df['TotalProcedureCount'] = df.apply(lambda row: df_manip.total_procedures(row), axis=1)
        df['EndoCase'] = df.apply(lambda row: endo.find_endo(row), axis=1)
        df['PainProcedureCount'] = df.apply(lambda row: pain.count_pain_procedure(row), axis=1)
        df['PainCase'] = df.apply(lambda row: pain.find_pain(row), axis=1)
        df.to_html('VolumesData.html')
        df.to_csv('VolumesData.csv')

        return df
    else:
        print("Import file is require") 
        sys.exit()


