import pygame as pg

from PygameShapes import PygameRectangle


def isMouseOver(rectangle):
    '''
    Return True if the mouse cursor is over the button
    '''
    if type(rectangle) == PygameRectangle:
        rectangle = rectangle.getTuple()
    cur = pg.mouse.get_pos()
    return pointOnOrInRectangle(cur, rectangle)


def pointOnOrInRectangle(point, rectangle):
    
    return point[0] >= rectangle[0] and point[0] <= rectangle[0] + rectangle[2] \
       and point[1] >= rectangle[1] and point[1] <= rectangle[1] + rectangle[3]
       

def pointsToRectangle(point1, point2):
    
    return (min(point1[0], point2[0]), 
            min(point1[1], point2[1]), 
            abs(point1[0] - point2[0]), 
            abs(point1[1] - point2[1]))


def offsetRectangle(rectangle, relativeOffset):
    
    return (rectangle[0] + relativeOffset[0],
            rectangle[1] + relativeOffset[1],
            rectangle[2], rectangle[3])
            

def getMousePos():
    
    cur = pg.mouse.get_pos()
    return cur


def getMouseX():
    
    return getMousePos()[0]


def getMouseY():
    
    return getMousePos()[1]
    
