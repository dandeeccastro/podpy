# Native libraries 
import sys
import random 
from pathlib import Path
import audioop

# Pip installed libraries 
from pydub import AudioSegment

class BackgroundMusicCompiler:
#    final_output = None
    instances = []
    lastMusicIndex = -1

    def __init__(self,id):
        self.id = id
        self.output = None
        self.files = []
        BackgroundMusicCompiler.instances.append(self)

    def __del__(self):
        print('Background Compiler shutting down...')

    def gatherFiles(self, voiceCompiler ,paths):
        """ Collects files from music folder to use in the mix, and will do so while
        randomizing choices and avoiding already used songs 
        """
        voiceLength = voiceCompiler.output.duration_seconds * 1000
        mixDuration = 0
        i = 0
        files = [songFile for songFile in paths.iterdir()]
        usedMusicIndexes = []
        while (mixDuration < voiceLength):
            randomIndex = random.randint(0,len(files) - 1)
            if randomIndex in usedMusicIndexes or randomIndex is BackgroundMusicCompiler.lastMusicIndex:
                continue
            else:
                usedMusicIndexes.append(rand)
                BackgroundMusicCompiler.lastMusicIndex = randomIndex
                audio = AudioSegment.from_file( files[ randomIndex ] )
                self.files.append( audio )
                mixDuration += self.files[i].duration_seconds * 1000
                i += 1

    def generateMusicMix(self, voiceLength):
        """ Mixes background music to cover voiceLength + transition time twice, for fade-in and fade-out. 
            It'll adjust the song length and effects based on if it's the beginning of the mix, getting to the end
            or in the middle.
        """
        musicLength = voiceLength + Main.transitionTime*2
        i = 0
        outputLength = 0

        # I don't really know why is this here and why I didn't notice it before lol
        # TODO: change this somehow
        for song in self.files:
            song = song

        while musicLength > outputLength:
            song = self.files[i].apply_gain(Main.decay)
            if self.output is None :
                if ( musicLength <= len(song) ):
                    diff = musicLength - outputLength
                    song = song[:diff].fade_in(Main.transitionTime).fade_out(Main.transitionTime)
                    self.output = song
                else:
                    self.output = song.fade_in(Main.transitionTime).fade_out(Main.transitionTime)
            else:
                if ( musicLength <= len(song) + outputLength ):
                    diff = musicLength - outputLength
                    song = song[:diff].fade_in(Main.transitionTime).fade_out(Main.transitionTime)
                    self.output += song
                else:
                    song = song.fade_in(Main.transitionTime).fade_out(Main.transitionTime)
                    self.output += song
            outputLength = len(self.output)
            i = i + 1 % len(self.files)

    def getFinalOutput(self):
        """ Getter for this instances output variable """
        return self.output
    

class VoiceCompiler:
#    final_output = None	
    instances = []

    def __init__(self, id):
        self.id = id
        self.files = []
        self.output = None
        VoiceCompiler.instances.append(self)

    def __del__(self):
        print('Voice Compiler shutting down...')

    def gatherFiles(self, paths):
        """ Gathers all voice files from project filesystem """
        for voiceFile in paths.iterdir():
            self.files.append( str(voiceFile) )

    def getPureFileName(self, filename):
        """ Gets file name without file extension from elem """
        return filename.split('.')[0].split('/')[-1]
    
#    def getFileFormat(self,elem):
#        """ Gets file format of elem """
#        return elem.split('.')[-1]

    def orderVoiceFiles(self):
        """ Orders voice files based by their filename """
        self.files.sort(key=self.getPureFileName)
        print(self.files)

    def generateFinalOutput(self):
        """ Generates output for this VoiceCompiler's instance """
        for i in range(len(self.files)):
            self.files[i] = AudioSegment.from_file(self.files[i]).apply_gain(Main.voiceGain)
        self.output = sum(self.files)

    def getFinalOutput(self):
        """ Getter for this VoiceCompiler's output """
        return self.output

#    def uniteOutput(self):
#        """ Unites all VoiceCompiler outputs into one final variable """
#        if VoiceCompiler.final_output is None:
#            VoiceCompiler.final_output = self.output.fade_in(1000)
#        else:
#            VoiceCompiler.final_output = VoiceCompiler.final_output.append(self.output)
#
#    def getPrivateOutputLength(self):
#        """ Getter for this instance's output duration in seconds """
#        return self.output.duration_seconds
#
#    def exportFinalOutput(self):
#        """ Exports final output from all VoiceCompilers instances """
#        return self.final_output.export("pod.mp3",format="mp3")

