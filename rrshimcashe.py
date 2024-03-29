# -*- coding: UTF-8 -*-

import re
import argparse

def createParser ():
	parser = argparse.ArgumentParser()
	parser.add_argument ('-if','--infile', nargs='?', type=argparse.FileType(encoding="windows-1251", errors='ignore'),required=True, help='imput file. Result of RegRipper')
	parser.add_argument ('-of','--outfile', nargs='?',  type=argparse.FileType(mode='w',encoding="windows-1251", errors='ignore'), default='file.csv', help='output csv file')

	return parser
 
keys=[
	'OBJECT',
	'PATH',
	'FILE',
	'DATE',
	'TIME',
	'EXECUTED'
	]
	
month={
	'Jan':'01',
	'Feb':'02',
	'Mar':'03',
	'Apr':'04',
	'May':'05',
	'Jun':'06',
	'Jul':'07',
	'Aug':'08',
	'Sep':'09',
	'Oct':'10',
	'Nov':'11',
	'Dec':'12',
	}	
	
def clear_record(rec=None):
	rec={}
	for key in keys:
		rec[key]=''
	return rec

if __name__ == '__main__':
	
	parser = createParser()
	namespace = parser.parse_args()
	record=clear_record()
	shimcahe=False
	list=[]      
	
	for line in namespace.infile:
		if 'appcompatcache' in line:
			shimcahe=True
		if shimcahe:
			if line.strip()!='':
				if ':\\' in line:
					match=re.search(r'((.*\\)(.*))',line.rstrip())
					record['OBJECT']=match.group(1)
					record['PATH']=match.group(2)
					record['FILE']=match.group(3)
				elif 'Executed' in line:
					record['EXECUTED']='Executed'
				elif 'ModTime:' in line:
					date=line.strip()[13:-2]
					record['DATE']=(date[4:6]+'.'+month[date[:3]]+'.'+date[-4:]).lstrip()
					record['TIME']=line.strip()[20:28]
			else:
				list.append(record)
				record=clear_record()
			if '----------------------------------------' in line:
				break

	namespace.outfile.write(';'.join(keys))
	for item in list:
		namespace.outfile.write(';'.join(item.values()))
		namespace.outfile.write('\n')
	if not shimcahe:
		print('ShimCache not found')
