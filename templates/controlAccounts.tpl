<html>
<head>
	<meta charset="utf-8">
	<meta generator="MSM/MusicSync">
	<meta http-equiv="Content-Type" content="text/html">
	<title>Accounts & access control management - {{fsname}}</title>
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
<h1>Accounts & access control</h1>
<h2>Permissions control</h2>
{{!permCtl}}
<h2>Accounts management</h2>
<form action="{{cproot}}/createAccount" method="post" enctype="multipart/form-data">Create new account: <input type="text" name="username" placeholder='Username'/>
<input type="password" name="password" placeholder='Password'/>
<select name="access_level">
<option value="3">Disabled account</option>
<option value="2">User</option>
<option value="1">Editor</option>
<option value="0">Administrator</option>
</select>
<input type="submit" value="Create account" /></form>
<br />
<style>
form {display: inline-block;}
</style>
<table border="1" width="800px">
	<tr>
		<th>Account name</th>
		<th width="40px">Control</th>
	</tr>
{{!alist}}
</table><br />
</body>
</html>