from build123d import *
from ocp_vscode import *
from pprint import pprint
class CreateBox():
    def __init__(self,
                 length:float,
                 width:float,
                 height:float,
                 thickness:float,
                 plane_divisions:int=1,
                 height_divisions:int=1,
                 clearance:float=0.15,
                 corner_R=3
                 ) -> None:
        self.__length=length
        self.__width=width
        self.__height=height
        self.__thickness=thickness
        self.__plane_divisions=plane_divisions
        self.__height_divisions=height_divisions
        self.__clearance=clearance
        self.__corner_R=corner_R
    def create_box(self)->Curve | Sketch | Part | Compound:


        box=self.__create_top_box()-self.__create_bottom_box()
        #inner_box=Pos(0,0,self.__thickness)*Box(self.__length-self.__thickness, self.__width-self.__thickness, self.__height)
        return box
    def __create_top_box(self):
        top_face=Pos(self.__length/2, self.__width/2)*Rectangle(self.__length, self.__width)
        top_box=extrude(top_face, self.__height)
        top_box=fillet(top_box.edges().filter_by(Axis.Z),self.__corner_R)
        top_box=fillet(top_box.edges().group_by(Axis.Z)[0],0.5)
        return top_box
    def __create_bottom_box(self):
        bottom_face=Rectangle(self.__length-self.__thickness*2, self.__width-self.__thickness*2)
        bottom_face=Pos(self.__length/2, self.__width/2,self.__thickness)*bottom_face
        bottom_box=extrude(bottom_face,self.__height)
        if self.__corner_R-self.__thickness>0:
            bottom_box=fillet(bottom_box.edges().filter_by(Axis.Z),self.__corner_R-self.__thickness)
        bottom_box=fillet(bottom_box.edges().group_by(Axis.Z)[0],0.5)
        return bottom_box
    def create_outer_box(self):
        box=Box(self.__length, self.__width, self.__height)
        return box.edges()
if __name__=="__main__":
    box=CreateBox(40.0,40.0,40.0,thickness=1.0,corner_R=4)
    ex=box.create_box()
    #outer_box=box.create_outer_box()
    #face2=ex.faces().filter_by(Axis.Z).sort_by()[0].edges()
    show_all()
    #show(face2)