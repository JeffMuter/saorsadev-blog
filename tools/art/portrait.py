import math
from PIL import Image, ImageDraw
BG=(11,11,8); AM=(255,176,0); DA=(201,133,0); CR=(255,176,0); RD=(214,52,36); DK=(58,36,18); SK=(255,210,150)
W,H=188,188; N=96
HAIR=(58,36,18); HI=(58,36,18); WOOD=(58,36,18)
G={'m':["10001","11011","10101","10001","10001"],'u':["101","101","101","101","111"],
't':["111","010","010","010","010"],'e':["111","100","111","100","111"],'r':["110","101","110","101","101"],
':':["0","1","0","1","0"],'s':["111","100","111","001","111"],'p':["110","101","110","100","100"],'g':["111","101","111","001","111"],'v':["101","101","101","101","010"],'i':["1","0","1","1","1"],'b':["100","110","101","101","110"],' ':["00","00","00","00","00"]}
def text(d,x,y,s,col,k=3):
    for ch in s:
        g=G[ch]
        for r,row in enumerate(g):
            for c,b in enumerate(row):
                if b=='1': d.rectangle([x+c*k,y+r*k,x+c*k+k-1,y+r*k+k-1],fill=col)
        x+=(len(g[0])+1)*k
def frame(t):
    L=Image.new('RGB',(212,96),BG); d=ImageDraw.Draw(L)
    # panels
    d.rectangle([1,1,94,94],outline=CR)
    # bubbles
    for i,(bx,by,r) in enumerate([(10,80,2),(18,50,1),(8,20,2),(89,70,1),(86,35,2),(74,12,1),(24,88,1),(90,90,2)]):
        y=round(by-84*t/N)%84+5
        x=bx+round(1.2*math.sin(2*math.pi*t/N+i*1.7))
        if y>86 or y<4: continue
        col=DA if r==1 else AM
        d.ellipse([x-r,y-r,x+r,y+r],outline=col)
    # palette-locked figure: lit skin, dark hair/suit, amber trim
    SK=AM; SH=DA; MID=(140,92,0); SUIT=DK
    # body axis x=47; everything below mirrors about it
    d.polygon([(12,94),(12,78),(16,70),(24,63),(36,59),(42,57),(52,57),(58,59),(70,63),(78,70),(82,78),(82,94)],fill=SUIT)
    # neck
    d.rectangle([42,48,52,58],fill=SH)
    # shirt: one bright V with two flat collar points
    d.polygon([(37,57),(57,57),(47,71)],fill=AM)
    # tie: square knot then straight taper, one solid mid-amber shape
    d.rectangle([45,60,49,63],fill=DA)
    d.polygon([(45,64),(49,64),(49,78),(45,78)],fill=DA)
    d.polygon([(45,64),(49,64),(48,78),(46,78)],fill=DA)
    # ears
    d.rectangle([35,34,36,40],fill=SH); d.rectangle([58,34,59,40],fill=SH)
    # head: squared jaw, lit from the left
    d.rectangle([37,23,57,44],fill=SK)
    d.polygon([(37,44),(57,44),(57,47),(55,51),(51,52),(43,52),(39,51),(37,47)],fill=SK)
    d.rectangle([54,26,57,45],fill=SH)
    # clean-shaven: plain skin jaw, light shade on the right only
    d.rectangle([54,26,57,45],fill=SH)
    d.polygon([(54,46),(57,46),(55,51),(54,51)],fill=SH)
    # hair: short, smooth, side-swept; one highlight on the top edge
    d.rectangle([38,18,56,22],fill=HAIR)
    d.rectangle([40,17,55,17],fill=HAIR)
    d.rectangle([43,16,53,16],fill=HAIR)
    d.rectangle([37,22,38,27],fill=HAIR); d.rectangle([56,22,57,27],fill=HAIR)
    d.rectangle([38,23,56,23],fill=HAIR)
    d.rectangle([38,24,44,24],fill=HAIR)   # fringe swept from the left part
    d.line([(46,16),(51,16)],fill=MID)
    # eyes: one solid dark block each under a level soft brow
    for lx in (39,50):
        d.rectangle([lx,30,lx+5,30],fill=MID)             # brow, level
        d.rectangle([lx+1,32,lx+4,33],fill=HAIR)          # eye block 4x2
    d.rectangle([46,38,48,42],fill=SH)
    # mouth: flat calm line, right end stepped up one px
    d.rectangle([44,47,49,47],fill=HAIR)
    d.rectangle([50,46,51,46],fill=HAIR)
    # desk
    d.rectangle([2,80,93,93],fill=WOOD)
    d.line([(2,80),(93,80)],fill=AM); d.line([(2,81),(93,81)],fill=DA)
    d.line([(2,86),(93,86)],fill=DK)
    d.rectangle([1,1,94,94],outline=CR)  # restore panel frame
    # mug on desk surface
    d.rectangle([70,68,80,79],fill=BG,outline=CR)
    d.rectangle([72,69,78,71],fill=DA)
    d.rectangle([81,70,84,76],outline=CR)
    # steam (gentle)
    for c,(sx,ph) in enumerate([(72,0),(75,4),(78,2)]):
        for k in range(2):
            u=((t*0.5+k*6+ph*0.7)%12)
            y=66-u*0.9; x=sx+round(1.4*math.sin((u+ph)/2.2))
            col=AM if u<8 else DA
            if u<11: d.rectangle([x,round(y),x+1,round(y)+2],fill=col)
    # portrait panel only; Recent/Topics are separate HTML boxes beside it in home.html
    I=L.crop((1,1,95,95)).resize((W,H),Image.NEAREST)  # exactly the frame, flush with the HTML boxes
    return I
fr=[frame(t) for t in range(N)]
import os; out=os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..')),'static')+'/'
pal=[f.quantize(colors=8,method=Image.MEDIANCUT,dither=Image.NONE) for f in fr]
fr[0].save(out+'portrait-hero.png')
fr[0].convert('P',palette=Image.ADAPTIVE,colors=8).save(out+'portrait-hero.png',optimize=True)
pal[0].save(out+'portrait-hero.gif',save_all=True,append_images=pal[1:],duration=[160 if t in (60,61,62) else 125 for t in range(N)],loop=0,disposal=1)
pass
