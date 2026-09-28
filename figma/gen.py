"""Generates paste-into-Figma SVGs for TripUp: wireflow.svg, hifi-02-trip.svg, hifi-06-poll.svg."""
import html, os
OUT = os.path.dirname(__file__)
W, H = 393, 852
esc = html.escape

# ---------- primitives ----------
def rect(x,y,w,h,fill="none",stroke=None,r=0,sw=1,extra=""):
    s=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"'
    if stroke: s+=f' stroke="{stroke}" stroke-width="{sw}"'
    return s+f' {extra}/>'
def text(x,y,t,size=14,fill="#141414",font="Figtree",weight=400,anchor="start",style="normal",extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}" font-style="{style}" {extra}>{esc(t)}</text>')
def circle(cx,cy,r,fill,stroke=None,sw=1):
    s=f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"'
    if stroke: s+=f' stroke="{stroke}" stroke-width="{sw}"'
    return s+'/>'
def arrow_fwd(cx,cy,color="#fff",s=1):
    # material arrow_forward, simplified
    return (f'<path d="M{cx-6*s} {cy} h12 M{cx+1*s} {cy-5*s} l5 5 -5 5" fill="none" stroke="{color}" '
            f'stroke-width="{1.8*s}" stroke-linecap="round" stroke-linejoin="round"/>')
