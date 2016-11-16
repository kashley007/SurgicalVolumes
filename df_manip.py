"""
This module manipulates the pandas df and includes filters 
and new column creations
"""
import endo

def total_procedures(row):
	"""Get the total procedure count from procedure column"""
	procedure_count = row['Procedures'].count(']')
	return procedure_count

def non_endo_procedures(row):
	"""Find non endo procedure count"""
	non_endo_pro = total_procedures(row) - endo.count_endo_procedures(row)
	return non_endo_pro

def get_main_df(df):
	"""Filter the Dataset to include non endo cases"""
	df_main = df.query('EndoCase == ["Non Endo", "Both"] and Room != "RMH-PACU ROOM" and Room != "RMH-O ROOM"')
	return df_main

def add_patient_type(row):
	"""patient Type (Inpatient or Outpatient) based on value in the Class column"""
	if row['Class'] == 'Hospital Ambulatory Surgery' or row['Class'] == 'Outpatient':
		return 'Outpatient'
	else:
		return 'Inpatient'

def fiscal_year(row):
	"""Correct the Year column based on fiscal year starting in Oct."""

	if row['Month'] > 9:
		return row['Year'] + 1
	else:
		return row['Year']

def apply_month_year_filter(df, month, year):
	"""Filter Dataset based on Log Status, month and year"""

	month_year_filter = df.query('LogStatus == ["Posted", "Complete"] and Month == @month and Year == @year')
	return month_year_filter

def apply_location_filter(df, loc):
	"""Filter Dataset based on location"""

	location_filter = df.query('@loc in Location')   
	return location_filter

