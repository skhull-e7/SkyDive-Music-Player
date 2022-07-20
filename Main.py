# Importing tkinter, os, pygame and random Modules
from tkinter import *
from tkinter import ttk, filedialog as fd, messagebox as mb
from tkinter.font import BOLD
import os, pygame, random


# Creating Special Buttons for Music Player App
class musicPlayerButton(Button):

    def __init__(self, *args, **kwargs):
        """ Takes Methods From Button Class of Tkinter Module """
        super().__init__(*args, **kwargs)
        self.config(bd=0, relief=FLAT)
        self.__fg, self.__bg, self.__b, self.__f = self['fg'], self['bg'], 'grey', 'white'
        self.bind('<Enter>', self.__enter)
        self.bind('<Leave>', self.__leave)

    def chooseColor(self, enterBG, enterFG):
        """ Background And Foreground Color when pointer hovers on Button """
        self.__b, self.__f = enterBG, enterFG
    
    def __enter(self, evnt):
        """ when pointer hovers on Button """
        if self['state'] != DISABLED:
            self.config(bg=self.__b, fg=self.__f)
                
    def __leave(self, evnt):
        """ when pointer leaves Button """
        self.config(bg=self.__bg, fg=self.__fg)


# Creating A Settings Window For App
class musicPlayerSettings(Toplevel):

    def __init__(self, *args, **kwargs):
        """ Takes Methods From Toplevel Class of Tkinter Module """
        super().__init__(*args, **kwargs)
        self.master = args[0]
        self.title('Settings - Sky Dive Music Player')
        self.geometry('400x200')
        self.master.eval(f'tk::PlaceWindow {str(self)} center')
        self.resizable(False, False)
        self.config(bg='#10111b')
        self.grab_set()
        self.protocol('WM_DELETE_WINDOW', self.__onExit)

    def addFrame(self):
        """ Adds a Labeled Frame in Settings Window """
        self.settingFrame = LabelFrame(self, bg='#10111b', text='Select Default Folder', font=('Courier New', 16), bd=0, fg='yellow')
        self.settingFrame.pack(fill=BOTH, expand=YES, pady=10, padx=10)

    def addLocationEntry(self):
        """ Adds Entry Section in SEttings Window """
        self.locationEntry = Entry(self.settingFrame, font=('Consolas', 20), bd=0, highlightthickness=0)
        self.locationEntry.pack(side=LEFT, expand=YES, fill=X, padx=5, pady=5)

    def addLocationButton(self):
        """ Adds Folder Choosing Button """
        self.locationButton = musicPlayerButton(self.settingFrame, font=('Consolas', 20), text='📁', bg='#10111b', fg='yellow', activebackground='white', activeforeground='yellow', command=self.__addFolder)
        self.locationButton.chooseColor(enterBG='grey', enterFG='yellow')
        self.locationButton.pack(side=LEFT, expand=NO, fill=X, padx=10, pady=5)

    def addSubmitButton(self):
        """ Adds Confirm Folder Button and checks if Folder really exists """
        self.submitButton = musicPlayerButton(self.settingFrame, text='Select Folder', font=('@MS Gothic', 15, BOLD), activebackground='black', activeforeground='green', command=self.__selectFolder)
        self.submitButton.chooseColor(enterBG='sky blue', enterFG='green')
        self.submitButton.pack(side=BOTTOM, expand=YES, fill=BOTH, padx=10, pady=10)
        
    def addResettButton(self):
        """ Adds Rest Button """
        self.resetButton = musicPlayerButton(self.settingFrame, text='Restore Defaults', font=('@MS Gothic', 15, BOLD), activebackground='black', activeforeground='green', command=self.__restoreDefaults)
        self.resetButton.chooseColor(enterBG='sky blue', enterFG='green')
        self.resetButton.pack(side=BOTTOM, expand=YES, fill=BOTH, padx=10, pady=10)
    
    def __addFolder(self):
        """ Function for Default Folder Choosing """
        try:
            self.__folder = fd.askdirectory()
            self.locationEntry.delete(0, END)
            self.locationEntry.insert(END, self.__folder)
        except:
            pass

    def __selectFolder(self):
        """ Confirms if Location Exists for Default Location """
        if os.path.exists(self.locationEntry.get()):
            with open('Location.txt', 'w', encoding='utf-8') as f:
                f.write(self.locationEntry.get())
        else:
            mb.showerror(title='Settings - Sky Dive Music Player', message='Location You Entered Does Not Exist.\nPlease Try Again.')

    def __restoreDefaults(self):
        """ Make the App Run from Beginning """
        with open('Location.txt', 'w') as f:
            f.write('')
        self.master.SongNumbers.config(text='Select Music Directory -> ', font=('Consolas', 20))
        self.master.musicList.delete(0, END)
        pygame.mixer.music.unload()
        self.master.songTitle.config(text='None Playing !')
        mb.showinfo(title='Settings - Sky Dive Music Player', message='Default Location is Removed. App Will Start From Beginning.')

    def __onExit(self):
        """ Function when you Exit the Settings Window """
        if self.master.songTitle['text'] == 'None Playing !':
            try:
                with open('Location.txt', 'r') as f:
                    x = f.read()
                self.master.__folder = x
                self.master.__songs = os.listdir(self.master.__folder)
                self.master.__Songs = []
                self.master.musicList.delete(0, END)
                for item in self.master.__songs:
                    if item[-4:] == '.mp3':
                        self.master.__Songs.append(item[:-4])
                        self.master.musicList.insert(END, item[:-4])
                self.master.SongNumbers.config(text=f'{self.master.musicList.size()} Songs', font=('Segoe Script', 19, BOLD))
                self.destroy()
            except:
                self.destroy()
        else:
            self.destroy()


