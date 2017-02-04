# -*- coding: utf-8 -*-
dbPath='msync.db'
print('MusicSync Server version 170205\nCopyright (C) 2017 MelnikovSM')
import pickle, os, sys, json, hashlib, random, string
import dblib
from bottle import route, run, template, static_file, error, request, HTTPResponse, response, abort
from urllib2 import unquote
from copy import copy
from getpass import getpass
reload(sys)  
sys.setdefaultencoding('utf8')

dbPath=os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), dbPath)

def read(prompt, defaultvalue=''):
	a=''
	while a=='':
		sys.stdout.write(prompt)
		a=sys.stdin.readline()
		a=a[0:(len(a)-1)]
		if a=='' and defaultvalue<>'': a=defaultvalue
	return a

if not os.path.isfile(dbPath):
	db=dblib.newDBStruct
	print('Processing inital configuration of your MusicSync Server installation..')
	db['settings']['servername']=read('Server name (leave for "'+db['settings']['servername']+'"): ', db['settings']['servername'])
	db['settings']['musicdir']=read('Path to audios dir (leave for "'+db['settings']['musicdir']+'"): ', db['settings']['musicdir'])
	db['settings']['httpdip']=read('HTTP Server IP (leave for '+db['settings']['httpdip']+'): ', db['settings']['httpdip'])
	db['settings']['httpdport']=read('HTTP Server Port (leave for '+db['settings']['httpdport']+'): ', db['settings']['httpdport'])
	db['settings']['httpdroot']=read('HTTP Root URL (leave for "'+db['settings']['httpdroot']+'"): ', db['settings']['httpdroot'])
	db['settings']['passwd_salt']=(''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(6)))
	admname=read('Administrative account name (leave for "admin"): ', 'admin')
	while True:
		passwd=getpass('Administrative account password: ')
		passwd2=getpass('Repeat: ')
		if passwd<>passwd2: print('Passwords mismatch, try again.')
		else: break
	db['accounts'][admname]={'access_level': 0, 'passwd': hashlib.md5(db['settings']['passwd_salt']+passwd).hexdigest()}
	admname=None # Security cleanup
	passwd=None
	passwd2=None

	print('Initial configuration complete!')
	dblib.saveDB(dbPath, db)
else: db=dblib.loadDB(dbPath)

footer=db['settings']['footer']
header=template(db['settings']['header'], servername=db['settings']['servername'], static=os.path.join(db['settings']['httpdroot'], 'static'))
if header=='': header=db['settings']['servername']


def get_size(start_path = '.'): # Get directory size
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

# Authentification processor

# access levels:
# 0 - administrator
# 1 - content manager
# 2 - user
# 3 - guest

def genToken(user,passwd): return (hashlib.md5(db['settings']['passwd_salt']+user).hexdigest())+(hashlib.md5(db['settings']['passwd_salt']+passwd).hexdigest())
def checkToken(token):
	alevel=3 # guest by default
	username='anonymous'
	for user in db['accounts']:
		if token==(hashlib.md5(db['settings']['passwd_salt']+user).hexdigest())+db['accounts'][user]['passwd']:
			username=user
			alevel=db['accounts'][user]['access_level']
	return alevel, username
def auth(access_level=3, token=''):
	if access_level<3:
		if ('token' in request.cookies) and (checkToken(request.cookies['token'])[0] <= access_level): return
		if (checkToken(token)[0] <= access_level): return
		abort(401)
	else: return

@error(401)
def loginWindow(error): return template(open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),'templates/login.tpl'), 'r').read(), content=template('''<h3 style="color: white; font-family: 'Tahoma', Arial, sans-serif;">Authentication or permissions escalation required:</h3><form action="{{root}}login" method="post" enctype="multipart/form-data" name='login'>
<input type="text" name="username" placeholder='Username' /><br>
<input type="password" name="password" placeholder='Password' /><br>
<input type="submit" value="Log in" /><br>
</form>''', root=db['settings']['httpdroot']), sname=db['settings']['servername'], header=header, footer=footer)
@route('/login', method='GET')
def loginWindow():
	a=template(open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),'templates/login.tpl'), 'r').read(), content=template('''<h3 style="color: white; font-family: 'Tahoma', Arial, sans-serif;">Login:</h3><form action="{{root}}login" method="post" enctype="multipart/form-data" name='login'>
<input type="text" name="username" placeholder='Username' /><br>
<input type="password" name="password" placeholder='Password' /><br>
<input type="submit" value="Log in" /><br>
</form>''', root=db['settings']['httpdroot']), sname=db['settings']['servername'], header=header, footer=footer)
	if ('token' in request.cookies):
		if (checkToken(request.cookies['token'])[0] <= 3):
			perms=['Administrators', 'Editors', 'Users', 'Guests']
			if ('username' in request.cookies): 
				username=request.cookies['username']
				if (username in db['accounts']): avl=db['accounts'][username]['access_level']
				else: return a
			else:
				username='Anonymous'
				avl=3
			return template(open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),'templates/login.tpl'), 'r').read(), content=template('''<h3 style="color: white; font-family: 'Tahoma', Arial, sans-serif;">You are already logged in as {{account}} (group {{group}}). You also may <a href='{{root}}logout'>logout</a>.</h3>''', root=db['settings']['httpdroot'], account=username, group=perms[avl]), sname=db['settings']['servername'], header=header, footer=footer)
		else: return a
	else: return a
@route('/login', method='POST') # login handler
def loginHandler():
	login = request.forms.get('username')
	pasw = request.forms.get('password')
	token=genToken(login, pasw)
	if (checkToken(token)[0]<3):
		response.set_cookie('token', token)
		response.set_cookie('username', checkToken(token)[1])
		return template(open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),'templates/login.tpl'), 'r').read(), content='''<h1 style="color: white; font-family: 'Tahoma', Arial, sans-serif;">Authentication succeeded!</h1><script>location.replace(document.referrer);</script>''', sname=db['settings']['servername'], header=header, footer=footer)
	else: return template(open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),'templates/login.tpl'), 'r').read(), content='''<h1 style="color: white; font-family: 'Tahoma', Arial, sans-serif;">Authentication failed!</h1><script>location.replace(document.referrer);</script>''', sname=db['settings']['servername'], header=header, footer=footer)

@route('/logout', method='GET')
def logout():
	if ('token' in request.cookies): response.set_cookie('token', '', expires=0)
	if ('username' in request.cookies): response.set_cookie('username', '', expires=0)
	return template(open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),'templates/login.tpl'), 'r').read(), content='''<h1 style="color: white; font-family: 'Tahoma', Arial, sans-serif;">Logout succeeded!</h1><script>location.replace(document.referrer);</script>''', sname=db['settings']['servername'], header=header, footer=footer)

# User Web Interface

