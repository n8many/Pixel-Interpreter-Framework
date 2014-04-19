from commands.command import Command
from gmusicapi import Mobileclient
from fuzzywuzzy import fuzz, process
from player import Player
import threading
import time
import subprocess
import random
import os

class Gmusic(Command):
    def __init__(self, credentials):
        print 'Loading music module'
        self.keywords = ['music','playlist','song','artist','album']
        self.gmusic = Mobileclient()
        self.queue = list()
        self.currentsong = dict()
        print 'Logging in to music client'
        self.gmusic.login(credentials['u'], credentials['pass'])
        self.isPlaying = False
        self.queueindex = 0
        self.defaultPlaylist = credentials['playlist']
        self.updateSongs()
        self.deviceid = credentials['id']
        self.player = None
        self.minimumaccuracy = 75

    def stripQueue(self, queue):
        queue2 = list()
        for song in queue:
            try:
                queue2 += [song['trackId']]
            except:
                queue2 += [song['id']]
        return queue2

    def getInfo(self, songid):
        song = dict()
        for s in self.library:
            if s['id'] == songid:
                song = s
                break
        return song

    def updateSongs(self):
        print 'Loading songs'
        self.library = self.gmusic.get_all_songs()
        print 'Loading playlists'
        self.playlists = self.gmusic.get_all_user_playlist_contents()
        
        print 'Getting song info'
        self.artists = []
        self.albums = []
        self.songTitles = []
        self.playlistNames = []
        for song in self.library:
            self.songTitles += [song['title']]
            if song['album'] not in self.albums:
                self.albums += [song['album']]
            if song['artist'] not in self.artists:
                self.artists += [song['artist']]

        print 'Getting playlist info'
        for playlist in self.playlists:
            self.playlistNames += [playlist['name']]
        if not self.queue:
            self.queueindex = 0
            self.queue = self.findPlaylist(self.defaultPlaylist)
            print len(self.queue)
            random.shuffle(self.queue)

        if not self.currentsong:
            self.currentsong = self.getInfo(self.queue[self.queueindex])

    def play(self, csid = None):
        if csid == None:
            csid = self.queue[self.queueindex]
        self.isPlaying = True
        url = self.gmusic.get_stream_url(csid,self.deviceid)
        self.currentsong = self.getInfo(csid)
        albumurl = self.currentsong['albumArtRef'][0]['url']
        self.player = Player(url, albumurl, 'Google Music')
        self.player.start()
        print 'play' + self.currentsong['title']
        self.nextSong()

    def pause(self):
        self.isPlaying = False
        try:
            self.player.terminate()
        except:
            pass
        print 'pausing'

    def nextSong(self):
        self.pause()
        self.queueindex += 1
        if self.queueindex >= len(self.queue):
            self.queueindex = 0
        else:
            self.play()

    def previousSong(self):
        self.pause()
        self.queueindex -= 1
        if self.queueindex < 0:
            self.queueindex = 0
        self.play()

    def rickRoll(self):
        q = self.findSong('Never Gonna Give You Up')
        return q

    def findSong(self, songname):
        q = list()
        songtitle, acc = process.extractOne(songname, self.songTitles)
        if acc < self.minimumaccuracy:
            print 'Warning, low accuracy match'
        for song in self.library:
            if songtitle == song['title']:
                q = [song['id']]
                break
        return q
    
    def findAlbum(self, albumname):
        q = list()
        album, acc = process.extractOne(albumname, self.albums) 
        if acc < self.minimumaccuracy:
            print 'Warning, low accuracy match'
        for song in self.library:
            if album == song['album']:
                q += [song]
        if len(q) > 0:
            q = sorted(q , key=lambda k: k['track'])
            q = stripQueue(q)
        return q

    def findArtist(self, artistname):
        q = list()
        artist, acc = process.extractOne(artistname, self.artists)
        if acc < self.minimumaccuracy:
            print 'Warning, low accuracy match'
        for song in self.library:
            if artist == song['artist']:
                q += [song]  
        if len(q) > 0:
            q = stripQueue(q)
            random.shuffle(q)

        return q

    def findPlaylist(self, playlistname):
        q = list()
        (name, acc) = process.extractOne(playlistname, self.playlistNames)
        if acc < self.minimumaccuracy:
            print 'Warning, low accuracy match'
        for playlist in self.playlists:
            if name == playlist['name']: 
                q = playlist['tracks']
                q = self.stripQueue(q)
                break
        random.shuffle(q)
        return q

    def run(self, commandlist):
        command = {'action':'toggle', 'what':[],
            'method':'replace','shuffle':False}
        for i in xrange(0,len(commandlist)):
            if commandlist[i] == 'play':
                command['action'] = 'play'
            elif commandlist[i] == "playlist":
                command['what'] = self.findPlaylist(' '.join(commandlist[i:]))
                command['action'] = 'play'
                break
            elif commandlist[i] == "song":
                command['what'] = self.findSong(' '.join(commandlist[i:]))
                command['action'] = 'play'
                break
            elif commandlist[i] == 'artist':
                command['what'] = self.findArtist(' '.join(commandlist[i:]))
                command['action'] = 'play'
                break
            elif commandlist[i] == 'album':
                command['what'] = self.findAlbum(' '.join(commandlist[i:]))
                command['action'] = 'play'
                break
            elif commandlist[i] == 'pause':
                command = {'action':'pause'}
                break
            elif commandlist[i] == 'skip':
                command = {'action':'skip'}
                break   
            elif commandlist[i] == 'previous' or commandlist[i] == 'back':
                command = {'action':'previous'}
            elif commandlist[i] == 'shuffle':
                command['shuffle'] = True
            elif commandlist[i] == 'next':
                command['method'] = 'next'
            elif commandlist[i] == 'add':
                command['method'] = 'add'

        if command['action'] == 'toggle':
            if self.isPlaying:
                command['action'] = 'pause'
            else:
                command['action'] = 'play'

        if command['action'] == 'pause':
            self.pause()
        elif command['action'] == 'skip':
            self.nextSong()
        elif command['action'] == 'previous':
            self.previousSong()
        elif command['action'] == 'play' or command['shuffle']:
            a = self.queue[:self.queueindex+1]
            b = self.queue[self.queueindex+1:]
            if command['method'] == 'add':
                q = b + command['what']
            elif command['method'] == 'next':
                q = command['what'] + b
            elif command['method'] == 'replace':
                if self.isPlaying:
                    self.pause()
                a = []
                if len(command['what']) > 0:
                    q = command['what']
                else:
                    q = self.queue
                self.queueindex = 0
            if command['shuffle']:
                random.shuffle(q)
            self.queue = a + q
            if not self.isPlaying:
                self.play()

