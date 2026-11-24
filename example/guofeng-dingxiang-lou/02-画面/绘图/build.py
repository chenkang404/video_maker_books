"""Code-drawn Chinese costume animation. Run with the user's llm_new Python."""
from pathlib import Path
import json, math, re, shutil
import numpy as np
import soundfile as sf

P=Path(__file__).resolve().parent
ROOT=P.parents[2]
A=P/'assets'; C=P/'compositions'
A.mkdir(exist_ok=True); C.mkdir(exist_ok=True); (A/'fonts').mkdir(exist_ok=True)
OLD=ROOT/'generated_video/贾队长-慌啥子嘛-客栈录音室/project/assets'
shutil.copyfile(OLD/'gsap.min.js',A/'gsap.min.js')
shutil.copyfile('/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc',A/'fonts/serif.ttc')
shutil.copyfile(ROOT/'generated_audio/贾队长-慌啥子嘛-客栈录音室/贾队长-慌啥子嘛-清唱开场接伴奏.wav',A/'song.wav')
w,sr=sf.read(ROOT/'generated_audio/贾队长-慌啥子嘛-客栈录音室/口型驱动-清唱.wav')
if w.ndim>1:w=w.mean(axis=1)
activity=[]
for i in range(math.ceil(36.3*12)):
 a=w[int(i*sr/12):int((i+1)*sr/12)]
 activity.append(float(np.sqrt(np.mean(a*a))) if len(a) else 0.)
(A/'activity.json').write_text(json.dumps([round(v,5) for v in activity]))

def path(d,fill='none',stroke='#302b28',width=1.4,extra=''):
 return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'
def rect(x,y,w,h,fill,stroke='none',width=1,extra=''):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" {extra}/>'
def ellipse(x,y,rx,ry,fill,stroke='none',width=1,extra=''):
 return f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" {extra}/>'
def text(x,y,t,size=20,fill='#eee0b7',extra=''):
 return f'<text x="{x}" y="{y}" font-family="Guofeng" font-size="{size}" fill="{fill}" {extra}>{t}</text>'
def group(content,extra=''):
 return f'<g {extra}>{content}</g>'

DEFS='''<defs>
<linearGradient id="wall" x2="0.8" y2="1"><stop stop-color="#d2b993"/><stop offset=".6" stop-color="#a28a6b"/><stop offset="1" stop-color="#6e6454"/></linearGradient>
<linearGradient id="wood" x2="1" y2="0"><stop stop-color="#352f29"/><stop offset=".42" stop-color="#72533b"/><stop offset=".7" stop-color="#5d4433"/><stop offset="1" stop-color="#2f302b"/></linearGradient>
<linearGradient id="floor" x2=".1" y2="1"><stop stop-color="#877153"/><stop offset="1" stop-color="#3f443c"/></linearGradient>
<linearGradient id="window" x2=".5" y2="1"><stop stop-color="#90a9a1"/><stop offset=".5" stop-color="#b1bbb0"/><stop offset="1" stop-color="#7b9690"/></linearGradient>
<linearGradient id="robe" x2="1" y2=".25"><stop stop-color="#11191b"/><stop offset=".30" stop-color="#242c2e"/><stop offset=".53" stop-color="#191f22"/><stop offset=".84" stop-color="#2a3030"/><stop offset="1" stop-color="#121b1d"/></linearGradient>
<linearGradient id="skin" x2="1" y2=".3"><stop stop-color="#bd8965"/><stop offset=".42" stop-color="#e1b98e"/><stop offset=".75" stop-color="#d6a77d"/><stop offset="1" stop-color="#a67456"/></linearGradient>
<linearGradient id="leather" x2="1" y2=".3"><stop stop-color="#30241e"/><stop offset=".45" stop-color="#76523a"/><stop offset="1" stop-color="#412d24"/></linearGradient>
<radialGradient id="lamp"><stop stop-color="#fff0b3"/><stop offset=".65" stop-color="#d6a45d"/><stop offset="1" stop-color="#ac6939"/></radialGradient>
<linearGradient id="fade" x2="0" y2="1"><stop stop-color="#182824" stop-opacity="0"/><stop offset="1" stop-color="#17241f" stop-opacity=".66"/></linearGradient>
<pattern id="paper" width="85" height="89" patternUnits="userSpaceOnUse"><path d="M3 17l14 2m25 32l8-1m17 19l10 1M14 78l7-2M59 10l9 2" stroke="#f7e4bd" opacity=".11" stroke-width=".5"/><path d="M21 37l13 1m17 38l4-1" stroke="#433e31" opacity=".08" stroke-width=".6"/></pattern>
<pattern id="silk" width="17" height="21" patternUnits="userSpaceOnUse"><path d="M2 2l3 8m7 0l-2 8" stroke="#b8baa2" opacity=".035" stroke-width=".6"/></pattern>
<clipPath id="windowClip"><path d="M350 243Q416 212 492 244V599H350Z"/></clipPath>
</defs>'''