def arrow_back(cx,cy,color="#141414"):
    return (f'<path d="M{cx+7} {cy} h-14 M{cx-2} {cy-5} l-5 5 5 5" fill="none" stroke="{color}" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
def bell(cx,cy,color="#141414"):
    return (f'<path d="M{cx-6} {cy+3} v-5 a6 6 0 0 1 12 0 v5 l2 3 h-16 z M{cx-2} {cy+8} a2 2 0 0 0 4 0" '
            f'fill="none" stroke="{color}" stroke-width="1.6" stroke-linejoin="round"/>')
def share(cx,cy,color="#141414"):
    return (f'<path d="M{cx} {cy+2} v-12 M{cx-4} {cy-6} l4 -4 4 4 M{cx-7} {cy-2} h-1 v10 h16 v-10 h-1" '
            f'fill="none" stroke="{color}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>')
def g(x,y,inner,extra=""):
    return f'<g transform="translate({x},{y})" {extra}>{"".join(inner)}</g>'

AV = {"A":"#FFB48A","N":"#FFD9A8","M":"#BFE6D2","T":"#C9D8FF","S":"#F9C4DF","R":"#E8DDF5"}
def avatars(x,y,letters,size=26,ring="#F7F3EC",dim=()):
    out=[]; step=size-10
    for i,l in enumerate(letters):
        cx=x+i*step+size/2; cy=y+size/2
        op = ' opacity="0.45"' if l in dim else ''
        out.append(f'<g{op}>'+circle(cx,cy,size/2,AV[l],ring,2.5)+
                   text(cx,cy+size*0.17,l,size*0.42,"#141414","Figtree",700,"middle")+'</g>')
    return "".join(out)

def status_bar(dark=False):
    c="#fff" if dark else "#141414"
    return (text(34,40,"9:41",16,c,"Figtree",700)+rect(150,20,92,26,"#141414",r=13)+
            f'<path d="M318 38 h3 v-5 h-3z M323 38 h3 v-8 h-3z M328 38 h3 v-11 h-3z M333 38 h3 v-14 h-3z" fill="{c}"/>'
            +rect(344,27,22,11,"none",c,3.5,1.2)+rect(346,29,15,7,c,r=2)+rect(367,30,2,5,c,r=1))
def home_indicator(c="#141414"):
    return rect(129,838,135,5,c,r=3,extra='opacity="0.9"')

def pill(x,y,w,label,h=52):
    return (rect(x,y,w,h,"#141414",r=999,extra='filter="url(#pillsh)"')+
            text(x+22,y+h/2+5,label,15,"#fff","Figtree",700)+
            circle(x+w-14-14,y+h/2,14,"#fff")+arrow_fwd(x+w-28,y+h/2,"#141414"))
def chip(x,y,label,w=None,solid=False,icon=False):
    w = w or (len(label)*7.2+28+(20 if icon else 0))
    bg = "#141414" if solid else "none"; fg="#fff" if solid else "#141414"
    s = rect(x,y,w,34,bg,"#141414",999,1.5)
    tx = x+14
    if icon:
        s += rect(tx,y+11,12,12,"none",fg,2,1.5); tx+=20
    s += text(tx,y+22,label,13,fg,"Figtree",700)
    return s, w

def tabs(active):
    out=[rect(0,770,W,82,"#F7F3EC"), f'<line x1="0" y1="770" x2="{W}" y2="770" stroke="#EAE3D8"/>']
    names=["Trips","Polls","Plan","Money"]
    glyph=['M-9 4 l9 -9 9 9 v9 h-18z','M-9 -5 h18 v14 h-18z M-4 -9 h8 M0 -9 v6','M-9 -7 h18 v16 h-18z M-9 -2 h18','M-9 -6 h18 v14 h-18z M3 0 h6']
    for i,n in enumerate(names):
        cx = W/8*(2*i+1); on = n==active
        out.append(f'<path transform="translate({cx},{796})" d="{glyph[i]}" fill="{"#141414" if on else "none"}" stroke="#141414" stroke-width="1.6" stroke-linejoin="round"/>')
        out.append(text(cx,826,n,11,"#141414","Figtree",700 if on else 500,"middle"))
    return "".join(out)

DEFS = '''<defs>
<filter id="pillsh" x="-10%" y="-30%" width="120%" height="180%"><feDropShadow dx="0" dy="8" stdDeviation="9" flood-color="#141414" flood-opacity="0.18"/></filter>
<filter id="cardsh" x="-5%" y="-10%" width="110%" height="130%"><feDropShadow dx="0" dy="2" stdDeviation="5" flood-color="#141414" flood-opacity="0.04"/></filter>
<linearGradient id="lead" x1="0" x2="1"><stop offset="0" stop-color="#FF7A3D"/><stop offset="1" stop-color="#FF5CA8"/></linearGradient>
<linearGradient id="photo" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#D9C3A5"/><stop offset="1" stop-color="#8C7B66"/></linearGradient>
<linearGradient id="photo2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#E9B08A"/><stop offset="1" stop-color="#8A4A3A"/></linearGradient>
<linearGradient id="dim" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#141414" stop-opacity="0"/><stop offset="1" stop-color="#141414" stop-opacity="0.75"/></linearGradient>
</defs>'''

def photo(x,y,w,h,r,label,grad="photo"):
    return rect(x,y,w,h,f"url(#{grad})",r=r)+text(x+w/2,y+h/2+4,label,11,"#fff","Figtree",600,"middle",extra='opacity="0.8"')

def row(x,y,w,title,sub,icon_bg,icon_fg,icon_text,h=70):
    return (rect(x,y,w,h,"#fff",r=20,extra='filter="url(#cardsh)"')+
            circle(x+14+23,y+h/2,23,icon_bg)+text(x+37,y+h/2+5,icon_text,13,icon_fg,"Figtree",700,"middle")+
            text(x+72,y+h/2-4,title,15,"#141414","Figtree",700)+text(x+72,y+h/2+14,sub,13,"#8A837A")+
            circle(x+w-14-17,y+h/2,17,"#141414")+arrow_fwd(x+w-31,y+h/2,"#fff",0.9))

# ---------- HI-FI 02 ----------
def screen02():
    s=[rect(0,0,W,H,"#F7F3EC"),status_bar()]
    s+=[circle(30,80,17,"#fff"),arrow_back(30,80), circle(363,80,17,"#fff"),bell(363,80)]
    s+=[text(20,127,"Last night in",38,"#141414","Newsreader"),text(20,167,"Lisbon",38,"#8A837A","Newsreader")]
    # group photo card
    s+=[photo(20,188,353,96,20,""), rect(20,188,353,96,"url(#dim)",r=20)]
    s+=[text(34,258,"Nic",13,"#fff","Figtree",700), rect(58,247,68,15,"#fff",r=4,extra='opacity="0.92"'),
        text(92,258,"ORGANIZER",9,"#141414","Figtree",700,"middle",extra='letter-spacing="0.6"'),
        text(132,258,"· Ari · Maya · Theo · Sam",13,"#fff","Figtree",500)]
    s+=[text(34,232,"5 friends · Ren joins tonight",11,"#fff","Figtree",500,extra='opacity="0.8"')]
    s+=[avatars(232,214,"ANMTS",28,"#4a4038")]
    s+=[circle(232+5*18+14,228,14,"none","#fff",1.5,) .replace('stroke-width="1.5"','stroke-width="1.5" stroke-dasharray="3 3"'),
        text(232+5*18+14,233,"+",16,"#fff","Figtree",400,"middle")]
    # beige panel
    s+=[rect(20,296,353,140,"#F1EBE2",r=22),
        text(196,327,"Dinner tonight is still open",17,"#141414","Figtree",700,"middle"),
        text(196,349,"Three places from the group's wishlist, ready to poll.",13,"#5C5750","Figtree",400,"middle"),
        pill(36,368,321,"Start the poll")]
    s+=[text(20,472,"Today",17,"#141414","Figtree",700),text(373,472,"Full plan",13,"#8A837A","Figtree",400,"end")]
    y=486
    for t,sub,lab,ic,bg,fg in [("Torre de Belém","Sightseeing","10:00","10:00","#DDEFE4","#2F7D5B"),
                              ("LX Factory","Lunch","14:00","14:00","#FFE2C9","#E0562E")]:
        s+=[rect(20,y,353,70,"#fff",r=20,extra='filter="url(#cardsh)"'),circle(57,y+35,23,bg),
            text(57,y+39,ic,11,fg,"Figtree",700,"middle"),
            text(92,y+31,sub,13,"#8A837A"),text(92,y+50,t,15,"#141414","Figtree",700),
            circle(342,y+35,17,"#141414"),arrow_fwd(342,y+35,"#fff",0.9)]
        y+=82
    s+=[text(92,y-82+50+0,"",1)]
    # override LX meta
    s[-1]=text(92,y-82+50,"LX Factory",15,"#141414","Figtree",700)
    s.append(text(180,y-82+50,"",1))
    s+=[rect(20,y,353,70,"#fff",r=20,extra='filter="url(#cardsh)"'),circle(57,y+35,23,"#E3E9FF"),
        text(57,y+40,"€",15,"#3B5BB5","Figtree",700,"middle"),
        text(92,y+26,"Trip money",13,"#8A837A"),text(92,y+44,"You're owed €42",15,"#141414","Figtree",700),
        text(92,y+60,"Settle with Apple Pay or Revolut",12,"#8A837A"),
        circle(342,y+35,17,"#141414"),arrow_fwd(342,y+35,"#fff",0.9)]
    # LX sub-meta
    s+=[text(190,486+82+50,"",1)]
    s+=[tabs("Trips"),home_indicator()]
    return s

# ---------- HI-FI 06 ----------
def poll_option(y,name,meta,count,voters,pct,leading=False):
    s=[rect(20,y,353,96,"#fff","#FF9AA8" if leading else None,20,1.5,'filter="url(#cardsh)"')]
    s+=[photo(34,y+14,56,56,14,"",("photo2" if leading else "photo"))]
    s+=[text(102,y+34,name,15,"#141414","Figtree",700),text(102,y+52,meta,12,"#8A837A")]
    s+=[text(358,y+44,str(count),28,"#141414" if count else "#C4BDB2","Newsreader",400,"end")]
    if leading: s+=[text(358,y+60,"LEADING",10,"#E0562E","Figtree",700,"end",extra='letter-spacing="0.8"')]
    s+=[rect(34,y+76,325,5,"#F1EBE2",r=3)]
    if pct: s+=[rect(34,y+76,325*pct,5,"url(#lead)" if leading else "#C4BDB2",r=3)]
    s+=[text(359,y+92,voters,12,"#8A837A","Figtree",400,"end")]
    return "".join(s)

def screen06():
    s=[rect(0,0,W,H,"#F7F3EC"),status_bar()]
    s+=[circle(30,80,17,"#fff"),arrow_back(30,80), circle(363,80,17,"#fff"),share(363,80)]
    s+=[rect(20,110,353,132,"#fff",r=22,extra='filter="url(#cardsh)"'),circle(57,143,23,"#FFE2C9"),
        f'<path transform="translate(57,143)" d="M-5 -8 v16 M-8 -8 v5 a3 3 0 0 0 6 0 v-5 M4 -8 c-4 0 -4 8 0 8 v8" fill="none" stroke="#E0562E" stroke-width="1.8" stroke-linecap="round"/>',
        text(92,151,"Where for dinner?",26,"#141414","Newsreader")]
    s+=[text(34,187,"Tonight 19:30 · asked by Ari · ",13,"#8A837A"),text(34+178,187,"4 of 6 voted",13,"#141414","Figtree",700)]
    c1,w1=chip(34,200,"Share to chat",icon=True); c2,_=chip(34+w1+8,200,"Nudge Theo & Ren",icon=True); s+=[c1,c2]
    s+=[text(20,276,"Options",17,"#141414","Figtree",700)]
    s+=[poll_option(290,"Cervejaria Ramiro","Seafood · €€ · 12 min · open late",3,"You, Nic, Sam",0.62,True),
        poll_option(398,"Taberna da Rua das Flores","Petiscos · €€ · 6 min · no bookings",1,"Maya",0.2),
        poll_option(506,"Time Out Market","Food hall · € · 15 min",0,"No votes yet",0)]
    s+=[text(20,640,"Group",17,"#141414","Figtree",700),rect(20,654,353,58,"#fff",r=20,extra='filter="url(#cardsh)"'),
        avatars(34,670,"ANMSTR",26,"#fff",dim="TR"),
        text(164,678,"4 voted · ",13,"#8A837A"),text(164+58,678,"Theo and Ren",13,"#141414","Figtree",700),
        text(164,696,"haven't yet",13,"#8A837A")]
    s+=[text(20,732,"Closes when everyone has voted, or when you close it.",12,"#8A837A")]
    # sticky pill with fade
    s+=[rect(0,740,W,112,"#F7F3EC",extra='opacity="0.96"'),pill(20,760,353,"Close poll · Ramiro wins"),home_indicator()]
    return s

def svg(w,h,body,bg=None):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'+DEFS+
            (rect(0,0,w,h,bg) if bg else "")+"".join(body)+'</svg>')

