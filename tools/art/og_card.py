"""Link-preview card: full Oggie (frog + wings) centred on near-black, 1200x630.
Reuses static/oggie-v2.png, scaled with nearest-neighbour. Writes static/og-card.png."""
from PIL import Image
import os
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
BG=(11,11,8,255)
W,H=1200,630
SCALE=9
sprite=Image.open(os.path.join(ROOT,'static','oggie-v2.png')).convert('RGBA')
sprite=sprite.crop(sprite.getbbox())
sprite=sprite.resize((sprite.width*SCALE,sprite.height*SCALE),Image.NEAREST)
card=Image.new('RGBA',(W,H),BG)
card.alpha_composite(sprite,((W-sprite.width)//2,(H-sprite.height)//2))
card.convert('RGB').save(os.path.join(ROOT,'static','og-card.png'))
