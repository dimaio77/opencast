# opencast

Advanced audio streaming system for Second Life.
================================================

Opencast solves the problem of listeners disconnecting when an audio stream changes from one Shoutcast or Icecast server to a new one, when the Dj gets disconnected etc.
It also provides a platform for social djing with a chat controlled jukebox and the possiblity to create games (dj battles, name that tune, etc.).

How does it work?
-----------------
You set the land sound URL to your Opencast server, which relays other streams seamlessly, without disconnecting listeners.

Software
--------

Opencast uses the following Open Source software stack:

Opencast Songboard/HUD ->  (http requests) -> Flask -> mpd -> liquidsoap -> Icecast

In Second Life:
---------------

Opencast songboard - (LSL) 10 line / 96 character songboard controls jukebox and switching streams
Opencast HUD - (LSL) used to switch streams and control jukebox

On the server side:
-------------------

* Flask - Web application receives commands from Second Life (switch the stream, change songs in jukebox etc.). Also used for uploading songs to jukebox.
* mpd - Music Player Daemon controlls the jukebox and relaying streams
* python-mp2 - Python library used to control mpd server
* liquidsoap - The liquidsoap server ensures continuous streaming without dropping listeners; switches to a playlist when it detects silence or Dj drops out
* Icecast - The audio streaming server. (Shoutcast blows.)




