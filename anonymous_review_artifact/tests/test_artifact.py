import json,unittest,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def jl(n):return [json.loads(l) for l in (ROOT/'data'/n).read_text(encoding='utf-8').splitlines() if l.strip()]
class ReviewArtifact(unittest.TestCase):
 def test_items(self):
  r=jl('items.jsonl');self.assertEqual(len(r),66);self.assertEqual(len({x['id'] for x in r}),66)
 def test_reviews(self):
  r=jl('reviews.jsonl');self.assertEqual(len(r),836);self.assertEqual(len({x['release_id'] for x in r}),836);self.assertEqual(len({(x['campaign'],x['item'],x['model'],x['mode']) for x in r}),660)
 def test_annotations(self):
  a=jl('annotations.jsonl');ids={r['release_id'] for r in jl('reviews.jsonl')};self.assertEqual(len(a),686);self.assertTrue({r['release_id'] for r in a}.issubset(ids));self.assertTrue(all(x['label']!='ADJUDICATE' for r in a for x in r['issues']))
 def test_pilot(self):
  r=jl('pilot_reviews.jsonl');self.assertEqual(len(r),72);self.assertEqual(len(jl('pilot_items.jsonl')),18);self.assertEqual({x['review_id'] for x in r},{x['review_id'] for x in jl('pilot_annotations.jsonl')})
 def test_metrics(self):
  s=json.loads((ROOT/'outputs/summary.json').read_text(encoding='utf-8'));self.assertEqual(s['human_review_labels_core']['T'],71);self.assertEqual(s['expansion_sampling_stability']['naming_unanimous_cells'],85)
 def test_prompt(self):
  r=subprocess.run([sys.executable,'-B',str(ROOT/'render_prompt.py'),'D2-a','bare'],capture_output=True,text=True,encoding='utf-8');self.assertEqual(r.returncode,0,r.stderr);d=json.loads(r.stdout);self.assertEqual(d['mode'],'bare');self.assertTrue(d['user_messages'][0]['content'])
if __name__=='__main__':unittest.main()
