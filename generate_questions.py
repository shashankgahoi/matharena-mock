import json, random, math
random.seed(42)

def make_mcq(q, opts, ans_idx, topic):
    return {"q": q, "type": "MCQ", "topic": topic, "opts": opts, "ans": opts[ans_idx]}

def make_tita(q, ans, topic):
    return {"q": q, "type": "TITA", "topic": topic, "opts": [], "ans": str(ans)}

questions_by_topic = {}

# ── 1. NUMBER SYSTEM ──────────────────────────────────────────────────────────
ns = []
pairs = [(12,18,6),(15,25,5),(24,36,12),(18,30,6),(14,21,7),(16,40,8),(9,27,9),(20,45,5)]
for a,b,g in pairs:
    l = a*b//g
    ns.append(make_mcq(f"Find the LCM of {a} and {b}.",
        [str(l-6),str(l),str(l+6),str(l+12)],1,"Number System"))
    ns.append(make_tita(f"Find the HCF of {a} and {b}.",g,"Number System"))

for n in [100,200,150,120,180,250,300,360]:
    cnt = sum(1 for x in range(1,n+1) if n%x==0)
    ns.append(make_mcq(f"How many positive divisors does {n} have?",
        [str(cnt-2),str(cnt-1),str(cnt),str(cnt+1)],2,"Number System"))

for r,d in [(17,5),(23,7),(31,6),(45,8),(52,9),(67,11),(83,13),(91,7)]:
    rem = r % d
    ns.append(make_tita(f"What is the remainder when {r} is divided by {d}?",rem,"Number System"))

for base,exp,mod in [(2,10,100),(3,8,100),(7,4,50),(5,6,100),(2,12,100),(4,5,50)]:
    val = (base**exp) % mod
    ns.append(make_tita(f"Find the last two digits of {base}^{exp}.",val,"Number System"))

# Unit digit patterns
for b,e,ud in [(7,4,1),(3,5,3),(2,6,4),(8,3,2),(4,7,4),(6,15,6),(9,9,9),(1,100,1)]:
    ns.append(make_mcq(f"What is the units digit of {b}^{e}?",
        [str(ud-2) if ud>2 else str(ud+6), str(ud-1) if ud>0 else str(9),str(ud),str(ud+1) if ud<9 else str(1)],2,"Number System"))

questions_by_topic["Number System"] = ns

# ── 2. ALGEBRA ────────────────────────────────────────────────────────────────
al = []
for a,b,c in [(3,5,20),(2,7,15),(4,3,23),(5,2,18),(6,1,25),(7,4,32),(8,3,35),(9,2,29)]:
    x = (c-b)//a
    al.append(make_mcq(f"If {a}x + {b} = {c}, find x.",
        [str(x-2),str(x-1),str(x),str(x+1)],2,"Algebra"))

for p,q,r in [(1,-5,6),(1,-7,12),(1,-6,8),(1,-9,20),(2,-7,6),(3,-10,8),(1,-8,15),(2,-9,10)]:
    disc = q*q - 4*p*r
    if disc >= 0:
        s = int(-q/p); pr = int(r/p)
        al.append(make_mcq(f"For x² {'+'if q<0 else '-'} {abs(q)}x {'+'if r>0 else '-'} {abs(r)} = 0, sum of roots is:",
            [str(s-2),str(s-1),str(s),str(s+1)],2,"Algebra"))
        al.append(make_tita(f"For x² {'+'if q<0 else '-'} {abs(q)}x {'+'if r>0 else '-'} {abs(r)} = 0, product of roots is:",pr,"Algebra"))

for a,b in [(2,3),(3,4),(4,5),(5,6),(3,2),(5,3),(7,2),(4,3)]:
    val = a**2 + b**2 + 2*a*b
    al.append(make_tita(f"If a = {a} and b = {b}, find (a + b)².",val,"Algebra"))
    val2 = a**2 + b**2 - 2*a*b
    al.append(make_tita(f"If a = {a} and b = {b}, find (a - b)².",val2,"Algebra"))

for x,y in [(2,3),(1,4),(3,5),(2,7),(4,3),(5,2)]:
    val = x**3 + y**3; s = x+y; p = x*y
    al.append(make_mcq(f"If x = {x} and y = {y}, find x³ + y³.",
        [str(val-6),str(val-3),str(val),str(val+3)],2,"Algebra"))

questions_by_topic["Algebra"] = al

