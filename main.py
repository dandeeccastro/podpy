import sys
from pathlib import Path
import audioop
from pydub import AudioSegment

class VoiceCompiler:
    final_output = None	

    def __init__(self, id, file_path):
        self.id = id
        self.files = []
        self.output = None
        self.gatherFiles(Path(file_path))

    def __del__(self):
        if (len(self.files) is 0):
            print('Folder ' + str(self.id) + ' has no files to generate')
        print('Compiler shutting down...')

    def gatherFiles(self, traverser):
        print('Compiler ' + str(self.id) + ' gathering files')

        i = 0
        for item in traverser.iterdir():
            self.files.append(str(item))
            i += 1

        if (len(self.files) == 0):
            del self

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
        self.output.export("test"+str(self.id)+".mp3",format="mp3")

    # TODO adicionar transição entre caps
    def uniteOutput(self):
        if VoiceCompiler.final_output is None:
            VoiceCompiler.final_output = self.output
        else:
            VoiceCompiler.final_output += self.output

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
              Main.voice_compilers.append(VoiceCompiler(i+1, Main.path + 'assets/' + str(i+1)))

        for vc in Main.voice_compilers:
            vc.orderVoiceFiles()
            vc.generateFinalOutput()
            vc.uniteOutput()

        VoiceCompiler.exportFinalOutput()

    def main(self):
          print('main: TODO implement me')


if __name__ == '__main__':
    if(len(sys.argv) < 2):
        Main().main()
    else:
        Main(sys.argv[1]).main()
