from build123d import *
from ocp_vscode import *

class InnerBox():
    def __init__(self):
        self.box:Part
        self.length:float
        self.width:float
        self.height:float

class CreateBox():
    def __init__(self,
                 length:float,
                 width:float,
                 height:float,
                 thickness:float,
                 length_divisions:int=1,
                 width_divisions:int=1,
                 height_divisions:int=1,
                 depth_clearance:float=6,
                 clearance:float=0.15,
                 corner_R=3
                 ) -> None:
        """分割用の箱を生成する

        Args:
            length (float): 分割する箱の奥行内寸
            width (float): 分割する箱の幅内寸
            height (float): 分割する箱の高さ方向内寸
            thickness (float): 壁厚
            length_divisions (int, optional): 奥行分割数. Defaults to 1.
            width_divisions (int, optional): 幅方向分割数. Defaults to 1.
            height_divisions (int, optional): 高さ方向分割数. Defaults to 1.
            depth_clearance (float, optional): 高さ方向に対する最終的なクリアランス. Defaults to 6.
            clearance (float, optional): 部品全体のクリアランス. Defaults to 0.15.
            corner_R (int, optional): 四つ角の大きなR. Defaults to 3.
        """
        self.__length=length
        self.width=width
        self.__height=height
        self.__thickness=thickness
        self.length_divisions=length_divisions
        self.width_divisions=width_divisions
        self.height_divisions=height_divisions
        self.__depth_clearance=depth_clearance
        self.clearance=clearance
        self.__corner_R=corner_R
        self.__foot_thickness:float=3.0
        self.__min_length=(self.__length-2*self.clearance)/self.length_divisions
        self.__min_width=(self.width-2*self.clearance)/self.width_divisions
        self.__min_height=(self.__height-self.__foot_thickness-2*self.clearance-self.__depth_clearance)/self.height_divisions
        self.__foot_length=self.__min_length-(self.__thickness+self.clearance)*2
        self.__foot_width=self.__min_width-(self.__thickness+self.clearance)*2
        self.__foot_box=self.__create_bottom_box()
    def create_box(self,length_num:int=1,width_num:int=1,height_num:int=1)->InnerBox|None:
        if length_num<=self.length_divisions and height_num<=self.height_divisions:
            outer_box=self.__create_top_outer_box(
                length_num,
                width_num,
                height_num
            )
            inner_box=self.__create_top_inner_box(
                length_num,
                width_num,
                height_num
            )
            #台形の切り欠きを追加
            cutout_line=[
                (0,inner_box[2]/2-10,inner_box[3]-10+self.__foot_thickness),
                (0,inner_box[2]/2+10,inner_box[3]-10+self.__foot_thickness),
                (0,inner_box[2]/2+11.8,inner_box[3]+self.__foot_thickness),
                (0,inner_box[2]/2-11.8,inner_box[3]+self.__foot_thickness),
                (0,inner_box[2]/2-10,inner_box[3]-10+self.__foot_thickness)
            ]
            l1=Polyline(*cutout_line)
            face = make_face(Plane.XY *l1)
            cutout_box=extrude(face,self.__length)
            top_box=outer_box[0]
            #切り抜く
            box=top_box-cutout_box
            #切り欠き部分のあたるところにRつける
            l2=box.edges().group_by(Axis.Z)[-3].filter_by(Axis.X)
            l3=box.edges().group_by(Axis.Z)[-1].filter_by(Axis.X)[1:3]
            box=fillet(l2+l3,2)
            #中をくりぬく
            box-=inner_box[0]
            #壁のあたり面をR面取り
            box=fillet(box.edges().group_by(Axis.Z)[-1],self.__thickness/4)
            
            #足を追加
            wall_clearance=self.__thickness+self.clearance
            bottom_box=self.__foot_box
            foot_box:list=[]
            for i in range(1,length_num+1):
                for j in range(1,width_num+1):
                    foot_box.append(Pos((2*i-1)*wall_clearance+(i-1)*self.__foot_length,Y=(2*j-1)*wall_clearance+(j-1)*self.__foot_width)*bottom_box)
            box+=foot_box
            #topf=box.faces().filter_by(Plane.YX).last
            #box=offset(box,amount=-self.__thickness,openings=topf)
            box_info=InnerBox()
            if isinstance(box,Part):
                box_info.box=box
            box_info.length=outer_box[1]
            box_info.width=outer_box[2]
            box_info.height=outer_box[3]+inner_box[3]
            return box_info
        return None
    def __create_top_outer_box(self,length_num:int,width_num:int,height_num:int):
        """箱本体の外側を生成する

        Args:
            length_num (int): 奥行分割数
            width_num (int): 幅分割数
            height_num (int): 高さ方向分割数

        Returns:
            ボックス: 箱本体の外側
        """
        length=self.__min_length*length_num
        width=self.__min_width*width_num
        height=self.__min_height*height_num
        top_face=Pos(length/2, width/2,self.__foot_thickness)*Rectangle(length, width)
        top_box=extrude(top_face, height)
        top_box=fillet(top_box.edges().filter_by(Axis.Z),self.__corner_R)
        top_box=fillet(top_box.edges().group_by(Axis.Z)[0],0.5)
        return (top_box,length,width,height)
    def __create_top_inner_box(self,length_num,width_num,height_num):
        length=self.__min_length*length_num
        width=self.__min_width*width_num
        height=self.__min_height*height_num
        bottom_face=Rectangle(length-self.__thickness*2,width-self.__thickness*2)
        bottom_face=Pos(length/2, width/2,self.__thickness+self.__foot_thickness)*bottom_face
        bottom_box=extrude(bottom_face,height)
        if self.__corner_R-self.__thickness>0:
            bottom_box=fillet(bottom_box.edges().filter_by(Axis.Z),self.__corner_R-self.__thickness)
        bottom_box=fillet(bottom_box.edges().group_by(Axis.Z)[0],0.5)
        return (bottom_box,length,width,height)
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
        box=Pos(self.__length/2, self.width/2,self.__height/2)*Box(self.__length, self.width, self.__height)
        return box.edges()

if __name__=="__main__":
    box=CreateBox(
        length=335.0,
        width=225.0,
        height=85.0,
        thickness=1.0,
        length_divisions=6,
        width_divisions=6,
        height_divisions=2,
        corner_R=4)
    ex=box.create_box(5,2,2)
    outer_box=box.create_outer_box()
    #face2=ex.faces().filter_by(Axis.Z).sort_by()[0].edges()
    show(ex.box,outer_box)
    #show(face2)
