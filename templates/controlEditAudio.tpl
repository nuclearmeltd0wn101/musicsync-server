<html>
<head>
	<meta charset="utf-8">
	<meta generator="MSM/MusicSync">
	<meta http-equiv="Content-Type" content="text/html">
	<title>Edit audio - {{fsname}}</title>
</head>
<body>
<h1>Edit audio - <a href='{{cproot}}'>Control panel</a></h1>
<form action="{{purl}}" method="post" enctype="multipart/form-data">
<input type="hidden" name="id" value="{{id}}" />
New Artist:  <input type="text" name="artist" value="{{pra}}" /><br>
New Title: <input type="text" name="title" value="{{prt}}" /><br>
<input type="submit" value="Modify audio" />
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