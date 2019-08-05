#Rule 5 - In VOICE_ONLY column there should not be any sentence such as "For more information, visit this link or website.” Instead it should be "For more information, visit the campus website".
import re
import os
import sys
import json
import openpyxl
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

file_name=sys.argv[0]
rule=file_name[:file_name.find('.py')]
file_directory=sys.argv[1]
config_file=sys.argv[2]
target=sys.argv[3]
all_files=os.listdir(file_directory)
files=[]

config=pd.read_excel(config_file)
newdf=config[config['RULE']==rule]
to_check=''
for index,row in newdf.iterrows():
	to_check=row['TO_CHECK']
to_check=json.loads(to_check)
files_to_apply=to_check['files_to_apply']
strings_to_apply=to_check['strings_to_apply']

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
		column_value=row['VOICE_ONLY']
		if(type(column_value)!=float):
			for string in strings_to_apply:
				if(column_value.find(string)!=-1):
					#print(index)
					entry=[index,file,'VOICE_ONLY column has '+string+' in its contents']
					print('The row '+str(index)+' in the file '+file+' has the text\' '+string+' \'in the voice_only column')
					data.append(entry)

df1 = pd.DataFrame(data, columns = ['ROW_NO', 'FILE_NAME', 'COMMENTS'])
with ExcelWriter(target,engine='openpyxl',mode='a') as writer:
	df1.to_excel(writer,sheet_name=rule,index=False)