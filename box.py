class Box(object):

    def __init__(self, xl, yt, xr, yb):
        """
        Initiate a box with four corners.        
        """
        if xl > xr or yt > yb:
            raise Error("UR BAD, You're box dimensions don't work")
        self._xl = xl
        self._yt = yt
        self._xr = xr 
        self._yb = yb

    def collidesWith(self, b1, offsetx, offsety):
        """
        Check if one box is touches another box. Offset can be used to see 
        in the future, without the need for a flux capacitor. Imagine that!
        """
        return ((self._xr+offsetx >= b1._xl) and (b1._xr >= self._xl+offsetx)) and ((b1._yb >= self._yt+offsety) and (self._yb+offsety >= b1._yt))