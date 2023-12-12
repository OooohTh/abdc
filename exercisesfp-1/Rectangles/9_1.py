from dataclasses import dataclass
from math import sqrt

@dataclass
class Point:
    h:int
    v:int

@dataclass
class Rect:
    top:int
    left:int
    bottom:int
    right:int

def get_Center(r:Rect) -> Point:
    return Point((r.top-r.bottom)/2+r.bottom,(r.right-r.left)/2+r.left)

def get_distance_points(p1:Point,p2:Point) -> float:
    return sqrt((p1.v-p2.v)**2+(p1.h-p2.h)**2)

def get_distance(val1:int,val2:int) -> int:
    return abs(val2-val1)

def get_Height(r:Rect) -> float:
    return abs(r.top-r.bottom)

def get_Width (r:Rect) -> float:
    return abs(r.right-r.left)

def new_Point(_h:int,_v:int) -> Point:
    return Point (h=_h,v=_v)

#  top>=bottom and left <= right
def new_Rect(_top,_left,_bottom,_right) -> Rect:
#   return Rect(top = _top, left=_left, bottom=_bottom, right=_right)
    return Rect(_top, _left, _bottom, _right)

def get_topleft(r:Rect) -> Point:
    return Point (r.left,r.top)

def get_botright(r:Rect) -> Point:
    return Point (r.right,r.bottom)

def __in_interval(x,l,h):
    return l<=x and x<=h or l>=x>=h

def point_in_rect(p:Point, r:Rect) -> bool:
    return __in_interval(p.h,r.left,r.right) and __in_interval(p.v,r.bottom,r.top)

def offset_rect(r:Rect, dh,dv) -> Rect:
    return Rect(r.top+dv,r.left+dh,r.bottom+dv,r.right+dh)

def offset_rect_upd(r:Rect, dh,dv) -> Rect:
    r.top += dv
    r.left += dh
    r.bottom += dv
    r.right += dh
    return r

def grow_rect(r:Rect, dh, dv) -> Rect:
    return Rect(r.top+dv,r.left-dh,r.bottom-dv,r.right+dh)

def union_rect(r1:Rect, r2:Rect) -> Rect:
    top = max(r1.top,r2.top)
    left = min(r1.left,r2.left)
    bottom = min(r1.bottom,r2.bottom)
    right= max(r1.right,r2.right)
    return Rect(top,left,bottom,right)

def flip_rect(r:Rect) -> Rect:
    center=get_Center(r)
    newHeight=get_Width(r)
    newWidth=get_Height(r)
    return Rect(center.h+(newHeight/2),center.v-(newWidth/2),center.h-(newHeight/2),center.v+(newWidth/2))

def sect_rect(r1:Rect, r2:Rect) -> (Rect|None):
    rect1=(r1.top,r1.left,r1.bottom,r1.right)
    rect2=(r2.top,r2.left,r2.bottom,r2.right)
    center1=get_Center(r1)
    center2=get_Center(r2)
    dist_h=get_distance(center1.h,center2.h)
    dist_v=get_distance(center1.v,center2.v)
    width1=get_Width(r1)
    width2=get_Width(r2)
    height1=get_Height(r1)
    height2=get_Height(r2)
    sect_rect=[0,0,0,0]
    if dist_h<(height1+height2)/2 and dist_v<(width1+width2)/2: #Verifica se os retângulos se intersetam
        for i in range(4):
            if __in_interval(rect1[i],rect2[i],rect2[(i+2)%4]):
                sect_rect[i]=rect1[i]
            else:
                sect_rect[i]=rect2[i]
        sect_rect=Rect(sect_rect[0],sect_rect[1],sect_rect[2],sect_rect[3])
        return  sect_rect
    return None

def divide_rect(rec:Rect,lin:int,x_y:str):
    if x_y=='x':
        if __in_interval(lin,rec.left,rec.right):
            return Rect(rec.top,rec.left,rec.bottom,lin),Rect(rec.top,lin,rec.bottom,rec.right)
    elif x_y=='y':
        if __in_interval(lin,rec.top,rec.bottom):
            return Rect(rec.top,rec.left,lin,rec.right),Rect(lin,rec.left,rec.bottom,rec.right)


