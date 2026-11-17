import argparse, json, sys, urllib.error, urllib.request

def get_json(url, timeout):
    req=urllib.request.Request(url,headers={'Accept':'application/json','User-Agent':'llama-server-preflight/1.0'})
    try:
        with urllib.request.urlopen(req,timeout=timeout) as response:
            body=response.read(1024*1024+1)
            if len(body)>1024*1024: raise ValueError('response exceeds 1 MiB safety limit')
            return response.status,json.loads(body.decode('utf-8'))
    except urllib.error.HTTPError as e:
        return e.code, {'error':str(e)}

def check(base_url, expected_model=None, timeout=3):
    base=base_url.rstrip('/')+'/'
    health_status,health=get_json(urllib.request.urljoin(base,'health'),timeout)
    models_status,models=get_json(urllib.request.urljoin(base,'v1/models'),timeout)
    ids=[]
    if isinstance(models,dict) and isinstance(models.get('data'),list):
        ids=[str(x.get('id')) for x in models['data'] if isinstance(x,dict) and x.get('id')]
    model_ok=expected_model is None or expected_model in ids
    ready=health_status==200 and models_status==200 and model_ok
    return {'ready':ready,'base_url':base_url,'health_status':health_status,'models_status':models_status,'models':ids,'expected_model':expected_model,'expected_model_available':model_ok}

def main():
    p=argparse.ArgumentParser(description='Preflight a llama.cpp OpenAI-compatible server')
    p.add_argument('--base-url',default='http://127.0.0.1:8080'); p.add_argument('--model'); p.add_argument('--timeout',type=float,default=3.0); p.add_argument('--json',action='store_true')
    a=p.parse_args()
    if not (a.base_url.startswith('http://') or a.base_url.startswith('https://')): p.error('--base-url must be HTTP(S)')
    if a.timeout<=0: p.error('--timeout must be positive')
    try: result=check(a.base_url,a.model,a.timeout)
    except (OSError,ValueError,TimeoutError) as e:
        print(f'error: {e}',file=sys.stderr); return 2
    if a.json: print(json.dumps(result,indent=2))
    else:
        print(('READY' if result['ready'] else 'NOT READY')+'  '+a.base_url)
        print(f"Health: HTTP {result['health_status']}\nModels: {', '.join(result['models']) or '(none)'}")
        if a.model: print('Expected model: '+('available' if result['expected_model_available'] else 'missing'))
    return 0 if result['ready'] else 1
if __name__=='__main__': raise SystemExit(main())
