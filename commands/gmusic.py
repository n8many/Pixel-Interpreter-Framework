from commands.command import Command
from fuzzywuzzy import fuzz, process
import thread
import time
import random
import os
import mpd

class Gmusic(Command):
    def __init__(self, credentials):
        print 'Loading music module'
        self.keywords = ['music','playlist','song','artist','album']
        self.client = mpd.MPDClient()
        self.restart()
        self.minimumaccuracy = 75
        self.defaultPlaylist = credentials['playlist']

    def restart(self):
        self.client = mpd.MPDClient()
        try:
            self.client.connect('127.0.0.1','6600')
        except:
            print "Reconnecting..."
            self.restart()
        self.updateSongs()

    def moduleData(self):
        info = dict()
        info['playing'] = client.status()['state']
        info['index'] = client.currentsong()['pos']
        info['queuelength'] = len(self.queue)
        info['currentsong'] = client.currentsong()
        info['artists'] = self.artists
        info['albums'] = self.albums
        info['playlists'] = self.playlistNames
        return info

    def getInfo(self, songid):
        pass

    def updateSongs(self):
        pass


    def play(self, csid = None):
        if csid == None:
            if self.client.currentsong == {}:
                self.client.load(self.defaultPlaylist)
            self.client.play()
        else:
            self.client.play(csid)

    def stop(self):
        if self.client.status()['state'] in ('pause', 'play'):
            self.client.stop()
        print 'stopping'

    def pause(self):
        if self.client.status()['state'] == 'play':
            self.client.pause()
        print 'pausing'

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
        self.restart()
        command = {'action':'toggle', 'what':[],
            'method':'replace','shuffle':False}
        for i in xrange(0,len(commandlist)):
            if commandlist[i] == 'play':
                command['action'] = 'play'
            elif commandlist[i] == "playlist":
#                command['what'] = self.findPlaylist(' '.join(commandlist[i:]))
                command['action'] = 'play'
                break
            elif commandlist[i] == "song":
#                command['what'] = self.findSong(' '.join(commandlist[i:]))
                command['action'] = 'play'
                break
            elif commandlist[i] == 'artist':
#                command['what'] = self.findArtist(' '.join(commandlist[i:]))
                command['action'] = 'play'
                break
            elif commandlist[i] == 'album':
#                command['what'] = self.findAlbum(' '.join(commandlist[i:]))
                command['action'] = 'play'
                break
            elif commandlist[i] == 'pause':
                command['action'] = 'pause'
                self.pause()            
                break
            elif commandlist[i] in ('previous','back'):
                command['action'] = 'previous'
                self.client.previous()
            elif commandlist[i] == 'shuffle':
                self.client.random(1)
            elif commandlist[i] in ('next', 'skip'):
                command['action'] = 'skip'
                self.client.next()
            elif commandlist[i] == 'add':
                command['method'] = 'add'

        if command['action'] == 'toggle':
            if self.client.status()['state'] == 'play':
                self.client.pause()
            else:
                self.client.play() 
        elif command['action'] == 'play':
            self.play()
