<html>
<head>
	<meta charset="utf-8">
	<meta generator="MSM/WSADM">
	<meta http-equiv="Refresh" content="90" />
	<meta http-equiv="Content-Type" content="text/html">
	<title>Menu</title>
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
<a href='{{root}}control/status' target='main'>Server summary</a><br />
<h3>Content management</h3>
<a href='{{root}}control/audios' target='main'>All audios ({{at}})</a><br />
{{!audiosCtlLinks}}
<a href='{{root}}control/albums' target='main'>Manage albums ({{al}})</a><br />

{{!admbtns}}
</body>
</html>