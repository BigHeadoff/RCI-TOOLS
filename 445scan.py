# скрипт сканирования данных NetFlow для поиска WannaCry
# настройки
port='445'     # номер порта назначения
dstportfiеld=7 # номер поля порта назначения
srcipfiled=3   # номер поля ip-адреса источника
dstipfiled=6   # номер поля ip-адреса назначения
threshold=5    # порог срабатывания

import time
import argparse

def createParser ():
	parser = argparse.ArgumentParser()
	parser.add_argument ('-if','--infile', nargs='?', type=argparse.FileType(encoding="windows-1251", errors='ignore'),required=True, help='imput file. Result of Flowprint')
	parser.add_argument ('-of','--outfile', nargs='?',  type=argparse.FileType(mode='w',encoding="windows-1251", errors='ignore'), default='file.csv', help='output csv file')

	return parser

if __name__ == '__main__':
	
	parser = createParser()
	namespace = parser.parse_args()
	base={}

	start=time.time()
	for line in namespace.infile:
		if len(line)>1:
			ln=line.split()
			if ln[dstportfiеld] == port:
				if not(ln[srcipfiled] in base):
					base[ln[srcipfiled]]=set()
				base[ln[srcipfiled]].add(ln[dstipfiled])

	namespace.outfile.write('IP,Danger\n')
	for key in base:
		cnt=len(base[key])
		if cnt>threshold: namespace.outfile.write(key+','+str(cnt)+'\n')
	stop=time.time()
	print('Scan complected: '+str(stop-start))
