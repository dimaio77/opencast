#!/usr/bin/env python

'''

mpd source client for Second Life

Author: Carrie Vordun

'''

import time
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

    def do_clear(self):
        '''Clear playlist including current song'''
        self.client.clear()
        return "Playlist cleared! You have 10 seconds to add a playlist."

    def do_crop(self):
        '''Crop playlist after current playing song'''
        pos = self.get_pos()
        self.client.delete((pos + 1,))
        return "Playlist cropped!"

    def do_metadata(self, metadata):
        '''Change stream metadata'''
        pass

    def do_switch(self, stream_url):
        """Relay another stream"""
        if stream_url.startswith('http://'):
            self.client.clear()
            self.client.add(stream_url)
            self.client.play()
            return "Switching stream to %s" % stream_url
        else:
            return "Stream URLs start with http://"

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

    def do_save(self, playlist):
        '''Save current playlist
        TODO: Prefix playlist names with user name for easier management.'''
        if ' ' in playlist:
            return "Please use a single word for the playlist name."
        file = '%s%s.m3u' % (PLAYLIST_DIR, playlist)
        if os.path.isfile(file):
            return "Playlist already exists!"
        self.client.save(playlist)
        return "Playlist '%s' saved!" % playlist

    def do_switchnext(self, path):
        '''Load path into playlist after current song'''
        pos = self.get_pos()
        self.client.addid(path, pos + 1)
        return "%s will be streamed next." % path

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

        cur_song = self.client.currentsong()
        status = self.client.status()
        print status
        print cur_song
        if int(status['playlistlength']) == 0:
            #Wait in case playlist is being manipulated, then fill playlist
            time.sleep(10)
            if int(status['playlistlength']) == 0:
                self.do_jukebox()
        elif status['state'] == 'stop':
            self.client.play()
        if cur_song.has_key('file') and cur_song['file'].startswith('http'):
            return self.display_stream()
        else:
            return self.display_playlist()

    def display_stream(self):
        '''Display stream and song info when in relay mode'''
        cur_song = self.client.currentsong()
        if cur_song.has_key('name'):
             name = cur_song['name']
        else:
             name = 'Unknown'
        if cur_song.has_key('title'):
             title = cur_song['title']
        else:
             title = 'Unknown - Unknown'
        text = "%s" % "\n".join(textwrap.wrap(name, 96))
        text += '\n \n \n'
        print title
        try:
            artist, song =  title.split('-')
        except ValueError:
            artist = ""
            song = title
        text += "Artist: %s\n" % artist
        text += "\n  Song: %s" % song.strip()
        text += "\n \nStream URL: %s " % cur_song['file']
        text += "\n \n"
        return text

    def display_playlist(self):
        '''Display 10 songs from playlist in jukebox mode'''
        cur_song = self.client.currentsong()
        current_pos = self.get_pos()
        if current_pos > 3:
            self.client.delete(0)
        playlist = self.client.playlistid()
        if cur_song.has_key('name'):
             name = cur_song['name']
        else:
             name = 'Unknown'
        if cur_song.has_key('title'):
             title = cur_song['title']
        else:
             title = 'Unknown - Unknown'
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
            if current_pos == None:
                current_pos = 0
            if d == current_pos + 1:
                status = self.client.status()
                length = cur_song['time']
                lm, ls = divmod(int(float(length)), 60)
                h, lm = divmod(lm, 60)
                lcur = "%02d:%02d" % (lm, ls)

                m, s = divmod(int(float(status['elapsed'])), 60)
                h, m = divmod(m, 60)
                cur = "%02d:%02d" % (m, s)
                lines += '* %s) %s - %s (%s/%s)\n' % (pos, artist, title, lcur, cur)
            else:
                lines += '  %s) %s - %s\n' % (pos, artist, title)
            if d >= 10: break
        return lines

    def do_delete(self, pos):
        '''Delete entry in playlist'''
        self.client.delete(int(pos) - 1)
        return "Deleted track %s from playlist." % pos

    def do_artist(self, artist):
        '''Search for songs by artist'''
        tracks = self.client.search('artist', artist)
        text = ""
        i = 0
        for song in tracks:
            text += '%s - %s\n' % (song['artist'], song['title'])
            if i >= 10:
                break
        return text

    def do_artistadd(self, artist):
        '''Search for songs by artist and add to current playlist'''
        tracks = self.client.search('artist', artist)
        text = "Added these to current playlist:\n"
        pos = self.get_pos()
        i = 0
        for song in tracks:
            self.client.addid(song['file'], pos+1)
            if i < 10:
                text += '%s - %s\n' % (song['artist'], song['title'])
        return text


    def do_song(self, title):
        '''Search for songs by title'''
        tracks = self.client.search('title', title)
        text = ""
        i = 0
        for song in tracks:
            if i < 10:
                try:
                    text += '%s - %s\n' % (song['artist'], song['title'])
                except KeyError:
                    text += song['file']
        return text

    def do_songadd(self, title):
        '''Search for songs by title and add to current playlist'''
        tracks = self.client.search('title', title)
        text = "Added these to current playlist:\n"
        pos = self.get_pos()
        i = 0
        for song in tracks:
            self.client.addid(song['file'], pos+1)
            if i < 10:
                try:
                    text += '%s - %s\n' % (song['artist'], song['title'])
                except KeyError:
                    pass
        return text

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


