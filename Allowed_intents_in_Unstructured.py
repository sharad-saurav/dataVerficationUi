#Rule 32 - It should contain the data of the following intents – Description, Instruction, Difference, Coverage, Type, Eligibility, Quantity and Limit.
def rule_unstructured():
	import re
	import os
	import sys
	import json
	import pandas as pd
	import openpyxl
	from pandas import ExcelWriter
	from pandas import ExcelFile
	import validators
	
	configFile = 'C:/Configuration.xlsx'
	file_name='Allowed_intents_in_Unstructured.py'
	rule=file_name[:file_name.find('.py')]
	file_directory= 'C:/uploads'
	
	config_file=configFile
	target= 'C:/Users/105666/projects/pythonProject/angular-python-flask-demo/DataFiles_Rules_Report.xlsx'

	all_files=os.listdir(file_directory)
	files=[]

	config=pd.read_excel(config_file)
	newdf=config[config['RULE']==rule]
	to_check=''
	for index,row in newdf.iterrows():
		to_check=row['TO_CHECK']
	to_check=json.loads(to_check)
	files_to_apply=to_check['files_to_apply']

	columns_to_apply=to_check['columns_to_apply']
	intents=to_check['intents_to_check']

	if(to_check['files_to_apply']=='ALL'):
		files = all_files
	else:
		for f in files_to_apply:
			for file in all_files:
				if(file.startswith(f)):
					files.append(file)

	data=[]

	for file in files:
		df = pd.read_excel(file_directory+'/'+file)
		df.index = range(2,df.shape[0]+2)
			
		for index, row in df.iterrows():
			column_value=row['INTENT']
			if(type(column_value)!=float):
				if(column_value not in intents):
					entry=[index,file,column_value+' is not a allowed intent in the Unstructured file']
					print('The row '+str(index)+' in the file '+file+' has intent which is not allowed')
					data.append(entry)
					
	df1 = pd.DataFrame(data, columns = ['ROW_NO', 'FILE_NAME', 'COMMENTS'])
	print('df1-------',df1)
	with ExcelWriter(target,engine='openpyxl',mode='a') as writer:
		df1.to_excel(writer,sheet_name=rule,index=False)