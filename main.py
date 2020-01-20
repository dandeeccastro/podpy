# Native libraries 
import sys
import random 
from pathlib import Path
import audioop

# Pip installed libraries 
from pydub import AudioSegment

# Global variables
TRANSITION_TIME = 1000 # 1s 
FINAL_FILENAME = "podcast.mp3"
FILE_PATH = "./"

# TODO figure out why is sound peaking between chapters
class BackgroundCompiler:
    final_output = None
    instances = []
    last_music_index = -1

    def __init__(self,id):
        self.id = id
        self.output = None
        self.files = []
        BackgroundCompiler.instances.append(self)

    def __del__(self):
        print('Background Compiler shutting down...')

    def gatherFiles(self, voice_compiler ,traverser):
        voice_length = voice_compiler.output.duration_seconds * 1000
        mix_duration = 0
        i = 0
        files = [j for j in traverser.iterdir()]
        used_music_indexes = []
        while (mix_duration < voice_length):
            rand = random.randint(0,len(files) - 1)
            if rand in used_music_indexes or rand is BackgroundCompiler.last_music_index:
                continue
            else:
                used_music_indexes.append(rand)
                BackgroundCompiler.last_music_index = rand
                audio = AudioSegment.from_file( files[ rand ] )
                self.files.append( audio )
                mix_duration += self.files[i].duration_seconds * 1000
                i += 1

    def generateMusicMix(self, voice_length):
        music_length = voice_length + TRANSITION_TIME*2
        i = 0
        output_length = 0
        while music_length > output_length:
            song = self.files[i]
            if self.output is None :
                if ( music_length <= len(song) ):
                    diff = music_length - output_length
                    song = song[:diff].fade_in(TRANSITION_TIME).fade_out(TRANSITION_TIME)
                    self.output = song
                else:
                    self.output = song.fade_in(TRANSITION_TIME).fade_out(TRANSITION_TIME)
            else:
                if ( music_length <= len(song) + output_length ):
                    diff = music_length - output_length
                    song = song[:diff].fade_in(TRANSITION_TIME).fade_out(TRANSITION_TIME)
                    self.output += song
                else:
                    song = song.fade_in(TRANSITION_TIME).fade_out(TRANSITION_TIME)
                    self.output += song
            output_length = len(self.output)
            i = i + 1 % len(self.files)

    def getFinalOutput(self):
        return self.output
    

class VoiceCompiler:
    final_output = None	
    instances = []

    def __init__(self, id):
        self.id = id
        self.files = []
        self.output = None
        VoiceCompiler.instances.append(self)

    def __del__(self):
        print('Voice Compiler shutting down...')

    def gatherFiles(self, traverser):
        for item in traverser.iterdir():
            self.files.append(str(item))

    def getPureFileName(self, elem):
        name = elem.split('.')[0].split('/')[-1]
        return name
    
    def getFileFormat(self,elem):
        name = elem.split('.')[-1]
        return name

    def orderVoiceFiles(self):
        self.files.sort(key=self.getPureFileName)
        print(self.files)

    def generateFinalOutput(self):
        for i in range(len(self.files)):
            self.files[i] = AudioSegment.from_file(self.files[i])
        self.output = sum(self.files)

    def getFinalOutput(self):
        return self.output

    def uniteOutput(self):
        if VoiceCompiler.final_output is None:
            VoiceCompiler.final_output = self.output.fade_in(1000)
        else:
            VoiceCompiler.final_output = VoiceCompiler.final_output.append(self.output)

    def getPrivateOutputLength(self):
        return self.output.duration_seconds

    def exportFinalOutput(self):
        return self.final_output.export("pod.mp3",format="mp3")

class Chapter:

    final_vc = None
    final_bc = None
    final_podcast = None
    instances = []

    def __init__(self,vc,bc):
        self.vc = vc
        self.bc = bc
        self.output_vc = None
        self.output_bc = None
        self.output = None
        Chapter.instances.append(self)

    def compile(self):
        self.vc.gatherFiles( Path(Main.path + 'assets/' + str(self.vc.id)) )
        self.vc.orderVoiceFiles()
        self.vc.generateFinalOutput()
        self.output_vc = self.vc.getFinalOutput()

        self.bc.gatherFiles( self.vc, Path(Main.path + "music/") )
        self.bc.generateMusicMix( len(self.output_vc) )
        self.output_bc = self.bc.getFinalOutput()

    def uniteVC(self):
        for vc in VoiceCompiler.instances:
            if Chapter.final_vc == None:
                Chapter.final_vc = AudioSegment.silent(duration=TRANSITION_TIME) + vc.output
            else:
                Chapter.final_vc = Chapter.final_vc + AudioSegment.silent(duration=TRANSITION_TIME*2) + vc.output

    def uniteBC(self):
        for bc in BackgroundCompiler.instances:
            if Chapter.final_bc is None:
                Chapter.final_bc = bc.output
            else:
                Chapter.final_bc += bc.output
    
    def uniteOutputs(self):
        diff = len(self.output_bc) - len(self.output_vc)
        print(diff)
        self.output = self.output_bc.overlay(self.output_vc,position=int(diff/2),gain_during_overlay=-16.0)

    def compileAndExport(self):
        for chapter in Chapter.instances:
            if Chapter.final_podcast is None:
                Chapter.final_podcast = chapter.output
            else:
                Chapter.final_podcast += chapter.output
        Chapter.final_podcast.export(FINAL_FILENAME,format='mp3')

class Main:

    path = './'
    chapters = None
    compilers = []

    def __init__(self, path=None):
        if path is not None:
            Main.path = path

        p = Path(Main.path + "assets/")
        Main.chapters = len([i for i in p.iterdir() if p.is_dir()])

        for i in range(Main.chapters):
              Main.compilers.append( Chapter( VoiceCompiler(i+1),BackgroundCompiler(i+1) ) )


    def main(self):
        for chapter in Main.compilers:
            chapter.compile()
            chapter.uniteOutputs()
        Main.compilers[0].compileAndExport()


if __name__ == '__main__':
    if(len(sys.argv) < 2):
        Main().main()
    else:
        # Parsing CLI arguments
        # TODO make this actually good
        FINAL_FILENAME = sys.argv[1]
        Main().main()
