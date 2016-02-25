# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 00:24:30 2015

@author: vahndi
"""

from PygameButtons import PygamePushButton, PygameOptionButton, PygameScrollButton
from PygameColours import white, black, grey, dark_grey, light_grey
import pygame as pg


class PygameButtonSet(object):
    
    
    def __init__(self, origin, isVisibleFunction = None,
                 buttonWidth = 100, buttonHeight = 30, buttonSpacing = 10):
        '''
        Inputs:
            :origin: The upper left corner of the button set
            :visibleFunction: a boolean function to test is True before displaying the button set
        '''
        self._origin = origin
        self._isVisibleFunction = isVisibleFunction
        self._buttonWidth = buttonWidth
        self._buttonHeight = buttonHeight
        self._buttonSpacing = buttonSpacing

        
    def setOriginY(self, originY):
        '''
        Move the origin y coordinate to a new value
        '''
        origin = self._origin
        origin[1] = originY
        self.setOrigin(origin)
    
    
    def setOrigin(self, origin):
        '''
        Move the origin to a new location
        '''
        self._origin = origin
        
        buttonX = origin[0]
        buttonY = origin[1]
        for button in self._buttons:
            buttonRect = [buttonX, buttonY, self._buttonWidth, self._buttonHeight]
            button.setRectangle(buttonRect)
            buttonX += self._buttonWidth + self._buttonSpacing
    
    
    def getHeight(self):
        return self._buttonHeight        
        
    
    def isVisible(self):
        
        if self._isVisibleFunction is not None:
            if self._isVisibleFunction() == False:
                return False
                
        return True
        
        
    def draw(self):
        
        if self.isVisible():
            for button in self._buttons:
                button.draw()


    def getMouseOverButtonName(self):
        
        if self.isVisible():
            for button in self._buttons:
                if button.isMouseOver():
                    return button.getButtonName()
        
        return None

        

class PygamePushButtonSet(PygameButtonSet):

    
    def __init__(self, surface, origin, buttonTuples, 
                 isVisibleFunction = None,
                 buttonWidth = 100, buttonHeight = 50, buttonSpacing = 10,
                 fontSize = 12, textColour = black, 
                 upColour = grey, downColour = dark_grey, mouseOverColour = light_grey):
        '''
        Inputs:
            :buttonTuples:  (name, text, clickedFunction)
        '''
        super(PygamePushButtonSet, self).__init__(origin, isVisibleFunction)
        
        buttonX = origin[0]
        buttonY = origin[1]
        self._buttons = []

        for buttonTuple in buttonTuples:
            buttonRect = [buttonX, buttonY, buttonWidth, buttonHeight]
            self._buttons.append(PygamePushButton(surface, buttonRect, 
                                                  buttonTuple[1], buttonTuple[2], fontSize = fontSize, textColour = textColour, 
                                                  upColour = upColour, downColour = downColour, mouseOverColour = mouseOverColour,
                                                  buttonName = buttonTuple[0]))
            buttonX += buttonWidth + buttonSpacing


    def clickButton(self, buttonName):
        
        for button in self._buttons:
            if button.getButtonName() == buttonName:
                button.invokeClicked()
                return True
        return False


    def sendMouseButton(self, event):
    
        if event.type == pg.MOUSEBUTTONUP: 
            clickedButtonName = self.getMouseOverButtonName()
            if clickedButtonName is not None:
                self.clickButton(clickedButtonName)


class PygameOptionButtonSet(PygameButtonSet):
    
    def __init__(self, surface, origin, buttonTuples, exclusiveSelect,
                 isVisibleFunction = None,
                 buttonWidth = 100, buttonHeight = 50, buttonSpacing = 10,
                 fontSize = 12, textColour = black, 
                 upColour = grey, downColour = dark_grey, mouseOverColour = light_grey):
        '''
        Inputs:
            :buttonTuples:  (name, text, isSelected, toggleFunction, downFunction, upFunction)
        '''
        super(PygameOptionButtonSet, self).__init__(origin, isVisibleFunction)

        self._exclusiveSelect = exclusiveSelect
        buttonX = origin[0]
        buttonY = origin[1]
        self._buttons = []
        
        for buttonTuple in buttonTuples:
            buttonName = buttonTuple[0]
            buttonText = buttonTuple[1]
            buttonSelected = buttonTuple[2]
            toggleFunc = buttonTuple[3]
            downFunc = buttonTuple[4]
            upFunc = buttonTuple[5]
            buttonRect = [buttonX, buttonY, buttonWidth, buttonHeight]
            self._buttons.append(PygameOptionButton(surface, buttonRect, buttonSelected, buttonText, 
                                                    toggleFunction = toggleFunc, downFunction = downFunc, upFunction = upFunc, 
                                                    fontSize = fontSize, textColour = textColour, 
                                                    upColour = upColour, downColour = downColour, mouseOverColour = mouseOverColour,
                                                    buttonName = buttonName))
            buttonX += buttonWidth + buttonSpacing

    
    def selectButton(self, buttonName):
        
        for button in self._buttons:
            if button.getButtonName() == buttonName:
                button.select()
            else:
                if self._exclusiveSelect and button.isSelected():
                    button.select(False)


    def toggleButton(self, buttonName):
        '''
        Toggles the on-state of the button and returns True if it is on 
        or False if it is off
        '''
        for button in self._buttons:
            if button.getButtonName() == buttonName:
                if button.isSelected():
                    button.select(False)
                    return False
                else:
                    self.selectButton(buttonName)
                    return True


    def sendMouseButton(self, event):
    
        if event.type == pg.MOUSEBUTTONUP: 
            clickedButtonName = self.getMouseOverButtonName()
            if clickedButtonName is not None:
                self.toggleButton(clickedButtonName)



class PygameScrollButtonSet(PygameButtonSet):
    
    def __init__(self, surface, origin, buttonTuples,
             isVisibleFunction = None,
             buttonWidth = 100, buttonHeight = 50, buttonSpacing = 10,
             fontSize = 12, textColour = black, 
             upColour = grey, downColour = dark_grey, mouseOverColour = light_grey):
        '''
        Inputs:
            :buttonTuples:  (name, text, values, initValue, clickFunction, scrollUpFunction, scrollDownFunction)
        '''
        super(PygameScrollButtonSet, self).__init__(origin, isVisibleFunction)
        
        buttonX = origin[0]
        buttonY = origin[1]
        self._buttons = []

        for buttonTuple in buttonTuples:
            buttonRect = [buttonX, buttonY, buttonWidth, buttonHeight]
            self._buttons.append(PygameScrollButton(surface, buttonRect, 
                                                    buttonTuple[1], buttonTuple[2], buttonTuple[3], buttonTuple[4], buttonTuple[5], buttonTuple[6], 
                                                    fontSize = fontSize, textColour = textColour, 
                                                    upColour = upColour, downColour = downColour, mouseOverColour = mouseOverColour,
                                                    buttonName = buttonTuple[0]))
            buttonX += buttonWidth + buttonSpacing
        
        
    def scrollUpButton(self, buttonName):
        
        for button in self._buttons:
            if button.getButtonName() == buttonName:
                button.invokeScrollUp()
    
    
    def scrollDownButton(self, buttonName):
        
        for button in self._buttons:
            if button.getButtonName() == buttonName:
                button.invokeScrollDown()


    def sendMouseButton(self, event):
        
        clickedButtonName = self.getMouseOverButtonName()
        if clickedButtonName is not None:
            if event.button == 4:
                self.scrollUpButton(clickedButtonName)
                return True
            elif event.button == 5:
                self.scrollDownButton(clickedButtonName)
                return True
        return False
