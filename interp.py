import gmusicapi
import beautifulhue
import alsaaudio
import collections

mode = ""
command = ""
value = ""

def resetcmd()

    global mode, command, value

    mode = ""
    command = ""
    value = ""

def interpret(self, speech)
    
    global mode, command, value
    words = collections.deque(speech.split())

    while words.len > 0:
        if mode == "lights":
            if command == "brightness":
                if type(words[0]) == int
                    #lights
                    resetcmd()
                else:
            if command == "color":
            else:
                if words.len == 0:
                    #light toggle
                    resetcmd()
                elif words[0] == "dim":
                    #dim lights
                    resetcmd()
                elif words[0] == "bright":
                    #brighten lights
                    resetcmd()
                elif words[0] == "color":
                    command = "color"
                elif words[0] == "brightness":
                    command = "brightness"
                else:
                   #light toggle
                   resetcmd()
                   continue
	elif mode == "music":
             if command == "play":
                 if words.len == 0;
                     #plays from where left off
                     resetcmd()
                 elif words[0] == "playlist":
                     #searches for and plays a playlist then shuffles
                     resetcmd()
                 elif words[0] == "song":
                     #plays a song
                     resetcmd()
                 elif words[0] == "album":
                     #plays an album w/ shuffle
                     resetcmd()
                 else:
                     #toggles play/pause and resets
                     resetcmd()
                     continue
             else:            
                if words[0] == "play":
                    command = "play"
                elif words[0] == "pause":
                    #pauses
                elif words[0] == "next":
                    #hits next in queue
                elif words[0] == "previous":
                    #hits prev in queue
        elif mode == "volume":
            if type(words[0]) == int:
                #Set volume
                resetcmd()
            else:
               	resetcmd()
        else 
            if words[0] == "lights" or words[0] == "light":
                mode = "lights"
            elif words[0] == "music":
                mode = "music"
        words.popback()

    while words.len > 0:
        if words[0] == "getStatus"
            words.popleft()
        if words[0] == "light" or words[0] == "lights":
            words.popleft()
            if words.len == 0:
                #toggle lights
            elif words[0] =="on":
                #turn lights on
                words.popleft()

            elif words[0] is "off":
                words.popleft()

            elif words[0] is "dim":
                words.popleft()
            elif words[0] is "bright":
                
            elif words[0] is "brightness":
             	#send brightness
            elif words[0] is "color":
		if words[0] is "cycle"
                elif words[0] is "warm"
                    if words[0] is "white"
                elif words[0] is "cool"
                    if words[0] is "white"
                elif words[0] is "red":
                elif words[0] is "blue":
                elif words[0] is "green":
                elif words[0] is "yellow":
                elif words[0] is "purple":
                elif words[0] is "pink":
                elif words[0] is "orange":
                else
            else
                #toggle lights
        elif words[0] is "volume":
                #set volume to int value
        elif words[0] is "play":
                #choose what to play
            if words[1] is "music":
            elif words[1] is "playlist":
            elif words[1] is "song":
            elif words[1] is "album":
            else
                #otherwise toggle playing
        elif words[0] is "pause":
                #pause playing
        elif words[0] is "next":
                #next song
        elif words[0] is "previous":
		#previous song

                                       
