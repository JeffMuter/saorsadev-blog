"""Oggie favicon: 16x16 hand-authored grid (left half, mirrored), nearest-neighbour to 64x64."""
from PIL import Image
import os
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
C={'O':(34,20,4),'G':(255,176,0),'g':(201,133,0),'E':(255,227,160),'k':(34,20,4),
   'Q':(138,90,0),'f':(255,227,160),'M':(34,20,4)}
HALF=[
"........",
"QQ..OOO.",
"QfQOEEEO",
"QffOEkEO",
"QfffGGGG",
"QfffGGGG",
"QQffMMMM",
".QfQGGGG",
"..QOGGGG",
"...OGGGG",
"...OGGGG",
"....OGGG",
"....gOOO",
"........",
"........",
"........",
]
HALF=["........"]+HALF[:-1]
def build(scale=4):
    im=Image.new('RGBA',(16,16),(0,0,0,0))
    for y,r in enumerate(HALF):
        row=r+r[::-1]
        for x,ch in enumerate(row):
            if ch!='.': im.putpixel((x,y),C[ch]+(255,))
    return im.resize((16*scale,16*scale),Image.NEAREST)
if __name__=='__main__':
    build().save(os.path.join(ROOT,'static','favicon.png'))
