<html>
<head>
	<meta charset="utf-8">
	<meta generator="MSM/MusicSync">
	<meta http-equiv="Content-Type" content="text/html">
	<title>Configure appearance - {{fsname}}</title>
</head>
<body>
<h1>Configure appearance - <a href='{{cproot}}'>Control panel</a></h1>
<form action="{{purl}}" method="post" enctype="multipart/form-data">
Header HTML: <input type="text" name="header" value="{{header}}" size=120 /><br>
Varribles: servername - server name, static - path to static content dir<br>
Footer HTML: <input type="text" name="footer" value="{{ffooter}}" size=120 /><br>
<input type="submit" value="Change appearance" />
</form>
<style>
#bottomdiv{
 position: absolute;
 bottom: 0px;
}
</style>
<div id="bottomdiv">{{!footer}}</div>
</body>
</html>