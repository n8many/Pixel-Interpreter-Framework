from commands.command import Command
from gmusicapi import Webclient
from alsaaudio import PCM
import random

class Music(Command):
    def __init__(self, credentials):
        self.keywords = ['music']
        self.gmusic = Webclient()
        self.gmusic.login(credentials['u'], credentials['pass'])
        self.currentPlaylist = list()
        self.currentSong = dict()
        self.isPlaying = False
        self.playlistIndex = 0
        self.updateSongs()
        self.player = PCM()

    def updateSongs(self):
        self.playlists = self.gmusic.get_all_playlist_ids()["user"]
        if len(self.currentPlaylist) == 0:
            self.currentPlaylist= self.gmusic.get_playlist_songs(self.playlists['Megalist'][0])
            random.shuffle(self.currentPlaylist)

        if not self.currentSong:
            self.currentSong = self.currentPlaylist[self.playlistIndex]

        self.library = self.gmusic.get_all_songs()
            
    def play(self, cs = None):
        if cs == None:
            cs = self.currentPlaylist[self.playlistIndex]
        self.currentSong = cs
        self.isPlaying = True
#       self.player.write(self.gmusic.get_stream_audio(self.currentSong[u'id']))
        print 'play' + self.currentSong['title']

    def pause(self):
        self.isPlaying = False
        print 'pausing'

    def nextSong(self):
        self.playlistIndex += 1
        if self.playlistIndex >= len(self.currentPlaylist):
            self.playlistIndex = 0
            self.pause()
        else:
            self.play()

    def previousSong(self):
        self.playlistIndex -= 1
        if self.playlistIndex < 0:
            self.playlistIndex = 0
        self.play()

    def rickRoll(self):
        self.playlist = list()
        for song in self.library:
            if song['titleNorm'] == 'never gonna give you up':
                self.currentPlaylist = [song]
                self.playlistIndex = 0
                self.play()

    def playSong(self, songname):
        for song in self.library:
            if songname in song['titleNorm']:
                self.play(cs = song)
                self.currentPlaylist = [song]
#               tempplaylist = self.gmusic.get_playlist_songs(self.playlists['Megalist'][0])
#               random.shuffle(tempplaylist)
#               self.currentPlaylist += tempplaylist
                break
    def playAlbum(self, albumname):
        tempplaylist = list()
        for song in self.library:
            if albumname in song["albumNorm"] or albumname in song["album"]:
                tempplaylist += [song]
        if len(tempplaylist) > 0:
            self.currentPlaylist = sorted(tempplaylist, key=lambda k: k['track'])
            self.play()

    def playArtist(self, artistname):
        tempplaylist = list()
        for song in self.library:
            if artistname in song["artistNorm"] or artistname in song["artist"]:
                tempplaylist += [song]    
        if len(templaylist) > 0:
            self.currentPlaylist = tempplaylist
            random.shuffle(self.currentPlaylist)
            self.playlistIndex = 0
            self.play()

    def playPlaylist(self, playlistname):
        self.currentPlaylist = self.gmusic.get_playlist_songs(self.playlists[playlistname][0])
        random.shuffle(self.currentPlaylist)
        self.playlistIndex = 0
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
                self.playPlaylist(" ".join(commandlist[2:]))

            elif commandlist [1] == "song":
                self.playSong(" ".join(commandlist[2:]))

            elif commandlist [1] == "artist":
                self.playArtist(" ".join(commandlist[2:]))

            elif commandlist[1] == "album":
                self.playAlbum(" ".join(commandlist[2:]))
            
            
        elif commandlist[0] == "pause":
            if self.isPlaying == True:
                self.pause()

        elif commandlist[0] == "next":
            self.nextSong()

        elif commandlist[0] == "previous":
            self.previousSong()

        else:
            print "m err"

