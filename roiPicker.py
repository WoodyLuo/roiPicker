'''
roiPicker - Cropping Region of interest(ROI) ROI using Tkinter with Pillow package.
                                                ____written by Woody, Lo Wen-Cheng. 
[ Instruction ]
Under the 'roiPicker.py' dictionary must have 'class1', 'class2', 'class3', 'class4'
'class5' and 'class6' folder, including 'default_img.jpg' image and 'icons' folder.

* This program is compatible for Window's user and macOS user.
'''

###########################################################################################
##  Variables Initialize 
###########################################################################################
debugMode       : bool = True
IMG_EXTENSIONS  : list = ['.jpg', '.jpeg', '.png', '.ppm', '.bmp', '.pgm', '.tif', '.tiff']


# Python Graphical User Interface, GUI Package.
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
# Python Operating System, OS Package.
import platform
import os
import sys
# Python Math Package.
import math
# Python Regular Expression Matching Operations.
import re


try:
    ''' 'PLT' package import '''
    from PIL import Image, ImageTk    # PIL is the Python Imaging Library
except ImportError:
    print( "'PIL::Image' wrapper for python not found!" )
    print( "'PIL::ImageTk' wrapper for python not found!" )
    print( "Using pip or pip3 to install:" )
    print( ">> pip/pip3 install Pillow" )
    # try..except.. - End

try:
    ''' import 'opencv-python' '''
    import cv2    # VideoCapture, VideoCapture.read, img.split, img.mean, imshow
except ImportError:
    print( "!!!!: 'cv2' wrapper for python not found!" )
    print( "  Using pip or pip3 to install:" )
    print( "  >> pip/pip3 install opencv-python" )
    print( "  AND  " )
    print( "  >> pip/pip3 install opencv-contrib-python" )
    # try..except.. - End

try:
    ''' import 'numpy' package '''
    import numpy as np    # Multi-dimensional Arrays, High-level Mathmatical Functions
except ImportError:
    print( "!!!!: 'numpy' wrapper for python not found!" )
    print( "  Using pip or pip3 to install:" )
    print( "  >> pip/pip3 install Pillow" )
    # try..except.. - End


class Debug(object):
    global debugMode;
    # Using slots to prevent the dynamic creation of attributes
    __slots__ = [   'tkWindowWidth', 'tkWindowHeight', 'pathDelimiter',
                    'fileNamePath', 'folderNamePath', 'folderImgList', 'osPlatform'   ]
    def __init__(self):
        self.tkWindowWidth  : int = 0
        self.tkWindowHeight : int = 0
        self.pathDelimiter  : str = ''
        self.fileNamePath   : str = ''
        self.folderNamePath : str = ''
        self.folderImgList  : list = [ ]
        self.osPlatform     : str = ''
        # END of '__init__()' FUNCTION.
    def set_tkWindowWidth( self, intVar:int ):
        self.tkWindowWidth = intVar
        # END of 'set_tkWindowWidth()' FUNCTION.
    def set_tkWindowHeight( self, intVar:int ):
        self.tkWindowHeight = intVar
        # END of 'set_tkWindowHeight()' FUNCTION.
    def set_pathDelimiter( self, strVar:str ):
        self.tkWindowHeight = strVar
        # END of 'set_pathDelimiter()' FUNCTION.
    def set_fileNamePath( self, strVar:str ):
        self.fileNamePath = strVar
        # END of 'set_fileNamePath()' FUNCTION.
    def set_folderNamePath( self, strVar:str ):
        self.folderNamePath = strVar
        # END of 'set_folderNamePath()' FUNCTION.
    def set_folderImgList( self, listVar:list ):
        self.folderImgList = listVar
        # END of 'set_folderImgList()' FUNCTION.
    def osCheck( self ):
        self.osPlatform = platform.platform()
        if( self.osPlatform.find('Darwin') != -1 ):
            self.pathDelimiter = '/'
        elif( self.osPlatform.find('Windows') != -1 ):
            self.pathDelimiter = '\\'
            # if..elif.. - End
        if( debugMode==True ):
            print( "Your path delimiter is:", self.pathDelimiter )
            print( "Your operating system is:", self.osPlatform )
            # if.. - End
        # END of 'osCheck()' FUNCTION.
    def __del__(self):
        pass
        # END of '__del__()' FUNCTION.
    # END of 'Debug()' CLASS.


