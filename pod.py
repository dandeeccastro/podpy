# Native libraries 
import sys
import random 
from pathlib import Path
import audioop

# My modules
import exceptions

# Pip installed libraries 
from pydub import AudioSegment

# Global variables
TRANSITION_TIME = 1000 # 1s 

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
        """ Collects files from music folder to use in the mix, and will do so while
        randomizing choices and avoiding already used songs 
        """
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
        """ Mixes background music to cover voice_length + transition time twice, for fade-in and fade-out. 
            It'll adjust the song length and effects based on if it's the beginning of the mix, getting to the end
            or in the middle.
        """
        music_length = voice_length + TRANSITION_TIME*2
        i = 0
        output_length = 0

        # I don't really know why is this here and why I didn't notice it before lol
        for song in self.files:
            song = song

        while music_length > output_length:
            song = self.files[i].apply_gain(-20.0)
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
        """ Getter for this instances output variable """
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
        """ Gathers all voice files from project filesystem """
        for item in traverser.iterdir():
            self.files.append(str(item))

    def getPureFileName(self, elem):
        """ Gets file name without file extension from elem """
        return elem.split('.')[0].split('/')[-1]
    
    def getFileFormat(self,elem):
        """ Gets file format of elem """
        return elem.split('.')[-1]

    def orderVoiceFiles(self):
        """ Orders voice files based by their filename """
        self.files.sort(key=self.getPureFileName)
        print(self.files)

    def generateFinalOutput(self):
        """ Generates output for this VoiceCompiler's instance """
        for i in range(len(self.files)):
            self.files[i] = AudioSegment.from_file(self.files[i])
        self.output = sum(self.files)

    def getFinalOutput(self):
        """ Getter for this VoiceCompiler's output """
        return self.output

    def uniteOutput(self):
        """ Unites all VoiceCompiler outputs into one final variable """
        if VoiceCompiler.final_output is None:
            VoiceCompiler.final_output = self.output.fade_in(1000)
        else:
            VoiceCompiler.final_output = VoiceCompiler.final_output.append(self.output)

    def getPrivateOutputLength(self):
        """ Getter for this instance's output duration in seconds """
        return self.output.duration_seconds

    def exportFinalOutput(self):
        """ Exports final output from all VoiceCompilers instances """
        return self.final_output.export("pod.mp3",format="mp3")

class Chapter:

    final_vc = None
    final_bc = None
    final_podcast = None
    instances = []

    def __init__(self,vc,bc):
        """ Stores VoiceCompiler and BackgroundCompiler instances to Chapter, and stores itself on a public attribute instances """
        self.vc = vc
        self.bc = bc
        self.output_vc = None
        self.output_bc = None
        self.output = None
        Chapter.instances.append(self)

    def compile(self):
        """ Compiles final results for this object's VoiceCompiler and BackgroundCompiler instances """
        self.vc.gatherFiles( Path(Main.path + 'assets/' + str(self.vc.id)) )
        self.vc.orderVoiceFiles()
        self.vc.generateFinalOutput()
        self.output_vc = self.vc.getFinalOutput()

        self.bc.gatherFiles( self.vc, Path(Main.path + "music/") )
        self.bc.generateMusicMix( len(self.output_vc) )
        self.output_bc = self.bc.getFinalOutput()

    def uniteVC(self):
        """ Unites all VoiceCompiler outputs into a single output blob and adds it to final_vc """
        for vc in VoiceCompiler.instances:
            if Chapter.final_vc == None:
                Chapter.final_vc = AudioSegment.silent(duration=TRANSITION_TIME) + vc.output
            else:
                Chapter.final_vc = Chapter.final_vc + AudioSegment.silent(duration=TRANSITION_TIME*2) + vc.output

    def uniteBC(self):
        """ Unites all BackgroundCompiler outputs to a single output and stores it in final_bc """
        for bc in BackgroundCompiler.instances:
            if Chapter.final_bc is None:
                Chapter.final_bc = bc.output
            else:
                Chapter.final_bc += bc.output
    
    def uniteOutputs(self):
        """ Compiles final podcast output, mixing voice and background output. It does so by calculating 
            the difference between output lengths, and settling the voice output in the middle of the background 
            output, so that fade-in and fade-out effects sound correct
        """
        diff = len(self.output_bc) - len(self.output_vc)
        print(diff)
        self.output = self.output_bc.overlay(self.output_vc,position=int(diff/2))

    def compileAndExport(self):
        """ Generates final file by adding up every single Chapter instance output  """
        for chapter in Chapter.instances:
            if Chapter.final_podcast is None:
                Chapter.final_podcast = chapter.output
            else:
                Chapter.final_podcast += chapter.output
        Chapter.final_podcast.export(Main.final_filename,format='mp3')

class Main:

    path = './'
    chapters = None
    compilers = []
    final_filename = "podcast.mp3"

    def __init__(self, path=None, final_filename=None):
        """ Initializer gets optional parameters, uses path to gather amount of chapters and 
            appends VoiceCompiler and BackgroundCompiler instances to compilers
        """
        if path is not None:
            Main.path = path
        if final_filename is not None:
            Main.final_filename = final_filename

        p = Path(Main.path + "assets/")
        Main.chapters = len([i for i in p.iterdir() if p.is_dir()])

        for i in range(Main.chapters):
              Main.compilers.append( Chapter( VoiceCompiler(i+1),BackgroundCompiler(i+1) ) )

    def main(self):
        """ Goes through the whole compiling process, generating chapter instances for each section in the
            file system, compiling voice and audio and generating the final file 
        """
        for chapter in Main.compilers:
            chapter.compile()
            chapter.uniteOutputs()
        Main.compilers[0].compileAndExport()
