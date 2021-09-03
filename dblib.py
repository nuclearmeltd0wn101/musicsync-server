import pickle
from time import time
import sys
reload(sys)  
sys.setdefaultencoding('utf8')

newDBStruct={
'audios': [], # Audios index list
'albums': {}, # Albums content dict
'alist':[],   # Albums index list
'settings': {
	'servername': 'Someone`s Music Storage', # Default server name
	'httpdip': '127.0.0.1', # Default Web-Server bind IP
	'httpdport': '8084', # Default Web-Server port
	'musicdir': 'audios', # Default audios dir
	'httpdroot': 'http://localhost:8084/', # Default portal root URL
	'header': '''{{servername}}''', # Default header HTML
	'footer': '''&copy 2017 <a style="color: orange" href="https://blog.nm101.tk" target="_blank">nuclearmeltd0wn101</a>. Powered by <a style="color: orange" href='https://github.com/nuclearmeltd0wn101/musicsync-server' target='_blank'>MusicSync Server</a> version {{srvversion}}''', # Default footer HTML
	'plUrl': '/playlist.m3u8', 'plsUrl': '/pl/<album>.m3u8', # URL to M3U playlists
	'welcometext': '''Welcome to new MusicSync Server installation!
This text may be changed at "Appearance" realm of control panel.
Please choose album below to view audio collection.''', # Default home page welcome text
	'permissions': { # Default access permissions
		'referalSong': 3, # Display single song from link (WebIf only) (by default allowed for guests and higher)
		'viewAlbum': 3, # Display album (WebIf only) (by default allowed for guests and higher)
		'view': 3, # View all audios, albums list, use search feature (default: guests and higher)
		'uapi': 2, # user-level WebAPI access, M3U generator (default: users and higher)
		'edit': 1, # WebIf and WebAPI access to content editing and everything, listed higher (default: editors and administrators)
		'system': 0 # WebIf and WebAPI access to server control and everything, listed higher (default: administrators only)
	}
	},
	'accounts': {}, # accounts
	'artists': [] # artists & theirs songs count
}

def postHandle(db, state):
	artists={}	
	for audio in db['audios']:
		if not ('lyrics' in audio): audio['lyrics']=''
		else: audio['lyrics']=audio['lyrics'].strip()
		artist = audio['artist']
		if not (artist in artists): artists[artist]=1
		else: artists[artist]+=1
	db['artists']=sorted(artists.items(), key=lambda x: x[1], reverse=True)


def saveDB(dbPath,db):
	postHandle(db, 1)
	output = open(dbPath, 'wb')
	pickle.dump(db, output)
	output.close()
def loadDB(dbPath):
	input = open(dbPath, 'rb')
	db = pickle.load(input)
	input.close()
	postHandle(db, 0)
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
		db['audios'][0]['lyrics']=''
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
	if id1>=0 and id1<len(dest):
		if id2<0:
			if id2==-1 or id2==-2:
				if id2==-1 and id1<(len(dest)-1): # move id1 below
					dest[id1], dest[id1+1] = dest[id1+1], dest[id1]
					return dest
				else: return False
				if id2==-2 and id1>0: # move id1 higher
					dest[id1], dest[id1-1] = dest[id1-1], dest[id1]
					return dest
				else: return False
			else: return False
		else:
			if id2<len(dest):
				s=dest.pop(id1)
				dest=dest[:id2]+[s]+dest[id2:]
				return dest
			else: return False
			
	else: return False

def modifyAudio(db, id, artist, title, lyrics=None):
	if id<len(db['audios']):
		db['audios'][id]['artist']=artist
		db['audios'][id]['title']=title
		if str(lyrics)<>'None': db['audios'][id]['lyrics']=lyrics
		return True
	else: return False
def searchAudio(audios, string):
	candidates=[]
	i=0
	for audio in audios:
		if (string.lower() in (audio['artist']+' - '+audio['title']).lower() ): candidates.append(i)
		i+=1
	return candidates