<html>
<head>
	<meta charset="utf-8">
	<meta generator="MSM/MusicSync">
	<meta http-equiv="Content-Type" content="text/html">
	<title>Configure system - {{fsname}}</title>
</head>
<body>
<style>
body {
		color: white;
	    background: #333;
		font-family: 'Tahoma', Arial, sans-serif;
}
a {
	color: orange;
	font-family: 'Tahoma', Arial, sans-serif;
}
a:hover {
	color: lightgreen;
	font-family: 'Tahoma', Arial, sans-serif;
}
</style>
<h1>Configure system</h1>
<table>
<form action="{{purl}}" method="post" enctype="multipart/form-data">
<h3>System & Web Interface</h3>
<tr><td style='color: orange'>Server IP <a style='color:red'>*</a> </td><td><input type="text" name="httpdip" value="{{httpdip}}" size=120 /></td></tr>
<tr><td style='color: orange'>Server Port <a style='color:red'>*</a></td> <td><input type="text" name="httpdport" value="{{httpdport}}" size=120 /></td></tr>
<tr><td style='color: orange'>Server Root URL: </td><td><input type="text" name="httpdroot" value="{{httpdroot}}" size=120 /></td></tr>
<tr><td style='color: orange'>Audios dir: </td><td><input type="text" name="musicdir" value="{{musicdir}}" size=120 /></td></tr>
</table>
<h3>M3U Playlists Generator</h3>
<table>
<tr><td style='color: orange'>M3U all audios playlist URL <a style='color:red'>*</a> <td><input type="text" name="plurl" value="{{plurl}}" size=120 /></td></tr>
<br>
<tr><td style='color: orange'>M3U albums playlist URL template <a style='color:red'>*</a></td> <td><input type="text" name="plsurl" value="{{plsurl}}" size=120 /></td></tr>
</table>
Varribles: album - album name<br>
<p style='color:red'>Notice: server restart required to apply changes for values, marked with "*".</p>
<input type="submit" value="Modify system config" />
</form>
</body>
</html>