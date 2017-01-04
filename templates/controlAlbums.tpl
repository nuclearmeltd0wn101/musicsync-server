<html>
<head>
	<meta charset="utf-8">
	<meta generator="MSM/MusicSync">
	<meta http-equiv="Content-Type" content="text/html">
	<title>Albums management - {{fsname}}</title>
</head>
<body>
<h1>Albums management - <a href='{{cproot}}'>Control panel</a></h1>
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