class MainTk(object):
    global debugMode;
    def __init__( self ):
        # Create tk.Tk (main window)
        self.root = tk.Tk()
        self.root.title( "roiPicker" )
        self.root.geometry( "720x480+0+0" )
        # Check window configure
        self.root.bind('<ButtonRelease-1>', self.check_window_config)
        self.root.bind('<Configure>', lambda c: self.main_window_click(True))
        self.menuBar = Menubar( self.root )
        self.root.config(menu=self.menuBar)
        # END of '__init__()' FUNCTION.
    def check_window_config(self, event):
        if( self.clicked ):
            tkWindow_Width = self.root.winfo_width()
            tkWindow_Height = self.root.winfo_height()
            self.main_window_click(False)
            # if.. - End
            if( debugMode==True ):
                print("I'm printed after <Configure>.")  # the action goes here!
                print( 'Window width:%d;  Window height:%d;' %(tkWindow_Width, tkWindow_Height) )
                # if.. - End
        # END of 'check_window_config()' FUNCTION.    
    def main_window_click(self, value):
        self.clicked = value
        # END of 'main_window_click()' FUNCTION. 
    def start(self):
        self.root.mainloop()
        # END of 'start()' FUNCTION. 
    def __del__(self):
        pass
        # END of '__del__()' FUNCTION. 
    # END of 'Main()' CLASS. 