def genPlLinks(): # Generate albums selector on play pages
	if len(db['alist'])>0:
		a='''<select onchange="window.location.href=this.options[this.selectedIndex].value" style="position: absolute; top: 10px; right:16px;">\n'''
		a+='''<option VALUE="#">Go to album..</option>\n'''
		a+='''<option VALUE="'''+os.path.join(db['settings']['httpdroot'], 'allAudios')+'''">All audios ('''+str(len(db['audios']))+''')</option>\n'''
		for alb in db['alist']:
			a+='''<option VALUE="'''+os.path.join(db['settings']['httpdroot'], 'album/'+alb)+'''">'''+alb+' ('+str(len(db['albums'][alb]))+')'+'''</option>\n'''
		a+='</select>\n'
	else: a=''
	return a

def genSearch(album='', atplayer=True, prefilled=''): 
	if not (album<>'' and (not (album in db['alist']))):
		if prefilled=='':
			if atplayer==True: return '<div style="position: absolute; top: 30px; right:16px;">'+template('''<form action="{{cproot}}search" method="post" enctype="multipart/form-data" name='searchAudio'><input type="hidden" name="album" value="{{album}}" /><input type="text" name="query" placeholder='Search..' /><input type="submit" value="Search" /></form><br>''', cproot=db['settings']['httpdroot'], album=album)+'</div>'
			else: return template('''<form action="{{cproot}}search" method="post" enctype="multipart/form-data" name='searchAudio'><input type="hidden" name="album" value="{{album}}" /><input type="text" name="query" placeholder='Search..' /><input type="submit" value="Search" /></form><br>''', cproot=db['settings']['httpdroot'], album=album)
		else:
			if atplayer==True: return '<div style="position: absolute; top: 30px; right:16px;">'+template('''<form action="{{cproot}}search" method="post" enctype="multipart/form-data" name='searchAudio'><input type="hidden" name="album" value="{{album}}" /><input type="text" name="query" placeholder='Search..' value='{{prefilled}}' /><input type="submit" value="Search" /></form><br>''', cproot=db['settings']['httpdroot'], album=album, prefilled=prefilled)+'</div>'
			else: return template('''<form action="{{cproot}}search" method="post" enctype="multipart/form-data" name='searchAudio'><input type="hidden" name="album" value="{{album}}" /><input type="text" name="query" placeholder='Search..' value='{{prefilled}}' /><input type="submit" value="Search" /></form><br>''', cproot=db['settings']['httpdroot'], album=album, prefilled=prefilled)
	else: return ''
def UIgenPlayer(audios): # Generate player UI
	playertpl=open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),'templates/player.tpl'), 'r').read()
	aformertpl=open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),'templates/audioformer.tpl'), 'r').read()
	a=''
	if not len(audios)==0:
		n=1
		lyrpp=''
		for audio in audios: 
			audioID=dblib.fname2id(db, str(audio['filename']))
			if ('lyrics' in audio) and (audio['lyrics']<>''): 
				lyrbtn=template('''<a href="#lyrics{{id}}" style='float: right'><img src='{{res}}player/media/data/lyrics.png' /> </a>''', id=n, res=os.path.join(db['settings']['httpdroot'], 'static/'))
				lyrics=''
				for ln in audio['lyrics'].splitlines(): lyrics+=ln+'<br />\n'
				lyrpp+=template('''<a href="#x" class="overlay" id="lyrics{{id}}"></a>
<div class="popup">
<center><h2>"{{fn}}" lyrics:</h2><br />
<div style="height:540px;width:100%;overflow:auto;">
{{!lyrics}}
</div>
</center>
<a class="close" title="Close" href="#close"></a>
</div>''', id=n, lyrics=lyrics, root=db['settings']['httpdroot'], aid=audio['filename'], fn=audio['artist']+' - '+audio['title'])
			else: lyrbtn=''
			a+=template(aformertpl, artist=audio['artist'], title=audio['title'], path=os.path.join(db['settings']['httpdroot'],'getAudio/', audio['filename']), id=str(audioID), num=str(n),res=os.path.join(db['settings']['httpdroot'], 'static/'), aid=audio['filename'], shr=os.path.join(db['settings']['httpdroot'], 'audio'), lyrbtn=lyrbtn, lyrpp=lyrpp)+'\n'
			n+=1
	return template(playertpl, body=a, res=os.path.join(db['settings']['httpdroot'], 'static/'))+'\n'+lyrpp

@route('/') # Main page
def mainPage():
	auth(db['settings']['permissions']['view'])
	perms=['Administrators', 'Editors', 'Users']
	if ('username' in request.cookies): 
		if (request.cookies['username'] in db['accounts']): welcomeback='Welcome back, '+request.cookies['username']+' (group '+perms[db['accounts'][request.cookies['username']]['access_level']]+')! If not, please <a href="'+db['settings']['httpdroot']+'logout">logout</a>.<br>'
		else: welcomeback='Hello, anonymous user! If you want <a href="'+db['settings']['httpdroot']+'login">login</a>, you`re always welcome.<br>'
	else: welcomeback='Hello, anonymous user! If you want <a href="'+db['settings']['httpdroot']+'login">login</a>, you`re always welcome.<br>'
	pagetpl=open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),'templates/mainPg.tpl'), 'r').read()
	linktpl=open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),'templates/mainPgLink.tpl'), 'r').read()
	links=template(linktpl, link=os.path.join(db['settings']['httpdroot'], 'allAudios'), name='All audios', itemsCount=str(len(db['audios'])))+'\n'
	for alb in db['alist']:
		links+=template(linktpl, link=os.path.join(db['settings']['httpdroot'], 'album', alb), name=alb, itemsCount=str(len(db['albums'][alb])))+'\n'
	
	return template(pagetpl, sname=db['settings']['servername'], res=os.path.join(db['settings']['httpdroot'], 'static/'), header=header, footer=footer, links=links, welcometext=welcomeback+db['settings']['welcometext'], search=genSearch('', False))



@route('/allAudios') # All audios
def allAudiosDisplay():
	auth(db['settings']['permissions']['view'])
	pagetpl=open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),'templates/audioscatalog.tpl'), 'r').read()
	audios=dblib.getAudios(db)[0]
	if not len(audios)==0:
		pllinks=genPlLinks()+genSearch('')
		a=UIgenPlayer(audios)
	else: 
		a='<br /><center><h2 style="color: white">No audios present :(</h2></center>'
		pllinks=''
	return template(pagetpl, pgname=('All audios - '+db['settings']['servername']), content=a, title=db['settings']['servername'],res=os.path.join(db['settings']['httpdroot'], 'static/'), pllinks=pllinks, header=header, footer=footer)

	
@route('/album') # Placeholder for case of no album specified
@route('/album/')
def albumIndex(): return HTTPResponse(status=424, body='<h1>Error: No album specified!</h1><script>location.replace(document.referrer);</script>')
			