def lantern(x,y,scale=1):
 s=path('M0 -75V-12',stroke='#514232',width=2)
 s+=path('M-17 -15Q0 -22 17 -15L22 2Q35 37 20 64Q0 76 -20 64Q-35 37 -22 2Z','url(#lamp)','#795338',1.5)
 for dx in [-17,-9,0,9,17]:
  s+=path(f'M{dx} -12 Q{dx*1.6} 27 {dx} 66',stroke='#9a5d36',width=.8,extra='opacity=".6"')
 s+=path('M-17 -13H17M-21 64H21',stroke='#73412e',width=4)
 s+=path('M0 69V88',stroke='#764230',width=3)
 for dx in [-4,-2,0,2,4]:s+=path(f'M{dx} 86L{dx+1} 109',stroke='#9d4b32',width=1)
 return group(s,f'transform="translate({x} {y}) scale({scale})" class="lantern"')

def background():
 b=rect(0,0,540,960,'url(#wall)')
 # Broad plaster washes are shapes rather than image filters.
 b+=path('M0 204Q170 125 318 225T540 178V404Q295 343 0 474Z','#d9c8a7','none',extra='opacity=".28"')
 b+=path('M10 677Q119 603 204 681T540 639V839H0Z','#4f6258','none',extra='opacity=".18"')
 # Window: distant mountains, moon, bamboo beyond wooden lattice.
 sky=rect(341,220,160,390,'url(#window)')
 sky+=ellipse(444,295,24,24,'#e4dbc0')
 sky+=path('M340 472L367 402 393 427 431 367 464 411 499 385V610H340Z','#6e8b84','none')
 sky+=path('M340 506Q399 423 431 462T500 461V607H340Z','#54746d','none')
 sky+=path('M350 555Q406 497 499 522V610H350Z','#3f645d','none')
 for x0,y0 in [(476,515),(462,574),(390,544)]:
  sky+=path(f'M{x0} 590Q{x0-8} {y0-45} {x0+4} {y0-100}',stroke='#3e5e50',width=2)
  for k in range(3):
   yy=y0-k*21
   sky+=path(f'M{x0-1} {yy}q-28-34-31-23q10 24 31 23m0 0q26-32 31-27q-5 23-31 27','#3f6150','none')
 b+=group(sky,'clip-path="url(#windowClip)"')
 b+=path('M346 240Q418 209 496 241V604H346Z','none','#514632',7)
 b+=path('M353 247Q420 220 489 247V596H353Z','none','#c1a270',2)
 for x in [372,404,436,468]:b+=path(f'M{x} 239V598',stroke='#645339',width=4)
 for y in [272,313,354,395,436,477,518,559]:
  b+=path(f'M350 {y}H492',stroke='#69563b',width=3)
 for x in [373,405,437,469]:
  for y in [275,357,439,521]:b+=path(f'M{x} {y}l15 17-15 17-15-17Z',stroke='#84714f',width=1.6)
 b+=rect(337,606,169,13,'#8b704c','#554632',1.5)
 # Recessed display cabinet and porcelain.
 b+=rect(45,296,111,312,'#4d4c3b','#5d4934',4)
 b+=rect(52,302,97,301,'#77715a')
 for y in [381,478,588]:
  b+=rect(45,y,111,8,'#b49764','#57432f',1)
 for x,y,sc in [(78,378,.8),(126,377,.58),(87,474,1),(127,474,.7),(71,583,.7),(121,583,1.0)]:
  v=path('M-9 0Q-17-21-9-31L-4-39V-45H5V-39L10-31Q18-17 9 0Z','#b9c5aa','#526c60',1.2)
  v+=path('M-11-21Q0-15 12-21M-9-11Q2-18 12-10',stroke='#5e8273',width=2)
  v+=ellipse(0,-44,5,1.6,'#778d7a')
  b+=group(v,f'transform="translate({x} {y}) scale({sc})"')
 # Scroll painting to the left of the actor.
 b+=rect(169,293,63,241,'#66533c')+rect(175,300,51,224,'#d0c19c')
 b+=path('M179 485L189 423 198 454 211 371 222 465V509H179Z','#88947b','none',extra='opacity=".65"')
 b+=path('M182 505Q196 477 220 492',stroke='#596e5d',width=2)
 for x,y in [(191,376),(207,336),(219,402)]:b+=path(f'M{x} {y}q-8-12-10-2q-2 10 10 2q11-14 12-3q-2 10-12 3','#687d67','none')
 b+=path('M167 295H234M168 531H233',stroke='#403d2d',width=5)
 # Timber pillars and beams, with restrained carved brackets.
 for x in [13,310,510]:
  width=19 if x==310 else 25
  b+=rect(x,0,width,735,'url(#wood)','#332f27',2)
  b+=path(f'M{x+4} 0V730',stroke='#b38a57',width=1.5,extra='opacity=".5"')
  for i in range(4):
   yy=242+i*103
   b+=path(f'M{x+8} {yy}q-5 27 0 42t1 45',stroke='#282d27',width=.7,extra='opacity=".35"')
 for y,h in [(42,34),(197,22),(691,14)]:
  b+=rect(0,y,540,h,'url(#wood)','#332e26',2)
  b+=path(f'M0 {y+5}H540',stroke='#b08858',width=1.3)
 for x in [34,302,509]:
  b+=path(f'M{x} 218h55q-3 15-21 16q-1 19-16 21q-1-22-18-26Z','#5e5038','#3d3829',1.5)
 # Architectural sign, calligraphy is part of the set.
 b+=path('M139 99L405 99 415 113 410 171 140 174 130 162 132 111Z','#443d2c','#272d24',2.5)
 b+=path('M142 106L399 106 405 114 402 164 145 165 138 158 140 114Z','none','#b09357',1.4)
 b+=text(273,151,'鼎 香 楼',37,'#e1ce94','text-anchor="middle" letter-spacing="6" data-layout-ignore="true"')
 b+=ellipse(150,134,3,3,'#ac7a42')+ellipse(392,132,3,3,'#ac7a42')
 # Floor perspective and daylight.
 b+=rect(0,709,540,251,'url(#floor)')
 for yy in [738,779,834,904]:b+=path(f'M0 {yy}Q270 {yy-10} 540 {yy}',stroke='#4e4d3b',width=1.6)
 for xx in [-200,-80,40,160,280,400,520,640,760]:b+=path(f'M{270+(xx-270)*.43} 709L{xx} 960',stroke='#474a3b',width=1.4)
 b+=path('M350 612L489 613 540 809 367 787Z','#d5c494','none',extra='opacity=".13"')
 # Left table and stool, stable contact with the floor.
 b+=path('M-24 721L153 713 187 747 0 766Z','#947b51','#3f4030',2)
 b+=path('M0 760L181 742V758L0 781Z','#544d35','#36392c',2)
 b+=path('M17 780L25 914 36 918 39 778M142 765L150 869 163 873 165 761','#514b36','#34392b',2)
 b+=path('M11 831L152 823',stroke='#60583d',width=7)
 b+=ellipse(81,729,38,10,'#574e37')
 pot=path('M-15 0Q-25-29-9-35Q9-41 20-24L27-18 40-28 44-22 33-8 20-3Q9 7-15 0Z','#91a88e','#3e594d',1.4)
 pot+=path('M-16-29Q-39-42-35-16Q-32-7-22-11','none','#658775',5)
 pot+=path('M-8-35Q-3-43 6-36',stroke='#4a6755',width=3)
 pot+=path('M-10-19Q-4-29 1-18T12-19',stroke='#607e69',width=1.3)
 b+=group(pot,'transform="translate(83 719) scale(.85)"')
 for x,y in [(135,735),(35,735)]:
  b+=ellipse(x,y,13,4,'#7d8b70','#3a5549',1)+path(f'M{x-9} {y-11}Q{x-10} {y+4} {x} {y+3}Q{x+10} {y+3} {x+9} {y-11}Z','#c2ceb1','#536d5c',1)+ellipse(x,y-11,9,3,'#758d73','#476152',1)
 b+=group(path('M89 684C75 674 97 664 84 650M96 686C109 670 90 663 102 647',stroke='#e6debc',width=1.5),'class="steam" opacity=".45"')
 # Right lower foreground peony arrangement.
 branch=path('M513 931Q487 844 505 721M492 866Q457 832 448 794M500 813Q521 786 533 769',stroke='#424f37',width=3)
 for x,y,ang in [(497,826,-35),(484,852,25),(456,812,-35),(513,788,30),(501,761,-25)]:
  branch+=group(path('M0 0Q-28-6-24-25Q-4-23 0 0Z','#536849','#374b35',.7)+path('M-3-4L-20-21',stroke='#87926b',width=.7),f'transform="translate({x} {y}) rotate({ang})"')
 for x,y,sc in [(505,724,1),(449,791,.68),(535,768,.6)]:
  flower=''
  for angle in range(0,360,45):
   flower+=group(ellipse(0,-11,9,16,'#bd826f','#8a5b4e',.8),f'transform="rotate({angle})"')
  flower+=ellipse(0,0,8,8,'#cfb177','#9a8158',1)
  branch+=group(flower,f'transform="translate({x} {y}) scale({sc})"')
 b+=group(branch,'class="flowers"')
 b+=lantern(73,230,.72)+lantern(465,157,.83)
 b+=rect(0,0,540,960,'url(#paper)')
 return b