class FunctionMenu(tk.Frame):
    global debugMode;
    def __init__(self, parent):
        tk.Frame.__init__( self, parent )
        self.place( x=0, rely=0.87, relheight=0.15, relwidth=1 )
        self.root = parent
        # ROI Size - tk.Label, tk.Entry, tk.StringVar.
        self.label_ROI = tk.Label( self.root, text='ROI Size:', foreground='black', background="white" )
        self.label_ROI.place( relx=0.08, rely=0.86, width=62 )
        self.userInputSIZE = tk.IntVar()
        self.entry_roiSize = tk.Entry( self.root, width=4, textvariable=self.userInputSIZE )
        self.entry_roiSize.place( relx=0.08, rely=0.9, width=66 )
        # Image Classes - tk.Label, tk.ttk.Combobox, tk.StringVar.
        self.labelClass = tk.Label( self.root, text='Choose Class:', foreground='black', background="white" )
        self.labelClass.place( relx=0.2, rely=0.86, width=125 )
        self.txtCLASS = LoadTxt()  # Open 'classes.txt' file.
        self.userInputCLASS = tk.StringVar()
        self.classChosen = tk.ttk.Combobox( self.root, width=12,textvariable=self.userInputCLASS )
        self.classChosen[ 'values' ] = tuple( self.txtCLASS.getAllClasses() )
        self.classChosen.current( 0 )  # Set first Class name as a defult value.
        self.classChosen.place( relx=0.2, rely=0.9, height=30 )
        # Image Index - tk.Label, tk.Entry, tk.StringVar.
        self.labelIndex = tk.Label( self.root, text='Saving Index:', foreground='black', background="white" )
        self.labelIndex.place( relx=0.4, rely=0.86, width=100 )
        self.userInputINDEX = tk.IntVar()
        self.indexEntered = tk.Entry( self.root, width=4, textvariable=self.userInputINDEX )
        self.indexEntered.place( relx=0.4, rely=0.9, width=100 )
        # Configure Settint - tk.Button.
        self.buttonOK = tk.Button( self.root, text='OK', command=self.configOK )
        self.buttonOK.place( relx=0.55, rely=0.895 )
        # Create 'ImageFrame()' Object.
        self.imageFrame = ImageFrame( self.root )
        # Create 'Icons()' Object
        self.imgICONS = Icons()
        # Image(Folder) - tk.Button, tk.PhotoImage, HoverInfo
        self.img_aFolder = self.imgICONS.get_img_aFolder()
        self.buttonFOLDER = tk.Button( self.root, image=self.img_aFolder, command=self.__openFolder )
        self.buttonFOLDER.place( relx=0.715, rely=0.88 )
        self.hoverFOLDER = HoverInfo( self.root, self.buttonFOLDER, 'Load a folder' )
        # Image(Image) - tk.Button, tk.PhotoImage, HoverInfo
        self.img_aImage = self.imgICONS.get_img_aImage()
        self.buttonIMAGE = tk.Button( self.root, image=self.img_aImage, command=self.__openImg )
        self.buttonIMAGE.place( relx=0.78, rely=0.88 )
        self.hoverIMAGE = HoverInfo( self.root, self.buttonIMAGE, 'Load an image' )
        # Image(Left Arrow)  - tk.Button, tk.PhotoImage, HoverInfo
        self.img_leftArrow = self.imgICONS.get_img_leftArrow()
        self.button_leftIMAGE = tk.Button( self.root, image=self.img_leftArrow, command=self.previousIndex )
        self.button_leftIMAGE.place( relx=0.84, rely=0.88 )
        self.hover_leftIMAGE = HoverInfo( self.root, self.button_leftIMAGE, 'View previous image' )
        # Image(Right Arrow) - tk.Button, tk.PhotoImage, HoverInfo
        self.img_rightArrow = self.imgICONS.get_img_rightArrow()
        self.button_rightIMAGE = tk.Button( self.root, image=self.img_rightArrow, command=self.nextIndex )
        self.button_rightIMAGE.place( relx=0.9, rely=0.88 )
        self.hover_rightIMAGE = HoverInfo( self.root, self.button_rightIMAGE, 'View next image' )
        # Keyboard event binding for main tk.Tk window.
        self.root.bind( "x", self.addBoxSize )   
        self.root.bind( "s", self.minusBoxSize )
        # END of '__init__()' FUNCTION.
    def configOK(self):
        self.imageFrame.SIZE  = self.userInputSIZE.get()
        self.imageFrame.CLASS = self.userInputCLASS.get()
        self.imageFrame.INDEX = self.userInputINDEX.get()
        self.root.focus_set()
        if( debugMode==True ):
            print( 'SIZE:%d, CLASS:%s, INDEX:%d \n'
                    %(self.imageFrame.SIZE, self.imageFrame.CLASS, self.imageFrame.INDEX) )
            # if.. - End
    def __openImg( self ):
        self.filename = filedialog.askopenfilename()
        if( self.filename!='' ):
            debug.set_fileNamePath( self.filename )
            self.imageFrame.addImg( self.filename )
            self.imageFrame.loadedFolder = False
            # if.. - End
        if( debugMode==True and self.filename=='' ):
            priint( 'Empty Image Path!' )
        elif( debugMode==True ):
            print( 'self.filename:', self.filename )
            # if..elif.. - End
        # END of '__openImg()' FUNCTION.
    def __openFolder( self ):
        self.directory = filedialog.askdirectory()
        if( self.directory!='' ):
            self.pathsList =  setFolderPath( self.directory )
            debug.set_folderNamePath( self.directory )
            debug.set_folderImgList( self.pathsList )
            self.imageFrame.imgsIndex = 0
            self.imageFrame.addImgs( self.pathsList )
            self.imageFrame.loadedFolder = True
            # if.. - End
        if( debugMode==True and self.filename=='' ):
            priint( 'Empty Image Directory!' )
        elif( debugMode==True ):
            print( 'self.directory:', self.directory )
            # if..elif.. - End
        # END of '__openFolder()' FUNCTION.
    def nextIndex( self ):
        if( self.imageFrame.loadedFolder==True ):
            self.imageFrame.imgsIndex = self.imageFrame.imgsIndex + 1
            self.imageFrame.addImgs( self.imageFrame.imgPaths )
        else:
            pass
            # if.. - End
        # END of 'nextIndex()' - Function.
    def previousIndex( self ):
        if( self.imageFrame.loadedFolder==True ):
            self.imageFrame.imgsIndex = self.imageFrame.imgsIndex - 1
            self.imageFrame.addImgs( self.imageFrame.imgPaths )
        else:
            pass
            # if.. - End
        # END of 'previousIndex()' - Function.
    def addBoxSize( self, event ):
        self.userInputSIZE.set( self.imageFrame.SIZE+1 )
        self.imageFrame.SIZE = self.userInputSIZE.get()
        # END of 'addBoxSize()' - Function.
    def minusBoxSize( self, event ):
        if( self.imageFrame.SIZE<=1 ):
            self.userInputSIZE.set( 1 )
        else:
            self.userInputSIZE.set( self.imageFrame.SIZE-1 )
            self.imageFrame.SIZE = self.userInputSIZE.get()
            # if..else.. - End
        # END of 'minusBoxSize()' - Function.
    # END of 'FunctionMenu()' CLASS. 