# ── 3. GEOMETRY ───────────────────────────────────────────────────────────────
geo = []
# Triangles
for a,b,c in [(3,4,5),(5,12,13),(8,15,17),(7,24,25),(6,8,10),(9,12,15)]:
    area = int(a*b/2)
    geo.append(make_mcq(f"A right triangle has legs {a} and {b}. Its area is:",
        [str(area-6),str(area-3),str(area),str(area+3)],2,"Geometry"))
    geo.append(make_tita(f"A right triangle has legs {a} and {b}. Its hypotenuse is:",c,"Geometry"))

# Circles
for r in [3,4,5,6,7,8,10,12]:
    area = round(math.pi*r*r, 2)
    circ = round(2*math.pi*r, 2)
    geo.append(make_mcq(f"A circle has radius {r} cm. Its area (approx) is:",
        [str(round(math.pi*(r-1)**2,2)), str(round(math.pi*(r)**2,2)),
         str(round(math.pi*(r+1)**2,2)), str(round(math.pi*(r+2)**2,2))],1,"Geometry"))

# Angles
for a,b in [(60,120),(45,135),(30,150),(70,110),(55,125),(80,100)]:
    geo.append(make_mcq(f"Two supplementary angles are in ratio where one is {a}°. The other is:",
        [str(b-10),str(b-5),str(b),str(b+5)],2,"Geometry"))

# Areas
for l,w in [(6,4),(8,5),(10,7),(12,9),(15,8),(20,6)]:
    area = l*w; peri = 2*(l+w)
    geo.append(make_tita(f"A rectangle has length {l} and width {w}. Find its area.",area,"Geometry"))
    geo.append(make_tita(f"A rectangle has length {l} and width {w}. Find its perimeter.",peri,"Geometry"))

# Cubes and cylinders
for s in [3,4,5,6]:
    vol = s**3
    geo.append(make_mcq(f"Volume of a cube with side {s} cm is:",
        [str(vol-9),str(vol-3),str(vol),str(vol+3)],2,"Geometry"))

questions_by_topic["Geometry"] = geo

# ── 4. RATIOS & PROPORTIONS ───────────────────────────────────────────────────
ra = []
for a,b,tot in [(2,3,50),(3,5,80),(1,4,60),(5,7,120),(3,4,70),(2,5,140),(4,7,110),(3,7,100)]:
    part_a = tot*a//(a+b)
    ra.append(make_mcq(f"Divide {tot} in ratio {a}:{b}. Smaller part is:",
        [str(part_a-5),str(part_a-2),str(part_a),str(part_a+3)],2,"Ratios"))
    ra.append(make_tita(f"Divide {tot} in ratio {a}:{b}. Larger part is:",tot-part_a,"Ratios"))

for a,b,c,tot in [(2,3,5,100),(1,2,3,60),(3,4,5,120),(2,5,3,200)]:
    pa = tot*a//(a+b+c)
    ra.append(make_tita(f"Three parts in ratio {a}:{b}:{c} from {tot}. Smallest part is:",pa,"Ratios"))

for x,y in [(4,5),(3,7),(5,8),(2,9),(6,11)]:
    z = x+y
    ra.append(make_mcq(f"A:B = {x}:{y}. What fraction is A of total?",
        [f"{x-1}/{z}",f"{x}/{z}",f"{y}/{z}",f"{x+1}/{z}"],1,"Ratios"))

questions_by_topic["Ratios"] = ra

# ── 5. TIME, SPEED & DISTANCE ─────────────────────────────────────────────────
tsd = []
for d,t in [(60,2),(90,3),(120,4),(150,5),(180,6),(240,8),(300,5),(350,7)]:
    s = d//t
    tsd.append(make_mcq(f"A car travels {d} km in {t} hours. Speed (km/h) is:",
        [str(s-5),str(s-2),str(s),str(s+5)],2,"TSD"))

for s,t in [(40,3),(60,2.5),(80,4),(50,2),(100,3),(72,2.5)]:
    d = int(s*t)
    tsd.append(make_tita(f"A train moves at {s} km/h for {t} hours. Distance (km) covered is:",d,"TSD"))

for d,s in [(120,40),(180,60),(240,80),(300,75),(360,90)]:
    t = d//s
    tsd.append(make_tita(f"Distance = {d} km, speed = {s} km/h. Time (hours) taken is:",t,"TSD"))

# Relative speed
for s1,s2,d in [(40,60,100),(30,50,80),(20,70,90),(60,90,150)]:
    t_opp = round(d/(s1+s2)*60)
    t_same = d//(s2-s1)
    tsd.append(make_mcq(f"Two trains speed {s1} and {s2} km/h move towards each other. {d} km apart. Meet in (min):",
        [str(t_opp-5),str(t_opp-2),str(t_opp),str(t_opp+5)],2,"TSD"))

