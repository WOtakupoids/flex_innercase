from case import create_case
from build123d import *
from ocp_vscode import *
from rich.progress import Progress

def get_color_range(divisions:int,index):
    min_color=256/divisions-1
    return int(min_color*index)
if __name__=="__main__":
    length_divisions=6
    width_divisions=6
    height_divisions=2
    innner_box=create_case.CreateBox(
        length=335.0,
        width=225.0,
        height=85.0,
        thickness=1.0,
        length_divisions=length_divisions,
        width_divisions=width_divisions,
        height_divisions=height_divisions,
        corner_R=4)
    ex:list=[]
    move_width:float=0.0
    move_length:float=0.0
    box_length:float=0.0
    total_task=innner_box.length_divisions*innner_box.width_divisions*innner_box.height_divisions
    with Progress() as progress:
        task1=progress.add_task("[red]Create Box...",total=total_task)
        for i in range(innner_box.height_divisions,0,-1):
            for j in range(1,innner_box.length_divisions+1):
                move_width=0.0
                for k in range(1,innner_box.width_divisions+1):
                    new_box=innner_box.create_box(j,k,i)
                    if new_box is not None:
                        new_box.box.position+=(move_length,move_width,0)
                        new_box.box.name=str(j)+'x'+str(k)+'x'+str(i)
                        new_box.box.color=(get_color_range(length_divisions,j),
                                                  get_color_range(width_divisions,k),
                                                  get_color_range(height_divisions,i)
                                                  )
                        ex.append(new_box.box)
                        progress.update(task_id=task1,advance=1)
                        move_width+=new_box.width+10
                        box_length=new_box.length
                move_length+=box_length+10
    outer_box=innner_box.create_outer_box()
    #ex[0].color=(0,100,100)
    #face2=ex.faces().filter_by(Axis.Z).sort_by()[0].edges()
    show(ex,names='a')
    #show(face2)