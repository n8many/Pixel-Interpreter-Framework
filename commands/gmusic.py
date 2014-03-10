from commands.command import Command
from gmusicapi import Mobileclient
import subprocess
import random
import os

class Gmusic(Command):
    def __init__(self, credentials):
        self.keywords = ['music']
        self.gmusic = Mobileclient()
        self.queue = list()
        self.cSong = dict()
        self.gmusic.login(credentials['u'], credentials['pass'])
        self.isPlaying = False
        self.qIndex = 0
        self.defaultPlaylist = credentials['playlist']
        self.updateSongs()
        self.devid = credentials['id']

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
                'null', '%s' % url], stdin=subprocess.PIPE, stdout=temp)
        self.cSong = self.getInfo(csid)
        print 'play' + self.cSong['title']
    
    def pause(self):
        self.isPlaying = False
        print 'pausing'

    def nextSong(self):
        self.playlistIndex += 1
        if self.qIndex >= len(self.currentPlaylist):
            self.qIndex = 0
            self.pause()
        else:
            self.play()

    def previousSong(self):
        self.qIndex -= 1
        if self.qIndex < 0:
            self.qIndex = 0
        self.play()

    def rickRoll(self):
        for song in self.library:
            if song['title'] == 'Never Gonna Give You Up':
                self.queue = [song['id']]
                self.qIndex = 0
                self.play()

    def findSong(self, songname):
        for song in self.library:
            if songname in song['title']:
                self.queue = [song['id']]
                self.qIndex = 0
                self.play()
#               tempplaylist = self.gmusic.get_playlist_songs(self.playlists['Megalist'][0])
#               random.shuffle(tempplaylist)
#               self.queue += tempplaylist
                break
    
    def findAlbum(self, albumname):
        tempplaylist = list()
        for song in self.library:
            if albumname in song['album']:
                tempplaylist += [song]
        if len(tempplaylist) > 0:
            tempplaylist = sorted(tempplaylist, key=lambda k: k['track'])
            self.queue = self.stripQueue(tempplaylist)
            self.play()

    def findArtist(self, artistname):
        tempplaylist = list()
        for song in self.library:
            if artistname in song['artist']:
                tempplaylist += [song]    
        if len(templaylist) > 0:
            self.queue = stripQueue(tempplaylist)
            random.shuffle(self.queue)
            self.qIndex = 0
            self.play()

    def findPlaylist(self, playlistname):
        for playlist in self.playlists:
            if playlist['name'] == playlistname:
                tempq = playlist['tracks']
                self.queue = self.stripQueue(tempq)
        random.shuffle(self.queue)
        self.qIndex = 0
        self.play()

    def run(self, commandlist):
        if len(commandlist) == 0:
            if self.isPlaying == True:
                self.pause()
            else:
                self.play()
            print "music toggle"

        elif commandlist[0] == "play":
            if len(commandlist) == 1:
                if self.isPlaying == False:
                    self.play()
                    print "play music"

            elif commandlist [1] == "playlist":
                self.findPlaylist(" ".join(commandlist[2:]))

            elif commandlist [1] == "song":
                self.findSong(" ".join(commandlist[2:]))

            elif commandlist [1] == "artist":
                self.findArtist(" ".join(commandlist[2:]))

            elif commandlist[1] == "album":
                self.findAlbum(" ".join(commandlist[2:]))
            
            
        elif commandlist[0] == "pause":
            if self.isPlaying == True:
                self.pause()

        elif commandlist[0] == "next":
            self.nextSong()

        elif commandlist[0] == "previous":
            self.previousSong()

        else:
            print "m err"
