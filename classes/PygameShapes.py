# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 13:37:43 2015

@author: Vahndi
"""

class PygameRectangle(object):
    
    
    def __init__(self, left, top, width, height):
        
        self._left = left
        self._top = top
        self._width = width
        self._height = height

    
    @classmethod
    def fromPoints(cls, point1, point2):
        
        return PygameRectangle(min(point1[0], point2[0]), 
                               min(point1[1], point2[1]), 
                               abs(point1[0] - point2[0]), 
                               abs(point1[1] - point2[1]))

        
    def applyOffset(self, relativeOffset):
        
        self._left += relativeOffset[0]
        self._top += relativeOffset[1]

    
    def offsetBy(self, relativeOffset):
        
        return PygameRectangle(self._left + relativeOffset[0],
                               self._top + relativeOffset[1],
                               self._width,
                               self._height)
    
    def multiplyBy(self, multiplier):
        
        return PygameRectangle(multiplier * self._left,
                               multiplier * self._top,
                               multiplier * self._width,
                               multiplier * self._height)
    
    def getTuple(self):
        
        return (self._left, self._top, self._width, self._height)

    def getTop(self):
        return self._top
    def getLeft(self):
        return self._left
    def getRight(self):
        return self._left + self._width
    def getBottom(self):
        return self._top + self._height
    def getWidth(self):
        return self._width
    def getHeight(self):
        return self._height

    def setLeftEdge(self, left):
        offset = left - self._left
        self._left += offset
        self._width -= offset
    def setRightEdge(self, right):
        self._width += right - self.getRight()
    def setTopEdge(self, top):
        offset = top - self._top
        self._top += offset
        self._height -= offset
    def setBottomEdge(self, bottom):
        self._height += bottom - self.getBottom()

    def getCornerPoints(self):
        
        return (self._left, self._top), (self.getRight(), self.getBottom())


    def moveLeftEdge(self, offset, minLeft = None):
        if minLeft is None:
            self.setLeftEdge(self._left + offset)
        else:
            self.setLeftEdge(max(self._left + offset, minLeft))

    def moveRightEdge(self, offset, maxRight = None):
        if maxRight is None:
            self.setRightEdge(self.getRight() + offset)
        else:
            self.setRightEdge(min(self.getRight() + offset, maxRight))
            
    def moveTopEdge(self, offset, minTop = None):
        if minTop is None:
            self.setTopEdge(self._top + offset)
        else:
            self.setTopEdge(max(self._top + offset, minTop))

    def moveBottomEdge(self, offset, maxBottom = None):
        if maxBottom is None:
            self.setBottomEdge(self.getBottom() + offset)
        else:
            self.setBottomEdge(min(self.getBottom() + offset, maxBottom))


    def getArea(self):
        
        return self._width * self._height