# python reindent 
class Box(object):

    def __init__(self, xl, yt, xr, yb):
        """
        - Just switch the values and document:
            ~ May cause the user to cascade into a pit of not knowing
        - Catch the user in an infinite loop of doom?
            ~ Dont.
        - Return an error
            ~ Pythonic: TypeError's 
        - Comment telling them to not give bad coordinates
        
        - Return an "empty" type and then implement functions to also deal with empty boxes
        - Set internal variables to invalid values
            ~ Reasonable. 
        - Returning an invalid type like none
        _ Print a statement, ask if they want to flip them (User Input)
            ~ Imagine if they do 1000's of boxes at once... (too polite) it wont 
            get noticed
        """
        if xl > xr or yt > yb:
            raise Error("UR BAD")
        self._xl = xl
        self._yt = yt
        self._xr = xr 
        self._yb = yb

        def xl(self):
            return self._xl

        def moveBy(self, dx, dy):
            #move the (x, y), position of the box b to new position (x+dx, y+dy)
            self._xl += dx
            self._xr += dx

            self._yt += dy
            self._yb += dy

    def contains(self, x, y):
        return (self._xl <= x <= self._xr) and (self._yt <= y <= self._yb)
        #check if point (x, y) is inside the box b
        #if not ((self.cxl <= x <= self.cxr) and (self.cyt <= y <= self.cyb)):
        #    return False
        #return True

    def collidesWith(self, b1, offsetx, offsety):
        #check if a box b is touching or overlapping another box b1
        # Check to see if self contains any points within b1.
        #### DONT USE RANGE BECASUE INTEGERS COULD BE FLOATS ####
      
        return ((self._xr+offsetx >= b1._xl) and (b1._xr >= self._xl+offsetx)) and ((b1._yb >= self._yt+offsety) and (self._yb+offsety >= b1._yt))