def head():
 # Skull top -202 to chin -24 is one head. Neck below it is 0.3 of that, then widens into the collar.
 h=path('M-46-148Q-56-154-52-132Q-50-116-40-116M38-146Q50-154 46-132Q44-116 36-118','url(#skin)','#634e3c',1.1)
 h+=path('M-42-172Q-48-154-44-134Q-46-116-40-102Q-34-86-30-72Q-26-58-24-46Q-22-34-21-24Q-19-6-17 8Q-24 22-32 32L-34 78H34L32 32Q24 22 17 8Q19-6 21-24Q22-34 24-46Q26-58 30-72Q36-96 38-116Q44-138 38-160L32-174Q6-202-42-172Z','url(#skin)','#674e3c',1.4)
 h+=path('M-38-132Q-40-108-28-90L-16-80Q-32-98-30-124Z','#a87858','none',extra='opacity=".55"')
 h+=path('M30-134Q38-108 24-90L12-78Q28-96 32-122Z','#9a6e52','none',extra='opacity=".5"')
 # Hair follows the narrower skull, keeping the side part.
 h+=path('M-44-138Q-50-158-46-180Q-44-208-20-218Q-2-224 8-218Q28-222 42-198Q50-178 42-150L36-138 32-172Q14-180 6-206Q-6-176-34-166L-38-136Z','#172328','#1e2928',1.4)
 h+=path('M6-210Q-6-186-38-174M12-208Q22-188 40-178M-2-212Q-20-208-38-184',stroke='#50605c',width=1.1)
 h+=path('M-36-198Q-16-216 2-212M22-204Q36-196 42-184',stroke='#6e7770',width=.65)
 h+=path('M-46-158L-40-128M40-154L36-126',stroke='#18272a',width=3.4)
 h+=path('M-36-128Q-24-122-12-128M10-127Q22-122 32-130',stroke='#a77a5a',width=2)
 eyes=path('M-38-138Q-25-145-12-137Q-24-127-37-135Z','#e6d0ac','#634b39',1.1)
 eyes+=path('M10-137Q22-146 34-138Q23-128 11-134Z','#e7d1af','#634b39',1.1)
 eyes+=ellipse(-22,-136,3.2,4.6,'#292f2a')+ellipse(21,-137,3.1,4.6,'#292f2a')
 eyes+=ellipse(-21,-138,1,1,'#fcf0d2')+ellipse(22,-139,1,1,'#fcf0d2')
 h+=group(eyes,'class="eyes"')
 lids=path('M-38-137Q-25-130-12-137M10-136Q22-130 34-138',stroke='#624735',width=2)
 h+=group(lids,'class="lids" opacity="0"')
 h+=path('M-38-148Q-24-155-10-148Q-22-148-34-144Z','#36332a','none')
 h+=path('M10-149Q22-156 34-149L32-145Q22-150 12-146Z','#36332a','none')
 h+=path('M-30-158Q-16-161-6-157M10-160Q22-163 30-159M-42-140l-3-3M36-139l5-4',stroke='#b0815f',width=.75)
 h+=path('M-1-136Q-8-118-8-106Q-4-100 4-103M7-128L11-108Q18-101 11-99M-6-101Q1-96 9-101',stroke='#91674b',width=1.35)
 h+=path('M0-131Q-3-112 0-109',stroke='#edc79b',width=1.6)
 h+=path('M-14-108Q-20-94-16-80M16-108Q22-94 18-80',stroke='#ac7c5b',width=1.1)
 h+=path('M-1-92Q-10-92-16-82Q-8-82 0-87L3-85Q11-80 18-82Q12-92 5-92L2-90Z','#443a2d','none')
 for x in [-11,-8,-4,7,10,13]:h+=path(f'M{x}-88l-2 5',stroke='#75604a',width=.55)
 h+=path('M-14-74Q2-70 16-74',stroke='#674738',width=1.4)
 mouth=ellipse(2,-68,10,4.2,'#54392e','#78503c',.7)
 mouth+=path('M-5-71Q3-73 10-71L8-68H-4Z','#e1c6a0','none')
 mouth+=ellipse(3,-66,5,1.4,'#a36d58')
 h+=group(mouth,'class="mouth" opacity="0"')
 h+=path('M-6-60Q3-57 12-61',stroke='#ae805d',width=1)
 h+=path('M-46-138q-7-6-3 7M40-138q6-5 3 8',stroke='#986c50',width=1)
 clipped=f'<defs><clipPath id="headclip"><path d="M-150-260H150V14L34 32Q14 46 2 48Q-8 46-34 32L-150 14Z"/></clipPath></defs>'
 clipped+=group(h,'clip-path="url(#headclip)"')
 clipped+=path('M-32 32Q-8 46 2 48Q14 46 32 32',stroke='#c0bea6',width=2.4)
 # Scale onto the 7.5-head grid: skull at -210, chin at -126, collar at -101.
 return group(group(clipped,'transform="translate(0 -210) scale(0.4704) translate(0 202)"'),'class="head"')

