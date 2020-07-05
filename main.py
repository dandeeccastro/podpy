from pod import Main
import sys
from optparse import OptionParser
import os

def main():

    usage = "%prog [options] project_folder"

    parser = OptionParser(usage)

    parser.add_option("-f","--filename",type="string",dest="filename",default="podcast.mp3",help="final filename for project")
    parser.add_option("-m","--music-folder",type="string",dest="musicFolder",default="~/Music/",help="music folder for generating the music mix [default= Music]")
    parser.add_option("-s","--song-gain",type="float",dest="musicGain",default=-20.0,help="sound gain in decibels for music mix [default= -20db]")
    parser.add_option("-t","--transition-time",type="int",dest="transitionTime",default=2000,help="transition time between chapters in millisecconds [default=2000]")
    parser.add_option("-a","--audio-gain",type="float",dest="voiceGain",default=0,help="sound gain in decibels for voice audio [default = 0db]")

    (options,args) = parser.parse_args()

    if(len(args) > 0):
        projectPath = os.path.abspath(args[0])
        musicFolderPath = os.path.abspath(options.music_folder)

        Main( projectPath, options.filename, musicFolderPath, options.musicGain, options.transitionTime, options.voiceGain ).main()
    else:
        # Aqui deveria ter um error handling mais extensivo
        print("No project folder specified")

if __name__ == "__main__":
    main()
