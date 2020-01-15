from threading import Thread
import audiood

class VoiceLine(Thread):
    discourse = None # Full podcast voice line by the end

class BackgroundLine(Thread):
    background = None # Full background music by the end
