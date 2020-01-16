import sys
from pathlib import Path
import audioop
from pydub import AudioSegment

class VoiceCompiler:
    final_output = None	

    def __init__(self, id):
        self.id = id
        self.files = []
        self.output = None

    def __del__(self):
        print('Compiler shutting down...')

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

    # TODO adicionar transição entre caps
    def uniteOutput(self):
        if VoiceCompiler.final_output is None:
            VoiceCompiler.final_output = self.output.fade_in(1000)
        else:
            VoiceCompiler.final_output = VoiceCompiler.final_output.append(self.output)

    def exportFinalOutput():
        VoiceCompiler.final_output.export("pod.mp3",format="mp3")


class Main:

    path = './'
    chapters = None
    voice_compilers = []

    def __init__(self, path=None):
        if path is not None:
            Main.path = path

        p = Path(Main.path + "assets/")
        Main.chapters = len([i for i in p.iterdir() if p.is_dir()])

        for i in range(Main.chapters):
              Main.voice_compilers.append(VoiceCompiler(i+1))


    def main(self):
        for vc in Main.voice_compilers:
            vc.gatherFiles( Path(Main.path + "assets/" + str(vc.id)) )
            vc.orderVoiceFiles()
            vc.generateFinalOutput()
            vc.uniteOutput()

        VoiceCompiler.exportFinalOutput()


if __name__ == '__main__':
    if(len(sys.argv) < 2):
        Main().main()
    else:
        Main(sys.argv[1]).main()