@route('/album/<album>') # Album display
def albumDisplay(album):
	auth(db['settings']['permissions']['view'])
	album=unquote(album)
	pagetpl=open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),'templates/audioscatalog.tpl'), 'r').read()
	aformertpl=open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),'templates/audioformer.tpl'), 'r').read()
	if (album in db['alist']):
		a=''
		audios,relreq=dblib.getAudios(db, album)
		if relreq: dblib.saveDB(dbPath, db)
		if not len(audios)==0:
			a=UIgenPlayer(dblib.getAudios(db, album)[0])
		else: a+='<br /><center><h2 style="color: white">No audios present :(</h2></center>'
		pgn=('Album \"'+album+'\" display - '+db['settings']['servername'])
	else:
		a='<br /><center><h2 style="color: white">Album \"'+album+'\" does not exist :(</h2></center>'
		pgn=('Album \"'+album+'\" not exist - '+db['settings']['servername'])
	return template(pagetpl, pgname=pgn, content=a, title=db['settings']['servername'],res=os.path.join(db['settings']['httpdroot'], 'static/'), pllinks=genPlLinks()+'\n'+genSearch(album), header=header, footer=footer)

@route('/audio<aid:int>') # Shared audio display
def audioDisplay(aid):
	auth(db['settings']['permissions']['view'])
	pagetpl=open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),'templates/audioscatalog.tpl'), 'r').read()
	aformertpl=open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),'templates/audioformer.tpl'), 'r').read()
	audioID=dblib.fname2id(db, aid)
	if audioID>-1:
		audio=db['audios'][audioID]
		lyrpp=''
		if ('lyrics' in audio) and (audio['lyrics']<>''): 
				lyrbtn=template('''<a href="#lyrics{{id}}" style='float: right'><img src='{{res}}player/media/data/lyrics.png' /> </a>''', id=1, res=os.path.join(db['settings']['httpdroot'], 'static/'))
				lyrics=''
				for ln in audio['lyrics'].splitlines(): lyrics+=ln+'<br />\n'
				lyrpp+=template('''<a href="#x" class="overlay" id="lyrics{{id}}"></a>
<div class="popup">
<center><h2>"{{fn}}" lyrics:</h2><br />
<div style="height:540px;width:100%;overflow:auto;">
{{!lyrics}}
</div>
</center>
<a class="close" title="Close" href="#close"></a>
</div>''', id=1, lyrics=lyrics, root=db['settings']['httpdroot'], aid=audio['filename'], fn=audio['artist']+' - '+audio['title'])
		else: lyrbtn=''
		a=template(open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),'templates/player.tpl'), 'r').read(), body=template(aformertpl, artist=audio['artist'], title=audio['title'], lyrbtn=lyrbtn, path=os.path.join(db['settings']['httpdroot'],'getAudio/', audio['filename']), id=str(audioID), num='0',res=os.path.join(db['settings']['httpdroot'], 'static/'), aid=audio['filename'], shr=os.path.join(db['settings']['httpdroot'], 'audio'))+'\n', res=os.path.join(db['settings']['httpdroot'], 'static/'))+'\n'+lyrpp
		pgn=('\"'+audio['artist']+' - '+audio['title']+'\" - '+db['settings']['servername'])
	else:
		pgn=('Audio not exist - '+db['settings']['servername'])
		a='<br /><center><h2 style="color: white">Audio not exist :(</h2></center>'
	return template(pagetpl, pgname=pgn, content=a, title=db['settings']['servername'],res=os.path.join(db['settings']['httpdroot'], 'static/'), pllinks=genPlLinks(), header=header, footer=footer)

# User API

@route('/getAudio') # Placeholder for case of no audio ID specified
@route('/getAudio/')
def gaph():
	return HTTPResponse(status=424, body='<h1>Error: Audio ID expected!</h1>')
@route('/getAudio/<num>') # Audios fetching
def server_audios(num):
	auth(db['settings']['permissions']['view'])
	try:
		id=dblib.fname2id(db, int(num))
		if int(id)<0: return HTTPResponse(status=404, body='<h1>Error: Audio not found!</h1>')
		else:
			return static_file(db['audios'][id]['filename'], root=db['settings']['musicdir'])
	except ValueError: return HTTPResponse(status=424, body='<h1>Error: Incorrect audio ID!</h1>')

@route('/getAudio/lyrics') # Placeholder for case of no audio ID specified
@route('/getAudio/lyrics/')
def gaph():
	return HTTPResponse(status=424, body='<h1>Error: Audio ID expected!</h1>')
@route('/getAudio/lyrics/<num>') # Lyrics fetching
def server_audios(num):
	auth(db['settings']['permissions']['view'])
	try:
		id=dblib.fname2id(db, int(num))
		if int(id)<0: return HTTPResponse(status=404, body='<h1>Error: Audio not found!</h1>')
		else:
			try: return db['audios'][id]['lyrics']
			except KeyError: return ''
	except ValueError: return HTTPResponse(status=424, body='<h1>Error: Incorrect audio ID!</h1>')

@route('/static/<path:path>') # Static files
def server_static(path):
	auth(db['settings']['permissions']['view'])
	path=unquote(path)
	if path=='player/js/jquery.html5audio.settings_playlist_selector_with_scroll.js': # Icons path fix
		return template(open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),'static', path), 'r').read(),res=os.path.join(db['settings']['httpdroot'], 'static/player/'))
	else: return static_file( os.path.basename(path), (os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), 'static/', os.path.dirname(path))))

def genplm3u8(audios):
	auth(db['settings']['permissions']['view'])
	out='#EXTM3U\n'
	for audio in audios: out+=template('#EXTINF:,{{!name}}\n{{!url}}\n', name=audio['artist']+' - '+audio['title'], url=os.path.join(db['settings']['httpdroot'], 'getAudio', audio['filename']))
	return out
@route(db['settings']['plUrl']) #  m3u8 playlist api
def genm3upl():
	auth(db['settings']['permissions']['view'])
	return genplm3u8(db['audios'])
@route(db['settings']['plsUrl'])
def genm3upla(album):
	auth(db['settings']['permissions']['view'])
	album = unquote(album)
	if album==None: album=''
	if (album in db['alist']) or album=='': return genplm3u8(dblib.getAudios(db, album)[0])
	else: return HTTPResponse(status=404, body='Album not found!')
@route(db['settings']['plUrl'], method='POST')
def genm3uplalb():
	auth(db['settings']['permissions']['view'], unquote(str(request.forms.get('token'))))
	album = request.forms.get('album')
	if album==None: album=''
	if (album in db['alist']) or album=='': return genplm3u8(dblib.getAudios(db, album)[0])
	else: return HTTPResponse(status=404, body='Album not found!')	

@route('/api/playlist') #  JSON playlist api
def genPlJSON():
	auth(db['settings']['permissions']['view'])
	return json.dumps(db['audios'])
@route('/api/playlist/<album>')
def genPlJSON(album):
	auth(db['settings']['permissions']['view'])
	album = unquote(album)
	if album==None: album=''
	if (album in db['alist']) or album=='': return json.dumps(dblib.getAudios(db, album)[0])
	else: return HTTPResponse(status=404, body='Album not found!')
