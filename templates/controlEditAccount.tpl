<html>
<head>
	<meta charset="utf-8">
	<meta generator="MSM/MusicSync">
	<meta http-equiv="Content-Type" content="text/html">
	<title>Edit account - {{fsname}}</title>
</head>
<body>
<h1>Edit account - <a href='{{cproot}}'>Control panel</a></h1>
<form action="{{purl}}" method="post" enctype="multipart/form-data">
<input type="hidden" name="username" value="{{pru}}" />
New username:  <input type="text" name="newusername" value="{{pru}}" /><br>
New password: <input type="password" name="password" value="" /><br>
Account status: {{!grlst}}<br>
<input type="submit" value="Modify account" />
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