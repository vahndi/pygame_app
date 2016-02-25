# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 00:24:30 2015

@author: vahndi
"""

from PygameColours import white, black, grey, dark_grey, light_grey
import pygame
from PygameLogic import pointOnOrInRectangle

pygame.font.init()



class PygameButton(object):
    
    def __init__(self, surface, rectangle, 
                 text, fontSize = 12, textColour = black, 
                 upColour = grey, downColour = dark_grey, mouseOverColour = light_grey,
                 buttonName = None):
        
        self._surface = surface
        self._rectangle = rectangle
        
        self._text = text
        self._textColour = textColour
        default_font = pygame.font.get_default_font()
        self._fontRenderer = pygame.font.Font(default_font, fontSize)
        
        self._upColour = upColour
        self._downColour = downColour
        self._mouseOverColour = mouseOverColour
        
        self._buttonName = buttonName
        
    
    def setRectangle(self, rectangle):
        
        self._rectangle = rectangle
        
    
    def getButtonName(self):
        
        return self._buttonName
        
        
    def getDrawColour(self):
        
        return white


    def isMouseOver(self):
        '''
        Return True if the mouse cursor is over the button
        '''
        cur = pygame.mouse.get_pos()
        return pointOnOrInRectangle(cur, self._rectangle)
        
        
    def draw(self):
        '''
        Draw the button in its current up or down state
        '''
        colour = self.getDrawColour()

        # draw the button rectangle
        pygame.draw.rect(self._surface, colour, self._rectangle, 0)
        
        #render the button text
        textSurface =  self._fontRenderer.render(self._text, True, self._textColour)
        textRect = textSurface.get_rect()
        textRect.center = (self._rectangle[0] + self._rectangle[2] / 2, self._rectangle[1] + self._rectangle[3] / 2)
        self._surface.blit(textSurface, textRect)



class PygamePushButton(PygameButton):
    
    
    def __init__(self, surface, rectangle, text, 
                 clickedFunction = None, 
                 fontSize = 12, textColour = black, 
                 upColour = grey, downColour = dark_grey, mouseOverColour = light_grey,
                 buttonName = None):
        
        super(PygamePushButton, self).__init__(surface, rectangle, 
                                               text, fontSize, textColour,
                                               upColour, downColour, mouseOverColour,
                                               buttonName)
        
        self._clickedFunction = clickedFunction


    def getDrawColour(self):
        
        if self.isMouseOver():
            colour = self._mouseOverColour
            if pygame.mouse.get_pressed()[0] == 1:
                colour = self._downColour
        else:
            colour = self._upColour
        
        return colour

    
    def invokeClicked(self):
        
        if self._clickedFunction is not None:
            self._clickedFunction()



class PygameOptionButton(PygameButton):
    
    
    def __init__(self, surface, rectangle, isSelected, text, 
                 toggleFunction = None, downFunction = None, upFunction = None, 
                 fontSize = 12, textColour = black, 
                 upColour = grey, downColour = dark_grey, mouseOverColour = light_grey,
                 buttonName = None):
                     
        super(PygameOptionButton, self).__init__(surface, rectangle, 
                                                 text, fontSize, textColour,
                                                 upColour, downColour, mouseOverColour,
                                                 buttonName)
        
        self._isSelected = isSelected

        self._toggleFunction = toggleFunction
        self._downFunction = downFunction
        self._upFunction = upFunction
        

    def getDrawColour(self):
        
        if self._isSelected:
            colour = self._downColour
        else:
            colour = self._upColour
            
        if self.isMouseOver():
            colour = self._mouseOverColour
        
        return colour
    
    
    def isSelected(self):
        
        return self._isSelected
    
    
    def select(self, value = True):
        
        self._isSelected = value
        self.invokeToggled()
        if value == True:
            self.invokeDown()
        else:
            self.invokeUp()


    def invokeToggled(self):
        
        if self._toggleFunction is not None:
            self._toggleFunction()


    def invokeDown(self):

        if self._downFunction is not None:
            self._downFunction()


    def invokeUp(self):

        if self._upFunction is not None:
            self._upFunction()            
    


class PygameScrollButton(PygameButton):
    
    
    def __init__(self, surface, rectangle, text, values, initValue,
                 clickedFunction = None, scrollUpFunction = None, scrollDownFunction = None,
                 fontSize = 12, textColour = black, 
                 upColour = grey, downColour = dark_grey, mouseOverColour= light_grey, 
                 buttonName = None):
        '''
        A button to scroll through preset values. Scrolling up or down changes the value, clicking resets the value.
        Inputs:
            :values (list): the values that the button can take on, from lowest to highest
            :initValue: the initial value to set the button to
            :scrollUpFunction: a function to pass the updated current value when the mouse wheel is scrolled up over the button
            :scrollDownFunction: a function to pass the updated current value when the mouse wheel is scrolled down over the button
        '''
        super(PygameScrollButton, self).__init__(surface, rectangle, 
                                                 text, fontSize, textColour,
                                                 upColour, downColour, mouseOverColour,
                                                 buttonName)
                                                 
        self._title = text                                
        self._values = values
        self._initValue = initValue
        self._currentValue = initValue
        self._updateText()
        self._clickedFunction = clickedFunction
        self._scrollUpFunction = scrollUpFunction
        self._scrollDownFunction = scrollDownFunction
        
        
    def _updateText(self):
        
        self._text = '%s: %s' %(self._title, str(self._currentValue))


    def invokeClicked(self):
        
        self._currentValue = self._initValue
        self._updateText()
        if self._clickedFunction is not None:
            self._clickedFunction()
    
    
    def invokeScrollUp(self):
        
        currentValueindex = self._values.index(self._currentValue)
        if currentValueindex < len(self._values) - 1:
            self._currentValue = self._values[currentValueindex + 1]
            self._updateText()
            if self._scrollUpFunction is not None:
                self._scrollUpFunction(self._currentValue)
    
    
    def invokeScrollDown(self):
        
        currentValueindex = self._values.index(self._currentValue)
        if currentValueindex > 0:
            self._currentValue = self._values[currentValueindex - 1]
            self._updateText()
            if self._scrollDownFunction is not None:
                self._scrollDownFunction(self._currentValue)
    