def character():
 # 7.5 heads from skull -210 to sole 418. Neck 0.3 head, shoulders about 2 head-widths.
 ch=ellipse(1,424,40,8,'#23352e',extra='opacity=".35"')
 ch+=path('M-30 398L-36 416Q-28 426-10 422L-6 398Z','#1c2829','#24332e',1.4)
 ch+=path('M10 398L14 422Q32 426 38 416L32 398Z','#1b2829','#24332e',1.4)
 body=path('M-14-106Q-32-102-44-86Q-50-48-32 8Q-26 41-24 72Q-27 100-26 125Q-24 198-22 271Q-24 340-34 402Q-8 416 2 416Q16 416 36 402Q28 340 26 271Q28 198 28 125Q30 100 26 72Q28 41 34 8Q50-48 44-86Q32-102 14-106Z','url(#robe)','#1f2c2b',2)
 body+=path('M-24 34Q0 28 26 34L24 52Q0 58-24 52Z','#10181a','#2c3836',1.2)
 body+=path('M2-70Q4 80 2 400',stroke='#668076',width=1.1,extra='opacity=".55"')
 body+=path('M-30 20Q-26 90-28 160L-32 250Q-24 150-22 80Z','#334a4c','none',extra='opacity=".7"')
 body+=path('M-16 90Q-4 180-14 300L-20 390Q-6 200-18 120Z','#101f27','none')
 body+=path('M22 40Q16 140 26 240L32 340 24 346Q12 220 16 120Z','#3b4c4a','none',extra='opacity=".7"')
 for d in ['M-28 60Q-20 100-24 150','M-22 180Q-24 260-20 340','M-4 80Q4 120 0 180','M20 150Q14 200 18 250','M0 240Q-4 320 0 390','M-30 390Q2 402 32 388']:
  body+=path(d,stroke='#62746a',width=.85,extra='opacity=".5"')
 for yy in [8,48,88,128]:
  body+=path(f'M2 {yy}q4-3 7 0q-2 4-6 1',stroke='#8d9680',width=1.2)
 # Strap from the raised-arm shoulder down to the holster at the opposite hip.
 body+=path('M30-96L44-84Q18 10-8 150L-22 158Q2 20 18-88Z','url(#leather)','#2c2b23',1.5)
 body+=path('M34-90Q14 20-16 154M42-82Q20 24-6 150',stroke='#b18a56',width=.7)
 body+=path('M-2 78L12 84 8 102-6 96Z','#aa8b50','#433b28',1.2)+path('M1 84L8 88 5 98-2 94Z','#423a2e','#c0a267',1)
 holster=path('M-3-22L16-23 21-2 9 5-6-3Z','#3a3430','#202926',1.3)
 holster+=path('M1-24L15-25 16-21 1-19Z','#6d5a40','#302d23',1)
 for y in [-17,-13,-9]:holster+=path(f'M1 {y}l12-2',stroke='#827052',width=1)
 holster+=path('M-22-2L22-5 29 18 21 84Q3 92-19 81L-29 18Z','url(#leather)','#2c2b23',2)
 holster+=path('M-29 5Q-4-9 25 0L23 24Q-1 38-26 24Z','#6e5037','#342e23',1.3)
 holster+=path('M-22 33L-15 75Q2 84 16 76L22 34',stroke='#b18b59',width=.8)
 holster+=ellipse(-1,20,3,3,'#a68c52','#3c3525',.8)
 body+=group(holster,'transform="translate(-6 168) rotate(8) scale(.82)"')
 body+=path('M18-102Q46-112 62-74L50-28Q30-64 12-94Z','url(#robe)','#1b2c2b',1.6)
 sleeve=path('M43-1Q70-3 86 34L107 90 84 122Q60 94 43 62L31 27Z','url(#robe)','#1b2c2b',2)
 sleeve+=path('M65 25Q72 59 97 88M53 45Q64 88 82 105',stroke='#647368',width=1,extra='opacity=".6"')
 sleeve+=path('M83 99L104 81 116 96 95 121Z','#b8b79e','#35483f',1.2)
 sleeve+=path('M95 102L107 94Q109 82 104 73Q102 66 106 65Q112 68 116 79L117 57Q118 49 122 53L125 77 128 52Q131 46 134 54L133 79 139 60Q143 55 145 61L139 88Q153 82 157 87Q158 91 145 99L128 114Q113 121 101 111Z','url(#skin)','#795a40',1.1)
 sleeve+=path('M110 94Q124 87 133 97M123 84l2 10M134 84l-2 9',stroke='#aa7c56',width=.8)
 body+=group(group(sleeve,'transform="translate(-16 -102)"'),'class="gesture"')
 body+=path('M-16-98Q-50-92-56-36L-48 48Q-34 78-22 86L-12 62Q-28 28-22-30Q-18-78-10-96Z','url(#robe)','#1b2c2b',1.6)
 body+=group(path('M-62 108L-46 102-38 114-50 126Z','#c2c0a6','#38473d',1.2)+path('M-50 116Q-48 104-40 108L-32 118-22 122Q-16 126-20 128L-32 126-26 134Q-24 138-28 138L-40 132Q-52 130-50 116Z','url(#skin)','#76573e',1.1),'transform="translate(4 -28)"')
 body+=head()
 ch+=group(body,'class="body"')
 return group(ch,'transform="translate(278 454)"')

