README For The Radio App Built Into PipOS

Songs Are At Path WhereverThisIsInstalled/holotape/radio/songs/
Songs Have An Outside Folder Where Inside Them They Then Have The Mp3 File And A SongName.json With the Below Structure
[{"name": "songname", "length": "int(s):2ints", "artist": "artist"}]

Playlists Are At WhereverThisIsInstalled/holotape/radio/playlists/
Playlists Are Just A name.json With The Below Structure
[{"name": "playlistname", "songlist": ["song1.json","song2.json"]}]
