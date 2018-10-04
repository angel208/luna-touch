from tkinter import PhotoImage
import time

class AnimatedGif():
    filename = ""
    delay = 60
    frames = []
    cFrame = 0
    fCount = 0

    def __init__(self, newFilename, frames, fps):

        self.filename = newFilename
        self.frames = frames
        self.fps = fps

        #get a list with the frames of the gif
        self.frames = [PhotoImage(file= self.filename ,format = 'gif -index %i' %(i)) for i in range(frames)]

        #store the length of the array
        self.fCount = len(self.frames)
		

    def nextFrame(self):

        returnFrame = self.frames[self.cFrame]

        self.cFrame = ( self.cFrame + 1 ) % self.fCount

        time.sleep(1 / self.fps)
        
        return returnFrame
	

    def currentFrame(self):
        return self.frames[self.cFrame]