BG=background(); ACTOR=character()
(A/'鼎香楼.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 540 960">{DEFS}{BG}</svg>')
(A/'贾队长.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 540 960">{DEFS}{ACTOR}</svg>')

# Compose five editorial framings; all drawings remain vector-native.
shots=[('intro',0,4.5,1.32,-5,80,1.37,-8,91),('room',4.5,7.78,1.0,0,0,1.035,-3,1),('verse',12.28,7.48,1.20,14,42,1.25,11,54),('refrain',19.76,7.42,1.15,-25,35,1.19,-21,42),('end',27.18,9.12,1.055,0,8,1.0,0,0)]
hosts=[]
for sid,start,dur,z,x,y,z2,x2,y2 in shots:
 svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 540 960" aria-label="黑袍贾队长在国风鼎香楼演唱"><g class="world">{DEFS}{BG}{ACTOR}</g></svg>'
 # Prefix definition IDs in each inline SVG to prevent cross-scene collisions.
 svg=re.sub(r'id="([^"]+)"',lambda m:f'id="{sid}-{m[1]}"',svg)
 svg=re.sub(r'url\(#([^)]+)\)',lambda m:f'url(#{sid}-{m[1]})',svg)
 events=[];last=None
 for i,r in enumerate(activity):
  t=i/12-start
  if 0<=t<dur:
   state=0 if r<.021 else (0.48 if r<.05 else (0.8 if r<.11 else 1.05))
   if i%7==0:state*=.3
   if state!=last:
    events.append(f'tl.set("#{sid}-scene .mouth",{{opacity:{int(state>0)},scaleY:{max(.12,state):.2f}}},{t:.4f});');last=state
 blink=[]
 for t in [1.55,4.1,6.4,8.45]:
  if t+.16<dur:blink.append(f'tl.set("#{sid}-scene .eyes",{{opacity:0}},{t});tl.set("#{sid}-scene .lids",{{opacity:1}},{t});tl.set("#{sid}-scene .eyes",{{opacity:1}},{t+.16});tl.set("#{sid}-scene .lids",{{opacity:0}},{t+.16});')
 html=f'''<template>
<style>
@font-face{{font-family:Guofeng;src:url('assets/fonts/serif.ttc')}}
#root{{position:absolute;inset:0;overflow:hidden;background:#aa9678}}
#{sid}-scene{{position:absolute;inset:0}}svg{{display:block;width:100%;height:100%}}
</style>
<div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920" data-duration="{dur}"><div id="{sid}-scene" data-layout-allow-overflow="true">{svg}</div></div>
<script>
const tl=gsap.timeline({{paused:true}});
tl.set("#{sid}-scene .world",{{svgOrigin:"270 480",scale:{z},x:{x},y:{y}}},0);
tl.to("#{sid}-scene .world",{{scale:{z2},x:{x2},y:{y2},duration:{dur-.05},ease:"sine.inOut"}},0);
tl.set("#{sid}-scene .body",{{svgOrigin:"278 872"}},0);
tl.to("#{sid}-scene .body",{{rotation:.7,y:-1.3,duration:1.65,yoyo:true,repeat:{math.ceil(dur/1.65)},ease:"sine.inOut"}},0);
tl.set("#{sid}-scene .head",{{svgOrigin:"278 340"}},0);
tl.fromTo("#{sid}-scene .head",{{rotation:-1.0}},{{rotation:1.5,duration:1.85,yoyo:true,repeat:{math.ceil(dur/1.85)},ease:"sine.inOut"}},.16);
tl.set("#{sid}-scene .gesture",{{svgOrigin:"305 351"}},0);
tl.fromTo("#{sid}-scene .gesture",{{rotation:7}},{{rotation:-7,duration:2.1,yoyo:true,repeat:{math.ceil(dur/2.1)},ease:"sine.inOut"}},.35);
tl.set("#{sid}-scene .mouth",{{svgOrigin:"279 307"}},0);
tl.fromTo("#{sid}-scene .steam",{{y:3,opacity:.25}},{{y:-7,opacity:.55,duration:2.8,yoyo:true,repeat:{math.ceil(dur/2.8)},ease:"sine.inOut"}},0);
{''.join(events)}{''.join(blink)}
window.__timelines["{sid}"]=tl;
</script></template>'''
 (C/f'{sid}.html').write_text(html)
 hosts.append(f'<section id="{sid}" class="clip" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" data-start="{start}" data-duration="{dur}" data-track-index="0" data-track-kind="graphics"></section>')

