import pickle
from time import time
import sys
reload(sys)  
sys.setdefaultencoding('utf8')

newDBStruct={'audios': [], 'alist': [], 'albums': {}, 'alist':[],  'settings': {'servername': 'Someone`s Music Storage', 'httpdip': '127.0.0.1', 'httpdport': '8084', 'musicdir': 'audios', 'httpdroot': 'http://localhost:8084/', 'header': '''{{servername}}''', 'footer': '''&copy 2017 <a style="color: orange" href="https://melnikovsm.tk" target="_blank">MelnikovSM</a>. Powered by <a style="color: orange" href='https://github.com/MelnikovSM/musicsync-server' target='_blank'>MelnikovSM`s MusicSync</a>''', 'plUrl': '/playlist.m3u8', 'plsUrl': '/pl/<album>.m3u8'}}

def saveDB(dbPath,db):
	output = open(dbPath, 'wb')
	pickle.dump(db, output)
	output.close()
def loadDB(dbPath):
	input = open(dbPath, 'rb')
	db = pickle.load(input)
	input.close()
	return db

def fname2id(db, fname):
	id=-1
	for n in range(len(db['audios'])):
		try:
			if int(db['audios'][n]['filename'])==int(fname): 
				id=n
		except ValueError: return -1
	return id

def fname2idL(alist, fname):
	id=-1
	for n in range(len(alist)):
		try:
			if int(alist[n]['filename'])==int(fname): 
				id=n
		except ValueError: return -1
	return id
	
def getAudios(db, album=''):
	if album=='': return db['audios'], False
	else:
		relreq=False
		if (album in db['albums']):
			o=[]
			for n in db['albums'][album]:
				id=fname2id(db, n)
				if id>=0: o.append(db['audios'][id])
				else: 
					relreq=True
					db['albums'][album].remove(n)
			return o, relreq
		else: return False, relreq

def albumAdd(db, album, id):
	if (album in db['albums']):
		db['albums'][album].insert(0, id)
		return True
	else: return False

def albumDel(db, album, id):
	if (album in db['albums']) and (id in db['albums'][album]) :
		db['albums'][album].remove(id)	
		return True
	else: return False

def moveAlbum(db, id1, id2):
	id1=int(id1)
	id2=int(id2)
	dest=db['alist']
	if id1>=0:
		if id2<0:
			if id2==-1 or id2==-2:
				if id2==-1 and id1<(len(dest)-1): # move id1 below
					dest[id1], dest[id1+1] = dest[id1+1], dest[id1]
					return True
				else: return False
				if id2==-2 and id1>0: # move id1 higher
					dest[id1], dest[id1-1] = dest[id1-1], dest[id1]
					return True
				else: return False
			else: return False
		else: return False
	else: return False

def renameAlbum(db, old, new):
	if (not ((new in db['albums']) or (new in db['alist']))) and ((old in db['albums']) and (old in db['alist'])):
		index=0
		for aname in db['alist']:
			if aname==old: break
			index+=1
		db['alist'][index]=new
		db['albums'][new]=db['albums'].pop(old)
		return True
	else: return False


def addAlbum(db, album):
	if not ((album in db['albums']) or (album in db['alist'])):
		db['alist'].insert(0, album)
		db['albums'][album]=[]
		return True
	else: return False
def delAlbum(db, album):
	if (album in db['albums']) and (album in db['alist']):
		db['alist'].remove(album)
		del db['albums'][album]
		return True
	else: return False

def regAudio(db, artist, title):
	try:
		db['audios'].insert(0, {})
		db['audios'][0]['filename']=str(int(time()*10000))
		db['audios'][0]['artist']=artist
		db['audios'][0]['title']=title
		return db['audios'][0]['filename']
	except: return False

def unregAudio(db, id):
	if id<len(db['audios']):
		return db['audios'].pop(id)['filename']
	else: return False

def moveAudio(db, id1, id2, album=''):
	id1=int(id1)
	id2=int(id2)
	if album=='': dest=db['audios']
	else: dest=db['albums'][album]
	if id1>=0:
		if id2<0:
			if id2==-1 or id2==-2:
				if id2==-1 and id1<(len(dest)-1): # move id1 below
					dest[id1], dest[id1+1] = dest[id1+1], dest[id1]
					return True
				else: return False
				if id2==-2 and id1>0: # move id1 higher
					dest[id1], dest[id1-1] = dest[id1-1], dest[id1]
					return True
				else: return False
			else: return False
		else: return False
	else: return False

def modifyAudio(db, id, artist, title):
	if id<len(db['audios']):
		db['audios'][id]['artist']=artist
		db['audios'][id]['title']=title
		return True
	else: return False