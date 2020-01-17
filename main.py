# Native libraries 
import sys
import random 
from pathlib import Path
import audioop

# Pip installed libraries 
from pydub import AudioSegment

class BackgroundCompiler:
    final_output = None
    instances = []

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
        print(len(files))
        while (mix_duration < voice_length):
            audio = AudioSegment.from_file( files[ random.randint(0,len(files) - 1 ) ])
            self.files.append( audio )
            mix_duration += self.files[i].duration_seconds * 1000
            i += 1
        print(self.files)

    def generateMusicMix(self, voice_length):
        music_length = voice_length + 1000
        for song in self.files:
            if self.output is None :
                self.output = song.fade_in(500)
            else:
                self.output = self.output.append(song,crossfade=500)

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

    def __init__(self,vc,bc):
        self.vc = vc
        self.bc = bc
        self.output_vc = None
        self.output_bc = None

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
                Chapter.final_vc = vc.output
            else:
                Chapter.final_vc = Chapter.final_vc.append(vc.output)

    def uniteBC(self):
        for bc in BackgroundCompiler.instances:
            if Chapter.final_bc is None:
                Chapter.final_bc = bc.output
            else:
                Chapter.final_bc = Chapter.final_bc.append(bc.output)

    def compileAndExport(self):
        Chapter.final_vc.export('final_vc.mp3',format='mp3')
        Chapter.final_bc.export('final_bc.mp3',format='mp3')

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
        Main.compilers[0].uniteVC()
        Main.compilers[0].uniteBC()
        Main.compilers[0].compileAndExport()


if __name__ == '__main__':
    if(len(sys.argv) < 2):
        Main().main()
    else:
        Main(sys.argv[1]).main()