@route('/api/playlist', method='POST')
def genPlJSONalb():
	auth(db['settings']['permissions']['view'], unquote(str(request.forms.get('token'))))
	album = request.forms.get('album')
	if album==None: album=''
	if (album in db['alist']) or album=='': return json.dumps(dblib.getAudios(db, album)[0])
	else: return HTTPResponse(status=404, body='Album not found!')
@route('/api/albums')
def genAlbListJSON():
	auth(db['settings']['permissions']['view'], unquote(str(request.forms.get('token'))))
	return json.dumps(db['alist'])

# Control API

@route('/control/reload') # reload database from disk
def reloadDB():
	global db
	auth(db['settings']['permissions']['system'], request.forms.get('token'))
	db=dblib.loadDB(dbPath)
	sys.stdout.write('DB has reloaded from disk by Control API request!\n')
	return '<h1>Success!</h1><script>location.replace(document.referrer);</script>'
	
@route('/control/upload', method='POST') # Upload new audio
def uploadAudio():
	auth(db['settings']['permissions']['edit'], request.forms.get('token'))
	try:
		artist = request.forms.get('artist')
		title = request.forms.get('title')
		audioFile = request.files.get('audioFile')
		name, ext = os.path.splitext(audioFile.filename)
		fname=dblib.regAudio(db, artist, title)
		if fname<>False:
			save_path = "/tmp/{category}"
			if not os.path.exists(db['settings']['musicdir']):
				os.makedirs(db['settings']['musicdir'])
			audioFile.save(os.path.join(db['settings']['musicdir'],fname))
			dblib.saveDB(dbPath, db)
			return '<h1>Success!</h1><script>location.replace(document.referrer);</script>'
		else: return HTTPResponse(status=500, body='<h1>Upload error at server side :(</h1><script>location.replace(document.referrer);</script>')
	except AttributeError: return HTTPResponse(status=424, body='<h1>Error: No file pushed!</h1><script>location.replace(document.referrer);</script>')

@route('/control/delAudio', method='POST') # Delete audio
def delAudio():
	auth(db['settings']['permissions']['edit'], request.forms.get('token'))
	id = request.forms.get('id')
	try:
		id=int(id)
		fname=dblib.unregAudio(db, id)
		if fname<>False:
			try: os.remove(os.path.join(db['settings']['musicdir'], fname))
			except OSError as e: print(e)
			dblib.saveDB(dbPath, db)
			return '<h1>Success!</h1><script>location.replace(document.referrer);</script>'
		else: return HTTPResponse(status=404, body='<h1>Error: Audio with specified ID not found</h1><script>location.replace(document.referrer);</script>')
	except ValueError: return HTTPResponse(status=424, body='<h1>Request error: Incorrect ID!</h1><script>location.replace(document.referrer);</script>')

@route('/control/modifyAudio', method='POST') # Modify audio
def modAudio():
	auth(db['settings']['permissions']['edit'], request.forms.get('token'))
	try:
		id = int(request.forms.get('id'))
		artist = request.forms.get('artist')
		title = request.forms.get('title')
		lyrics = request.forms.get('lyrics')
		if dblib.modifyAudio(db, id, artist, title, lyrics):
			dblib.saveDB(dbPath, db)
			return '<h1>Success!</h1><script>location.replace(document.referrer);</script>'
		else: return HTTPResponse(status=404, body='<h1>Error: Audio with specified ID not found</h1><script>location.replace(document.referrer);</script>')
	except ValueError: return HTTPResponse(status=417, body='<h1>Error: Incorrect ID value (int expected)</h1><script>location.replace(document.referrer);</script>')

@route('/control/moveAudio', method='POST') # Move audio higher/below in list
def moveAudio():
	auth(db['settings']['permissions']['edit'], request.forms.get('token'))
	try:
		id1 = int(request.forms.get('id1'))
		id2 = int(request.forms.get('id2'))
	except ValueError: return HTTPResponse(status=417, body='<h1>Error: Bad IDs fields data!</h1><script>location.replace(document.referrer);</script>')
	album = request.forms.get('album')
	if album==None: album=''
	if dblib.moveAudio(db, id1, id2, album):
		dblib.saveDB(dbPath, db)
		return '<h1>Success!</h1><script>location.replace(document.referrer);</script>'
	else: return HTTPResponse(status=424, body='<h1>Request error</h1><script>location.replace(document.referrer);</script>')

@route('/control/addAlbum', method='POST') # Create album
def addAlbum():
	auth(db['settings']['permissions']['edit'], request.forms.get('token'))
	album = request.forms.get('album')
	if album<>None:
		if dblib.addAlbum(db, album):
			dblib.saveDB(dbPath, db)
			return '<h1>Success!</h1><script>location.replace(document.referrer);</script>'
		else: return HTTPResponse(status=424, body='<h1>Error: Album already exist!</h1><script>location.replace(document.referrer);</script>')
	else: return HTTPResponse(status=417, body='<h1>Error: Empty \"Album\" field!</h1><script>location.replace(document.referrer);</script>')

@route('/control/delAlbum', method='POST') # Delete album
def delAlbum():
	auth(db['settings']['permissions']['edit'], request.forms.get('token'))
	album = request.forms.get('album')
	if album<>None:
		if dblib.delAlbum(db, album):
			dblib.saveDB(dbPath, db)
			return '<h1>Success!</h1><script>location.replace(document.referrer);</script>'
		else: return HTTPResponse(status=424, body='<h1>Error: Album not exist!</h1><script>location.replace(document.referrer);</script>')
	else: return HTTPResponse(status=417, body='<h1>Error: Empty \"Album\" field!</h1><script>location.replace(document.referrer);</script>')

@route('/control/albumAdd', method='POST') # Add audio to album
def albumAdd():
	auth(db['settings']['permissions']['edit'], request.forms.get('token'))
	try:
		try:
			id = int(request.forms.get('id'))
		except TypeError: return '<h1>Error: Incorrect ID field value</h1><script>location.replace(document.referrer);</script>'	
		album = request.forms.get('album')
		if dblib.albumAdd(db, album, id):
			dblib.saveDB(dbPath, db)
			return '<h1>Success!</h1><script>location.replace(document.referrer);</script>'
		else: return HTTPResponse(status=404, body='<h1>Error: Audio with specified ID not found</h1><script>location.replace(document.referrer);</script>')
	except ValueError: return HTTPResponse(status=424, body='<h1>Error: Incorrect ID field value</h1><script>location.replace(document.referrer);</script>')

@route('/control/albumDel', method='POST') # Delete audio from album
def albumDel():
	auth(db['settings']['permissions']['edit'], request.forms.get('token'))
	try:
		try:
			id = int(request.forms.get('id'))
		except TypeError: return '<h1>Error: Incorrect ID field value</h1><script>location.replace(document.referrer);</script>'	
		album = request.forms.get('album')
		if dblib.albumDel(db, album, id):
			dblib.saveDB(dbPath, db)
			return '<h1>Success!</h1><script>location.replace(document.referrer);</script>'
		else: return HTTPResponse(status=404, body='<h1>Error: Audio with specified ID not found</h1><script>location.replace(document.referrer);</script>')
	except ValueError: return HTTPResponse(status=424, body='<h1>Error: Incorrect ID field value</h1><script>location.replace(document.referrer);</script>')

