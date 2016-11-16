"""
This module includes the necessary functions to
find and analyze endo cases performed in the OR
"""

def find_endo(row):
	"""Find Endo Cases"""

	if((row['TotalProcedureCount'] > 0) and (row['TotalProcedureCount'] == row['EndoProcedureCount'])):
		return 'Endo'
	elif((row['Location'] == 'CRMH MAIN OR') and (row['TotalProcedureCount'] > row['EndoProcedureCount']) and (row['EndoProcedureCount'] > 0)):
		return 'Both'
	else:
		return 'Non Endo'

def get_endo_cases(df):
	"""Filter the Dataframe with Endo cases only"""

	df_endo = df.query('EndoCase == "Endo"')
	return df_endo

def count_endo_procedures(row):
	"""Count the Endo procedures performed in the OR"""

	endo_procedure_count = 0
	endo_pro = row['Procedures'].lower()
	procedures = endo_pro.split("]")
	for procedure in procedures:
		if('(endo)' in procedure):
			endo_procedure_count = endo_procedure_count + 1
		elif('(endo)' not in procedure):
			endo_procedure_count = endo_pro.count('egd') + endo_pro.count('ercp') + \
			endo_pro.count('colonoscopy') + endo_pro.count('sigmoidoscopy') + endo_pro.count('bronchoscopy')
	return endo_procedure_count
