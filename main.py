# import audiood
import sys
from pathlib import Path

class VoiceCompiler:
    voice = None
    def __init__(self,chapters):
        self.chapters = chapters

class BackgroundCompiler:
    background_music = None
    def __init__(self,chapters):
        self.chapters = chapters

class Main:
    def __init__(self,file_path):
        self.file_path = file_path
        p = Path(file_path)
        x = [i for i in p.iterdir() if i.is_dir()]
        x = len(x)
        self.voice_compiler = VoiceCompiler(x)
        self.background_compiler = BackgroundCompiler(x)
        self.main()

    def main(self):
        print(self.voice_compiler.chapters)

if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print('Usage: podcast file_path')
        exit()
    file_path = sys.argv[1]
    Main(file_path)
