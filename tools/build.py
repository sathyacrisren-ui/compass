#!/usr/bin/env python3
"""Build index.html from src/app.html + the O*NET tables in data/.

O*NET 31.0 database, U.S. Department of Labor, Employment and Training
Administration, CC BY 4.0. Interest Profiler Short Form items, same source.
"""
import csv, json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, 'data')

occ = {r['O*NET-SOC Code']: r for r in csv.DictReader(open(os.path.join(D, 'occupation_data.csv')))}
jz = {r['O*NET-SOC Code']: int(r['Job Zone']) for r in csv.DictReader(open(os.path.join(D, 'job_zones.csv')))}
AREAS = ['Realistic', 'Investigative', 'Artistic', 'Social', 'Enterprising', 'Conventional']
ci = {}
for r in csv.DictReader(open(os.path.join(D, 'Career Interest Types.txt')), delimiter='\t'):
    if r['Scale ID'] == 'OI':
        ci.setdefault(r['O*NET-SOC Code'], {})[r['Element Name']] = float(r['Data Value'])

def short(s, n=200):
    s = s.strip()
    if len(s) <= n: return s
    cut = s[:n]
    m = re.search(r'^(.*[.;])\s', cut)
    return (m.group(1) if m else cut.rsplit(' ', 1)[0] + '…')

jobs = []
for code, v in ci.items():
    if code not in occ or code not in jz: continue
    if len(v) != 6: continue
    jobs.append({'c': code, 't': occ[code]['Title'], 'd': short(occ[code]['Description']),
                 'z': jz[code], 'i': [v[a] for a in AREAS]})
jobs.sort(key=lambda j: j['t'])

# O*NET Interest Profiler Short Form, 60 items (U.S. Department of Labor, CC BY 4.0)
ip = {
 'Realistic': ['Build kitchen cabinets','Lay brick or tile','Repair household appliances','Raise fish in a fish hatchery','Assemble electronic parts','Drive a truck to deliver packages to offices and homes','Test the quality of parts before shipment','Repair and install locks','Set up and operate machines to make products','Put out forest fires'],
 'Investigative': ['Develop a new medicine','Study ways to reduce water pollution','Conduct chemical experiments','Study the movement of planets','Examine blood samples using a microscope','Investigate the cause of a fire','Develop a way to better predict the weather','Work in a biology lab','Invent a replacement for sugar','Do laboratory tests to identify diseases'],
 'Artistic': ['Write books or plays','Play a musical instrument','Compose or arrange music','Draw pictures','Create special effects for movies','Paint sets for plays','Write scripts for movies or television shows','Perform jazz or tap dance','Sing in a band','Edit movies'],
 'Social': ['Teach an individual an exercise routine','Help people with personal or emotional problems','Give career guidance to people','Perform rehabilitation therapy','Do volunteer work at a non-profit organization','Teach children how to play sports','Teach sign language to people who are deaf or hard of hearing','Help conduct a group therapy session','Take care of children at a day-care center','Teach a high-school class'],
 'Enterprising': ['Buy and sell stocks and bonds','Manage a retail store','Operate a beauty salon or barber shop','Manage a department within a large company','Start your own business','Negotiate business contracts','Represent a client in a lawsuit','Market a new line of clothing','Sell merchandise at a department store','Manage a clothing store'],
 'Conventional': ['Develop a spreadsheet using computer software','Proofread records or forms','Install software across computers on a large network','Operate a calculator','Keep shipping and receiving records','Calculate the wages of employees','Inventory supplies using a hand-held computer','Record rent payments','Keep inventory records','Stamp, sort, and distribute mail for an organization'],
}
ip_items = [{'a': i, 'q': q} for i, a in enumerate(AREAS) for q in ip[a]]
assert len(ip_items) == 60, len(ip_items)

src = open(os.path.join(ROOT, 'src', 'app.html')).read()
data = 'const JOBS=' + json.dumps(jobs, separators=(',', ':'), ensure_ascii=False) + ';\nconst IP_ITEMS=' + json.dumps(ip_items, separators=(',', ':'), ensure_ascii=False) + ';'
assert '/*DATA*/' in src
out = src.replace('/*DATA*/', data)
open(os.path.join(ROOT, 'index.html'), 'w').write(out)
print('index.html', len(out) // 1024, 'KB,', len(jobs), 'occupations')
