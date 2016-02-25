import pygame as pg
from pygame.locals import RESIZABLE


class PygameApplication(object):
    '''
    A Pygame application shell
    '''
    def __init__(self, appTitle, mode = (800, 600)):
        '''
        Arguments:
            :appTitle: Title of the application
            :mode: The size of the application
        '''
        pg.init()
        self._appDisplay = pg.display.set_mode(mode, RESIZABLE)
        pg.display.set_caption(appTitle)
        self._isClosed = False
        self._keypressHandlerSets = []
        self._buttonSets = []
        self._screenAreas = []
        self._trackBars = []

    def run(self):
        
        while self._isClosed == False:
            
            # Handle ui events
            events = pg.event.get()
            for event in events:
                self.handleEvent(event)
        
            self.drawScreen() 
            pg.display.flip()
        
        # Quit pygame and release captures
        pg.quit()
        self.cleanUp()

    
    def drawScreen(self):
        '''
        Override this method to do anything necessary to update the game screen,
        including drawing controls
        '''
        pass


    def cleanUp(self):
        '''
        Override this method to do anything necessary to clean up after pygame has exited
        '''
        pass
    

    def handleEvent(self, event):
        
        if event.type == pg.QUIT:
            self.close()
            
        elif event.type == pg.KEYDOWN:
             
            for handlerSet in self._keypressHandlerSets:                 
                 handlerSet.handleEvent(event)
                 
            for screenArea in self._screenAreas:
                screenArea.handleKeyPress(event)   
        
        elif event.type == pg.MOUSEBUTTONUP:
            
            for buttonSet in self._buttonSets:
                buttonSet.sendMouseButton(event)
            
            for screenArea in self._screenAreas:
                screenArea.handleMouseButtonUp(event)
            
            for trackBar in self._trackBars:
                trackBar.handleMouseButtonUp(event)
                
        elif event.type == pg.MOUSEBUTTONDOWN:
            
            for screenArea in self._screenAreas:
                screenArea.handleMouseButtonDown(event)
            for trackBar in self._trackBars:
                trackBar.handleMouseButtonDown(event)
                
            
        elif event.type == pg.MOUSEMOTION:
            
            for screenArea in self._screenAreas:
                screenArea.handleMouseMotion(event)
            for trackBar in self._trackBars:
                trackBar.handleMouseMotion(event)
    
    
    def close(self):
        
        self._isClosed = True
        
