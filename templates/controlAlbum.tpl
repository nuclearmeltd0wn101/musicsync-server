<html>
<head>
	<meta charset="utf-8">
	<meta generator="MSM/MusicSync">
	<meta http-equiv="Content-Type" content="text/html">
	<script src="{{!res}}player/js/jquery-1.11.1.min.js"></script>
	<title>Edit album - {{fsname}}</title>
</head>
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
<body>
<h1>Edit album "{{albname}}"</h1>
<form action="{{!rootUrl}}control/albumRename" method="post" enctype="multipart/form-data" name='renameAlbum'><input type="hidden" name="old" value="{{albname}}" />Rename album: <input type="text" name="new" value='{{albname}}'/><input type="submit" value="Rename" /></form><br>
<form action="{{!rootUrl}}control/albumAdd" method="post" enctype="multipart/form-data">{{!addlist}}<input type="submit" value="Add to album" /></form>
<style>
form {display: inline-block;}
</style>
<div class='pl'><b>Loading entries, please wait..</b></div>
<script>

// Request Details
token='{{!token}}';
playlist='{{!albname}}';
rootUrl='{{!rootUrl}}';

// Request URL parser

decodeBase64 = function(s) {
    var e={},i,b=0,c,x,l=0,a,r='',w=String.fromCharCode,L=s.length;
    var A="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    for(i=0;i<64;i++){e[A.charAt(i)]=i;}
    for(x=0;x<L;x++){
        c=e[s.charAt(x)];b=(b<<6)+c;l+=6;
        while(l>=8){((a=(b>>>(l-=8))&0xff)||(x<(L-2)))&&(r+=w(a));}
    }
    return r;
};

if(token!='') {
	if(playlist=='') { var playlist='$aau' }
	var reqUrl=rootUrl+'api/playlist/'+playlist+'/'+decodeBase64(token);
}
else {
	if(playlist=='') { reqUrl=rootUrl+'api/playlist' }
	var reqUrl=rootUrl+'api/playlist/'+playlist
}

// JSON parser

$.getJSON( reqUrl , function( data ) {
  $( ".pl" ).replaceWith( '<div class="pl"></div>' );
  var items = [];
  console.log('Total '+data.length+' entries Loaded');
  items.push('<tr>\n<th width="50px">№</th>\n<th>Artist</th>\n<th>Title</th>\n<th width="100px">Controls</th>\n</tr>');

  	function genActs(id, len) {
  		a='<p style="form { display: inline; }">'
  		if(id!=0) { a+='<form action="'+rootUrl+'control/moveAudio" name=\'mvUp'+id+'\' method="post"><input type="hidden" name="album" value="'+playlist+'" /><input type="hidden" name="id1" value="'+(parseInt(id) - 1)+'" /><input type="hidden" name="id2" value="-1" /><input type=\'submit\' value=\'^\' /></form>' }
  		if((id+1)!=len) { a+='<form action="'+rootUrl+'control/moveAudio" name=\'mvDown'+id+'\' method="post"><input type="hidden" name="album" value="'+playlist+'" /><input type="hidden" name="id1" value="'+id+'"/><input type="hidden" name="id2" value="-1" /><input type=\'submit\' value=\'v\' /></form>' }
  		a+='<form onSubmit="if(!confirm(\'Are you sure want delete this album entry? This action is irreversible.\')){return false;}" action="'+rootUrl+'control/albumDel" name=\'del'+id+'\' method="post"><input type="hidden" name="album" value="'+playlist+'" /><input type="hidden" name="id" value="'+data[id]['filename']+'" /><input type=\'submit\' value=\'X\'/></form></p>';
  		return a;

  	}

  $.each( data, function( key, val ) {
  	items.push( '<tr>\n<td width="50px">' + (parseInt(key) + 1) + '</td>\n<td>' + val['artist'] + '</td>\n<td>' + val['title'] + '</td>\n<td width="100px"><div align="right" style="height: 20px; margin: 0;">' + (genActs(key, data.length)) + '</div></td>\n</tr>');
    //items.push( "#" + (parseInt(key) + 1) + '. ' + val['artist'] + " - " + val['title'] + "<br />" );
  });
 
  $( '<table />', {
    "class": "album_conten",
    "width": "100%",
    "border": '1',
    html: items.join( "" )
  }).appendTo( ".pl" );
}).fail(function() {
	$( ".pl" ).replaceWith( '<div class="pl"><b color="red">Entries load failed!</b></div>' );
    console.log( "[Fatal] Unable to load entries!" );
  });

</script>
<br />
</body>
</html>