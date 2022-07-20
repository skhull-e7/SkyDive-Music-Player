# Import MusicPlayer Class from Main.py
from Main import MusicPlayer

# Create App using MusicPlayer Class of Main.py
if __name__ == '__main__':
    App = MusicPlayer()
    App.addFrames()
    App.addTitleBar()
    App.addScrollBarRegions()
    App.addListBar()
    App.appIconSet()
    App.addMusicControlFrame()
    App.addSettingsFrame()
    App.setTitleBar()
    App.setListBar()
    App.setVerticalScrollbar()
    App.setHorizontalScrollbar()
    App.updateScrollbars()
    App.songTitleSet()
    App.addMusicControls()
    App.bindFunctions()
    App.onStart()
    App.checkForSong()
    App.mainloop()