def frame(name,body):  # a named group so Figma imports a frame
    return f'<g id="{esc(name)}"><clipPath id="c{abs(hash(name))}"><rect width="{W}" height="{H}" rx="44"/></clipPath><g clip-path="url(#c{abs(hash(name))})">{"".join(body)}</g><rect width="{W}" height="{H}" rx="44" fill="none" stroke="#D9D2C6"/></g>'

open(f"{OUT}/hifi-02-trip.svg","w").write(svg(W,H,[frame("02 Trip group view",screen02())]))
open(f"{OUT}/hifi-06-poll.svg","w").write(svg(W,H,[frame("06 Live poll",screen06())]))

# ---------- WIREFLOW ----------
INK="#333"; GREY="#8a8a8a"; LINE="#bdbdbd"
def wf_box(x,y,w,h,label,sub=None,fill="#fff",bold=False):
    s=rect(x,y,w,h,fill,"#555",6,1.2)+text(x+10,y+(h/2+5 if not sub else h/2-2),label,13,INK,"Open Sans",600 if bold else 400)
    if sub: s+=text(x+10,y+h/2+14,sub,11,GREY,"Open Sans")
    return s
def wf_btn(x,y,w,label,h=44):
    return rect(x,y,w,h,"#333",r=6)+text(x+w/2,y+h/2+5,label,13,"#fff","Open Sans",700,"middle")
