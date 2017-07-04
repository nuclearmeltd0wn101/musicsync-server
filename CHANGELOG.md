MusicSync Server changelog:

04 Jul 2017 [20170704]:

* Added audio additional information (song ID, upload timestamp, mp3 size) display at audio edit page
* Server will attempt to write MP3 ID3 tags to audio after upload or when editing audio
* Added audios artists indexing and display at /artists page by artist`s audios descending
* Added (by add time) ascending/descending album content sort

28 Jun 2017 [20170628]:

* Server will attempt to read MP3 ID3 tags from uploaded audio if you leave 'artist' or 'title' fields unfilled [now server requires mutagen module from pip]

1 May 2017 [20170501]:

* Audios & album control pages migrated to JS entries load

5 Apr 2017 [20170405]:

* Minor bugfixes
* Permissions configuration expansion (added 3 new permissions)
* Control panel redesign

5 Feb 2017 [20170205]:

* Added modifiable main page
* All audios moved to dedicated page
* Added search ability
* Implemented authenication & access control

29 Jan 2017 [20170129]:
* Added lyrics add ability
* Playlist selector hides automatically if no user playlists created

25 Jan 2017 [20170125]:
* Improved appearance control page
* Added system settings edit page
* Fixed audios total zero size display if audios dir path is modified

20 Jan 2017 [20170120]:
* Added header & footer HTML code modification ability from C.P.
* Added .m3u8 online play playlists (/playlist.m3u8, /pl/<album>.m3u8)
* Modified template: messages show ability istead of player
* Added 210% page zoom at mobile browsers for better view & touch control ability

5 Jan 2017 [20170105]:
* Initial stable release
