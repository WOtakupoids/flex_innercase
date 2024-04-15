from build123d import *
from ocp_vscode import *
from pprint import pprint
class CreateBox():
    def __init__(self,
                 length:float,
                 width:float,
                 height:float,
                 thickness:float,
                 length_divisions:int=1,
                 width_divisions:int=1,
                 height_divisions:int=1,
                 clearance:float=0.15,
                 corner_R=3
                 ) -> None:
        self.__length=length
        self.__width=width
        self.__height=height
        self.__thickness=thickness
        self.__length_divisions=length_divisions
        self.__width_divisions=width_divisions
        self.__height_divisions=height_divisions
        self.__clearance=clearance
        self.__corner_R=corner_R
        self.__foot_thickness:float=3.0
        self.__min_length=(self.__length-2*self.__clearance)/self.__length_divisions
        self.__min_width=(self.__width-2*self.__clearance)/self.__width_divisions
        self.__min_height=(self.__height-self.__foot_thickness-2*self.__clearance)/self.__height_divisions
        self.__foot_length=self.__min_length-(self.__thickness+self.__clearance)*2
        self.__foot_width=self.__min_width-(self.__thickness+self.__clearance)*2
    def create_box(self,length_num:int=1,width_num:int=1,height_num:int=1)->Curve | Sketch | Part | Compound|None:
        if length_num<=self.__length_divisions and height_num<=self.__height_divisions:
            outer_box=self.__create_top_outer_box(
                length=self.__min_length*length_num,
                width=self.__min_width*width_num,
                height=self.__min_height*height_num
            )
            inner_box=self.__create_top_inner_box(
                length=self.__min_length*length_num,
                width=self.__min_width*width_num,
                height=self.__min_height*height_num,
            )
            top_box=outer_box-inner_box
            
            wall_clearance=self.__thickness+self.__clearance
            for i in range(1,length_num+1):
                for j in range(1,width_num+1):
                    bottom_box=self.__create_bottom_box()
                    top_box+=Pos((2*i-1)*wall_clearance+(i-1)*self.__foot_length,Y=(2*j-1)*wall_clearance+(j-1)*self.__foot_width)*bottom_box
                    print('i:'+str(i))
                    print('j:'+str(j))
            return top_box
        return None
    def __create_top_outer_box(self,length,width,height):
        top_face=Pos(length/2, width/2,self.__foot_thickness)*Rectangle(length, width)
        top_box=extrude(top_face, height)
        top_box=fillet(top_box.edges().filter_by(Axis.Z),self.__corner_R)
        top_box=fillet(top_box.edges().group_by(Axis.Z)[0],0.5)
        return top_box
    def __create_top_inner_box(self,length,width,height):
        bottom_face=Rectangle(length-self.__thickness*2,width-self.__thickness*2)
        bottom_face=Pos(length/2, width/2,self.__thickness+self.__foot_thickness)*bottom_face
        bottom_box=extrude(bottom_face,height)
        if self.__corner_R-self.__thickness>0:
            bottom_box=fillet(bottom_box.edges().filter_by(Axis.Z),self.__corner_R-self.__thickness)
        bottom_box=fillet(bottom_box.edges().group_by(Axis.Z)[0],0.5)
        return bottom_box
    def __create_bottom_box(self):
        length=self.__foot_length
        width=self.__foot_width
        bottom_face=Rectangle(length,width)
        bottom_face=Pos(length/2, width/2)*bottom_face
        box=extrude(bottom_face,self.__foot_thickness)
        box=fillet(box.edges().filter_by(Axis.Z),self.__corner_R-self.__thickness)
        box=fillet(box.edges().group_by(Axis.Z)[0],0.5)
        return box
    def create_outer_box(self):
        box=Pos(self.__length/2, self.__width/2,self.__height/2)*Box(self.__length, self.__width, self.__height)
        return box.edges()
if __name__=="__main__":
    box=CreateBox(
        length=100.0,
        width=100.0,
        height=100.0,
        thickness=1.0,
        length_divisions=5,
        width_divisions=5,
        height_divisions=2,
        corner_R=4)
    ex=box.create_box(4,4)
    outer_box=box.create_outer_box()
    #face2=ex.faces().filter_by(Axis.Z).sort_by()[0].edges()
    show_all()
    #show(face2)