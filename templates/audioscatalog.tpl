<html>
<head>
	<meta charset="utf-8">
	<meta generator="MSM/MusicSync">
	<meta http-equiv="Content-Type" content="text/html">
	<title>{{pgname}}</title>

  <link rel="stylesheet" type="text/css" href="{{res}}player/css/jquery.jscrollpane.css" media="all" />
	<link rel="stylesheet" type="text/css" href="{{res}}player/css/jquery.selectbox.css" />
	<link rel="stylesheet" type="text/css" href="{{res}}player/css/html5audio_default.css" />
	<link rel="stylesheet" type="text/css" href="{{res}}player/css/html5audio_playlist_selector_with_scroll.css" />

	<script type="text/javascript" src="{{res}}player/js/swfobject.js"></script><!-- flash backup --> 
	<script type="text/javascript" src="{{res}}player/js/jquery-1.11.1.min.js"></script>
	<script type="text/javascript" src="{{res}}player/js/jquery-ui-1.10.3.custom.min.js"></script><!-- jquery ui sortable/draggable -->
	<script type="text/javascript" src="{{res}}player/js/jquery.ui.touch-punch.min.js"></script><!-- mobile drag/sort -->
	<script type="text/javascript" src="{{res}}player/js/jquery.mousewheel.min.js"></script><!-- scroll in playlist -->
	<script type="text/javascript" src="{{res}}player/js/jquery.jscrollpane.min.js"></script><!-- scroll in playlist -->
	<script type="text/javascript" src="{{res}}player/js/jquery.selectbox-0.2.js"></script><!-- playlist selector dropdown -->
	<script type="text/javascript" src="{{res}}player/js/id3-minimized.js"></script><!-- id3 tags -->
	<script type="text/javascript" src="{{res}}player/js/jquery.html5audio.min.js"></script>
	<script type="text/javascript" src="{{res}}player/js/jquery.html5audio.func.js"></script>
	<script type="text/javascript" src="{{res}}player/js/jquery.html5audio.settings_playlist_selector_with_scroll.js"></script>
</head>
<body>
<h1 style="color: white">{{!header}}</h1>
<div id="componentWrapper">
<div class="playerHolder">
<div class="player_mediaName_Mask">
<div class="player_mediaName"></div>
</div>
<div class="player_mediaTime">
<div class="player_mediaTime_current">0:00</div><div class="player_mediaTime_total">0:00</div>
</div>
<div class="player_controls">
<div class="controls_prev"><img src='{{res}}player/media/data/icons/set1/prev.png' alt='controls_prev'/></div>
<div class="controls_toggle"><img src='{{res}}player/media/data/icons/set1/play.png' alt='controls_toggle'/></div>
<div class="controls_next"><img src='{{res}}player/media/data/icons/set1/next.png' alt='controls_next'/></div>
<div class="player_volume"><img src='{{res}}player/media/data/icons/set1/volume.png' alt='player_volume'/></div>
<div class="volume_seekbar">
<div class="volume_bg"></div>
<div class="volume_level"></div>
<div class="player_volume_tooltip"><p></p></div>
</div>
<div class="player_loop"><img src='{{res}}player/media/data/icons/set1/loop.png' alt='player_loop'/></div>
<div class="player_shuffle"><img src='{{res}}player/media/data/icons/set1/shuffle.png' alt='player_shuffle'/></div>
</div>
<div class="player_progress">
<div class="progress_bg"></div>
<div class="load_progress"></div>
<div class="play_progress"></div>
<div class="player_progress_tooltip"><p></p></div>
</div>
</div>
<div class="playlistHolder">
<div class="componentPlaylist">
<div class="playlist_inner">
</div>
</div>
<div class="preloader"></div>
</div>
</div>  
<div id="playlist_list">
<ul id='playlist1'>
{{!body}}
</ul>
</div>

<style>
#bottomdiv{
 position: absolute;
 bottom: 0px;
 right: 0px;
}
</style>
<div id="bottomdiv"><p style="color: white">{{!footer}}</div>
{{!pllinks}}
</body>
</html>