def wf_screen(name,title,elems,sheet=False,note=None):
    s=[rect(0,0,W,H,"#fff","#333",24,1.5),status_bar_wf()]
    s+=[text(20,96,title,26,INK,"Open Sans",600)]
    s+=elems
    s+=[text(0,-16,name,15,INK,"Open Sans",700)]
    if note: s+=[text(0,H+26,note[0],12,GREY,"Open Sans"),text(0,H+44,note[1] if len(note)>1 else "",12,GREY,"Open Sans")]
    return "".join(s)
def status_bar_wf():
    return text(30,40,"9:41",14,INK,"Open Sans",600)+rect(150,20,92,24,"#333",r=12)+text(330,40,"▮▮▮ ▲ ▮",11,INK,"Open Sans")
def wf_tabs(active):
    out=[f'<line x1="0" y1="770" x2="{W}" y2="770" stroke="#555"/>']
    for i,n in enumerate(["Trips","Polls","Plan","Money"]):
        cx=W/8*(2*i+1); out.append(rect(cx-11,786,22,18,"#333" if n==active else "none","#333",3,1.2)); out.append(text(cx,826,n,11,INK,"Open Sans",700 if n==active else 400,"middle"))
    return "".join(out)
def callout(x,y,kind,lines,w=250):
    col={"DECISION":"#E0562E","STATE":"#2F7D5B","PATTERN":"#3B5BB5"}[kind]
    h=22+16*len(lines)+10
    s=rect(x,y,w,h,"#fff",col,6,1.2)+rect(x,y,w,22,col,r=6)+rect(x,y+16,w,6,col)+text(x+8,y+15,kind,10,"#fff","Open Sans",700,extra='letter-spacing="1"')
    for i,l in enumerate(lines): s+=text(x+8,y+38+16*i,l,10.5,INK,"Open Sans")
    return s