questions_by_topic["TSD"] = tsd

# ── 6. TIME & WORK ────────────────────────────────────────────────────────────
tw = []
for a,b in [(6,12),(8,12),(10,15),(12,18),(4,6),(6,9),(15,20),(10,30)]:
    combined = int(a*b/(a+b))
    tw.append(make_mcq(f"A does a job in {a} days, B in {b} days. Together they finish in (days):",
        [str(combined-2),str(combined-1),str(combined),str(combined+1)],2,"Time & Work"))
    tw.append(make_tita(f"A can finish in {a} days. B in {b} days. Working together, days to finish:",combined,"Time & Work"))

for a,d in [(20,4),(30,5),(24,6),(18,3),(40,8)]:
    done = round(d/a*100)
    tw.append(make_mcq(f"A completes a job in {a} days. In {d} days, % work done is:",
        [str(done-5),str(done-2),str(done),str(done+5)],2,"Time & Work"))

for t,m in [(12,4),(20,5),(30,6),(24,8),(15,3)]:
    tw.append(make_tita(f"A tank fills in {t} hours. How much fills in 1 hour (fraction)?",1,"Time & Work"))
    tw.append(make_mcq(f"{m} men finish a job in {t} days. {m*2} men finish in (days):",
        [str(t//2-2),str(t//2-1),str(t//2),str(t//2+1)],2,"Time & Work"))

questions_by_topic["Time & Work"] = tw

# ── 7. PROGRESSIONS ───────────────────────────────────────────────────────────
prog = []
for a,d,n in [(2,3,10),(1,4,8),(5,2,12),(3,5,7),(4,3,9),(1,5,10)]:
    nth = a + (n-1)*d
    s = n*(2*a+(n-1)*d)//2
    prog.append(make_mcq(f"AP: first term {a}, common difference {d}. {n}th term is:",
        [str(nth-3),str(nth-1),str(nth),str(nth+2)],2,"Progressions"))
    prog.append(make_tita(f"AP: first term {a}, common difference {d}. Sum of first {n} terms:",s,"Progressions"))

for a,r,n in [(2,3,5),(3,2,6),(1,4,4),(2,2,8),(5,2,4),(4,3,4)]:
    nth = a * r**(n-1)
    s = int(a*(r**n-1)//(r-1))
    prog.append(make_mcq(f"GP: first term {a}, common ratio {r}. {n}th term is:",
        [str(nth-a),str(nth),str(nth+a),str(nth+2*a)],1,"Progressions"))
    prog.append(make_tita(f"GP: first term {a}, ratio {r}. Sum of {n} terms:",s,"Progressions"))

questions_by_topic["Progressions"] = prog

# ── 8. LOGARITHMS ─────────────────────────────────────────────────────────────
log = []
for base,result,exp in [(2,8,3),(3,27,3),(5,125,3),(2,16,4),(10,1000,3),(4,64,3),(2,32,5),(3,81,4)]:
    log.append(make_mcq(f"log_{base}({result}) = ?",
        [str(exp-2),str(exp-1),str(exp),str(exp+1)],2,"Logarithms"))
    log.append(make_tita(f"If log_{base}(x) = {exp}, find x.",result,"Logarithms"))

for a,b in [(2,8),(3,9),(5,25),(2,4),(10,100)]:
    log.append(make_mcq(f"log_{a}({a**2}) + log_{a}({b}) = ?",
        ["2","3","4","5"],0,"Logarithms"))

for n in [1,10,100,1000]:
    v = int(math.log10(n))
    log.append(make_tita(f"log₁₀({n}) = ?",v,"Logarithms"))

questions_by_topic["Logarithms"] = log

# ── 9. SI / CI ────────────────────────────────────────────────────────────────
sici = []
for p,r,t in [(1000,10,2),(2000,5,3),(5000,8,2),(3000,12,1),(4000,6,3),(2500,10,4)]:
    si = p*r*t//100
    sici.append(make_mcq(f"SI on ₹{p} at {r}% p.a. for {t} years:",
        [str(si-100),str(si-50),str(si),str(si+50)],2,"SI/CI"))
    sici.append(make_tita(f"SI on ₹{p} at {r}% p.a. for {t} years. Amount = ?",p+si,"SI/CI"))

for p,r,t in [(1000,10,2),(2000,20,2),(5000,10,2),(4000,5,2)]:
    ci = int(p*(1+r/100)**t) - p
    sici.append(make_mcq(f"CI on ₹{p} at {r}% compounded annually for {t} years:",
        [str(ci-50),str(ci-10),str(ci),str(ci+50)],2,"SI/CI"))

questions_by_topic["SI/CI"] = sici

# ── 10. PROFIT & LOSS ─────────────────────────────────────────────────────────
pl = []
for cp,sp in [(100,120),(150,180),(200,250),(80,100),(250,300),(400,480),(500,600),(600,720)]:
    profit = sp-cp; pct = profit*100//cp
    pl.append(make_mcq(f"CP = ₹{cp}, SP = ₹{sp}. Profit % is:",
        [str(pct-5),str(pct-2),str(pct),str(pct+5)],2,"Profit/Loss"))
    pl.append(make_tita(f"CP = ₹{cp}, SP = ₹{sp}. Profit = ₹?",profit,"Profit/Loss"))

for cp,loss_pct in [(200,10),(500,20),(400,15),(300,25)]:
    sp = cp*(100-loss_pct)//100
    pl.append(make_mcq(f"CP = ₹{cp}, loss = {loss_pct}%. SP is:",
        [str(sp-20),str(sp-10),str(sp),str(sp+10)],2,"Profit/Loss"))

for mp,disc in [(200,10),(500,20),(400,15),(300,25),(600,10)]:
    sp = mp*(100-disc)//100
    pl.append(make_tita(f"Marked price = ₹{mp}, discount = {disc}%. Selling price = ₹?",sp,"Profit/Loss"))

questions_by_topic["Profit/Loss"] = pl

# ── 11. PnC ───────────────────────────────────────────────────────────────────
pnc = []
factorials = {0:1,1:1,2:2,3:6,4:24,5:120,6:720,7:5040,8:40320}
for n,r in [(5,2),(6,3),(7,2),(8,2),(4,2),(5,3),(6,2),(7,3)]:
    p = factorials[n]//factorials[n-r]
    c = p//factorials[r]
    pnc.append(make_mcq(f"P({n},{r}) = ?",
        [str(p-r*factorials[r]),str(p),str(p+factorials[r]),str(p+2*factorials[r])],1,"PnC"))
    pnc.append(make_mcq(f"C({n},{r}) = ?",
        [str(c-5),str(c-2),str(c),str(c+3)],2,"PnC"))

for n in [3,4,5,6]:
    pnc.append(make_tita(f"In how many ways can {n} people sit in a row?",factorials[n],"PnC"))
    pnc.append(make_mcq(f"In how many ways can {n} people sit in a circle?",
        [str(factorials[n-1]-6),str(factorials[n-1]-2),str(factorials[n-1]),str(factorials[n-1]+2)],2,"PnC"))

questions_by_topic["PnC"] = pnc

# ── 12. MIXTURES ──────────────────────────────────────────────────────────────
mix = []
for v1,c1,v2,c2 in [(4,10,6,20),(3,15,7,25),(5,30,5,50),(10,40,10,60),(2,20,8,40)]:
    avg = (v1*c1+v2*c2)//(v1+v2)
    mix.append(make_mcq(f"{v1}L at {c1}% mixed with {v2}L at {c2}%. Result %:",
        [str(avg-3),str(avg-1),str(avg),str(avg+2)],2,"Mixtures"))

for tot,c1,c2,result in [(10,20,80,44),(20,10,60,35),(15,30,90,66)]:
    v1 = int(tot*(result-c2)/(c1-c2))
    mix.append(make_tita(f"Mix {c1}% and {c2}% solutions to get {result}% in {tot}L. Amount of {c1}% solution:",v1,"Mixtures"))

for milk,water,add in [(4,1,2),(6,2,3),(8,2,4),(10,5,5)]:
    tot = milk+water+add
    new_ratio_milk = milk; new_ratio_water = water+add
    mix.append(make_mcq(f"Milk:Water = {milk}:{water}. Add {add}L water. New water%:",
        [str(new_ratio_water*100//tot-5),str(new_ratio_water*100//tot-2),
         str(new_ratio_water*100//tot),str(new_ratio_water*100//tot+5)],2,"Mixtures"))

questions_by_topic["Mixtures"] = mix

# ── 13. FUNCTIONS ─────────────────────────────────────────────────────────────
fn = []
for a,b,x in [(2,3,4),(3,-1,2),(5,2,3),(-1,4,5),(4,-3,7),(2,5,6)]:
    val = a*x + b
    fn.append(make_mcq(f"If f(x) = {a}x {'+'if b>=0 else ''}{b}, find f({x}).",
        [str(val-4),str(val-2),str(val),str(val+3)],2,"Functions"))

for a,b,c,x in [(1,-5,6,3),(2,1,-3,2),(1,3,2,4),(3,-2,1,1)]:
    val = a*x*x + b*x + c
    fn.append(make_tita(f"If f(x) = {a}x² {'+'if b>=0 else ''}{b}x {'+'if c>=0 else ''}{c}, find f({x}).",val,"Functions"))

for a,b in [(1,2),(2,3),(3,4),(4,5)]:
    fn.append(make_mcq(f"Domain of f(x) = 1/(x−{a}) excludes:",
        [str(a-1),str(a),str(a+1),str(a+2)],1,"Functions"))

questions_by_topic["Functions"] = fn

# ── 14. CO-ORDINATE GEOMETRY ─────────────────────────────────────────────────
cg = []
for x1,y1,x2,y2 in [(0,0,3,4),(1,2,4,6),(2,3,5,7),(0,0,5,12),(1,1,4,5)]:
    dist = int(math.sqrt((x2-x1)**2+(y2-y1)**2))
    cg.append(make_mcq(f"Distance between ({x1},{y1}) and ({x2},{y2}):",
        [str(dist-2),str(dist-1),str(dist),str(dist+1)],2,"Co-Geo"))

for x1,y1,x2,y2 in [(0,0,4,6),(2,4,6,8),(1,3,5,7),(0,0,6,10)]:
    mx = (x1+x2)//2; my = (y1+y2)//2
    cg.append(make_tita(f"Midpoint of ({x1},{y1}) and ({x2},{y2}): x-coordinate is?",mx,"Co-Geo"))
    cg.append(make_tita(f"Midpoint of ({x1},{y1}) and ({x2},{y2}): y-coordinate is?",my,"Co-Geo"))

for m,c,x in [(2,3,4),(3,-1,2),(4,5,1),(-2,7,3)]:
    y = m*x+c
    cg.append(make_mcq(f"Line y = {m}x {'+'if c>=0 else ''}{c}. At x = {x}, y is:",
        [str(y-4),str(y-2),str(y),str(y+2)],2,"Co-Geo"))

for m1,m2 in [(2,3),(4,5),(1,7),(3,6)]:
    cg.append(make_mcq(f"Lines with slopes {m1} and {m2} are:",
        ["Parallel","Perpendicular","Coincident","Neither parallel nor perpendicular"],3,"Co-Geo"))

questions_by_topic["Co-Geo"] = cg

# ─── BUILD PAPER SETS ─────────────────────────────────────────────────────────
all_q = {}
topics = list(questions_by_topic.keys())

def make_cat_paper(label, seed_offset):
    random.seed(42 + seed_offset)
    paper = []
    per_topic = 22 // len(topics) + 1
    for t in topics:
        pool = questions_by_topic[t]
        n = min(per_topic, len(pool))
        paper.extend(random.sample(pool, n))
    random.shuffle(paper)
    return paper[:22]

def make_ipm_paper(label, seed_offset):
    random.seed(100 + seed_offset)
    paper = []
    per_topic = 45 // len(topics) + 1
    for t in topics:
        pool = questions_by_topic[t]
        n = min(per_topic, len(pool))
        paper.extend(random.sample(pool, n))
    random.shuffle(paper)
    return paper[:45]

# CAT papers
for slot in range(1,4):
    all_q[f"CAT_SET_{slot}A"] = make_cat_paper(f"CAT Set {slot}A", slot)
    all_q[f"CAT_SET_{slot}B"] = make_cat_paper(f"CAT Set {slot}B", slot+10)
    all_q[f"CAT_SET_{slot}C"] = make_cat_paper(f"CAT Set {slot}C", slot+20)

# More CAT papers
for i in range(1,9):
    all_q[f"CAT_MOCK_{i}"] = make_cat_paper(f"CAT Mock {i}", i+30)

# IPM papers
for i in range(1,7):
    all_q[f"IPM_MOCK_{i}"] = make_ipm_paper(f"IPM Mock {i}", i+50)

# Stats
total = sum(len(v) for v in all_q.values())
print(f"Generated {len(all_q)} papers with {total} total question slots")
for t,qs in questions_by_topic.items():
    print(f"  {t}: {len(qs)} questions")

with open("/sessions/vibrant-serene-hawking/matharena-mock/data/questions.json","w") as f:
    json.dump(all_q, f)
print("Saved questions.json")