@route('/control/moveAlbum', method='POST') # Move album higher/below in list
def moveAlbum():
	auth(db['settings']['permissions']['edit'], request.forms.get('token'))
	try:
		id1 = str(request.forms.get('id1'))
		id2 = int(request.forms.get('id2'))
	except: return HTTPResponse(status=424, body='<h1>Request error</h1><script>location.replace(document.referrer);</script>')
	if dblib.moveAlbum(db, id1, id2):
		dblib.saveDB(dbPath, db)
		return '<h1>Success!</h1><script>location.replace(document.referrer);</script>'
	else: return HTTPResponse(status=424, body='<h1>Request error</h1><script>location.replace(document.referrer);</script>')

@route('/control/albumRename', method='POST') # Rename album
def renameAlbum():
	auth(db['settings']['permissions']['edit'], request.forms.get('token'))
	id1 = str(request.forms.get('old'))
	id2 = str(request.forms.get('new'))
	if dblib.renameAlbum(db, id1, id2):
		dblib.saveDB(dbPath, db)
		return '<h1>Success!</h1><script>location.replace(document.referrer);</script>'
	else: return HTTPResponse(status=424, body='<h1>Request error</h1><script>location.replace(document.referrer);</script>')
	
@route('/control/appearance', method='POST') # Appearance set
def cpApppearance():
	auth(db['settings']['permissions']['system'], request.forms.get('token'))
	global header
	global footer
	header = str(request.forms.get('header'))
	footer = str(request.forms.get('footer'))
	servername=str(request.forms.get('servername'))
	wtext = str(request.forms.get('wtext'))
	if header=='': header=dblib.newDBStruct['settings']['header']
	if wtext=='': wtext=dblib.newDBStruct['settings']['welcometext']
	if footer=='': footer=dblib.newDBStruct['settings']['footer']
	if servername=='': servername=dblib.newDBStruct['settings']['servername']
	db['settings']['servername']=servername
	db['settings']['welcometext']=wtext
	db['settings']['header']=header
	db['settings']['footer']=footer
	header=template(db['settings']['header'], servername=db['settings']['servername'], static=os.path.join(db['settings']['httpdroot'], 'static'))
	dblib.saveDB(dbPath, db)
	return '<h1>Success!</h1><script>location.replace(document.referrer);</script>'

@route('/control/system', method='POST') # System config set
def cpSystem():
	auth(db['settings']['permissions']['system'], request.forms.get('token'))
	plUrl = str(request.forms.get('plurl'))
	plsUrl = str(request.forms.get('plsurl'))
	musicdir = str(request.forms.get('musicdir'))
	httpdip = str(request.forms.get('httpdip'))
	httpdport = str(request.forms.get('httpdport'))
	httpdroot = str(request.forms.get('httpdroot'))
	if musicdir=='': musicdir=dblib.newDBStruct['settings']['musicdir']
	if httpdip=='': httpdip=dblib.newDBStruct['settings']['httpdip']
	if httpdport=='': httpdport=dblib.newDBStruct['settings']['httpdport']
	if httpdroot=='': httpdroot=dblib.newDBStruct['settings']['httpdroot']
	if plUrl=='': plUrl=dblib.newDBStruct['settings']['plUrl']
	if plsUrl=='': plsUrl=dblib.newDBStruct['settings']['plsUrl']
	db['settings']['plUrl']=plUrl
	db['settings']['plsUrl']=plsUrl
	db['settings']['musicdir']=musicdir
	db['settings']['httpdip']=httpdip
	db['settings']['httpdport']=httpdport
	db['settings']['httpdroot']=httpdroot
	dblib.saveDB(dbPath, db)
	return '<h1>Success!</h1><script>location.replace(document.referrer);</script>'
# Control Panel Web Interface

@route('/control')
@route('/control/')
def controlIndex():
	auth(db['settings']['permissions']['edit'], request.forms.get('token'))
	perms=['Administrators', 'Editors', 'Users', 'Guests']
	if ('username' in request.cookies): 
		if (request.cookies['username'] in db['accounts']): welcomeback='Welcome back, '+request.cookies['username']+' (group '+perms[db['accounts'][request.cookies['username']]['access_level']]+')! If not, please <a href="'+db['settings']['httpdroot']+'logout">logout</a>.<br>'
		else: welcomeback='Hello, anonymous user! If you want <a href="'+db['settings']['httpdroot']+'login">login</a>, you`re always welcome.<br>'
	else: welcomeback='Hello, anonymous user! If you want <a href="'+db['settings']['httpdroot']+'login">login</a>, you`re always welcome.<br>'
	return template(open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),'templates/control.tpl'), 'r').read(), httproot=db['settings']['httpdroot'], cdw=os.path.join(db['settings']['httpdroot'], 'control'), fsname=db['settings']['servername'], footer=footer, asize=str(float(get_size(db['settings']['musicdir'])*10/1024/1024)/10), acount=str(len(dblib.getAudios(db)[0])),dsize=str(float(os.path.getsize('msync.db')*10/1024)/10), bcount=str(len(db['albums'])), welcomeback=welcomeback)

@route('/control/audios')
@route('/control/audios/')
def cAudios():
	auth(db['settings']['permissions']['edit'], request.forms.get('token'))
	a=''
	def genActs(id):
		a='<p style="form { display: inline; }">'
		if id<(len(dblib.getAudios(db)[0])-1): a+=template('<form action="{{purl}}" name=\'mvDown{{id}}\' method="post"><input type="hidden" name="id1" value="{{id}}" align="right" /><input type="hidden" name="id2" value="-1" /><input type=\'submit\' value=\'v\' align=top/></form>', purl=os.path.join(db['settings']['httpdroot'], 'control/moveAudio'), id=id) 
		if id>0: a+=template('<form action="{{purl}}" name=\'mvUp{{fid}}\' method="post"><input type="hidden" name="id1" value="{{id}}" /><input type="hidden" name="id2" value="-1" /><input type=\'submit\' value=\'^\'/></form>', purl=os.path.join(db['settings']['httpdroot'], 'control/moveAudio'), id=id-1, fid=id) 
		a+=template('<form></form><a href="{{r}}{{id}}" target="_blank"><button>E</button></a>', r=os.path.join(db['settings']['httpdroot'], 'control/audios/'), id=id)
		a+=template('<form onSubmit="if(!confirm(\'Are you sure want remove this audio? This action is irreversible.\')){return false;}" action="{{purl}}" name=\'del{{id}}\' method="post"><input type="hidden" name="id" value="{{id}}" /><input type=\'submit\' value=\'X\'/></form>', purl=os.path.join(db['settings']['httpdroot'], 'control/delAudio'), id=id) 
		a+='</p>'
		return a
	for audio in dblib.getAudios(db)[0]:
		id=dblib.fname2id(db, audio['filename'])
		a+=template('''	<tr>
	<td width="50px">{{id}}</td>
		<td width="80px">{{fname}}</td>
		<td>{{artist}}</td>
		<td>{{title}}</td>
		<td width="100px"><div align="right" style="height: 20px; margin: 0;">{{!acts}}</div></td>
	</tr>''',id=str(id), fname=audio['filename'], artist=audio['artist'], title=audio['title'], acts=genActs(id))
	return template(open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),'templates/controlAudios.tpl'), 'r').read(), cproot=os.path.join(db['settings']['httpdroot'], 'control'), fsname=db['settings']['servername'], alist=a, footer=footer, res=os.path.join(db['settings']['httpdroot'], 'static/'))