def flow_arrow(x1,y1,x2,y2,label=None):
    s=f'<path d="M{x1} {y1} C{x1+60} {y1} {x2-60} {y2} {x2} {y2}" fill="none" stroke="#555" stroke-width="1.5" marker-end="url(#ah)"/>'
    if label: s+=rect((x1+x2)/2-60,(y1+y2)/2-22,120,18,"#fff")+text((x1+x2)/2,(y1+y2)/2-9,label,11,INK,"Open Sans",600,"middle")
    return s

def L(items,y=130,gap=10,h=52,x=20,w=353):
    out=[];
    for it in items:
        if isinstance(it,tuple): out.append(wf_box(x,y,w,h,it[0],it[1] if len(it)>1 else None,fill=it[2] if len(it)>2 else "#fff",bold=len(it)>3))
        elif it is None: y+=14; continue
        else: out.append(text(x,y+14,it,13,INK,"Open Sans",700)); y-=h-24
        y+=h+gap
    return out

screens = [
 ("01 · Home","Your trips", L([("Lisbon · Sep 24–28 · Day 4 of 4","Tonight: dinner still open · You're owed €42","#eee",1),None,None,None,None,"Coming up",
    ("Primavera Sound, Barcelona","Jun 3–6, 2027 · 8 friends"),("Dolomites hut-to-hut","Past · settled"),("+ New trip   ·   Import from Splitwise",)],h=56)+[wf_btn(36,196,321,"Open trip"),wf_tabs("Trips")],
   ("Live trip is the hero; the two soft chips are the next action and the money state.",)),
 ("02 · Trip group view","Last night in Lisbon", L([("Nic ORGANIZER · Ari · Maya · Theo · Sam   [+]","group photo · tap + → 03","#eee")]+
    [("Dinner tonight is still open","3 places from the wishlist, ready to poll","#f4f4f4",1)],h=64)+[wf_btn(36,262,321,"Start the poll → 04")]+
    L(["Today",("10:00 · Torre de Belém",),("14:00 · LX Factory","€86 · logged by Maya"),("Trip money · You're owed €42","→ 09")],y=330)+[wf_tabs("Trips")],
   ("Empty slot in today's plan = the one call to action. Money is a row, not a tab-jump.",)),
 ("03 · Add Ren (sheet)","Add someone to Lisbon", [rect(0,0,W,H,"#cfcfcf"),rect(0,100,W,H-100,"#fff",r=24),rect(W/2-20,112,40,4,"#999",r=2)]+L([("Share the join link","tripup.app/j/lisbon → group chat","#f4f4f4",1),
    ("1 Tap link · 2 Confirm number · 3 In","no install · no password · no profile"),"or add from contacts",("☑ Ren Okafor","+351 ··· 42 18 · joining for dinner tonight","#eee"),
    ("Joining tonight only  [on]","Skips the earlier expenses automatically")],y=140)+[wf_btn(20,520,353,"Add Ren → toast “Ren joined”")],
   ("Ren's side (03b) is a browser page: phone + 4-digit code, then vote & pay from there.",)),
 ("04 · Create poll","Where for dinner?", L([("Wishlist · 7  |  Near me  |  Search Maps","options ranked: saved by more › open now › walk › price","#f4f4f4"),
    ("Cervejaria Ramiro · Seafood €€ · 12 min","Saved by Maya & Theo            ×"),("Taberna da Rua das Flores · €€ · 6 min","Saved by Nic                          ×"),
    ("Time Out Market · € · 15 min","Pasted in chat by Sam              ×"),("4 more on the wishlist · swap one in",),"Settings",("Closes: when everyone has voted",),("Winner goes into tonight's plan · 19:30",)],h=50)+[wf_btn(20,760,353,"Send to the group → 05")],
   ("AI drafts three options from the wishlist; every one is removable. No timer.",)),
 ("05 · Push + chat card","Group chat (any messenger)", [rect(20,110,353,54,"#eee","#555",8,1.2),text(32,132,"TripUp · now",11,GREY,"Open Sans"),text(32,150,"Ari asks: Where for dinner? Tap to vote",12,INK,"Open Sans"),
    rect(20,190,240,36,"#f4f4f4",r=8),text(30,213,"Ren joined via Ari's link",11,GREY,"Open Sans"),
    rect(20,240,220,40,"#f4f4f4",r=8),text(30,264,"Maya: dinner?? I'm starving",12,INK,"Open Sans"),
    rect(120,300,253,230,"#fff","#555",8,1.5),text(132,322,"TRIPUP · LIVE POLL · 4 of 6 voted",10,GREY,"Open Sans",700),text(132,346,"Where for dinner?",15,INK,"Open Sans",700),
    text(132,370,"Ramiro ▮▮▮▮▮▮ 3",12,INK,"Open Sans"),text(132,392,"Taberna ▮▮ 1",12,INK,"Open Sans"),text(132,414,"Time Out 0",12,INK,"Open Sans"),wf_btn(132,470,229,"Vote · no app needed",40),
    rect(20,560,200,40,"#f4f4f4",r=8),text(30,584,"Sam: voted, ramiro obviously",12,INK,"Open Sans"),rect(20,720,353,40,"#fff","#555",20,1.2)],
   ("Every event has a push + a chat-card twin, so nobody has to open the app to vote.",)),
 ("06 · Live poll","Where for dinner?", L([("Tonight 19:30 · asked by Ari · 4 of 6 voted","[Share to chat] [Nudge Theo & Ren]","#f4f4f4"),"Options",
    ("Cervejaria Ramiro ▮▮▮▮▮▮▮▮ 3 · LEADING","You, Nic, Sam","#fff",1),("Taberna da Rua das Flores ▮▮ 1","Maya"),("Time Out Market  0","No votes yet"),
    "Group",("A N M S · T R (dimmed)","4 voted · Theo and Ren haven't yet")],h=56)+[text(20,640,"Closes when everyone has voted, or when you close it.",11,GREY,"Open Sans"),wf_btn(20,760,353,"Close poll · Ramiro wins → 07")],
   ("Votes arrive live: counts and bars animate, cards re-sort. Close is enabled once a majority exists.",)),
 ("07 · Plan updated","Ramiro it is. Added to tonight", L([("Cervejaria Ramiro · Won 4 of 6 · 19:30","[Directions] [Book a table]","#f4f4f4",1),"Today · Sat 27",
    ("10:00 · Torre de Belém","Done · 5 went"),("14:00 · LX Factory","€86 · logged by Maya"),("19:30 · Dinner · Cervejaria Ramiro  [poll]","From tonight's poll · 6 going","#eee",1),
    ("After dinner · suggestion: Miradouro da Graça","Saved by Sam · [Poll it]")],h=56)+[wf_tabs("Plan")],
   ("Result lands in the itinerary automatically and is traceable (“from poll”). Next empty slot gets a suggestion.",)),
 ("08 · Log expense","Dinner at Ramiro", L([("TOTAL €214.00","Paid by you · 6 people · receipt scanned","#f4f4f4",1),"Split by item",("Food €166","Everyone · €27.67 each"),
    ("Wine €48 · 4 people · €12 each","[Ari][Maya][Theo][Sam]  (Nic) (Ren)","#fff",1),("AI note: Nic and Ren usually skip wine. Tap a name to change",)],h=58)+[wf_btn(20,760,353,"Save · updates 6 balances → 09")],
   ("Item-level exclusion, suggested from habits, never auto-applied.",)),
 ("09 · Balances","Trip money · €1,284 total", L([("€214 per person · €402 you paid · +€188 you're owed",None,"#f4f4f4"),"3 transfers instead of 7   (?)",
    ("N → A   Nic pays you €96",),("T → A   Theo pays you €92",),("R → M   Ren pays Maya €28","Instead of paying you, one transfer fewer"),
    ("Why? Ren owes you €28, you owe Maya €28","so Ren pays Maya directly","#f4f4f4"),("[Nudge Nic & Theo]  [Paid in cash?]",)],h=52)+[wf_tabs("Money")],
   ("Tap a transfer → settle sheet: Apple Pay / Revolut·Wise / Bank (IBAN copied) / Cash. All paid → 10.",)),
 ("10 · Settled","Lisbon is squared up.", L([("6 of 6 settled · €1,284 across 4 days","A N M T S R","#f4f4f4",1),"Received",("€96 from Nic · Apple Pay · just now","Paid"),
    ("€92 from Theo · Revolut · 2 min ago","Paid"),("Posted to the group chat","“All settled, ready for the next one”")],h=56)+[wf_btn(20,760,353,"Plan the next trip → 01")],
   ("Confirmation is group-wide, not private. closes the loop where it started (the chat).",)),
]

