<script>
function copyToClipboard(element) {
  var $temp = $("<input>");
  $("body").append($temp);
  $temp.val($(element).text()).select();
  document.execCommand("copy");
  $temp.remove();
}
</script>
<script type="text/javascript" src="{{res}}player/js/jquery.html5audio.min.js"></script>
<script type="text/javascript" src="{{res}}player/js/jquery.html5audio.func.js"></script>
<script type="text/javascript" src="{{res}}player/js/jquery.html5audio.settings_playlist_selector_with_scroll.js"></script>
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