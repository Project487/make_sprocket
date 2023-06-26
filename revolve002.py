import cadquery as cq
import math

n = 40                          #number of teeth
p = 3.81                        #film pitch

r = n * p / (2 * math.pi)       #hub radius
w = 15                          #hub thickness
a = 5                           #axle diameter
bd = 10                         #hub boss diameter
bh = 7                          #hub boss height

th = 1.8                        #tooth height
tf = 1.0                        #tooth flank height 
tw = 1.2                        #tooth width
tt = 1.6                        #tooth thickness
td = 3                          #distance between top face and teeth

of = w/2 - (td + tt/2)          #offset of teeth sketch from centre of hub

def drawTooth(theta):
    s = (
        cq.Sketch()
        .segment(rotate(r, 0, theta), rotate(math.sqrt(r*r - tw*tw/4), tw/2, theta))
        .segment(rotate(r+tf, tw/2, theta))
        .segment(rotate(r+th, 0, theta))
        .segment(rotate(r+tf,-tw/2, theta))
        .segment(rotate(math.sqrt(r*r - tw*tw/4), -tw/2, theta))
        .close()
        .assemble(tag='tprof')
    )
    tooth = (
        cq.Workplane('XZ')
        .placeSketch(s)
        .extrude(tt/2, both = True)
    )
    return tooth

def drawHub():
    s = (
        cq.Sketch()
        .segment((a/2, -w/2), (a/2,-bh-w/2))
        .segment((bd, -bh-w/2))
        .segment((bd, -w/2))
        .segment((r, -w/2))
        .segment((r, w/2))
        .segment((a/2, w/2))
        .close()
        .assemble(tag='hprof')
    )
    hub = (
        cq.Workplane('XY')
        .center(0, -of)
        .placeSketch(s)
        .revolve(360)
    )
    
    return hub

def rotate(x, y, theta):
    xt = x * math.cos(theta) - y * math.sin(theta)
    yt = x * math.sin(theta) + y * math.cos(theta)
    return xt, yt

arcTerm = math.asin(tw/(2*r)) *180 / math.pi

hub = drawHub()

teeth = cq.Workplane('XZ')
for t in range(0, n):
    tooth = drawTooth(2 * math.pi * t / n)
    teeth = teeth.union(tooth)

sprocket = (
    cq.Assembly(name='sprocket')
    .add(hub, name='hub')
    .add(teeth, name='teeth')
)

show_object(sprocket)

sprocket.save('sprocket_'+str(n)+'.step')