callouts = {
 0:[("DECISION",["Which trip? The live one is promoted;","past trips collapse to a row."])],
 1:[("STATE",["Members: 5 → 6 after 03.","Today's open slot drives the CTA."])],
 2:[("DECISION",["Link vs contacts. Link is default:","zero accounts, browser only."]),("STATE",["'Joining tonight only' = Ren is","excluded from earlier splits."])],
 3:[("DECISION",["Option source: wishlist › near me ›","search. Close rule: all voted / manual."])],
 4:[("PATTERN",["Chat-card twin of every event.","Guests vote without the app."])],
 5:[("STATE",["Votes 3/1/0 → Theo votes → 4/1/0.","Bars, counts, order update live."]),("DECISION",["Wait for all 6, or close now","(allowed once majority reached)."])],
 6:[("STATE",["Itinerary: +19:30 Dinner, tagged","'from poll'. Notification to all."])],
 7:[("DECISION",["Who's in on each item. AI suggests","Nic & Ren out of wine; editable."])],
 8:[("STATE",["Balances recomputed for 6.","7 debts simplified to 3 transfers."]),("DECISION",["Payment rail per transfer.","TripUp never holds money."])],
 9:[("STATE",["All paid → group confirmation","posted to chat. Loop closed."])],
}

def diamond(cx,cy,w,h,lines):
    s=f'<polygon points="{cx},{cy-h/2} {cx+w/2},{cy} {cx},{cy+h/2} {cx-w/2},{cy}" fill="#fff" stroke="#555" stroke-width="1.5"/>'
    for i,l in enumerate(lines): s+=text(cx,cy+4+(i-(len(lines)-1)/2)*14,l,11,INK,"Open Sans",600,"middle")
    return s
