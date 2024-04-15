from build123d import *
from ocp_vscode import *

class CreateBox():
    def __init__(self,
                 length:float,
                 width:float,
                 height:float,
                 thickness:float,
                 plane_divisions:int=1,
                 height_divisions:int=1,
                 clearance:float=0.15
                 ) -> None:
        self.__length=length
        self.__width=width
        self.__height=height
        self.__thickness=thickness
        self.__plane_divisions=plane_divisions
        self.__height_divisions=height_divisions
        self.__clearance=clearance
    def create_box(self)->Curve | Sketch | Part | Compound:
        box = Box(self.__length, self.__width, self.__height)
        topf = box.faces().sort_by().last
        box = offset(box, amount=-self.__thickness, openings=topf)
        return box
if __name__=="__main__":
    box=CreateBox(30.0,30.0,30.0,2)
    show(box.create_box())