class ImageFrame(tk.Frame):
    global debugMode;
    def __init__(self, parent):
        tk.Frame.__init__( self, parent )
        self.configure( highlightbackground='black', highlightthickness=1, borderwidth=1 )
        self.place( relx=0.02, rely=0.02, relheight=0.84, relwidth=0.95 )
        self.root = parent
        self.INDEX        : int=0      # INDEX: A number for saving roi image.
        self.SIZE         : int=1      # SIZE: roi(rectangle) size.
        self.CLASS        : str=''     # CLASS: Image class name.
        self.imgsIndex    : int=0      # imgsIndex: Index of images list.
        self.imgPaths     : list=[]    # imgPaths: User chosen.
        self.loadedFolder : bool=False # loadedFolder: Folder be loaded.
        # Create scroll canvas.
        self.canvas = tk.Canvas( self, width=4000, height=4000, background=None )
        self.roiBox = self.canvas.create_rectangle( 0,0,1,1, width=2, outline='red' )
        self.xsb = tk.Scrollbar( self, orient="horizontal", command=self.canvas.xview )
        self.ysb = tk.Scrollbar( self, orient="vertical", command=self.canvas.yview )
        self.canvas.configure( yscrollcommand=self.ysb.set, xscrollcommand=self.xsb.set )
        self.canvas.configure( scrollregion=(0,0,6000,6000) )
        self.xsb.grid( row=1, column=0, sticky="ew" )
        self.ysb.grid( row=0, column=1, sticky="ns" )
        self.canvas.place( x=0, y=0 )
        self.grid_rowconfigure( 0, weight=1 )
        self.grid_columnconfigure( 0, weight=1 )       
        # File Path - tk.Label. Using: tk.Label.configure(  text='Updata' ) to updata text configure.
        self.label_Path = tk.Label( self.root, text='File Path', foreground='black', background="white" )
        self.label_Path.place( rely=0.96, relwidth=1 )
        # Enables scrolling canvas with the mouse event.
        self.canvas.bind( "<ButtonPress-1>", self.scroll_start )
        self.canvas.bind( "<B1-Motion>", self.scroll_move )
        self.canvas.bind( '<Motion>', self.mouseMove )
        self.canvas.bind( '<Double-ButtonPress-1>', self.saveROI )
        # Keyboard event binding for main tk.Tk window.
        self.root.bind( "z", self.nextIndex )
        self.root.bind( "a", self.previousIndex )
        # END of '__init__()' FUNCTION.
    def scroll_start(self, event):
        # Sets the scanning anchor.
        self.canvas.scan_mark(event.x, event.y)
        # END of 'scroll_start()' - Function
    def scroll_move(self, event):
        # Scrolls the widget contents relative to the scanning anchor. 
        self.canvas.scan_dragto(event.x, event.y, gain=1)
    def mouseMove( self, event ):
        # Get the current coordinates of mouse at tk.Canvas. 
        self.x, self.y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        # Calculate a LeftUpCorner and a RightDownCorner for ROI size.
        self.roiPosX0 = int( self.x - self.SIZE*0.5 )
        self.roiPosY0 = int( self.y - self.SIZE*0.5 )
        self.roiPosX1 = int( self.x + math.ceil(self.SIZE*0.5) )
        self.roiPosY1 = int( self.y + math.ceil(self.SIZE*0.5) )
        # Returns(moves) the coordinates for an item(tk.Canvas Object).
        self.canvas.coords( self.roiBox, self.roiPosX0, self.roiPosY0, self.roiPosX1, self.roiPosY1 )
        if( debugMode==True ):
            print( 'LeftUpCorner:(%d, %d)' %(self.roiPosX0, self.roiPosY0),
                   'RightDownCorner:(%d, %d)' %(self.roiPosX1, self.roiPosY1) )
            # if.. - End
        # END of 'mouseMove()' - Function
    def addImg( self, strImgPath ):
        self.imgPath = strImgPath
        # Create an image container
        self.img = ImgContainer( self.imgPath )
        self.imgTK = cvMat2tkBitmap( self.img.get_ndarray() )
        self.canvas_Img = self.canvas.create_image( 0, 0, image=self.imgTK, anchor='nw' )
        self.canvas.tag_raise( self.roiBox )  # Moving 'self.roiBox' item to top level at 'self.canvas'
        # Update label text
        self.label_Path.configure( text='File Path: ' + strImgPath )
        # Update tk.Canvas congigure
        self.canvas.update()
        self.canvas.itemconfigure( self.canvas_Img )
        #self.root.focus_set()
        if( debugMode==True ):
            print( self.imgsIndex )
            # if.. - End
        # END of 'addImg()' - Function.
    def addImgs( self, strImgPaths ):
        self.imgPaths = strImgPaths
        N = len( strImgPaths )
        if( self.imgsIndex<0 ):
            self.imgsIndex = 0
            # if.. - End
        if( self.imgsIndex>N-1 ):
            self.imgsIndex = N-1
            # if.. - End
        self.addImg( self.imgPaths[self.imgsIndex] )
        # END of 'mouseMove()' - Function.
    def saveROI( self, event ):
        if( self.CLASS=='' ):
            self.label_Path.configure( text="Please click 'OK' Button, and set a configure first!!" )
        else:
            self.label_Path.configure( text='File Path: ' + self.imgPath )
            self.img.saveROI( self.roiPosX0, self.roiPosY0, self.roiPosX1, self.roiPosY1, self.CLASS, self.INDEX )
            self.canvas.create_rectangle( self.roiPosX0, self.roiPosY0, self.roiPosX1, self.roiPosY1, width=2, outline='red' )
            self.INDEX = self.INDEX + 1
            # if..else.. - End
        # END of 'saveROI()' - Function.
    def nextIndex( self, event ):
        if( self.loadedFolder==True ):
            self.imgsIndex = self.imgsIndex + 1
            self.addImgs( self.imgPaths )
        else:
            pass
            # if.. - End
        # END of 'nextIndex()' - Function.
    def previousIndex( self, event ):
        if( self.loadedFolder==True ):
            self.imgsIndex = self.imgsIndex - 1
            self.addImgs( self.imgPaths )
        else:
            pass
            # if.. - End
        # END of 'previousIndex()' - Function.
    def __del__(self):
        pass
        # END of '__del__()' FUNCTION. 
    # END of 'ImageFrame()' CLASS.


