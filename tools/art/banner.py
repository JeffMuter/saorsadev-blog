from PIL import Image
import os; ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..')); S=os.path.join(ROOT,'static')+'/'
C={'O':(34,20,4),'G':(255,176,0),'g':(201,133,0),'L':(255,211,106),'Y':(255,211,106),'y':(201,133,0),
   'E':(255,227,160),'W':(255,227,160),'P':(34,20,4),
   'B':(138,90,0),'b':(90,62,0),'w':(255,227,160),'s':(138,90,0),
   'D':(138,106,0),'d':(90,67,0),'R':(176,136,10),'T':(120,70,30),'M':(80,60,25),'r':(107,74,0),'p':(255,227,160)}
frog_half=[
"....OOOOOO...",
"..OOGGGGGGOOO",
".OGGEEEEEEGGG",
".OGEEkkkkEEGG",
".OGEkEEEEkEGG",
".OGEEEEEEEEGG",
".OGGEEEEEEGGG",
"OLGGGGkGGGGGG",
"OGKKGGGkkkkkk",
"OGGGGGGGGGGGG",
".OGGGGGGYYYYY",
".OGGGGGYYYYYY",
".OGGGGYYYYYYY",
"OGGGGGYYYYYYY",
"OGLGGGYYYYYYY",
"OGGGGGYYYYYYY",
"OGGGGGGYYYYYY",
"OGGGGGGGYYYYY",
"OGGGGGGGGYYYY",
".OGGgGGGGGGGG",
"..OGGGGOGGGGG",
"...OOOOOOOOOO"]
WING_L=[
".QQQ..........",
".QffQQ........",
".QffffQQ......",
".QffffffQQ....",
".QQfffffffQ...",
"QQfQQQfffffQ..",
"QfffffffffffQ.",
"QfffffffffffQ.",
".QfffffQQQfffQ",
"..QQffQfffQffQ",
".QfffQffffQffQ",
"..QffQfffQfffQ",
"...QQQffffffQ.",
"......QffffQ..",
".......QQQQ..."]
C['k']=(60,30,0); C['K']=(190,100,10)
C['Q']=(138,90,0); C['f']=(255,227,160)
def mirror(rows): return [r+r[::-1] for r in rows]
def put(img,rows,x,y):
    for j,r in enumerate(rows):
        for i,ch in enumerate(r):
            if ch!='.': img.putpixel((x+i,y+j),C[ch]+(255,))
def frog_sprite():
    W=26+2*12
    im=Image.new('RGBA',(W,26),(0,0,0,0))
    L=WING_L; R=[r[::-1] for r in WING_L]
    put(im,L,0,3); put(im,R,W-14,3)
    put(im,mirror(frog_half),12,3)
    return im
def banner():
    g=Image.new('RGBA',(200,32),(0,0,0,0))
    cx=100
    # water line
    for x in range(200):
        if (x//3)%2==0 or True: g.putpixel((x,29),C['r']+(255,))
    for x in range(0,200):
        if (x*7)%5 in (0,1): g.putpixel((x,31),C['b']+(255,))
    # centre pad
    def pad(cx,cy,w,notch=True):
        for dx in range(-w,w+1):
            h=1 if abs(dx)>w-3 else 2
            for dy in range(0,h+1):
                if abs(dx)>w-1 and dy==0: continue
                g.putpixel((cx+dx,cy+dy),C['D'] +(255,))
        for dx in range(-w,w+1):
            g.putpixel((cx+dx,cy+(1 if abs(dx)>w-3 else 2)),C['d']+(255,))
            if abs(dx)<w-3: g.putpixel((cx+dx,cy),C['R']+(255,))
    pad(cx,26,16)
    fs=frog_sprite()
    g.alpha_composite(fs,(cx-fs.width//2,0))
    # side pads
    for px in (62,138): pad(px,29-1,7)
    for px in (28,172): pad(px,28,5)
    import random
    rnd=random.Random(7)
    def px(x,y,c):
        if 0<=x<200 and 0<=y<32: g.putpixel((x,y),C[c]+(255,) if c in C else tuple(c)+(255,))
    def blade(x,h,lean,base=28):
        for k in range(h):
            xo=x+(lean*k//3 if lean else 0)
            px(xo,base-k,(90,67,0) if k<h*0.5 else ((138,106,0) if k<h-1 else (176,136,10)))
    def clump(x,s):
        n=2+s*2+rnd.randint(0,1)
        for i in range(n):
            ox=rnd.randint(-1-s,1+s)
            h=rnd.randint(3+s*2,5+s*3)
            blade(x+ox,h,rnd.choice((-2,-1,0,0,1,2)))
    def shroom(x,cap,s,base=28):
        stem=C['E']; spot=(60,30,0)
        for k in range(2+s): px(x,base-k,stem)
        if s>=2: px(x+1,base-1,stem)
        t=base-(2+s); w=1+s
        for dx in range(-w-1,w+2): px(x+dx,t,cap)
        for dx in range(-w,w+1): px(x+dx,t-1,cap)
        for dx in range(-w+1,w): px(x+dx,t-2,cap)
        if s>=2:
            for dx in range(-w+2,w-1): px(x+dx,t-3,cap)
        px(x-1,t-1,spot); px(x+w-1,t-1,spot)
        if s>=2: px(x,t-2,spot); px(x-w+1,t,spot)
    def cluster(x,s):
        caps=[(200,90,20),(255,176,0),(170,60,10)]
        shroom(x,rnd.choice(caps),s)
        shroom(x-4-s,rnd.choice(caps),max(0,s-1))
        if s>=1: shroom(x+4+s,rnd.choice(caps),max(0,s-rnd.randint(1,2)))
    def sprout(x):
        px(x,28,(90,67,0)); px(x,27,(90,67,0)); px(x,26,(176,136,10)); px(x-1,26,(138,106,0)); px(x+1,26,(138,106,0))
    # (offset from centre, kind, size) ramp: small near frog, larger at edges
    items=[(24,'sp',0),(30,'g',0),(37,'m',0),(43,'g',0),(49,'g',1),(55,'m',1),(61,'g',1),
           (67,'g',2),(72,'g',2),(78,'m',2),(85,'g',2),(89,'g',2),(94,'m',2),(97,'g',2)]
    for side in (-1,1):
        for off,k,sz in sorted(items,key=lambda t:t[1]=='m'):
            x=cx+side*(off+rnd.randint(-1,1))
            if k=='sp': sprout(x)
            elif k=='g': clump(x,sz)
            else: cluster(x,sz)
    for px_ in (62,138): pad(px_,28,7)
    return g
ban=banner().resize((400,64),Image.NEAREST)
ban.save(S+'border-home1.png')
sp=frog_sprite().resize((frog_sprite().width*2,26*2),Image.NEAREST); sp.save(S+'oggie-v2.png')
bg=Image.new('RGBA',ban.size,(11,11,8,255)); bg.alpha_composite(ban)
print(sp.size)