@route('/control/audios/<id>', method='GET')
def cEditAudio(id):
	auth(db['settings']['permissions']['edit'], request.forms.get('token'))
	try:
		id=int(id)
	except ValueError: return HTTPResponse(status=424, body='<h1>Error: Incorrect ID!</h1><script>location.replace(document.referrer);</script>')
	try:
		pra=dblib.getAudios(db)[0][id]['artist']
		prt=dblib.getAudios(db)[0][id]['title']
		try: prl=dblib.getAudios(db)[0][id]['lyrics']
		except KeyError:
			dblib.getAudios(db)[0][id]['lyrics']=''
			prl=''
		return template(open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),'templates/controlEditAudio.tpl'), 'r').read(), cproot=os.path.join(db['settings']['httpdroot'], 'control/audios'), fsname=db['settings']['servername'], pra=pra, prt=prt, purl=os.path.join(db['settings']['httpdroot'], 'control/modifyAudio'), id=str(id), footer=footer, lyrics=prl)
	except IndexError: return HTTPResponse(status=404, body='<h1>Error: Audio with specified ID not found</h1><script>location.replace(document.referrer);</script>')
	
@route('/control/albums')
@route('/control/albums/')
def cAlbums():
	auth(db['settings']['permissions']['edit'], request.forms.get('token'))
	a=''
	def genActs(album, num):
		a='<p align=left style="form { display: inline; };">'
		if num<(len(db['alist'])-1): a+=template('<form action="{{purl}}" name=\'mvDown{{id}}\' method="post"><input type="hidden" name="id1" value="{{id}}" align="right" /><input type="hidden" name="id2" value="-1" /><input type=\'submit\' value=\'v\' align=top/></form>', purl=os.path.join(db['settings']['httpdroot'], 'control/moveAlbum'), id=num) 
		if num>0: a+=template('<form action="{{purl}}" name=\'mvUp{{fid}}\' method="post"><input type="hidden" name="id1" value="{{id}}" /><input type="hidden" name="id2" value="-1" /><input type=\'submit\' value=\'^\'/></form>', purl=os.path.join(db['settings']['httpdroot'], 'control/moveAlbum'), id=num-1, fid=num) 
		a+=template('<form></form><a href="{{r}}{{num}}"><button>E</button></a>', r=os.path.join(db['settings']['httpdroot'], 'control/albums/'), num=num)
		a+=template('<form onSubmit="if(!confirm(\'Are you sure want delete this album? This action is irreversible.\')){return false;}" action="{{purl}}" name=\'del{{album}}\' method="post"><input type="hidden" name="album" value="{{album}}" /><input type=\'submit\' value=\'X\'/></form>', purl=os.path.join(db['settings']['httpdroot'], 'control/delAlbum'), album=album) 
		a+='</p>'
		return a
	n=0
	for album in db['alist']:
		a+=template('''	<tr>
		<td>{{aname}}</td>
		<td>{{acount}}</td>
		<td width="100px"><div align="right" style="height: 22px; margin: 0;">{{!acts}}</div></td>
	</tr>''', aname=album, acount=str(len(dblib.getAudios(db, album)[0])), acts=genActs(album, n))
		n+=1
	return template(open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),'templates/controlAlbums.tpl'), 'r').read(), cproot=os.path.join(db['settings']['httpdroot'], 'control'), fsname=db['settings']['servername'], alist=a, footer=footer, res=os.path.join(db['settings']['httpdroot'], 'static/'))

@route('/control/albums/<aid>')
def cAlbum(aid):
	auth(db['settings']['permissions']['edit'], request.forms.get('token'))
	try:
		aid=int(aid)
	except: return HTTPResponse(status=404, body='Album not found!')
	if (aid>=0) and (aid<=len(db['alist'])):
		album=db['alist'][aid]
		a=''
		def genActs(id, album, fname):
			a='<p style="form { display: inline; }">'
			if id<(len(dblib.getAudios(db, album)[0])-1): a+=template('<form action="{{purl}}" name=\'mvDown{{id}}\' method="post"><input type="hidden" name="album" value="{{albname}}" /><input type="hidden" name="id1" value="{{id}}"/><input type="hidden" name="id2" value="-1" /><input type=\'submit\' value=\'v\' /></form>', purl=os.path.join(db['settings']['httpdroot'], 'control/moveAudio'), id=id, albname=album)
			if id>0: a+=template('<form action="{{purl}}" name=\'mvUp{{fid}}\' method="post"><input type="hidden" name="album" value="{{albname}}" /><input type="hidden" name="id1" value="{{id}}" /><input type="hidden" name="id2" value="-1" /><input type=\'submit\' value=\'^\'/></form>', purl=os.path.join(db['settings']['httpdroot'], 'control/moveAudio'), id=id-1, fid=id, albname=album) 
			a+=template('<form onSubmit="if(!confirm(\'Are you sure want delete this album entry? This action is irreversible.\')){return false;}" action="{{purl}}" name=\'del{{id}}\' method="post"><input type="hidden" name="album" value="{{albname}}" /><input type="hidden" name="id" value="{{id}}" /><input type=\'submit\' value=\'X\'/></form>', purl=os.path.join(db['settings']['httpdroot'], 'control/albumDel'), id=fname, albname=album) 
			a+='</p>'
			return a
		sf='<input type="hidden" name="album" value="'+album+'" />\n<select name=\'id\'>'
		n=0
		for audio in db['audios']:
			if not int(audio['filename']) in db['albums'][album]:
				sf+='<option value=\''+audio['filename']+'\' >'+str((n+1))+'. '+audio['artist']+' - '+audio['title']+'</option>\n'
				n+=1
		sf+='</select>'
		id=0
		for audio in dblib.getAudios(db, album)[0]:
			a+=template('''	<tr>
		<td width="50px">{{id}}</td>
			<td>{{artist}}</td>
			<td>{{title}}</td>
			<td width="100px"><div align="right" style="height: 20px; margin: 0;">{{!acts}}</div></td>
		</tr>''',id=str(id), artist=audio['artist'], title=audio['title'], acts=genActs(id, album, audio['filename']))
			id+=1
		return template(open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),'templates/controlAlbum.tpl'), 'r').read(), cproot=os.path.join(db['settings']['httpdroot'], 'control'), fsname=db['settings']['servername'], alist=a, footer=footer, res=os.path.join(db['settings']['httpdroot'], 'static/'), albname=album, addlist=sf)

