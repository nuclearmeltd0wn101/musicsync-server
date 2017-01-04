<html>
<head>
	<meta charset="utf-8">
	<meta generator="MSM/MusicSync">
	<meta http-equiv="Content-Type" content="text/html">
	<title>Edit album - {{fsname}}</title>
</head>
<body>
<h1>Edit album - <a href='{{cproot}}/albums'>Control panel</a></h1>
<form action="{{cproot}}/albumRename" method="post" enctype="multipart/form-data" name='renameAlbum'><input type="hidden" name="old" value="{{albname}}" />Rename album: <input type="text" name="new" value='{{albname}}'/><input type="submit" value="Rename" /></form><br>
<form action="{{cproot}}/albumAdd" method="post" enctype="multipart/form-data">{{!addlist}}<input type="submit" value="Add to album" /></form>
<style>
form {display: inline-block;}
</style>
<table border="1" width="800px">
	<tr>
		<th width="50px">Seq. ID</th>
		<th>Artist</th>
		<th>Title</th>
		<th width="100px">Control</th>
	</tr>
{{!alist}}
</table><br />
</body>
</html>