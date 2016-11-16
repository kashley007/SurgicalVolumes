"""
This module includes the necessary functions to
find and analyze pain cases performed in the OR
"""

def find_pain(row):
	"""Find Pain Cases"""

	if((row['TotalProcedureCount'] > 0) and (row['TotalProcedureCount'] == row['PainProcedureCount'])):
		return 'Pain'
	elif((row['Location'] == 'RCH AMB SURG') and (row['TotalProcedureCount'] > row['PainProcedureCount']) and (row['PainProcedureCount'] > 0) ):
		return 'Both'
	else:
		return 'Non Pain'

def pain_filter(df):
	"""Filter Dataset to include pain cases only"""

	df_pain = df.query('Service == "Pain"')
	return df_pain

def count_pain_procedure(row):
	"""Find the number of pain procedures in Dataset"""

	pain_procedure_count = 0
	pain_pro = row['Procedures'].lower()
	procedures = pain_pro.split("]")   

	for procedure in procedures:
		if('(pain)' in procedure):
			pain_procedure_count = pain_procedure_count + 1
	return pain_procedure_count