# Three small caption chapters avoid overly dense lanes while remaining editable.
lines=[(.35,3.95,'慌啥子嘛，慢慢来'),(4.88,8.56,'慌啥子嘛，慢慢来'),(8.56,12.28,'太阳下山有月亮爬上来'),(12.28,16.04,'云会散，花会开'),(16.04,19.76,'好运总会为你而等待'),(19.76,23.34,'慌啥子嘛，慢慢来'),(23.34,27.18,'每个人都有自己的节拍'),(27.18,31.18,'得不到，就放开'),(31.18,35.9,'一切都是最好的安排')]
caption_hosts=[]
for j,subset in enumerate([lines[:3],lines[3:6],lines[6:]]):
 sid=f'lyrics{j}';start=0 if j==0 else subset[0][0];end=subset[-1][1];dur=end-start
 tags=''.join(f'<div id="{sid}-{k}" class="clip line" data-start="{a-start:.4f}" data-duration="{b-a:.4f}" data-track-index="0"><span>{t}</span></div>' for k,(a,b,t) in enumerate(subset))
 (C/f'{sid}.html').write_text(f'''<template><style>@font-face{{font-family:Guofeng;src:url('assets/fonts/serif.ttc')}}#root{{position:absolute;inset:0;pointer-events:none}}.line{{position:absolute;inset:0;display:flex;align-items:flex-start;justify-content:center;padding-top:1128px;padding-left:110px;padding-right:160px;box-sizing:border-box}}.line span{{font:700 49px/1.45 Guofeng;color:#fff0c9;white-space:nowrap;padding:15px 26px;background:#23352fef;border-top:2px solid #ad9866;border-bottom:2px solid #ad9866}}</style><div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920" data-duration="{dur}">{tags}</div><script>const tl=gsap.timeline({{paused:true}});window.__timelines["{sid}"]=tl;</script></template>''')
 caption_hosts.append(f'<section id="{sid}" class="clip" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" data-start="{start}" data-duration="{dur}" data-track-index="0" data-track-kind="captions"></section>')
