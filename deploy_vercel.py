#!/usr/bin/env python3
"""Publica uma pasta estática no projeto Vercel (conta jrsana22) via REST API.
uso: deploy_vercel.py <pasta> <projeto>   (token lido de VERCEL_TOKEN)"""
import os, sys, json, base64, urllib.request
pasta, projeto = sys.argv[1], sys.argv[2]
TEAM='team_kREzFic8ObZySiTy8NmOsaWB'; TK=os.environ['VERCEL_TOKEN']
files=[]
for raiz,_,nomes in os.walk(pasta):
    if '.vercel' in raiz or '.git' in raiz: continue
    for n in nomes:
        if n in ('.gitignore',): continue
        p=os.path.join(raiz,n); rel=os.path.relpath(p,pasta)
        files.append({'file':rel,'data':base64.b64encode(open(p,'rb').read()).decode(),'encoding':'base64'})
body={'name':projeto,'project':projeto,'target':'production','files':files,'projectSettings':{'framework':None,'buildCommand':None,'outputDirectory':None,'installCommand':None}}
req=urllib.request.Request(f'https://api.vercel.com/v13/deployments?teamId={TEAM}&skipAutoDetectionConfirmation=1',data=json.dumps(body).encode(),headers={'Authorization':f'Bearer {TK}','Content-Type':'application/json'},method='POST')
d=json.load(urllib.request.urlopen(req,timeout=120))
print(d.get('id'), d.get('readyState'), d.get('url'), len(files),'arquivos')
