"""Verify Plumbline repository files, hashes, and data hygiene."""
import argparse,hashlib,json,re,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
SKIP={'MANIFEST.json'}
def release_files():
    return sorted(p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and '.git' not in p.parts and p.relative_to(ROOT).parts[0]!='outputs' and p.suffix!='.pyc')
def main():
    a=argparse.ArgumentParser();a.add_argument('--build-manifest',action='store_true');args=a.parse_args();errors=[];files=release_files();inventory={}
    secret=re.compile(r'\b(?:sk-[A-Za-z0-9_-]{24,}|ghp_[A-Za-z0-9]{24,}|github_pat_[A-Za-z0-9_]{24,})')
    local=re.compile(r'[A-Za-z]:[\\/](?:Users[\\/]|my[\\/]ICPC)',re.I)
    forbidden={'node_modules','.venv','__pycache__'}
    def inspect(text,name):
        if secret.search(text):errors.append('Credential-like token: '+name)
        if local.search(text.replace('\\\\','\\')):errors.append('Local-machine path: '+name)
    for p in files:
        rel=p.relative_to(ROOT).as_posix()
        if p.relative_to(ROOT).parts[0] in forbidden or p.name=='.env' or p.suffix in ['.key','.pem']:errors.append('Unexpected runtime/credential file: '+rel)
        if p.suffix in ['.json','.jsonl','.md','.py','.txt']:inspect(p.read_text(encoding='utf-8'),rel)
        if p.suffix=='.zip':
            with zipfile.ZipFile(p) as z:
                assert z.testzip() is None
                for name in z.namelist():
                    if any(x in name.split('/') for x in ['.git','.venv','__pycache__']):errors.append('Runtime/Git material in source snapshots: '+name)
                    try:inspect(z.read(name).decode('utf-8'),'source snapshot/'+name)
                    except UnicodeDecodeError:errors.append('Unexpected binary source snapshot: '+name)
        if rel not in SKIP:inventory[rel]={'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
    manifest=ROOT/'MANIFEST.json'
    if args.build_manifest:
        manifest.write_text(json.dumps({'project':'Plumbline','purpose':'public research repository','hash':'sha256','excluded_generated_directory':'outputs/','files':inventory},indent=2)+'\n',encoding='utf-8',newline='\n')
    else:
        expected=json.loads(manifest.read_text(encoding='utf-8'))['files']
        for name in sorted(set(expected)|set(inventory)):
            if expected.get(name)!=inventory.get(name):errors.append('Inventory/hash mismatch: '+name)
    if errors:
        print('\n'.join(errors));raise SystemExit(1)
    print(f'PASS: {len(inventory)} release files; hashes, source snapshot archive and data hygiene checked.')
if __name__=='__main__':main()
