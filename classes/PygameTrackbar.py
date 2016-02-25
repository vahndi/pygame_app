import pygame as pg
from PygameColours import grey, dark_grey, white, black
from PygameShapes import PygameRectangle
from PygameLogic import isMouseOver, getMouseX



class PygameTrackbar(object):
    
    
    def __init__(self, surface, origin, width, 
                 minValue = 0, maxValue = 100, numValues = 101, initValue = 0,
                 valueChangingFunction = None, valueChangedFunction = None,
                 trackDimension = 10, barSmallDimension = 10, barLargeDimension = 30,
                 trackOutlineColour = dark_grey, trackFillColour = grey, barOutlineColour = grey, barFillColour = white):
        
        self._surface = surface
        self._origin = origin
        self._width = width
        self._minValue = minValue
        self._maxValue = maxValue
        self._numValues = numValues
        self._initValue = initValue
        self._currentValue = initValue
        self._valueChangingFunction = valueChangingFunction
        self._valueChangedFunction = valueChangedFunction
        self._trackDimension = trackDimension
        self._barSmallDimension = barSmallDimension
        self._barLargeDimension = barLargeDimension
        self._trackOutlineColour = trackOutlineColour
        self._trackFillColour = trackFillColour
        self._barOutlineColour = barOutlineColour
        self._barFillColour = barFillColour
        
        self._updateRectangle()
    
        # State properties
        self._isDragging = False
    
    def _updateRectangle(self):
        
        self._rectangle = PygameRectangle(self._origin[0], self._origin[1], self._width, self._barLargeDimension)
    
    def setOrigin(self, origin):
        
        self._origin = origin
        self._updateRectangle()
    
    def setWidth(self, width):
        
        self._width = width
        self._updateRectangle()
    
    def setCurrentValue(self, toValue):
        
        self._currentValue = toValue
    
    def getHeight(self):
        
        return self._rectangle.getHeight()


    def _getIndexFromMouseX(self):
        '''
        N.B. x is relative to the origin
        '''
        mouseX = getMouseX()
        mouseXtrack = mouseX - self._origin[0]
        index = round(self._numValues * mouseXtrack / self._width)
        index = min(max(index, self._minValue), self._maxValue)
        return index
        

        

    def handleMouseButtonDown(self, event):
        
        if isMouseOver(self._rectangle):
            
            self._currentValue = self._getIndexFromMouseX()
            self._valueChangingFunction(self._currentValue)
            self._isDragging = True


    def handleMouseMotion(self, event):

        if pg.mouse.get_pressed()[0] and self._isDragging:
            self._currentValue = self._getIndexFromMouseX()
            self._valueChangingFunction(self._currentValue)


    def handleMouseButtonUp(self, event):
        
        if self._isDragging:
            self._isDragging = False
            self._currentValue = self._getIndexFromMouseX()
            self._valueChangedFunction(self._currentValue)
    

    def draw(self):

        # Clear the rectangle
        pg.draw.rect(self._surface, black, self._rectangle.getTuple(), 0)

        # Draw the track
        trackRect = (self._origin[0], 
                     self._origin[1] + self._barLargeDimension / 2 - self._trackDimension / 2, 
                     self._width, 
                     self._trackDimension)
        pg.draw.rect(self._surface, self._trackFillColour, trackRect, 0)
        pg.draw.rect(self._surface, self._trackOutlineColour, trackRect, 1)
        
        # Draw the bar
        barRect = (self._origin[0] + self._width 
                                       * (self._currentValue - self._minValue) / (self._maxValue - self._minValue)
                                   - self._barSmallDimension / 2,
                   self._origin[1],
                   self._barSmallDimension,
                   self._barLargeDimension)
        pg.draw.rect(self._surface, self._barFillColour, barRect, 0)
        pg.draw.rect(self._surface, self._barOutlineColour, barRect, 1)