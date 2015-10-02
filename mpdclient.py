#!/usr/bin/env python

'''

mpd source client for Second Life

Author: Carrie Vordun

'''

import textwrap
import os

import mpd

PLAYLIST_DIR='/var/lib/mpd/playlists/'

class MyMPD(object):

    '''Client class for MPD connection'''

    def __init__(self):
        '''Init this'''
        pass

    def connect(self):
        self.client = mpd.MPDClient(use_unicode=True)
        self.client.connect("localhost", 6600)
        return self.client

class Dispatcher(object):
    '''Command dispatcher

    All class methods starting with 'do_' are mpd commands
    received from the Second Life user.'''

    def __init__(self, client):
        self.client = client

    def get_pos(self):
        '''Get current position in playlist'''
        try:
           return int(self.client.currentsong()['pos'])
        except KeyError:
            return None

    def do_crop(self):
        '''Crop playlist after current playing song'''
        pos = self.get_pos()
        self.client.delete((pos + 1,))
        return "Playlist cropped!"

    def do_switch(self, stream_url):
        """Relay another stream"""
        self.client.clear()
        self.client.add(stream_url)
        self.client.play()
        return "Switching stream to %s" % args

    def do_next(self):
        '''Skip to next song in current playlist'''
        self.client.next()
        return "Skipping to next song in jukebox..."

    def do_prev(self):
        '''Skip to previous song in current playlist'''
        self.client.previous()
        return "Skipping to previous song in jukebox..."

    def do_stats(self):
        '''Show number of songs, albums and artists in jukebox'''
        stats = self.client.stats()
        return "Jukebox contains - Songs: %s, Artists: %s, Albums: %s" % \
            (stats()['songs'], stats()['artists'], stats()['albums'])

    def do_move(self, pos_from, pos_to):
        '''Move song from its position to another in the current playlist'''
        self.client.move(pos_from -1, pos_to -1)

    def do_load(self, playlist):
        '''Load playlist and start playing it immediately'''
        file = '%s%s.m3u' % (PLAYLIST_DIR, playlist)
        if os.path.isfile(file):
            try:
                self.client.clear()
                self.client.load(playlist)
                self.client.play()
                return "Playlist '%s' queued." % playlist
            except mpd.CommandError:
                self.do_jukebox()
        return "No such playlist (%s). Hint? Playlists are case-sensitive." % playlist

    def do_add(self, path):
        '''Clear playlist and load songs in path'''
        self.client.clear()
        self.client.add(path)
        self.client.shuffle()
        self.client.play()
        return "Added %s" % path

    def do_current(self):
        '''Display information about current song playing'''
        current=self.client.currentsong()
        if current.has_key('artist') and current.has_key('title'):
            return '%s - %s' % (current['artist'], current['title'])
        elif current.has_key('title'):
            return current['title']
        elif not current.has_key('title') and not current.has_key('artist'):
            if current.has_key('name'):
                return current['name']
            else:
                return 'Unknown - Unknown'
        else:
            return '%s - Unknown Title' % current['artist']

    def do_jukebox(self):
        '''Switch to jukebox mode with random playlist and start playing'''
        self.client.clear()
        self.client.add('/')
        self.client.shuffle()
        self.client.play()
        return "Switching to jukebox mode..."

    def do_playlist(self):
        '''Display current playlist
        The songboard has two display modes:

        * Relay stream (Displays stream URL, name, artist - song
        * Jukebox (First 10 songs displayed)'''

        current = self.get_pos()
        if current > 3:
            self.client.delete(0)

        playlist = self.client.playlistid()
        cur_song = self.client.currentsong()
        # Streaming mode:
        if cur_song.has_key('name'):
             name = cur_song['name']
        else:
             name = 'Unknown'
        if cur_song.has_key('title'):
             title = cur_song['title']
        else:
             title = 'Unknown - Unknown'
        if cur_song.has_key('file') and cur_song['file'].startswith('http'):
             text = "%s" % "\n".join(textwrap.wrap(name, 96))
             text += '\n \n \n'
             artist, song =  title.split('-')
             text += "Artist: %s\n" % artist
             text += "\n  Song: %s" % song.strip()
             text += "\n \nStream URL: %s " % cur_song['file']
             text += "\n \n"
             return text
        # Jukebox mode:
	lines = "\n"
        d = 0
        for song in playlist:
            d += 1
            pos = int(song['pos']) + 1
            if song.has_key('title'):
                title = song['title']
            else:
                #We have a stream queued
                if song['file'].startswith('http'):
                    title = song['file']
                else:
                    title = 'Unknown'
            if song.has_key('artist'):
                artist = song['artist']
            else:
                if song['file'].startswith('http'):
                    artist = ''
                else:
                    artist = 'Unknown'
            if current and d == current + 1:
                lines += '* %s) %s - %s [Now playing]\n' % (pos, artist, title) 
            else:
                lines += '  %s) %s - %s\n' % (pos, artist, title)
            if d >8: break
        return lines 

    def do_help(self):
        return '''
Relay another stream without disconnecting listeners:
   /42 switch http://SHOUTCAST_URL.com:8000/stream

Switch to Jukebox mode (chat controlled autodj):
   /42 jukebox

Skip to next song in Jukebox:
   /42 next  (or prev for previous)

Load playlist after current song:
   /42 load <playlist name>

Print current playlist:
    /42 playlist

Print number of songs, artists and albums in Jukebox:
   /42 stats
'''

    def dispatch(self, command, args):
        '''Execute a command received from Second Life'''
        mcommand = 'do_' + command
        if hasattr(self, mcommand):
            method = getattr(self, mcommand)
            if args:
                return method(args)
            else:
                return method()
        else:
            return "No such command %s" % command


