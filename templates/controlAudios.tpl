<html>
<head>
	<meta charset="utf-8">
	<meta generator="MSM/MusicSync">
	<meta http-equiv="Content-Type" content="text/html">
	<title>Audios management - {{fsname}}</title>
</head>
<body>
<h1>Audios management - <a href='{{cproot}}'>Control panel</a></h1>
<form action="{{cproot}}/upload" method="post" enctype="multipart/form-data" name='uploadNew'>Upload new: <input type="text" name="artist" placeholder='Artist'/> <input type="text" name="title" placeholder='Title'/> <input type="file" name="audioFile" /><input type="submit" value="Upload" /></form>
<br />
<style>
form {display: inline-block;}
</style>
<table border="1" width="800px">
	<tr>
		<th width="50px">Seq. ID</th>
		<th width="80px">File Name</th>
		<th>Artist</th>
		<th>Title</th>
		<th width="100px">Control</th>
	</tr>
{{!alist}}
</table><br />
</body>
</html>