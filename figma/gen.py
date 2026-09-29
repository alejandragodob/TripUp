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
def imgbox(x,y,w,h,label="image"):
    return (rect(x,y,w,h,"#E6E6E6","#8A8A8A",8,1.2)+f'<path d="M{x} {y} L{x+w} {y+h} M{x+w} {y} L{x} {y+h}" stroke="#B5B5B5" stroke-width="1"/>'
            +rect(x+w/2-len(label)*3.4-8,y+h/2-9,len(label)*6.8+16,18,"#FFFFFF","#8A8A8A",9,1)+text(x+w/2,y+h/2+4,label,10,GREY,"Open Sans",600,"middle"))
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
    col={"DECISION":"#E0562E","STATE":"#2F7D5B","PATTERN":"#3B5BB5","AI":"#7A2E9E"}[kind]
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
 ("01 · Home","Your trips", [imgbox(20,130,353,80,"Lisbon photo")]+L([("Lisbon · Sep 24–28 · Day 4 of 4","Tonight: dinner still open · You're owed €42","#eee",1),None,None,None,None,"Coming up",
    ("Primavera Sound, Barcelona","Jun 3–6, 2027 · 8 friends · [photo]"),("New York, Christmas markets","Past · settled · [photo]"),("+ New trip   ·   Import from Splitwise",)],y=222,h=56)+[wf_btn(36,292,321,"Open trip"),wf_tabs("Trips")],
   ("Live trip is the hero; the two soft chips are the next action and the money state.",)),
 ("02 · Trip group view","Last night in Lisbon", [imgbox(20,130,353,80,"Lisbon photo · members + [+] overlay")]+L([("Nic ORGANIZER · Ari · Maya · Theo · Sam   [+]","avatars · tap + → 03","#eee"),
    ("Dinner tonight is still open","3 places from the wishlist, ready to poll","#f4f4f4",1)],y=222,h=56)+[wf_btn(36,362,321,"Start the poll → 04"),wf_box(20,414,170,30,"✦ Ask TripUp"),wf_box(200,414,173,30,"Notifications")]+
    L(["Today",("10:00 · Torre de Belém","[photo]"),("14:00 · LX Factory","€86 · logged by Maya · [photo]"),("Trip money · You're owed €42","→ 09")],y=456,h=46)+[wf_tabs("Trips")],
   ("Empty slot in today's plan = the one call to action. Money is a row, not a tab-jump.",)),
 ("03 · Add Ren (sheet)","Add someone to Lisbon", [rect(0,0,W,H,"#cfcfcf"),rect(0,100,W,H-100,"#fff",r=24),rect(W/2-20,112,40,4,"#999",r=2)]+L([("Share the join link","tripup.app/j/lisbon → group chat","#f4f4f4",1),
    ("1 Tap link · 2 Confirm number · 3 In","no install · no password · no profile"),"or add from contacts",("☑ Ren Okafor","+351 ··· 42 18 · joining for dinner tonight","#eee"),
    ("Joining tonight only  [on]","Skips the earlier expenses automatically")],y=140)+[wf_btn(20,520,353,"Add Ren → toast “Ren joined”")],
   ("Ren's side (03b) is a browser page: phone + 4-digit code, then vote & pay from there.",)),
 ("04 · Create poll","Where for dinner?", L([("✦ Drafted by TripUp AI · why these?   [Regenerate]","reasons per option; regenerate proposes three others","#f4f4f4"),
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
 ("06 · Live poll","Where for dinner?", L([("Tonight 19:30 · asked by Ari · 4 of 6 voted","[Share to chat] [✦ Nudge Theo & Ren · AI drafts it]","#f4f4f4"),"Options",
    ("Cervejaria Ramiro ▮▮▮▮▮▮▮▮ 3 · LEADING","You, Nic, Sam","#fff",1),("Taberna da Rua das Flores ▮▮ 1","Maya"),("Time Out Market  0","No votes yet"),
    "Group",("A N M S · T R (dimmed)","4 voted · Theo and Ren haven't yet")],h=56)+[text(20,640,"Closes when everyone has voted, or when you close it.",11,GREY,"Open Sans"),wf_btn(20,760,353,"Close poll · Ramiro wins → 07")],
   ("Votes arrive live: counts and bars animate, cards re-sort. Close is enabled once a majority exists.",)),
 ("07 · Plan updated","Ramiro it is. Added to tonight", [imgbox(20,130,353,56,"restaurant photo")]+L([("Cervejaria Ramiro · Won 4 of 6 · 19:30","[Directions] [Book a table] [Maps]","#f4f4f4",1),"Today · Sat 27",
    ("10:00 · Torre de Belém","Done · 5 went"),("14:00 · LX Factory","€86 · logged by Maya"),("19:30 · Dinner · Cervejaria Ramiro  [poll]","From tonight's poll · 6 going","#eee",1),
    ("✦ After dinner · TripUp AI: Miradouro da Graça","Saved by Sam · fits the 21:30 gap · [Poll it]")],y=196,h=54)+[wf_tabs("Plan")],
   ("Result lands in the itinerary automatically and is traceable (“from poll”). Next empty slot gets a suggestion.",)),
 ("08 · Log expense","Dinner at Ramiro", L([("TOTAL €214.00","Paid by you · 6 people · ✦ receipt read into 7 lines","#f4f4f4",1),"Split by item",("Food €166","Everyone · €27.67 each"),
    ("Wine €48 · 4 people · €12 each","[Ari][Maya][Theo][Sam]  (Nic) (Ren)","#fff",1),("✦ Nic and Ren usually skip wine. Tap a name to change · Why?",)],h=58)+[wf_btn(20,760,353,"Save · updates 6 balances → 09")],
   ("Item-level exclusion, suggested from habits, never auto-applied.",)),
 ("09 · Balances","Trip money · €1,284 total", L([("€214 per person · €402 you paid · +€188 you're owed",None,"#f4f4f4"),"3 transfers instead of 7   (?)",
    ("N → A   Nic pays you €96",),("T → A   Theo pays you €92",),("R → M   Ren pays Maya €28","Instead of paying you, one transfer fewer"),
    ("Why? Ren owes you €28, you owe Maya €28","so Ren pays Maya directly","#f4f4f4"),("✦ Settle up in one message","AI drafts who pays whom; you post it to the chat","#f4f4f4",1),("[Nudge Nic & Theo]  [Paid in cash?]",)],h=50)+[wf_tabs("Money")],
   ("Tap a transfer → settle sheet: Apple Pay / Revolut·Wise / Bank (IBAN copied) / Cash. All paid → 10.",)),
 ("10 · Settled","Lisbon is squared up.", [imgbox(20,130,353,100,"Lisbon photo")]+L([("6 of 6 settled · €1,284 across 4 days","A N M T S R","#f4f4f4",1),"Received",("€96 from Nic · Apple Pay · just now","Paid"),
    ("€92 from Theo · Revolut · 2 min ago","Paid"),("Posted to the group chat","“All settled, ready for the next one”")],y=242,h=56)+[wf_btn(20,760,353,"Plan the next trip → 01")],
   ("Confirmation is group-wide, not private. closes the loop where it started (the chat).",)),
]

callouts = {
 0:[("DECISION",["Which trip? The live one is promoted;","past trips collapse to a row."])],
 1:[("STATE",["Members: 5 → 6 after 03.","Today's open slot drives the CTA."]),("AI",["Ask TripUp: answers about tonight,","votes and money from trip state."])],
 2:[("DECISION",["Link vs contacts. Link is default:","zero accounts, browser only."]),("STATE",["'Joining tonight only' = Ren is","excluded from earlier splits."])],
 3:[("DECISION",["Option source: wishlist › near me ›","search. Close rule: all voted / manual."]),("AI",["Drafts the three options and explains","why. Regenerate. Never auto-sends."])],
 4:[("PATTERN",["Chat-card twin of every event.","Guests vote without the app."])],
 5:[("STATE",["Votes 3/1/0 → Theo votes → 4/1/0.","Bars, counts, order update live."]),("DECISION",["Wait for all 6, or close now","(allowed once majority reached)."]),("AI",["Writes the nudge as Ari; editable","before it goes to the chat."])],
 6:[("STATE",["Itinerary: +19:30 Dinner, tagged","'from poll'. Notification to all."]),("AI",["Fills the next empty slot from","saved places. A suggestion, not a booking."])],
 7:[("AI",["Reads the receipt into items. Suggests","exclusions from habits; shows why."]),("DECISION",["Who's in on each item.","Every name is a tap to change."])],
 8:[("STATE",["Balances recomputed for 6.","7 debts simplified to 3 transfers."]),("AI",["Explains each transfer; drafts the","settle-up message for the chat."]),("DECISION",["Payment rail per transfer.","TripUp never holds money."])],
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
    cols=5; gx=270; gy=520; mx=170; my=190
    body=[f'<defs><marker id="ah" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0 0 L10 5 L0 10z" fill="#555"/></marker></defs>']
    body.append(text(mx,60,"TripUp wireflow · the Lisbon scenario in 10 screens",28,INK,"Open Sans",700))
    body.append(text(mx,88,"Lo-fi, iPhone 15 (393 × 852). Follow the numbered arrows. Diamonds are checks the app makes; callouts under each screen record the decision the user takes, the state that changes, the pattern in play, and where TripUp AI helps (always a suggestion, never applied on its own).",13,GREY,"Open Sans"))
    # legend
    lx=mx+5*W+4*gx-330; ly=40
    body.append(rect(lx,ly,330,86,"#fff","#555",8,1))
    body.append(text(lx+12,ly+20,"LEGEND",10,GREY,"Open Sans",700))
    body.append(f'<path d="M{lx+12} {ly+38} h40" stroke="#555" stroke-width="1.5" marker-end="url(#ah)"/>'+text(lx+62,ly+42,"trigger · what the user taps",11,INK,"Open Sans"))
    body.append(f'<polygon points="{lx+32},{ly+50} {lx+44},{ly+58} {lx+32},{ly+66} {lx+20},{ly+58}" fill="#fff" stroke="#555" stroke-width="1.2"/>'+text(lx+62,ly+62,"check the app makes",11,INK,"Open Sans"))
    for j,(k,c) in enumerate([("DECISION","#E0562E"),("STATE","#2F7D5B"),("PATTERN","#3B5BB5"),("AI","#7A2E9E")]):
        body.append(rect(lx+12+j*78,ly+72,10,10,c,r=2)+text(lx+26+j*78,ly+81,k.title(),10,INK,"Open Sans"))
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
    body.append(arrow_label(xl+W+70,cyl+34,"10 · Plan the next trip"))
    body.append(f'<path d="M{xl+W+70} {cyl+10} V{yl+H+300} H{x0-70} V{ay(y0)+60} v-40" fill="none" stroke="#555" stroke-width="1.2" stroke-dasharray="6 6" marker-end="url(#ah)"/>')
    body.append(arrow_label((x0+xl)/2+W/2,yl+H+300,"loop · back to Home for the next trip"))
    total_w=mx*2+cols*W+(cols-1)*gx+120; total_h=my+2*H+gy+340
    return svg(total_w,total_h,body,bg="#F5F5F3")

open(f"{OUT}/wireflow.svg","w").write(wireflow())

def wrap(t,n):
    out=[];line=""
    for w in t.split():
        if len(line)+len(w)+1>n: out.append(line);line=w
        else: line=(line+" "+w).strip()
    if line: out.append(line)
    return out
def card(x,y,w,title,items,kind="para",h=None):
    body=[];cy=y+52
    for it in items:
        if kind=="para":
            for l in wrap(it,int(w/6.6)): body.append(text(x+18,cy,l,12,INK,"Open Sans"));cy+=17
            cy+=8
        elif kind=="pair":
            k,v=it;body.append(text(x+18,cy,k,12,INK,"Open Sans",700));cy+=17
            for l in wrap(v,int(w/6.6)): body.append(text(x+18,cy,l,12,INK,"Open Sans"));cy+=17
            cy+=8
        elif kind=="step":
            n,k,v,ref=it
            body.append(f'<circle cx="{x+27}" cy="{cy-4}" r="10" fill="#333"/>'+text(x+27,cy,str(n),10,"#fff","Open Sans",700,"middle"))
            body.append(text(x+46,cy,k,12,INK,"Open Sans",700))
            body.append(rect(x+w-18-len(ref)*6.6-14,cy-13,len(ref)*6.6+14,18,"#fff","#555",9,1)+text(x+w-18-len(ref)*3.3-7,cy,ref,10,INK,"Open Sans",700,"middle"))
            cy+=16
            for l in wrap(v,int((w-46)/6.6)): body.append(text(x+46,cy,l,11.5,GREY,"Open Sans"));cy+=15
            cy+=8
        elif kind=="row":
            k,v=it
            body.append(text(x+18,cy,k,12,INK,"Open Sans",700));cy+=16
            for l in wrap(v,int(w/6.6)): body.append(text(x+18,cy,"→ "+l if l==wrap(v,int(w/6.6))[0] else "   "+l,11.5,GREY,"Open Sans"));cy+=15
            cy+=8
    hh=h or (cy-y+6)
    return rect(x,y,w,hh,"#fff","#555",10,1.2)+rect(x,y,w,34,"#333",r=10)+rect(x,y+24,w,10,"#333")+text(x+18,y+22,title.upper(),11,"#fff","Open Sans",700,extra='letter-spacing="1"')+"".join(body), hh

def brief():
    Wc=2440; body=[]
    body.append(text(80,60,"The brief, and how TripUp answers it",28,INK,"Open Sans",700))
    body.append(text(80,88,"TripUp design challenge · Bending Spoons. Left: what was asked. Right: where each ask is answered in the wireflow (screen numbers), the hi-fi and the prototype.",13,GREY,"Open Sans"))
    x0=80; y0=120; gap=24
    c1,h1=card(x0,y0,440,"Context",["Friend trips are great; organizing them is not. Deciding where to go, stay, eat and what to do, plus managing expenses and keeping everyone in the loop, gets frustrating fast.","TripUp is a mobile app for organizing group travel, from a weekend getaway to a festival abroad. Friends plan the trip, shape it as it unfolds, build itineraries together, vote on decisions, track and settle expenses.","The beta has traction; the team wants a full redesign."])
    c2,h2=card(x0,y0+h1+gap,440,"Who",[("The Organizer","Most proactive. Sets up the trip, invites the others, keeps things moving. In TripUp: Nic, tagged ORGANIZER on screen 02. Same powers as everyone else."),("The Participants","Want to be involved without being overwhelmed. Suggest ideas, vote, stay informed. In TripUp: Ari drives the whole evening as a participant, which is the point.")],"pair")
    c3,h3=card(x0,y0+h1+h2+gap*2,440,"How they behave",[("Spontaneous decisions","Most group choices happen on the fly, mid-trip. Answered by: one-tap poll from the trip screen (02 to 04), live votes (06)."),("Shared ownership","One person leads, everyone wants input on food, activities, money. Answered by: identical powers, votes from the chat (05), item-level splits anyone can edit (08)."),("Low tolerance for friction","More than a couple of taps and they switch to WhatsApp. Answered by: TripUp lives inside the chat (05), no account for guests (03b), no wallet (09).")],"pair")
    c4,h4=card(x0,y0+h1+h2+h3+gap*3,440,"What they want",[("Polls over chats","Quick, intuitive polls beat long threads. Answered by: 04, 05, 06."),("Simple expense tracking","Manage and settle group expenses, including in-app payments by bank transfer or digital methods. Answered by: 08, 09, settle sheet with Apple Pay, Revolut, Wise, bank, cash."),("Real-time feedback","Decisions reflected instantly in the itinerary and notifications. Answered by: live bars (06), auto-added dinner (07), push + chat card for every event.")],"pair")
    x1=x0+440+gap
    steps=[(1,"Ari opens TripUp","Last evening in Lisbon, back at the house. Home lists all her trips; the live one is the hero.","01"),
           (2,"Opens the group view","Members with Nic tagged organizer, today's plan, the open dinner slot as the one call to action.","02"),
           (3,"Adds Ren for the final dinner","Join link or contacts. Ren joins in the browser with her phone number, no app, no password. Joining tonight only keeps her out of earlier splits.","03 · 03b"),
           (4,"Creates a poll: three nearby restaurants","Drafted from the group's Google Maps wishlist, different vibes and prices. Near me and Search Maps add more. Every option opens in Maps.","04"),
           (5,"The app notifies everyone","Push to all six, and the poll lands in the group chat as a live card. Votes happen from the chat.","05"),
           (6,"The leading option updates in real time","Theo's vote arrives, bars animate, cards re-sort. Close is allowed once a majority exists.","06"),
           (7,"Poll closes, winner goes into the itinerary","Ramiro at 19:30, tagged from poll, with directions and booking. The next empty slot gets a suggestion.","07"),
           (8,"After dinner Ari logs the expense","Receipt scanned into items. Nic and Ren excluded from the wine; every name is a tap to change.","08"),
           (9,"Balances update, debts consolidated","3 transfers instead of 7, each explained in one sentence. Settle with the rails people already have.","09"),
           (10,"Confirmation to the group","Lisbon is squared up. Posted to the chat, where the evening started.","10")]
    c5,h5=card(x1,y0,640,"The scenario, step by step",steps,"step")
    x2=x1+640+gap
    c6,h6=card(x2,y0,560,"Deliverables",[("1 · Wireflow, the thinking","Section 1 in this file: 10 screens, numbered triggers, decision diamonds, decision / state / pattern callouts."),("2 · Hi-fi screens, the craft","Section 2: 02 Trip group view and 06 Live poll at full fidelity, Newsreader + Figtree, tokens from the spec."),("3 · Interactive prototype, the result","trip-up-three.vercel.app: React + Vite, mobile web, full journey, mock data, the two hi-fi screens inside it.")],"row")
    c7,h7=card(x2,y0+h6+gap,560,"What reviewers look for",[("Is the scenario completely satisfied?","Ten steps, ten screens; the reset at the end lets a PM run it again."),("Usable without guidance?","One primary action per screen; every tap responds; no dead ends (audited)."),("Polished and consistent?","One token set across Figma and code; AA contrast; 44 px targets."),("Does the prototype represent the design?","02 and 06 built pixel-close from the hi-fi; same photos, type and spacing."),("Could a PM interact with it and understand the product?","Live poll simulation, chat-card twin, settle sheet with real rails."),("Value beyond the brief?","Guest join without an account, wishlist and Maps sourcing, explained transfers, accessibility pass, and TripUp AI: drafts the poll and explains it, writes nudges, reads receipts and suggests splits, answers questions about the trip. Always editable, never applied on its own. Full critique in the repo: figma/CRITIQUE.md.")],"row")
    c8,h8=card(x2,y0+h6+h7+gap*2,560,"Constraints",[("Device","iPhone 15, 393 × 852. One device, kept throughout: frame on desktop, fills the screen on a phone."),("Submission","Figma link (view for anyone with the link), public prototype URL, optional GitHub repo. No zip files. English only.")],"row")
    body+= [c1,c2,c3,c4,c5,c6,c7,c8]
    Hc=max(y0+h1+h2+h3+h4+gap*3, y0+h5, y0+h6+h7+h8+gap*2)+80
    return svg(Wc,Hc,body,bg="#F5F5F3")

open(f"{OUT}/brief.svg","w").write(brief())

print("ok")
