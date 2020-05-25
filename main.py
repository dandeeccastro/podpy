from pod import Main
import sys
from optparse import OptionParser
import os

def main():

	usage = "%prog [options] project_folder"

	parser = OptionParser(usage)

	parser.add_option("-t","--transition-time",type="int",dest="transition_time",default=2000,help="transition time between chapters in millisecconds [default=2000]")
	parser.add_option("-s","--song-gain",type="float",dest="music_gain",default=-20.0,help="sound gain in decibels for music mix [default= -20db]")
	parser.add_option("-f","--filename",type="string",dest="filename",default="podcast.mp3",help="final filename for project")
	parser.add_option("-m","--music-folder",type="string",dest="music_folder",default="~/Music/",help="music folder for generating the music mix [default= Music]")
	parser.add_option("-a","--audio-gain",type="float",dest="voice_gain",default=0,help="sound gain in decibels for voice audio [default = 0db]")

	(options,args) = parser.parse_args()

	if(len(args) > 0):
		Main(os.path.abspath(args[0]),options.filename,os.path.abspath(options.music_folder),options.music_gain,options.transition_time,options.voice_gain).main()
	else:
		print("No project folder specified")
		
	 #Main().main()

if __name__ == "__main__":
	main()