class Menubar(tk.Menu):
    global debugMode;
    def __init__( self, parent ):
        tk.Menu.__init__( self, parent )
        self.root = parent
        #self.imageFrame = ImageFrame( self.root )
        self.functionMenu = FunctionMenu( self.root )
        self.fileMenu = tk.Menu( self, tearoff=False )      # Create a tk-Menu which named 'fileMenu'.
        self.fileMenu_Open = tk.Menu( self, tearoff=False ) # Create a tk-Menu which named 'fileMenu_Open'.
        self.aboutMenu = tk.Menu( self, tearoff=False )     # Create a tk-Menu which named 'aboutMenu'.
        # Add 'File' menu as a header menubar
        self.add_cascade( label='File', underline=0, menu=self.fileMenu )
        # Add 'fileMenu_Open' Sub-Meun in 'fileMenu'.
        self.fileMenu.add_cascade( label='Open', underline=1, menu=self.fileMenu_Open )
        self.fileMenu_Open.add_cascade( label='Load An Image', underline=1, command=self.__openImg )
        self.fileMenu_Open.add_cascade( label='Load A Folder', underline=1, command=self.__openFolder )
        self.fileMenu.add_cascade( label='Exit', underline=1, command=self.__quit )
        # Add 'Help' menu as a header menubar
        self.add_cascade( label='Help', underline=0, menu=self.aboutMenu )
        self.aboutMenu.add_cascade( label='About', underline=1, command=self.__about )
        # END of '__init__()' FUNCTION.
    def __openImg( self ):
        self.filename = filedialog.askopenfilename()
        if( self.filename!='' ):
            debug.set_fileNamePath( self.filename )
            self.functionMenu.imageFrame.loadedFolder = False
            self.functionMenu.imageFrame.addImg( self.filename )
            # if.. - End
        if( debugMode==True and self.filename=='' ):
            priint( 'Empty Image Path!' )
        elif( debugMode==True ):
            print( 'self.filename:', self.filename )
            # if..elif.. - End
        # END of '__openImg()' FUNCTION.
    def __openFolder( self ):
        self.directory = filedialog.askdirectory()
        if( self.directory!='' ):
            self.pathsList =  setFolderPath( self.directory )
            debug.set_folderNamePath( self.directory )
            debug.set_folderImgList( self.pathsList )
            self.functionMenu.imageFrame.imgsIndex = 0
            self.functionMenu.imageFrame.loadedFolder = True
            self.functionMenu.imageFrame.addImgs( self.pathsList )
            # if.. - End
        if( debugMode==True and self.filename=='' ):
            priint( 'Empty Image Directory!' )
        elif( debugMode==True ):
            print( 'self.directory:', self.directory )
            # if..elif.. - End
        # END of '__openFolder()' FUNCTION.
    def __quit( self ):
        sys.exit(0)
        # END of '__quit()' FUNCTION.
    def __about( self ):
        pass
        # END of '__about()' FUNCTION.
    def __del__( self ):
        pass
        # END of '__del__()' FUNCTION. 
    # END of 'Menubar()' CLASS.


