import threading
import subprocess
import os


class Player(threading.Thread):
    def __init__(self, songurl, albumarturl, source):
        super(Player, self).__init__()
        self.songurl = songurl
        self.albumarturl = albumarturl
        self.source = source

    def run(self)
        with open(os.devnull, 'w') as temp:
            self.player = subprocess.Popen(['mplayer','-cache', '8192', 
                '-ao', 'alsa', '-vo', 'null', '%s' % self.songurl], 
                stdin=subprocess.PIPE, stdout=temp, stderr=temp)
            self.display = subprocess.Popen(['sudo','fbi','-T','2','-d',
                'dev/fb1','-noverbose','-a', self.albumarturl], 
                stdin=subprocess.PIPE,)
        while self.player.returncode == None:
            self.player.poll()
            time.sleep(1)
    pass
