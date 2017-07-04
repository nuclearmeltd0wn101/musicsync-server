<html>
<head>
	<meta charset="utf-8">
	<meta generator="MSM/MusicSync">
	<meta http-equiv="Content-Type" content="text/html">
	<meta http-equiv="Refresh" content="90" />
	<title>Summary</title>
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
<h2>This server summary</h2>
<table>
	<tr>
		<td style='color: orange'>Server name: </td>
		<td>{{sname}}</td>
	</tr>
	<tr>
		<td style='color: orange'>MusicSync Server version: </td>
		<td>{{srvver}}</td>
	</tr>
	<tr>
		<td style='color: orange'>Total audios:</td>
		<td>{{ta}} (<font color='orange'>{{asz}} MB</font>)</td>
	</tr>
	<tr>
		<td style='color: orange'>Total <a href='{{root}}artists' target='_blank'>artists</a>: </td>
		<td>{{artst}}</td>
	</tr>
	<tr>
		<td style='color: orange'>Total albums: </td>
		<td>{{albst}}</td>
	</tr>
	<tr>
		<td style='color: orange'>Database size: </td>
		<td>{{dsize}} KB</td>
	</tr>
</table>
<h2>Quick actions</h2>
<h3>Quick upload</h3>
<form action="{{root}}control/upload" method="post" enctype="multipart/form-data" name='uploadNew'><input type="text" name="artist" placeholder='Artist'/> <input type="text" name="title" placeholder='Title'/> <input type="file" name="audioFile" /><input type="submit" value="Upload" /></form>
<p>{{!dbrel}}</p>
</body>
</html>