def cvMat2tkBitmap( img ):
    global debugMode
    __img = cv2.cvtColor( img, cv2.COLOR_BGR2RGB )
    __img = Image.fromarray( __img )
    __imgtk = ImageTk.PhotoImage( image=__img )
    if( debugMode==True ):
        print( "In 'cvMat2tkBitmap()' function: " )
        print( ">>> The type of image:", type(__imgtk) )
        # if.. - End
    return __imgtk
    # END of 'cvMat2tkBitmap()' FUNCTION.


class ImgContainer(object):
    global debugMode;
    def __init__( self, imgPath ):
        self.image = cv2.imread( imgPath )
        self.scriptDir = os.path.dirname( os.path.abspath(__file__) )
        # END of '__init__()' FUNCTION.
    def get_ndarray( self ):
        return self.image
        # END of 'get_ndarray()' FUNCTION.
    def saveROI( self, posX0, posY0, posX1, posY1, className, savingIndex ):
        self.savingPath = os.path.join( self.scriptDir, 'Output', className, str(savingIndex)+'.png' ) 
        cv2.imwrite( self.savingPath, self.image[ posY0:posY1, posX0:posX1 ], [cv2.IMWRITE_PNG_COMPRESSION, 0] )
        if( debugMode==True ):
            print( 'self.savingPath:', self.savingPath )
            # if.. - End
        # END of 'saveROI()' FUNCTION.
    def __del__( self ):
        pass
        # END of '__del__()' FUNCTION.
    # END of 'ImgContainer()' CLASS.


