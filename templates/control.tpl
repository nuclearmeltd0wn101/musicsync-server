<html>
<head>
	<meta charset="utf-8">
	<meta generator="MSM/MusicSync">
	<meta http-equiv="Content-Type" content="text/html">
	<title>Control panel - {{fsname}}</title>
</head>
<body>
<h1>Control Panel - <a href='{{httproot}}'>{{fsname}}</a></h1>
<style>
form {display: inline-block;}
</style>
<table border="1" width="800px">
	<tr>
		<th>Realm</th>
		<th width="120px">Total entries</th>
		<th width="160px">Size</th>
		<th width="30px">Control</th>
	</tr>
	<tr>
		<td>All audios</td>
		<td width="120px">{{acount}}</td>
		<td width="160px">{{asize}} MB</td>
		<td width="30px"><a href='{{cdw}}/audios'><button>Manage</button></a><br></td>
	</tr>
	<tr>
		<td>Albums</td>
		<td width="120px">{{bcount}}</td>
		<td width="160px">{{dsize}} KB*</td>
		<td width="30px"><a href='{{cdw}}/albums'><button>Manage</button></a><br></td>
	</tr>
</table><br />
* - DataBase total size, not albums only!<br>
You also may <a href='{{cdw}}/reload'><button>Reload DB from disk</button></a>
<style>
#bottomdiv{
 position: absolute;
 bottom: 0px;
}
</style>
<div id="bottomdiv">{{!footer}}</div>
</body>
</html>