# Opencast

Advanced audio streaming system for Second Life.
================================================

Opencast solves the problem of listeners disconnecting when an audio stream changes from one Shoutcast or Icecast server to a new one, when the Dj gets disconnected etc.
It also provides a platform for social djing with a chat controlled jukebox and the possiblity to create games (dj battles, name that tune, etc.).

HUD
---

![HUD screenshot](anticlub_hud_screenshot.png)

The audio player HUD lets you listen to a stream without using the land radio URL. You can listen uninterrupted in any sim and even listen during teleports.
You HUD relays streams without disconnecting the listener, no more toggling the play button!

How does it work?
-----------------
You set the land sound URL to your Opencast server, which relays other streams seamlessly, without disconnecting listeners.

Software
--------

Opencast uses the following Open Source software stack:

Opencast Songboard/HUD ->  (http requests) -> Flask -> mpd -> liquidsoap -> Icecast

In Second Life:
---------------

Opencast songboard - (LSL) 10 line x 96 character songboard controls jukebox and switching streams
Opencast HUD - (LSL) used to switch streams and control jukebox

On the server side:
-------------------

* Flask - Web application receives commands from Second Life (switch the stream, change songs in jukebox etc.). Also used for uploading songs to jukebox.
* mpd - Music Player Daemon controlls the jukebox and relaying streams
* python-mp2 - Python library used to control mpd server
* liquidsoap - The liquidsoap server ensures continuous streaming without dropping listeners; switches to a playlist when it detects silence or Dj drops out
* Icecast - The audio streaming server.



Songboard / HUD Commands
------------------------

All commands are prefixed with /42 e.g. '/42 next'
Opencast has two modes, relay and jukebox. Relay mode plays a remote stream, jukebox mode is chat controlled autodj.


`switch <stream URL>`


   Relay an Icecast or Shoutcast stream without disconnecting listeners

`jukebox`

   Switch to jukebox mode - chat controlled autodj

`next`

   Skip to next song in current playlist.

`prev`

   Skip to previous song in current playlist.

`load <playlist>`

   Load the selected playlist and start playing it immediately.

`del <nbr>`

   Delete song <nbr> from current playlist.

`move <from to>`

  Move song <from> to position <to> in the current playlist.

`search artist <name>`

  Show songs by artist named <name>

`add song <name>`

  Add songs named <name> to the current playlist

`search song <name>`

  Show songs by name <name>

`add song <name>`

  Add songs named <name> to the current playlist

`crop`

  Delete all songs after the current playing song