class Icons(object):
    global debugMode;
    def __init__( self ):
        self.scriptDir = os.path.dirname( os.path.abspath(__file__) )
        # END of '__init__()' FUNCTION.
    def get_img_aFolder( self ):
        """Make icon's path and create an tk.PhotoImage
        Args:
            None
        Returns:
            tk.PhotoImage()
        """
        self.iconFolderPath = os.path.join( self.scriptDir, 'Configure', 'icons', 'FOLDER.png' )
        self.img_aFolder = tk.PhotoImage( file = self.iconFolderPath )
        return self.img_aFolder
        # END of 'get_img_aFolder()' FUNCTION.
    def get_img_aImage( self ):
        """Make icon's path and create an tk.PhotoImage
        Args:
            None
        Returns:
            tk.PhotoImage()
        """
        self.iconImagePath = os.path.join( self.scriptDir, 'Configure', 'icons', 'IMAGE.png' )
        self.img_aImage = tk.PhotoImage( file = self.iconImagePath )
        return self.img_aImage
        # END of 'get_img_aImage()' FUNCTION.
    def get_img_rightArrow( self ):
        """Make icon's path and create an tk.PhotoImage
        Args:
            None
        Returns:
            tk.PhotoImage()
        """
        self.iconRightArrowPath = os.path.join( self.scriptDir, 'Configure', 'icons', 'RIGHT_ARROW.png' )
        self.img_rightArrow = tk.PhotoImage( file = self.iconRightArrowPath )
        return self.img_rightArrow
        # END of 'get_img_rightArrow()' FUNCTION.
    def get_img_leftArrow( self ):
        """Make icon's path and create an tk.PhotoImage
        Args:
            None
        Returns:
            tk.PhotoImage()
        """
        self.iconLeftArrowPath = os.path.join( self.scriptDir, 'Configure', 'icons', 'LEFT_ARROW.png' )
        self.img_leftArrow = tk.PhotoImage( file = self.iconLeftArrowPath )
        return self.img_leftArrow
        # END of 'get_img_leftArrow()' FUNCTION.
    def __del__( self ):
        pass
        # END of '__del__()' FUNCTION.
    # END of 'Icons()' CLASS.


def setFolderPath( strFolderPath ):
    global debugMode;
    """Pick all image files in list object.
    Args:
        strFolderPath (string): path to a folder
    Returns:
        list: all image paths in a folder
    """
    __images = [ ]
    for root, _, fnames in sorted( os.walk(strFolderPath) ):
        fnames.sort()
        for fname in fnames:
            if has_file_allowed_extension(fname):
                path = os.path.join(root, fname)
                __images.append( path )
    
    if( debugMode==True ):
        print( 'root:', root )
        print( 'fnames:', fnames )
        print( 'folderImgList:', __images )
    return __images
    # END of 'setFolderPath()' FUNCTION.


