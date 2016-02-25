import cv2
import pygame as pg

from PygameLogic import pointOnOrInRectangle
from PygameColours import red
from PygameShapes import PygameRectangle



class PygameScreenArea:


    def __init__(self, surface, rectangle, canAddRectangle = True):
        '''
        Arguments:
            :surface: the surface to display any rectangle objects on
            :rectangle: the location of the screen area within the pygame surface
        '''
        self._surface = surface
        self._rectangle = rectangle
        self._image = None
        
        self._canAddRectangle = canAddRectangle
        self._rectanglePoint1 = None
        self._rectanglePoint2 = None
        

    # Size getters and setters
    def getSize(self):
        return (self._rectangle[2], self._rectangle[3])
    def setSize(self, size):
        self._rectangle[2] = size[0]
        self._rectangle[3] = size[1]
    def getWidth(self):
        return self._rectangle[2]
    def setWidth(self, width):
        self._rectangle[2] = width
    def getHeight(self):
        return self._rectangle[3]
    def setHeight(self, height):
        self._rectangle[3] = height
    
    # Origin getters and setters
    def getOrigin(self):
        return (self._rectangle[0], self._rectangle[1])
    def setOrigin(self, origin):
        self._rectangle[0] = origin[0]
        self._rectangle[1] = origin[1]
    def getLeft(self):
        return self._rectangle[0]
    def setLeft(self, left):
        self._rectangle[0] = left
    def getTop(self):
        return self._rectangle[1]
    def setTop(self, top):
        self._rectangle[1] = top
    def getRight(self):
        return self.getLeft() + self.getWidth()
    def setRight(self, right):
        self.setWidth(right - self.getLeft())
    def getBottom(self):
        return self.getTop() + self.getHeight()
    def setBottom(self, bottom):
        self.setHeight(bottom - self.getTop())
    

    def setOpenCvImage(self, openCvImage):
        '''
        Displays an OpenCvImage in the screen area
        '''
        self._openCvImage = openCvImage
        self.setSize(openCvImage.getSize())
        if openCvImage.isColour():
            captureConversionType = cv2.COLOR_BGR2RGB
        else:
            captureConversionType = cv2.COLOR_GRAY2RGB
        rgbFrame = cv2.cvtColor(openCvImage.image(), captureConversionType)
        self._image = pg.image.frombuffer(rgbFrame.tostring(), openCvImage.shape(), 'RGB')

    def getOpenCvImage(self):
        
        return self._openCvImage
  
    def draw(self):
        
        if self._image:
            self._surface.blit(self._image, self.getOrigin())
            rect = self.getRectangle()
            if rect:
                pg.draw.rect(self._surface, red, rect.offsetBy(self.getOrigin()).getTuple(), 1)


    def hasRectangle(self):
        
        if self._rectanglePoint1 is None:
            return False
        if self._rectanglePoint2 is None:
            return False
        if self._rectanglePoint1 == self._rectanglePoint2:
            return False
        return True


    def getRectangle(self):
        
        if self.hasRectangle():
            return PygameRectangle.fromPoints(self._rectanglePoint1, 
                                              self._rectanglePoint2)
        return None
        
                                        
    def getRectangleTuple(self):
        
        rect = self.getRectangle()
        if rect:
            return rect.getTuple()
        else:
            return None


    def reset(self):
        
        self._image = None
        self.setSize((0, 0))
        self._rectanglePoint1 = None
        self._rectanglePoint2 = None
        

    def isMouseOver(self):
        '''
        Return True if the mouse cursor is over the button
        '''
        cur = pg.mouse.get_pos()
        return pointOnOrInRectangle(cur, self._rectangle)


    def handleMouseButtonUp(self, event):
        
        if not self.isMouseOver():
            return False
        
        cur =  pg.mouse.get_pos()
        self._rectanglePoint2 = (cur[0] - self.getLeft(), 
                                 cur[1] - self.getTop())


    def handleMouseButtonDown(self, event):
        
        if not self.isMouseOver():
            return False
        
        cur =  pg.mouse.get_pos()
        # Start rectangle
        if pg.mouse.get_pressed()[0]:
            self._rectanglePoint1 = (cur[0] - self.getLeft(), 
                                     cur[1] - self.getTop())
            self._rectanglePoint2 = self._rectanglePoint1
        # Cancel rectangle
        elif pg.mouse.get_pressed()[2]:
            self._rectanglePoint1 = None
            self._rectanglePoint2 = None

        
    def handleMouseMotion(self, event):
        
        if not self.isMouseOver():
            return False
        if pg.mouse.get_pressed()[0] == 1:
            cur =  pg.mouse.get_pos()
            self._rectanglePoint2 = (cur[0] - self.getLeft(), 
                                     cur[1] - self.getTop())
    
    
    def handleKeyPress(self, event):
        
        if self.isMouseOver() and self.hasRectangle():
            
            offsetSize = 1
            if pg.key.get_mods() & pg.KMOD_SHIFT:
                offsetSize = 5

            rect = PygameRectangle.fromPoints(self._rectanglePoint1,
                                              self._rectanglePoint2)

            if not pg.key.get_mods() & pg.KMOD_ALT:
                if event.key == pg.K_LEFT:
                    rect.moveLeftEdge(-offsetSize, 0)
                elif event.key == pg.K_RIGHT:
                    rect.moveRightEdge(offsetSize, self.getWidth())
                elif event.key == pg.K_UP:
                    rect.moveTopEdge(-offsetSize, 0)
                elif event.key == pg.K_DOWN:
                    rect.moveBottomEdge(offsetSize, self.getHeight())
            else:                
                if event.key == pg.K_LEFT:
                    rect.moveRightEdge(-offsetSize)
                elif event.key == pg.K_RIGHT:
                    rect.moveLeftEdge(offsetSize)
                elif event.key == pg.K_UP:
                    rect.moveBottomEdge(-offsetSize)
                elif event.key == pg.K_DOWN:
                    rect.moveTopEdge(offsetSize)

            self._rectanglePoint1, self._rectanglePoint2 = rect.getCornerPoints()                

                