# Creating Music Player(App) Class
class MusicPlayer(Tk):

    __songPlaying = 'None Playing !'
    with open('Location.txt', 'r') as f:
        __location = f.read()

    def __init__(self):
        """ Takes Methods From Tk Class of Tkinter Module """
        super().__init__()
        pygame.init()
        self.geometry('830x400+250+250')
        self.title('Sky Dive Music Player')
        self.resizable(False, False)
        self.config(bg='#10111b')
        #self.wm_iconbitmap(r'icon.ico')
        self.lift()
        self.MUSIC_END = pygame.USEREVENT+1
        pygame.mixer.music.set_endevent(self.MUSIC_END)

    def addFrames(self):
        """ Adds three diefferent Frames in App 
        These Frames are :
            leftFrame -> Shows Song List and Folder choosing option
            middleFrame -> Creates A Horizontal Line between left and right Frames
            rightFrame -> Shows Music Controls and Settings Option
        """
        self.leftFrame = Frame(self, bg='#10111b')
        self.middleLine = Frame(self, bg='White', width=2)
        self.rightFrame = Frame(self, width=350, bg='#10111b')
        self.leftFrame.pack(side=LEFT, expand=YES, fill=BOTH, padx=2, pady=2)
        self.middleLine.pack(side=LEFT, fill=Y, padx=2)
        self.rightFrame.pack(side=LEFT, fill=Y, padx=2, pady=2)
    
    def addTitleBar(self):
        """ Adds another Frame in left Frame
            Shows Number of Songs and Folder Button
        """
        self.titleBar = Frame(self.leftFrame, bg='#10111b')
        self.titleBar.pack(side=TOP, fill=X, padx=3, pady=3)

    def addListBar(self):
        """ Adds Frame for Listbox """
        self.listBar = Frame(self.leftFrame, bg='#10111b')
        self.listBar.pack(side=LEFT, expand=YES, fill=BOTH, padx=3, pady=3)
    
    def addScrollBarRegions(self):
        """ Adds Scroll Bar Regions/Frames in left Frame """
        self.vScrollRegion = Frame(self.leftFrame, bg='#10111b', width=15)
        self.vScrollRegion.pack(side=RIGHT, fill=Y, padx=3, pady=3)
        self.hScrollRegion = Frame(self.leftFrame, bg='#10111b', height=15)
        self.hScrollRegion.pack(side=BOTTOM, fill=X, padx=3, pady=3)

    def addMusicControlFrame(self):
        """ Adds a Frame for Song Playing Name And Music Control Buttons """
        self.musicControlFrame = Frame(self.rightFrame, bg='#10111b', width=350)
        self.musicControlFrame.pack(expand=YES, fill=BOTH, padx=3, pady=3)
    
    def addSettingsFrame(self):
        """ Adds a Frame for Settings Button and adds Settings Button in settings Frame """
        self._line = Frame(self.rightFrame, bg='cyan', width=350, height=3)
        self._line.pack()
        self.settingsButton = musicPlayerButton(self.rightFrame, bg='#10111b', fg='white', text='Settings', height=2, font=('@MS Gothic', 25, BOLD), command=self.__runSettings)
        self.settingsButton.pack(fill=BOTH)

    def setTitleBar(self):
        """ Set The titleFrame we Created Earlier """
        self.SongNumbers = Label(self.titleBar, text='Select Music Directory -> ', font=('Consolas', 20), fg='white', bg='#10111b')
        self.SongNumbers.pack(side=LEFT, expand=YES, fill=BOTH)
        self.fileButton = musicPlayerButton(self.titleBar, text='📁', fg='yellow', font=('Consolas', 23, BOLD), activebackground='gray', activeforeground='yellow', bg='#10111b', command=self.__changeDirectory)
        self.fileButton.chooseColor(enterBG='grey', enterFG='yellow')
        self.fileButton.pack(side=LEFT, fill=BOTH)
    
    def setListBar(self):
        """ Set Listbox in listBar Frame """
        self.musicList = Listbox(self.listBar, bg='#10111b', fg="white", selectbackground='#10111b', selectborderwidth=0, selectforeground='white', highlightthickness=0, bd=0, font=('Consolas', 16), takefocus=0, activestyle=NONE)
        self.musicList.pack(side=LEFT, expand=YES, fill=BOTH)

    def setVerticalScrollbar(self):
        """ Vertical Scrollbar for listbox """
        self.vScroll = Scrollbar(self.vScrollRegion, width=15, elementborderwidth=0, troughcolor='black')
        
    def setHorizontalScrollbar(self):
        """ Horizontal Scrollbar for listbox """
        self.hScroll = Scrollbar(self.hScrollRegion, width=15, orient=HORIZONTAL, elementborderwidth=0)

    def updateScrollbars(self):
        """ Set Scrollbars for Listbox """
        self.musicList.config(yscrollcommand=self.vScroll.set, xscrollcommand=self.hScroll.set)
        self.vScroll.config(command=self.musicList.yview)
        self.hScroll.config(command=self.musicList.xview)

    def appIconSet(self):
        """ Creates a Frame for SDMUSICPLAYER icon in right Frame """
        self.iconFrame = Frame(self.rightFrame, bg='#10111b', width=350, height=110)
        self.iconFrame.pack(fill=BOTH, expand=YES)
        Label(self.iconFrame, text='S', font='arial 45 bold', bg='#10111b', fg='red', bd=0).place(x=147, y=8, width=35)
        Label(self.iconFrame, text='D', font='arial 45 bold', bg='red', fg='#10111b', bd=0).place(x=187, y=13, height=60)
        Label(self.iconFrame, text='Music Player', font='consolas 15 bold', bg='#10111b', fg='red').place(x=120, y=73)
        Label(self.iconFrame, text='', bg='cyan').place(x=20, y=105, width=310, height=2)

    def songTitleSet(self):
        """ sets the song Playing name Bar """
        self.songTitle = Label(self.musicControlFrame, text='None Playing !', fg='Grey', bg='#10111b', font=('Courier New', 17, BOLD))
        self.songTitle.pack(fill=BOTH, expand=YES, side=TOP, anchor=N, pady=8)

    def addMusicControls(self):
        """ Adds Button in musicControls Frame """
        self.playPrevButton = musicPlayerButton(self.musicControlFrame, text='\u23ee', font=('Consolas', 31), fg='#53acb0', bg='#10111b', height=1, command=self.__playPrevSong)
        self.playButton = musicPlayerButton(self.musicControlFrame, text='\u25b6', font=('Consolas', 31), fg='#53acb0', bg='#10111b', height=1)
        self.playNextButton = musicPlayerButton(self.musicControlFrame, text='\u23ed', font=('Consolas',31), fg='#53acb0', bg='#10111b', height=1, command=self.__playNextSong)
        self.lastRow = Frame(self.musicControlFrame)
        self.shuffleButton = musicPlayerButton(self.lastRow, text='🔀', font=('Consolas', 31), fg='#53acb0', bg='#10111b', command=self.__changeShuffle)
        self.repeatButton = musicPlayerButton(self.lastRow, text='🔁', font=('Consolas', 31), fg='#53acb0', bg='#10111b', command=self.__changeRepeat)
        self.lastRow.pack(side=BOTTOM, fill=BOTH)
        self.shuffleButton.pack(side=LEFT, fill=X, expand=YES)
        self.repeatButton.pack(side=LEFT, fill=X, expand=YES)
        self.playPrevButton.pack(side=LEFT, anchor=CENTER, expand=YES, fill=BOTH)
        self.playButton.pack(side=LEFT, anchor=CENTER, expand=YES, fill=BOTH)
        self.playNextButton.pack(side=LEFT, anchor=CENTER, expand=YES, fill=BOTH)

    def addSettingsPage(self):
        """ Creates Settings Window """
        self.settingsWindow = musicPlayerSettings(self)
        self.settingsWindow.addFrame()
        self.settingsWindow.addResettButton()
        self.settingsWindow.addSubmitButton()
        self.settingsWindow.addLocationEntry()
        self.settingsWindow.addLocationButton()

    def bindFunctions(self):
        """ Bind Different functions for different Events in App """
        self.musicList.bind('<Enter>', self.__hideShowScrollbar)
        self.hScrollRegion.bind('<Enter>', self.__hideShowScrollbar)
        self.vScrollRegion.bind('<Enter>', self.__hideShowScrollbar)
        self.leftFrame.bind('<Leave>', self.__hideShowScrollbar)
        self.titleBar.bind('<Enter>', lambda x: self.__hideShowScrollbar(evnt='Leave'))
        self.musicList.bind('<Down>', NONE)
        self.musicList.bind('<Up>', NONE)
        self.musicList.bind('<Left>', NONE)
        self.musicList.bind('<Right>', NONE)
        self.bind('<Tab>', NONE)
        self.musicList.bind('<<ListboxSelect>>', self.__playSong)

    def onStart(self):
        """ Checks for Default Location in App for Music """
        if self.__location:
            try:
                self.__folder = self.__location
                self.__songs = os.listdir(self.__folder)
                self.__Songs = []
                self.musicList.delete(0, END)
                for item in self.__songs:
                    if item[-4:] == '.mp3':
                        self.__Songs.append(item[:-4])
                        self.musicList.insert(END, item[:-4])
                self.SongNumbers.config(text=f'{self.musicList.size()} Songs', font=('Segoe Script', 19, BOLD))
            except:
                pass
        else:
            pass

    def __hideShowScrollbar(self, evnt):
        """ Hide/Shows Scrollbar whenever pointer hovers on Music List or scrollbar regions """
        if 'Leave' in str(evnt):
            self.hScroll.pack_forget()
            self.vScroll.pack_forget()
        else:
            self.vScroll.pack(fill=BOTH, expand=YES)
            self.hScroll.pack(fill=BOTH, expand=YES)

    def __changeDirectory(self):
        """ Function for loading Songs from Folder """
        try:
            self.__folder = fd.askdirectory()
            self.__songs = os.listdir(self.__folder)
            self.__Songs = []
            self.musicList.delete(0, END)
            for item in self.__songs:
                if item[-4:] == '.mp3':
                    self.__Songs.append(item[:-4])
                    self.musicList.insert(END, item[:-4])
            self.SongNumbers.config(text=f'{self.musicList.size()} Songs', font=('Segoe Script', 19, BOLD))
        except:
            pass

    def __playSong(self, evnt=None, songToPlay=None):
        """ Plays Song """
        try:
            if evnt != None:
                songToPlay = self.__Songs[evnt.widget.curselection()[0]]
            pygame.mixer.music.unload()
            pygame.mixer.music.load(os.path.join(self.__folder, songToPlay+'.mp3'))
            pygame.mixer.music.play()
            self.__songPlaying = songToPlay
            self.title(f'{self.__songPlaying} - Sky Dive Music Player')
            if len(songToPlay)>=22:
                songToPlay = songToPlay[:19]+'...'
            self.songTitle.config(text=songToPlay, anchor=W)
            self.playButton.config(text='\u23f8', command=self.__pauseSong)
        except:
            pass

    def __pauseSong(self, evnt=None):
        """ Pause/Unpause Song """
        if self.playButton['text'] == '\u23f8':
            pygame.mixer.music.pause()
            self.playButton.config(text='\u25b6')
        else:
            pygame.mixer.music.unpause()
            self.playButton.config(text='\u23f8')

    def __playPrevSong(self, evnt=None):
        """ Play Previous Song from Music List
            -> if song is played for more than 10 seconds
                -> Song is rewinded
        """
        try:
            if self.__songPlaying == 'None Playing !':
                self.__playSong(songToPlay=self.__Songs[-1])
                return
            songPlaying = self.__songPlaying
            songPlayingIndex = self.__Songs.index(songPlaying)
            if pygame.mixer.music.get_pos()/1000 > 10.0:
                self.__playSong(songToPlay=songPlaying)
                return
            if self.shuffleButton['text'] == '🔀' and self.repeatButton['text'] == '🔁':
                songToPlay = random.choice(self.__Songs)
                self.__playSong(songToPlay=songToPlay)
            elif self.repeatButton['text'] == '🔂':
                self.__playSong(songToPlay=songPlaying)
            else:
                try:
                    self.__playSong(songToPlay=self.__Songs[songPlayingIndex-1])
                except:
                    self.__playSong(songToPlay=self.__Songs[-1])
        except:
            try:
                pygame.mixer.music.play()
            except:
                pass

    def __playNextSong(self, evnt=None):
        """ Plays Next Song from Music List """
        try:
            if self.__songPlaying == 'None Playing !':
                self.__playSong(songToPlay=self.__Songs[0])
                return
            songPlaying = self.__songPlaying
            songPlayingIndex = self.__Songs.index(songPlaying)
            if self.shuffleButton['text'] == '🔀' and self.repeatButton['text'] == '🔁':
                songToPlay = random.choice(self.__Songs)
                self.__playSong(songToPlay=songToPlay)
            elif self.repeatButton['text'] == '🔂':
                self.__playSong(songToPlay=songPlaying)
            else:
                try:
                    self.__playSong(songToPlay=self.__Songs[songPlayingIndex+1])
                except:
                    self.__playSong(songToPlay=self.__Songs[0])
        except:
            try:
                pygame.mixer.music.play()
            except:
                pass

    def checkForSong(self):
        """ Checks if Song has Stopped or not """
        for event in pygame.event.get():
            if event.type == self.MUSIC_END:
                self.__playNextSong()
        self.after(100, self.checkForSong)

    def __changeShuffle(self, evnt=None):
        """ Changes Shuffle Button """
        if self.shuffleButton['text'] == '🔀':
            self.shuffleButton.config(text='\u0336🔀')
        else:
            self.shuffleButton.config(text='🔀')

    def __changeRepeat(self, evnt=None):
        """ Changes Repeat Button """
        if self.repeatButton['text'] == "🔁":
            self.repeatButton.config(text="🔂")
        else:
            self.repeatButton.config(text="🔁")

    def __runSettings(self):
        """ Runs The Settings Window of App """
        self.addSettingsPage()
        self.settingsWindow.mainloop()

if __name__ == '__main__':
    print('Please Run \'MusicPlayer.py\'\n')
    input()
