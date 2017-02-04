<html>
<head>
	<meta charset="utf-8">
	<meta generator="MSM/MusicSync">
	<meta http-equiv="Content-Type" content="text/html">
	<title>Configure system - {{fsname}}</title>
</head>
<body>
<h1>Configure system - <a href='{{cproot}}'>Control panel</a></h1>
<form action="{{purl}}" method="post" enctype="multipart/form-data">
<h3>System & Web Interface</h3>
Server IP: <input type="text" name="httpdip" value="{{httpdip}}" size=120 /><br>
Server Port: <input type="text" name="httpdport" value="{{httpdport}}" size=120 /><br>
Server Root URL: <input type="text" name="httpdroot" value="{{httpdroot}}" size=120 /><br>
Audios dir: <input type="text" name="musicdir" value="{{musicdir}}" size=120 /><br>
<h3>M3U Playlists Generator</h3>
M3U all audios playlist URL: <input type="text" name="plurl" value="{{plurl}}" size=120 /><br>
<br>
M3U albums playlist URL template: <input type="text" name="plsurl" value="{{plsurl}}" size=120 /><br>
Varribles: album - album name<br>
<p style='color:red'>Notice: server restart required to apply changes, made on this page!</p>
<input type="submit" value="Modify system config" />
</form>
<style>
#bottomdiv{
 font-family: 'Tahoma', Arial, sans-serif;
 position: absolute;
 bottom: 0px;
}
</style>
<div id="bottomdiv">{{!footer}}</div>
</body>
</html>