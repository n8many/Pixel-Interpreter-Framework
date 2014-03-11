from commands.command import Command
from gmusicapi import Mobileclient
import subprocess
import random
import os

class Gmusic(Command):
    def __init__(self, credentials):
        self.keywords = ['music','playlist','song','artist','album']
        self.gmusic = Mobileclient()
        self.queue = list()
        self.cSong = dict()
        self.gmusic.login(credentials['u'], credentials['pass'])
        self.isPlaying = False
        self.qIndex = 0
        self.defaultPlaylist = credentials['playlist']
        self.updateSongs()
        self.devid = credentials['id']
        self.player = None 

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
        self.library = self.gmusic.get_all_songs()
        self.playlists = self.gmusic.get_all_user_playlist_contents()
        if len(self.queue) == 0:
            for playlist in self.playlists:
                if playlist['name'] == self.defaultPlaylist:
                    tempq = playlist['tracks']
                    self.queue = self.stripQueue(tempq)
            self.qIndex = 0
            random.shuffle(self.queue)

        if not self.cSong:
            self.cSong = self.getInfo(self.queue[self.qIndex])

    def play(self, csid = None):
        if csid == None:
            csid = self.queue[self.qIndex]
        self.isPlaying = True
        url = self.gmusic.get_stream_url(csid,self.devid)
        with open(os.devnull, 'w') as temp:
            self.player = subprocess.Popen(['mplayer','-cache', '8192',  '-ao', 'alsa', '-vo',
                'null', '%s' % url], stdin=subprocess.PIPE, stdout=temp, stderr=temp)
        self.cSong = self.getInfo(csid)
        print 'play' + self.cSong['title']
    
    def pause(self):
        self.isPlaying = False
        if isinstance(self.player, subprocess.Popen):
            self.player.terminate()
        print 'pausing'

    def nextSong(self):
        self.pause()
        self.qIndex += 1
        if self.qIndex >= len(self.queue):
            self.qIndex = 0
        else:
            self.play()

    def previousSong(self):
        self.pause()
        self.qIndex -= 1
        if self.qIndex < 0:
            self.qIndex = 0
        self.play()

    def rickRoll(self):
        q = self.findSong('Never Gonna Give You Up')
        return q

    def findSong(self, songname):
        q = list()
        for song in self.library:
            if songname in song['title']:
                q = [song['id']]
                break
        return q
    
    def findAlbum(self, albumname):
        q = list()
        for song in self.library:
            if albumname in song['album']:
                q += [song]
        if len(q) > 0:
            q = sorted(q , key=lambda k: k['track'])
            q = stripQueue(q)
        return q

    def findArtist(self, artistname):
        q = list()
        for song in self.library:
            if artistname in song['artist']:
                q += [song]    
        if len(q) > 0:
            q = stripQueue(q)
            random.shuffle(q)
        return q

    def findPlaylist(self, playlistname):
        q = list()
        for playlist in self.playlists:
            if playlist['name'] == playlistname:
                q = playlist['tracks']
                q = self.stripQueue(q)
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
            a = self.queue[:self.qIndex+1]
            b = self.queue[self.qIndex+1:]
            if command['method'] == 'add':
                q = b + command['what']
            elif command['method'] == 'next':
                q = command['what'] + b
            elif command['method'] == 'replace':
                if self.isPlaying:
                    self.pause()
                a = list()
                if len(command['what'])>0:
                    q = command['what']
                else:
                    q = self.queue
                self.qIndex = 0
            if command['shuffle']:
                random.shuffle(q)
            self.queue = a + q
            if not self.isPlaying:
                self.play()

