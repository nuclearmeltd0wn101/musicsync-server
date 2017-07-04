<html>
<head>
	<meta charset="utf-8">
	<meta generator="MSM/MusicSync">
	<meta http-equiv="Content-Type" content="text/html">
	<title>Albums management - {{fsname}}</title>
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
<h1>Albums management</h1>
<form action="{{cproot}}/addAlbum" method="post" enctype="multipart/form-data">Create new: <input type="text" name="album" placeholder='Album name'/><input type="submit" value="Create album" /></form>
<br />
<style>
form {display: inline-block;}
</style>
<table border="1" width="800px">
	<tr>
		<th>Album name</th>
		<th width="70px">Total entries</th>
		<th width="10	0px">Control</th>
	</tr>
{{!alist}}
</table><br />
</body>
</html>