def subtract_rect(r1:Rect, r2:Rect) -> list[Rect]:
    rect1=(r1.top,r1.left,r1.bottom,r1.right)
    Intersection=sect_rect(r1,r2)
    if Intersection==None:
        return None
    IntersectionTuple=(Intersection.top,Intersection.left,Intersection.bottom,Intersection.right)
    Sides_in_common=0
    for i in range(4):
        if rect1[i]==IntersectionTuple[i]:
            Sides_in_common+=1
    if Sides_in_common==0:
        if r1==Intersection:
            return []
        else:
            Left=Rect(r1.top,r1.left,r1.bottom,Intersection.left)
            Right=Rect(r1.top,Intersection.right,r1.bottom,r1.right)
            Up=Rect(r1.top,Intersection.left,Intersection.top,Intersection.right)
            Down=Rect(Intersection.bottom,Intersection.left,r1.bottom,Intersection.right)
            return[Left,Up,Right,Down]
    if Sides_in_common==1:
        Left=Rect(r1.top,r1.left,r1.bottom,Intersection.left)
        Right=Rect(r1.top,Intersection.right,r1.bottom,r1.right)
        Up=Rect(r1.top,Intersection.left,Intersection.top,Intersection.right)
        Down=Rect(Intersection.bottom,Intersection.left,r1.bottom,Intersection.right)
        if r1.top==Intersection.top:
            return [Left,Right,Down]
        elif r1.left==Intersection.left:
            return[Up,Right,Down]
        elif r1.bottom==Intersection.bottom:
            return[Left,Up,Right]
        else:
            return[Left,Up,Down]
    if Sides_in_common==2:
        if r1.top!=Intersection.top and r1.bottom!=Intersection.bottom:
            UpRect=Rect(r1.top,r1.left,Intersection.top,r1.right)
            DownRect=Rect(Intersection.bottom,r1.left,r1.bottom,r1.right)
            IntersectionCenter=get_Center(Intersection)
            LeftUp,RightUp=divide_rect(UpRect,IntersectionCenter.v,'x')
            LeftDown,RightDown=divide_rect(DownRect,IntersectionCenter.v,'x')
        elif r1.top==Intersection.top and r1.bottom==Intersection.bottom:
            LeftRect=Rect(r1.top,r1.left,r1.bottom,Intersection.left)
            RightRect=Rect(r1.top,Intersection.right,r1.bottom,r1.right)
            IntersectionCenter=get_Center(Intersection)
            LeftUp,LeftDown=divide_rect(LeftRect,IntersectionCenter.h,'y')
            RightUp,RightDown=divide_rect(RightRect,IntersectionCenter.h,'y')
        else:
            if r1.left==Intersection.left and r1.right!=Intersection.right:
                DifferentX=Intersection.right
            else:
                DifferentX=Intersection.left
            if r1.top!=Intersection.top and r1.bottom==Intersection.bottom:
                DifferentY=Intersection.top
            else:
                DifferentY=Intersection.bottom
            UpRect,DownRect=divide_rect(r1,DifferentY,'y')
            LeftUp,RightUp=divide_rect(UpRect,DifferentX,'x')
            LeftDown,RightDown=divide_rect(DownRect,DifferentX,'x')
        RectList=[LeftUp,LeftDown,RightUp,RightDown]
        for i in range(4):
            if RectList[i]==Intersection:
                RectList.remove(RectList[i])
                break
        return RectList
    if Sides_in_common==3:
        for i in range(4):
            if rect1[i]!=IntersectionTuple[i]:
                FinalRect=list(rect1)
                FinalRect[(i+2)%4]=IntersectionTuple[i]
                return Rect(FinalRect[0],FinalRect[1],FinalRect[2],FinalRect[3])
    

    

    divide_rect(r1,r2,)
    for i in Intersection:
        print (i)


a=Rect(4,2,2,6)
b=Rect(4,2,2,5)
print(subtract_rect(a,b))
