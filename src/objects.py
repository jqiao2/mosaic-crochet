from enum import Enum


"""
Deprecated: Using booleans to represent two tone images. Bring back color objects when we support 3+ colors
"""
class Color(Enum):
    WHITE = 0
    BLACK = 1


class Stitch:
    def __init__(self, is_double: bool, color: bool, child=None, grandchild=None):
        """

        :param is_double:   double stitch or single stitch
        :param color:       WHITE or BLACK
        :param child:       stitch below this stitch; must be other color
        :param grandchild:  stitch two below this stitch; must be this color
        """
        if child:
            assert (child.COLOR != color)
        if grandchild:
            assert (grandchild.COLOR == color)

        self.is_double = is_double
        self.COLOR = color
        self.display_color = color

        self.child = child
        self.grandchild = grandchild

    def __repr__(self):
        ret = ""
        ret += str(self.COLOR) + " "
        ret += "double" if self.is_double else "single"
        return ret