class Chapter:

    finalVoiceCompilation = None
    finalBackgroundMusicCompilation = None
    finalPodcast = None
    instances = []

    def __init__(self,voiceCompiler,backgroundCompiler):
        """ Stores VoiceCompiler and BackgroundMusicCompiler instances to Chapter, and stores itself on a public attribute instances """
        self.voiceCompiler = voiceCompiler
        self.backgroundCompiler = backgroundCompiler
        self.voiceCompilerOutput = None
        self.backgroundCompilerOutput = None
        self.output = None
        Chapter.instances.append(self)

    def compile(self):
        """ Compiles final results for this object's VoiceCompiler and BackgroundMusicCompiler instances """
        self.voiceCompiler.gatherFiles( Path(Main.path + '/assets/' + str(self.voiceCompiler.id)) )
        self.voiceCompiler.orderVoiceFiles()
        self.voiceCompiler.generateFinalOutput()
        self.voiceCompilerOutput = self.voiceCompiler.getFinalOutput()

        self.backgroundCompiler.gatherFiles( self.voiceCompiler, Path(Main.musicPath) )
        self.backgroundCompiler.generateMusicMix( len(self.voiceCompilerOutput) )
        self.backgroundCompilerOutput = self.backgroundCompiler.getFinalOutput()

#    def uniteVC(self):
#        """ Unites all VoiceCompiler outputs into a single output blob and adds it to finalVoiceCompilation """
#        for voiceCompiler in VoiceCompiler.instances:
#            if Chapter.finalVoiceCompilation == None:
#                Chapter.finalVoiceCompilation = AudioSegment.silent(duration=Main.transitionTime) + voiceCompiler.output
#            else:
#                Chapter.finalVoiceCompilation = Chapter.finalVoiceCompilation + AudioSegment.silent(duration=Main.transitionTime*2) + voiceCompiler.output
#
#    def uniteBC(self):
#        """ Unites all BackgroundMusicCompiler outputs to a single output and stores it in finalBackgroundMusicCompilation """
#        for backgroundCompiler in BackgroundMusicCompiler.instances:
#            if Chapter.finalBackgroundMusicCompilation is None:
#                Chapter.finalBackgroundMusicCompilation = backgroundCompiler.output
#            else:
#                Chapter.finalBackgroundMusicCompilation += backgroundCompiler.output
    
    def uniteOutputs(self):
        """ Compiles final podcast output, mixing voice and background output. It does so by calculating 
            the difference between output lengths, and settling the voice output in the middle of the background 
            output, so that fade-in and fade-out effects sound correct
        """
        diff = len(self.backgroundCompilerOutput) - len(self.voiceCompilerOutput)
        print(diff)
        self.output = self.backgroundCompilerOutput.overlay(self.voiceCompilerOutput,position=int(diff/2))

    def compileAndExport(self):
        """ Generates final file by adding up every single Chapter instance output  """
        for chapter in Chapter.instances:
            if Chapter.finalPodcast is None:
                Chapter.finalPodcast = chapter.output
            else:
                Chapter.finalPodcast += chapter.output
        Chapter.finalPodcast.export(Main.finalFilename,format='mp3')

class Main:

    # Arguments defaulted by optparse
    finalFilename = None
    transitionTime = None
    path = None
    musicPath = None
    voiceGain = None

    # Arguments programatically setted
    numberOfChapters = None
    chapters = []

    def __init__(self, path=None, finalFilename=None, musicPath=None, decay=None, transitionTime=None, voiceGain=None):
        """ Initializer gets optional parameters, uses path to gather amount of chapters and 
            appends VoiceCompiler and BackgroundMusicCompiler instances to compilers
        """

        Main.path = path
        Main.finalFilename = finalFilename
        Main.musicPath = musicPath
        Main.decay = decay
        Main.transitionTime = transitionTime
        Main.voiceGain = voiceGain

        paths = Path(Main.path + "/assets/")
        Main.numberOfChapters = len([item for item in paths.iterdir() if paths.is_dir()])

        for i in range(Main.numberOfChapters):
              Main.chapters.append( Chapter( VoiceCompiler(i+1),BackgroundMusicCompiler(i+1) ) )

    def main(self):
        """ Goes through the whole compiling process, generating chapter instances for each section in the
            file system, compiling voice and audio and generating the final file 
        """
        for chapter in Main.chapters:
            chapter.compile()
            chapter.uniteOutputs()
        Main.chapters[0].compileAndExport()