(C/'lyrics.html').write_text('<template><style>#root{position:absolute;inset:0;pointer-events:none}</style><div id="root" data-composition-id="lyrics" data-width="1080" data-height="1920" data-duration="36.3">'+''.join(caption_hosts)+'</div><script>const tl=gsap.timeline({paused:true});window.__timelines["lyrics"]=tl;</script></template>')
hosts.append('<section id="lyrics" class="clip" data-composition-id="lyrics" data-composition-src="compositions/lyrics.html" data-start="0" data-duration="36.3" data-track-index="1" data-track-kind="captions"></section>')
# Place the performance identification in the video, not technical implementation labels.
(P/'index.html').write_text('''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>鼎香楼 · 贾队长《慌啥子嘛》</title><script src="assets/gsap.min.js"></script><style>@font-face{font-family:Guofeng;src:url('assets/fonts/serif.ttc')}html,body{margin:0;width:100%;height:100%;background:#9b896b}#root{position:relative;width:100%;height:100%;overflow:hidden}.clip{position:absolute;inset:0}#signature{position:absolute;right:216px;top:444px;color:#f1e1b4;font:28px Guofeng;background:#26362eed;padding:10px 14px}#seal{position:absolute;left:125px;top:432px;writing-mode:vertical-rl;font:32px Guofeng;color:#f9e4c1;background:#864738;padding:16px 10px;border:2px solid #b78a63;letter-spacing:6px}</style></head><body><div id="root" data-composition-id="main" data-width="1080" data-height="1920" data-duration="36.3">'''+''.join(hosts)+'''<div id="signature"><span>AI翻唱</span></div><div id="seal">慢慢来</div><audio id="song" class="clip" src="assets/song.wav" data-start="0" data-duration="36.3" data-track-index="2" data-volume="1"></audio></div><script>const tl=gsap.timeline({paused:true});window.__timelines["main"]=tl;</script></body></html>''')
(P/'SPEC.md').write_text('''# 国风鼎香楼 · 制作规格

用户指定：代码实现，非像素国风，贾队长黑色长袍、斜挎王八盒子手枪，仍在鼎香楼唱《慌啥子嘛》。已有方案和“继续”授权下制作完整本地成片。

输出：1080×1920，24fps，36.3秒；H.264/AAC。
声音：复用原清唱开场接伴奏；0–3.95秒清唱、停顿至4.5秒、随后完整副歌。
美术：原生SVG贝塞尔曲线、1–2.5单位轮廓、局部渐变与手绘衣褶；540×960坐标映射到1080×1920。不是低分辨率像素放大。黑袍#191f22，皮革#76523a，灰绿窗#90a9a1，木梁#5d4433。
角色：7.5头身。头长从颅顶到下巴，不含头发。脖子约0.3头长，肩宽约2个头宽，腰窄于肩，胯约1.2个头宽，膝在大腿中段，脚落在地面。瘦长脸、窄下颌、无双下巴。分头、细胡子、黑长袍、棕色斜肩带、枪套中可见短枪柄；不持枪演出。手臂分层围绕肩旋转。
动作：清唱人声12Hz RMS驱动开口幅度，眨眼0.16秒，头部约±1.5度，抬手约±7度；没有全角度转身或打斗。
场景：木梁、雕花支撑、鼎香楼匾额、窗外山月与竹影、瓷瓶、挂画、灯笼、茶桌及牡丹。茶汽是代码图形动画。
镜头：0–4.5近景；4.5–12.28全景；12.28–19.76中景；19.76–27.18偏移中景；27.18–36.3回全景。
文字：本地思源宋体；歌词49px，y=1128px；AI翻唱标记位于444px。全部检查平台安全区。
禁用：像素风、图像生成模型、云端素材生成、现代录音室设备、发光粒子、强烈震屏、随机动画。
检查：所有机位中点、4.5秒切点、19.76秒切点、静音嘴形和尾帧；全片解码、音轨与源文件对比。
''')
(P/'BUILD.md').write_text('''# 本地代码制作

使用用户 `llm_new` Python 运行 `build.py`，复制既有音频并生成原生SVG、嘴形数据及HTML子合成；通过HyperFrames本地浏览器渲染。

无需图像/视频生成模型、API密钥或HeyGen登录。音频是已有AI翻唱素材，画面完全为代码绘制。剧照仅用于观察角色特征，没有拼贴照片进入画面。

`assets/鼎香楼.svg` 与 `assets/贾队长.svg` 是静态可编辑图形；HTML中嵌入相同图形供GSAP逐层动画。`build.py` 为生成源，重新运行会覆盖生成的HTML。
''')
print('Built vector art, five shots, nine lyrics and audio envelope:',len(activity))
