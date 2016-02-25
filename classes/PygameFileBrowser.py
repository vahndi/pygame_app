from fileFunctions import getParentPath, getFileNames, getFolderNames
import pygame
import os


letters = map(chr, range(97, 123))
numbers = map(chr, range(48, 58))
lettersAndNumbers = letters + numbers
punctuationKeys = (pygame.K_SPACE, pygame.K_PERIOD, pygame.K_COMMA, pygame.K_MINUS, pygame.K_KP_MINUS, pygame.K_UNDERSCORE)



class PygameFileBrowser(object):
    
    
    def __init__(self, path, printSurface):
        
        self._path = path
        self._browsing = False
        self._printSurface = printSurface
        self._matchString = ''


    def _getMatchingFoldersAndFiles(self, path):
        
        folders =  [f for f in getFolderNames(path, orderAlphabetically = True) if f.lower().startswith(self._matchString.lower())]
        files = [f for f in getFileNames(path, orderAlphabetically = True) if f.lower().startswith(self._matchString.lower())]
        return folders, files
    
    
    def handleEvent(self, event):
        
        keyName = pygame.key.name(event.key).lower()
        
        if event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
            self._browsing = False
        elif event.key == pygame.K_LEFT:
            self._path = getParentPath(self._path)
            self._matchString = ''
        elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
            folders, files = self._getMatchingFoldersAndFiles(self._path)
            if folders:
                self._path = os.path.join(self._path, folders[0])
            elif files:
                self._path = os.path.join(self._path, files[0])
            self._matchString = ''
        elif event.key == pygame.K_BACKSPACE:
            self._matchString = self._matchString[:-1]
        elif keyName in lettersAndNumbers or event.key in punctuationKeys:
            if keyName in lettersAndNumbers:
                self._matchString += keyName
            elif event.key == pygame.K_SPACE:
                self._matchString += ' '
            elif event.key == pygame.K_PERIOD:
                self._matchString += '.'
            elif event.key in (pygame.K_KP_MINUS, pygame.K_MINUS):
                self._matchString += '-'
        
        return self._path

    
    def getPath(self):
        
        return self._path

        
    def getSelectedFile(self):
        
        if os.path.isfile(self._path):
            return self._path
        else:
            return None


    def reset(self, path = None):
        
        if path is not None:
            self._path = path
        elif os.path.isfile(self._path):
            self._path = getParentPath(self._path)
        self._matchString = ''
    
    
    def _renderText(self, text, size = 12, location = (100, 100)):
        
        pygame.font.init()
        default_font = pygame.font.get_default_font()
        font_renderer = pygame.font.Font(default_font, size)
        label = font_renderer.render(text, 1,(255,255,255))
        self._printSurface.blit(label, location)
        
        
    def printPath(self):
    
        self._renderText(self._path, size = 16, location = (10, 10))
        if os.path.isdir(self._path):
            folders, files = self._getMatchingFoldersAndFiles(self._path)
            # print folders in directory
            yFolder = 25
            for folder in folders:
                self._renderText(folder, size = 14, location = (20, yFolder))
                yFolder += 15
            # print files in directory
            yFile = 25
            for fn in files:
                self._renderText(fn, size = 14, location = (300, yFile))
                yFile += 15
            # print path to browse
            yMatch = max(yFolder, yFile) + 15
            self._renderText(self._matchString, size = 16, location = (10, yMatch))
        