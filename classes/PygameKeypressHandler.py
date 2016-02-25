import pygame as pg



class PygameKeypressHandler(object):
    '''
    An object to store information about a Pygame keypress and any modifiers
    '''
    def __init__(self, key, handlerFunction, sendEvent = False, 
                 modifiers = None, conditionFunction = None):
        '''
        Arguments:
            :key: the pygame key that is pressed
            :handlerFunction: the function to call to handle the keypress
            :sendEvent: whether to send the event to the handler function
            :modifiers: any keyboard modifiers that must be active for the handler to be activated
            :conditionFunction: a boolean function that must evaluate to True for the handler to be activated
        '''
        self._key = key
        self._handlerFunction = handlerFunction
        self._sendEvent = sendEvent
        self._modifiers = modifiers        
        self._conditionFunction = conditionFunction

    
    def handleEvent(self, event):
        '''
        Determines if the given event matches the keypress object
        '''
        # Check the condition is met, if there is one
        if self._conditionFunction is not None:
            if not self._conditionFunction():
                return False
        # Check that the modifiers match, if the keypress has any
        if self._modifiers:
            if not pg.key.get_mods() & self._modifiers:
                return False
        # Check that the key matches
        if event.key == self._key:
            if self._sendEvent:
                self._handlerFunction(event)
            else:
                self._handlerFunction()
            return True

        return False


        
class PygameKeypressHandlerSet(object):

    
    def __init__(self, keypressHandlers, conditionFunction = None, notHandledFunction = None, sendEvent = False):
        '''
        Arguments:
            :keypressHandlers: a list of PygameKeypressHandlers
            :conditionFunction: an optional boolean function to check is True before passing the event to the keypress handlers
            :notHandledFunction: an optional function to call if the keypress was not handled (if the condition function was met)
            :sendEvent: whether to send the event to the notHandled function
        '''
        self._keypressHandlers = keypressHandlers
        self._conditionFunction = conditionFunction
        self._notHandledFunction = notHandledFunction
        self._sendEvent = sendEvent
        

    def handleEvent(self, event):
        '''
        Handles a keypress event by executing the associated function
        N.B. assumes that event.type == pygame.KEYDOWN has been checked
        Inputs:
            :event: a pygame event of type pygame.KEYDOWN
        Outputs:
            returns True if the keypress was found in the handler's list, and the internal condition function was met
        '''
        # Check condition function, if there is one
        if self._conditionFunction is not None:
            if not self._conditionFunction():
                return False
        # Pass on event to keypress handlers until one handles it
        for keypressHandler in self._keypressHandlers:
            if keypressHandler.handleEvent(event):
                return True
        
        # Call the notHandled function, if it exists
        if self._notHandledFunction is not None:
            if self._sendEvent:
                self._notHandledFunction(event)
            else:
                self._notHandledFunction()
            return False

        return False
