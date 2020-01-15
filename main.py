# import audiood
import sys
from pathlib import Path
import audioop

class VoiceCompiler:
    final_output = None
    
    # Se cria com um id (para a ordem do audio0
    # e o caminho dos arquivos 

    def __init__(self,id,file_path):
        self.id = id
        self.gatherFiles(Path(file_path))

    def __del__(self):
        if (len(self.files) is 0):
            print ('Folder ' + str(self.id) + ' has no files to generate')
        print ('Compiler shutting down...')

    def gatherFiles(self,traverser):
        print ('Compiler ' + str(self.id) + ' gathering files')
        i = 0
        self.files = []
        for item in traverser.iterdir():
            self.files.append(open(item))
            print (self.files[i])
            i+=1
        if (len(self.files) == 0):
            del self

    def generateFinalOutput(self):
        print("generateFinaloutput: TODO implement me")


class Main:
    path = './'
    chapters = None
    voice_compilers = []
    def __init__(self,path=None):
        if path is not None:
           Main.path = path 
        p = Path(Main.path + "assets/")
        Main.chapters = len([i for i in p.iterdir() if p.is_dir()])
        for i in range(Main.chapters):
            Main.voice_compilers.append(VoiceCompiler( i+1, Main.path + 'assets/' + str(i+1) ))

    def main(self):
        print('main: TODO implement me')

if __name__ == '__main__':
    if(len(sys.argv) < 2):
        Main().main()
    else:
        Main(sys.argv[1]).main()
