PATH="f:/pyton/"
IN="sys.txt"
OUT="sys.csv"
shimcahe=False
cnt=0;
list=[]
keys=[
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
	
record=clear_record()

f=open(PATH+IN,"r",encoding="windows-1251", errors='ignore')

for line in f:
	if 'appcompatcache' in line:
		shimcahe=True
	if shimcahe:
		if line.strip()!='':
			if ':\\' in line:
				record['FILE']=line.strip()
			if 'Executed' in line:
				record['EXECUTED']='Executed'
			if 'ModTime:' in line:
				date=line.strip()[13:-2]
				record['DATE']=(date[4:6]+'.'+month[date[:3]]+'.'+date[-4:]).lstrip()
				record['TIME']=line.strip()[20:28]
		else:
			list.append(record)
			cnt+=1
			record=clear_record()
		if '----------------------------------------' in line:
			break

f.close()
for item in list:
	print(item)
		
		
csv=open(PATH+OUT,'w',encoding="UTF-8")
csv.write(';'.join(keys))
for item in list:
	csv.write(';'.join(item.values()))
	csv.write('\n')
csv.close()

