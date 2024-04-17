from case import create_case
from build123d import *
from ocp_vscode import *
from rich.progress import Progress

if __name__=="__main__":
    innner_box=create_case.CreateBox(
        length=335.0,
        width=225.0,
        height=85.0,
        thickness=1.0,
        length_divisions=6,
        width_divisions=6,
        height_divisions=2,
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
                        ex.append(new_box.box)
                        progress.update(task_id=task1,advance=1)
                        move_width+=new_box.width+10
                        box_length=new_box.length
                move_length+=box_length+10
    outer_box=innner_box.create_outer_box()
    #face2=ex.faces().filter_by(Axis.Z).sort_by()[0].edges()
    show(ex)
    #show(face2)