@route('/control/appearance')
def cAppearance():
	auth(db['settings']['permissions']['system'], request.forms.get('token'))
	return template(open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),'templates/controlAppearance.tpl'), 'r').read(), cproot=os.path.join(db['settings']['httpdroot'], 'control'), fsname=db['settings']['servername'], header=db['settings']['header'], footer=db['settings']['footer'], purl=os.path.join(db['settings']['httpdroot'], 'control/appearance'), ffooter=footer, servername=db['settings']['servername'], wtext=db['settings']['welcometext'])

@route('/control/system')
def cSystem():
	auth(db['settings']['permissions']['system'], request.forms.get('token'))
	return template(open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),'templates/controlSystem.tpl'), 'r').read(), cproot=os.path.join(db['settings']['httpdroot'], 'control'), fsname=db['settings']['servername'], footer=db['settings']['footer'], purl=os.path.join(db['settings']['httpdroot'], 'control/system'), plurl=db['settings']['plUrl'], plsurl=db['settings']['plsUrl'], musicdir=db['settings']['musicdir'], httpdip=db['settings']['httpdip'], httpdport=db['settings']['httpdport'], httpdroot=db['settings']['httpdroot'])


# Accounts & access control realm

@route('/control/accounts')
@route('/control/accounts/')
def cAccounts():
	auth(db['settings']['permissions']['system'], request.forms.get('token'))
	
	systm=['', '', '', '']
	systm[db['settings']['permissions']['system']]=' selected'
	permCtl='''<form action="'''+db['settings']['httpdroot']+'''control/chPerms" method="post" enctype="multipart/form-data">System control permissions: <select name="system">
<option value="0"'''+systm[0]+'''>Administrators</option>
<option value="1"'''+systm[1]+'''>Editors</option>
<option value="2"'''+systm[2]+'''>Users</option>
<option value="3"'''+systm[3]+'''>Guests</option>
</select><br>\n'''
	edit=['', '', '', '']
	edit[db['settings']['permissions']['edit']]=' selected'
	permCtl+='''Content edit permissions: <select name="edit">
<option value="0"'''+edit[0]+'''>Administrators</option>
<option value="1"'''+edit[1]+'''>Editors</option>
<option value="2"'''+edit[2]+'''>Users</option>
<option value="3"'''+edit[3]+'''>Guests</option>
</select><br>\n'''
	view=['', '', '', '']
	view[db['settings']['permissions']['view']]=' selected'
	permCtl+='''View permissions: <select name="view">
<option value="0"'''+view[0]+'''>Administrators</option>
<option value="1"'''+view[1]+'''>Editors</option>
<option value="2"'''+view[2]+'''>Users</option>
<option value="3"'''+view[3]+'''>Guests</option>
</select><br /><input type="submit" value="Change permissions" /></form><br>\n'''
	def genActs(account):
		a='<p align=left style="form { display: inline; };">'
		a+=template('<form></form><a href="{{r}}{{num}}"><button>E</button></a>', r=os.path.join(db['settings']['httpdroot'], 'control/accounts/'), num=account)
		a+=template('<form onSubmit="if(!confirm(\'Are you sure want delete this account? This action is irreversible.\')){return false;}" action="{{purl}}" name=\'delAccount:{{account}}\' method="post"><input type="hidden" name="username" value="{{account}}" /><input type=\'submit\' value=\'X\'/></form>', purl=os.path.join(db['settings']['httpdroot'], 'control/delAccount'), account=account) 
		a+='</p>'
		return a
	n=0
	a=''
	for account in db['accounts']:
		a+=template('''	<tr>
		<td>{{aname}}</td>
		<td width="40px"><div align="right" style="height: 22px; margin: 0;">{{!acts}}</div></td>
	</tr>''', aname=account, acts=genActs(account))
		n+=1
	return template(open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),'templates/controlAccounts.tpl'), 'r').read(), cproot=os.path.join(db['settings']['httpdroot'], 'control'), fsname=db['settings']['servername'], alist=a, footer=footer, res=os.path.join(db['settings']['httpdroot'], 'static/'), permCtl=permCtl)

@route('/control/createAccount', method='POST') # Create account
def createAccount():
	auth(db['settings']['permissions']['system'], request.forms.get('token'))
	try:
		username = unquote(str(request.forms.get('username')))
		password = unquote(str(request.forms.get('password')))
		access_level = int(request.forms.get('access_level'))
		if username=='' or password=='' or access_level>3 or access_level<0: raise NameError, 'e'
		print(username+' '+password+' '+str(access_level))
		db['accounts'][username]={'access_level': access_level, 'passwd': hashlib.md5(db['settings']['passwd_salt']+password).hexdigest()}
		dblib.saveDB(dbPath, db)
		return '<h1>Success!</h1><script>location.replace(document.referrer);</script>'
	except: return HTTPResponse(status=424, body='<h1>Request error</h1><script>location.replace(document.referrer);</script>')

@route('/control/delAccount', method='POST') # Delete account
def deleteAccount():
	auth(db['settings']['permissions']['system'], request.forms.get('token'))
	try:
		username = unquote(str(request.forms.get('username')))
		if username=='': raise NameError, e
		db['accounts'].pop(username)
		dblib.saveDB(dbPath, db)
		return '<h1>Success!</h1><script>location.replace(document.referrer);</script>'
	except: return HTTPResponse(status=424, body='<h1>Request error</h1><script>location.replace(document.referrer);</script>')

@route('/control/chPerms', method='POST') # Change groups access permissions
def chPerms():
	auth(db['settings']['permissions']['system'], request.forms.get('token'))
	try:
		systm = int(request.forms.get('system'))
		edit = int(request.forms.get('edit'))
		view = int(request.forms.get('view'))
		if systm<0 or edit<0 or view<0 or systm>3 or edit>3 or view>3: raise NameError, 'e'
		db['settings']['permissions']['system']=systm
		db['settings']['permissions']['edit']=edit
		db['settings']['permissions']['view']=view
		dblib.saveDB(dbPath, db)
		return '<h1>Success!</h1><script>location.replace(document.referrer);</script>'
	except: return HTTPResponse(status=424, body='<h1>Request error</h1><script>location.replace(document.referrer);</script>')