def has_file_allowed_extension(filename):
    global debugMode, IMG_EXTENSIONS;
    """Checks if a file is an allowed extension.
    Args:
        filename (string): path to a file
        extensions (iterable of strings): extensions to consider (lowercase)
    Returns:
        bool: True if the filename ends with one of given extensions
    """
    filename_lower = filename.lower()
    return any(filename_lower.endswith(ext) for ext in IMG_EXTENSIONS)
    # END of 'has_file_allowed_extension()' FUNCTION.


def is_image_file(filename):
    global IMG_EXTENSIONS;
    """Checks if a file is an allowed image extension(IMG_EXTENSIONS).
    Args:
        filename (string): path to a file
    Returns:
        bool: True if the filename ends with a known image extension
    """
    return has_file_allowed_extension(filename, IMG_EXTENSIONS)
    # END of 'is_image_file()' FUNCTION.


class LoadTxt(object):
    def __init__(self):
        self.txtPath = self.makeTxtPath()
        self.txtFile = open( self.txtPath, 'r+' )
        # END of '__init__()' FUNCTION.
    def makeTxtPath( self ):
        """Make a path of classes.txt at Configure folder which folder must at the same folder as toiPicker.py .
        Args:
            None
        Returns:
            classesList (list): All classes in txt-file(depend on a line).
        """
        self.filePath = os.path.dirname( os.path.abspath(__file__) )
        self.classesTxt_Path = os.path.join( self.filePath, 'Configure', 'classes.txt' )
        return self.classesTxt_Path
        # END of 'makeTxtPath()' FUNCTION.
    def getAllClasses( self ):
        """Get all classes in classes.txt at Configure folder.
        Args:
            None
        Returns:
            classesList (list): All classes in txt-file(depend on a line).
        """
        self.classesList = [ (line.strip('\n')) for line in self.txtFile.readlines() ]
        return self.classesList
        # END of 'getAllClasses()' FUNCTION.
    def __del__( self ):
        self.txtFile.close()
        pass
        # END of '__del__()' FUNCTION.


class HoverInfo(tk.Menu):
    def __init__( self, superParent, parent, text, command=None ):
        self._com = command
        self.root = superParent
        self.btn = parent
        tk.Menu.__init__( self, parent, tearoff=0 )
        if( not isinstance(text, str) ):
            raise TypeError( 'Trying to initialise a Hover Menu with a non string type: ' + text.__class__.__name__ )
            # if.. - End
        self.toktext = re.split( '\n', text )
        for t in self.toktext:
            self.add_command( label=t )
            # for - End
        self._displayed = False
        self.btn.bind( "<Enter>", self.Display )
        self.btn.bind( "<Leave>", self.Remove )
        self.entryconfigure( 0, state='disabled' )
        # END of '__init__()' FUNCTION.
    def Display( self,event ):
        if( not self._displayed ):
            self._displayed = True
            self.post( event.x_root+15, event.y_root+15) 
            # if.. - End
        if( self._com != None ):
            self.btn.unbind_all( "<Return>" )
            self.btn.bind_all( "<Return>" )
            # if.. - End
        # END of 'Display()' TK BINDING FUNCTION.
    def Remove( self, event ):
        self.unpost()
        if( self._displayed ):
            self._displayed=False
            self.unpost()
            # if.. - End
        if( self._com != None ):
            self.unbind_all( "<Return>" )
            # if.. - End
        # END of 'Remove()' TK BINDING FUNCTION.
    def Click( self, event ):
        self._com()
        # END of 'Click()' FUNCTION.
    def __del__( self ):
        pass
        # END of '__del__()' FUNCTION.




###########################################################################################
#### __________________________________MAIN FUNCTION__________________________________ ####
if __name__ == "__main__":
    debugMode = False
    # Create Debug object
    debug = Debug()
    debug.osCheck()
    # Create MainTk(window) object
    root = MainTk()
    root.start()
    # if.. - End
#### _______________________________END OF MAIN FUNCTION_______________________________####
###########################################################################################