def arrow_label(x,y,label):
    w=len(label)*6.4+16
    return rect(x-w/2,y-9,w,18,"#fff","#555",9,1)+text(x,y+4,label,11,INK,"Open Sans",600,"middle")
def wireflow():
    cols=5; gx=270; gy=460; mx=170; my=190
    body=[f'<defs><marker id="ah" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0 0 L10 5 L0 10z" fill="#555"/></marker></defs>']
    body.append(text(mx,60,"TripUp wireflow · the Lisbon scenario in 10 screens",28,INK,"Open Sans",700))
    body.append(text(mx,88,"Lo-fi, iPhone 15 (393 × 852). Follow the numbered arrows. Diamonds are checks the app makes; callouts under each screen record the decision the user takes, the state that changes, and the pattern in play.",13,GREY,"Open Sans"))
    # legend
    lx=mx+5*W+4*gx-330; ly=40
    body.append(rect(lx,ly,330,86,"#fff","#555",8,1))
    body.append(text(lx+12,ly+20,"LEGEND",10,GREY,"Open Sans",700))
    body.append(f'<path d="M{lx+12} {ly+38} h40" stroke="#555" stroke-width="1.5" marker-end="url(#ah)"/>'+text(lx+62,ly+42,"trigger · what the user taps",11,INK,"Open Sans"))
    body.append(f'<polygon points="{lx+32},{ly+50} {lx+44},{ly+58} {lx+32},{ly+66} {lx+20},{ly+58}" fill="#fff" stroke="#555" stroke-width="1.2"/>'+text(lx+62,ly+62,"check the app makes",11,INK,"Open Sans"))
    for j,(k,c) in enumerate([("DECISION","#E0562E"),("STATE","#2F7D5B"),("PATTERN","#3B5BB5")]):
        body.append(rect(lx+12+j*104,ly+72,10,10,c,r=2)+text(lx+26+j*104,ly+81,k.title(),10,INK,"Open Sans"))
    pos=[]
    for i,(name,title,elems,note) in enumerate(screens):
        r,c=divmod(i,cols); x=mx+c*(W+gx); y=my+r*(H+gy)
        pos.append((x,y))
        body.append(g(x,y,[wf_screen(name,title,elems,note=note)]))
        cy=y+H+60
        for kind,lines in callouts.get(i,[]):
            body.append(callout(x,cy,kind,lines,w=W)); cy+=22+16*len(lines)+10+8
    triggers=["1 · tap Lisbon","2 · tap + on the group","3 · Add Ren, then Start the poll","4 · Send to the group","5 · tap Vote on the card","6 · Close poll","7 · Log the dinner","8 · Save","9 · settle each transfer"]
    checks={5:("Majority","reached?","no · nudge Theo & Ren, keep waiting"),8:("All","paid?","no · nudge Nic & Theo")}
    ay=lambda y: y+H/2+40
    for i in range(len(pos)-1):
        (x1,y1),(x2,y2)=pos[i],pos[i+1]
        if (i+1)%cols:
            if i in checks:
                a,b,no=checks[i]; cx=(x1+W+x2)/2; cy=ay(y1)
                body.append(f'<path d="M{x1+W} {cy} H{cx-62}" stroke="#555" stroke-width="1.5" marker-end="url(#ah)"/>')
                body.append(diamond(cx,cy,120,76,[a,b]))
                body.append(f'<path d="M{cx+60} {cy} H{x2-4}" stroke="#555" stroke-width="1.5" marker-end="url(#ah)"/>')
                body.append(text(cx+72,cy-8,"yes",11,INK,"Open Sans",700))
                body.append(f'<path d="M{cx} {cy-38} v-40 H{x1+W/2+120} v-1" fill="none" stroke="#555" stroke-width="1.2" stroke-dasharray="4 4" marker-end="url(#ah)"/>')
                body.append(arrow_label(cx,cy-96,no))
                body.append(arrow_label(cx,cy+66,triggers[i]))
            else:
                cy=ay(y1)
                body.append(f'<path d="M{x1+W} {cy} H{x2-4}" stroke="#555" stroke-width="1.5" marker-end="url(#ah)"/>')
                body.append(arrow_label((x1+W+x2)/2,cy-22,triggers[i]))
        else:
            stack=lambda k: sum(22+16*len(l)+10+8 for _,l in callouts.get(k,[]))
            rowmax=max(stack(k) for k in range(0,cols))
            yy=y1+H+60+rowmax+50
            body.append(f'<path d="M{x1+W/2} {y1+H+60+stack(i)+6} V{yy} H{x2+W/2} V{y2-34}" fill="none" stroke="#555" stroke-width="1.5" marker-end="url(#ah)"/>')
            body.append(arrow_label((x1+x2+W)/2,yy,triggers[i]))
    # start marker
    x0,y0=pos[0]
    body.append(f'<circle cx="{x0-70}" cy="{ay(y0)}" r="9" fill="#555"/>'+f'<path d="M{x0-60} {ay(y0)} H{x0-4}" stroke="#555" stroke-width="1.5" marker-end="url(#ah)"/>')
    body.append(text(x0-70,ay(y0)-18,"START",10,GREY,"Open Sans",700,"middle"))
    body.append(text(x0-70,ay(y0)+30,"Ari opens TripUp,",10,GREY,"Open Sans",400,"middle")+text(x0-70,ay(y0)+43,"Sat 18:52",10,GREY,"Open Sans",400,"middle"))
    # end + loop back 10 -> 01
    xl,yl=pos[-1]
    cyl=ay(yl)
    body.append(f'<circle cx="{xl+W+70}" cy="{cyl}" r="9" fill="#fff" stroke="#555" stroke-width="3"/>'+f'<path d="M{xl+W} {cyl} H{xl+W+56}" stroke="#555" stroke-width="1.5" marker-end="url(#ah)"/>')
    body.append(text(xl+W+70,cyl-18,"END",10,GREY,"Open Sans",700,"middle"))
    body.append(arrow_label(xl+W/2+40,cyl-22,"10 · Plan the next trip"))
    body.append(f'<path d="M{xl+W+70} {cyl+10} V{yl+H+300} H{x0-70} V{ay(y0)+60} v-40" fill="none" stroke="#555" stroke-width="1.2" stroke-dasharray="6 6" marker-end="url(#ah)"/>')
    body.append(arrow_label((x0+xl)/2+W/2,yl+H+300,"loop · back to Home for the next trip"))
    total_w=mx*2+cols*W+(cols-1)*gx+120; total_h=my+2*H+gy+340
    return svg(total_w,total_h,body,bg="#F5F5F3")

open(f"{OUT}/wireflow.svg","w").write(wireflow())
print("ok")