@route('/control/accounts/<account>', method='GET')
def cEditAccount(account):
	auth(db['settings']['permissions']['edit'], request.forms.get('token'))
	if (account in db['accounts']):
		pru=account
		group=['', '', '', '']
		group[db['accounts'][account]['access_level']]=' selected'
		chgr='''<select name="access_level"><option value="3"'''+group[3]+'''>Disabled account</option>
<option value="2"'''+group[2]+'''>User</option>
<option value="1"'''+group[1]+'''>Editor</option>
<option value="0"'''+group[0]+'''>Administrator</option></select>'''
		return template(open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),'templates/controlEditAccount.tpl'), 'r').read(), cproot=os.path.join(db['settings']['httpdroot'], 'control/accounts'), fsname=db['settings']['servername'], pru=account, purl=os.path.join(db['settings']['httpdroot'], 'control/modifyAccount'), footer=footer, grlst=chgr)
	else: return HTTPResponse(status=404, body='<h1>Error: Specified account not found!</h1><meta http-equiv="refresh" content="0; URL='+db['settings']['httpdroot']+'control/accounts" />')

@route('/control/modifyAccount', method='POST') # Modify account
def modAcc():
	auth(db['settings']['permissions']['system'], request.forms.get('token'))
	try:
		al=int(request.forms.get('access_level'))
		if al>3 or al<0: raise TypeError
	except: return HTTPResponse(status=424, body='<h1>Error: Incorrect access_level field value</h1><script>location.replace(document.referrer);</script>')
	prev=request.forms.get('username')
	new=pr=request.forms.get('newusername')
	passwd=pr=request.forms.get('password')
	if (prev in db['accounts']):
		db['accounts'][prev]['access_level']=al
		if passwd<>'': db['accounts'][prev]['passwd']=hashlib.md5(db['settings']['passwd_salt']+passwd).hexdigest()
		if (prev<>new) and (new<>''): db['accounts'][new]=db['accounts'].pop(prev)
		dblib.saveDB(dbPath, db)
		return '<h1>Success!</h1><script>location.replace(document.referrer);</script>'
	else: return HTTPResponse(status=424, body='<h1>Error: Incorrect access_level field value</h1><script>location.replace(document.referrer);</script>')
		

# Search function

@route('/search') # Main search page
def startSearch():
	auth(db['settings']['permissions']['view'], request.forms.get('token'))
	return template(open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),'templates/audioscatalog.tpl'), 'r').read(), pgname=('Search - '+db['settings']['servername']), content='<br /><center><h3 style="color: white">Search audio:</h3></center>', title=db['settings']['servername'],res=os.path.join(db['settings']['httpdroot'], 'static/'), pllinks=genPlLinks()+'<center>'+genSearch('', False)+'</center>', header=header, footer=footer)

@route('/search', method='POST') # Search director
def searchDirector():
	auth(db['settings']['permissions']['view'], request.forms.get('token'))
	album = str(request.forms.get('album'))
	query = str(request.forms.get('query'))
	if album=='':
		return template('<meta http-equiv="refresh" content="0; URL={{root}}search/{{req}}" />', root=db['settings']['httpdroot'], req=query)
	else: return template('<meta http-equiv="refresh" content="0; URL={{root}}search/{{alb}}/{{req}}" />', root=db['settings']['httpdroot'], req=query, alb=album)


@route('/search/<query>') # Search in album
def searchFrontEnd(query):
	auth(db['settings']['permissions']['view'], request.forms.get('token'))
	query=unquote(query)
	src=dblib.getAudios(db)[0]
	result=dblib.searchAudio(src, query)
	audios=[]
	for id in result: audios.append(src[id])
	pagetpl=open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),'templates/audioscatalog.tpl'), 'r').read()
	if not len(audios)==0:
		pllinks=genPlLinks()+'\n'+genSearch('', True, query)
		a=UIgenPlayer(audios)
	else: 
		a='<br /><center><h2 style="color: white">Nothing was found by your request :(</h2>\n'+genSearch('', False, query)+'</center>'
		pllinks=genPlLinks()
	return template(pagetpl, pgname=('Search results for "'+query+'"'+db['settings']['servername']), content=a, title=db['settings']['servername'],res=os.path.join(db['settings']['httpdroot'], 'static/'), pllinks=pllinks, header=header, footer=footer)

@route('/search/<album>/<query>') # Search in album
def searchAlbFrontEnd(query, album):
	auth(db['settings']['permissions']['view'], request.forms.get('token'))
	query=unquote(query)
	album=unquote(album)
	pagetpl=open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),'templates/audioscatalog.tpl'), 'r').read()
	if album in db['alist']:
		src=dblib.getAudios(db, album)[0]
		result=dblib.searchAudio(src, query)
		audios=[]
		for id in result: audios.append(src[id])
		
		if not len(audios)==0:
			pllinks=genPlLinks()+'\n'+genSearch(album, True, query)
			a=UIgenPlayer(audios)
		else: 
			a='<br /><center><h2 style="color: white">Nothing was found by your request :(</h2>\n'+genSearch(album, False, query)+'</center>'+'</center>'
			pllinks=genPlLinks()
		return template(pagetpl, pgname=('Search results for "'+query+'" in album "'+album+'" - '+db['settings']['servername']), content=a, title=db['settings']['servername'],res=os.path.join(db['settings']['httpdroot'], 'static/'), pllinks=pllinks, header=header, footer=footer)
	else: return template(pagetpl, pgname=('Album "'+album+'" not exist - '+db['settings']['servername']), content='<br /><center><h2 style="color: white">Album "'+album+'" not exist, no sense to search</h2></center>', title=db['settings']['servername'],res=os.path.join(db['settings']['httpdroot'], 'static/'), pllinks='', header=header, footer=footer)	

@route('/search/')
def emptySearch():
	auth(db['settings']['permissions']['view'], request.forms.get('token'))
	return template(open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),'templates/audioscatalog.tpl'), 'r').read(), pgname=('Empty search request " - '+db['settings']['servername']), content='<br /><center><h2 style="color: white">Search field is empty, no sense to search</h2></center>', title=db['settings']['servername'],res=os.path.join(db['settings']['httpdroot'], 'static/'), pllinks='', header=header, footer=footer)
@route('/search/<album>/')
def emptySearch(album):
	auth(db['settings']['permissions']['view'], request.forms.get('token'))
	return template(open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),'templates/audioscatalog.tpl'), 'r').read(), pgname=('Empty search request " - '+db['settings']['servername']), content='<br /><center><h2 style="color: white">Search field is empty, no sense to search</h2></center>', title=db['settings']['servername'],res=os.path.join(db['settings']['httpdroot'], 'static/'), pllinks='', header=header, footer=footer)

@error(404)
@error(403)
def mistake(code):
	return '<title>Not found</title><center><h1>404 Not Found</h1>\n<hr>MelnikovSM`s MusicSync Server</center	>'
@error(405)
def mistake(code):
	return '<title>Method Not Allowed</title><center><h1>405 Method Not Allowed</h1>\n<hr>MelnikovSM`s MusicSync Server</center>'

if __name__ == "__main__":
	print('Starting up..')
	run(host=db['settings']['httpdip'], port=int(db['settings']['httpdport']), server='paste')
