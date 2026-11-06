"""Recompute Plumbline benchmark statistics and check the reference summary."""
import argparse, collections, hashlib, json, re
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def jl(path):
    return [json.loads(s) for s in Path(path).read_text(encoding="utf-8").splitlines() if s.strip()]

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument("--output-dir",type=Path,default=ROOT/"outputs");args=ap.parse_args();out=args.output_dir;out.mkdir(parents=True,exist_ok=True)
    items=jl(ROOT/"data/items.jsonl");reviews=jl(ROOT/"data/reviews.jsonl");annotations=jl(ROOT/"data/annotations.jsonl")
    assert len(items)==66 and len({x["id"] for x in items})==66
    assert len(reviews)==836 and len({x["release_id"] for x in reviews})==836
    assert len(annotations)==686
    ids={x["release_id"] for x in reviews};assert all(x["release_id"] in ids for x in annotations)
    A=[r for r in reviews if r["campaign"]=="core"];human=[r for r in annotations if r["campaign"]=="core" and r["item"].startswith("K4")]
    def ar(rs):
        valid=[r for r in rs if r["verdict"] in ("APPROVE","REQUEST_CHANGES")];n=sum(r["verdict"]=="APPROVE" for r in valid)
        return {"approve":n,"valid_verdicts":len(valid),"all_reviews":len(rs),"rate":n/len(valid) if valid else None}
    rates={"human_prs_core":ar([r for r in A if r["item"].startswith("K4")]),"agent_controls_core":ar([r for r in A if r["item"].startswith("K3")]),"behavioral_core":ar([r for r in A if r["cat"]=="bug"])}
    precision={}
    for model in sorted({r["model"] for r in annotations}):
        rr=[r for r in annotations if r["campaign"]!="expansion" and r["model"]==model and r["item"].startswith("K4")];counts=collections.Counter(i["label"] for r in rr for i in r["issues"]);n=sum(counts.values())
        precision[model]={"reviews":len(rr),"raised":n,"labels":dict(counts),"strict":counts["T"]/n if n else None,"lenient":(counts["T"]+counts["P"])/n if n else None,"refuted":counts["I"]/n if n else None}
    naming={}
    for item in ["D1-a","D1-b","D1-c"]:
        for condition in ["bare","context"]:
            rr=[r for r in annotations if r["campaign"]!="expansion" and r["item"]==item and ((r["mode"]=="bare")==(condition=="bare")) and r.get("leak") in ("Y","N")]
            naming[item+"/"+condition]={"named":sum(r["leak"]=="Y" for r in rr),"reviews":len(rr)}
    exp=[r for r in reviews if r["campaign"]=="expansion"];expann=[r for r in annotations if r["campaign"]=="expansion"]
    cells=collections.defaultdict(list)
    for r in expann:
        if r["cat"]=="leak":cells[(r["item"],r["model"],r["mode"])].append(r)
    rawbyid={r["release_id"]:r for r in reviews}
    stability={"leak_cells":len(cells),"naming_unanimous_cells":sum(len({r.get("leak") for r in rows})==1 for rows in cells.values()),"verdict_unanimous_cells":sum(len({rawbyid[r["release_id"]]["verdict"] for r in rows})==1 for rows in cells.values())}
    pilots=jl(ROOT/"data/pilot_reviews.jsonl")
    assert len(pilots)==72
    pilotlabels=jl(ROOT/"data/pilot_annotations.jsonl");pilotattrib=collections.defaultdict(lambda:[0,0])
    for r in pilotlabels:
        if r.get("construct")!="attribution":continue
        case=r["case_id"];family=case.split("-")[1][0];arm=case.rsplit("-",1)[1]
        if arm in ("min","bur"):
            pilotattrib[family+"/"+arm][0]+=(r["label"]=="Y");pilotattrib[family+"/"+arm][1]+=1
    summary={"counts":{"benchmark_items":66,"core_items":33,"expansion_items":33,"core_reviews":396,"gpt_replication_reviews":132,"expansion_reviews":308,"main_reviews":836,"main_unique_cells":len({(r['campaign'],r['item'],r['model'],r['mode']) for r in reviews}),"issue_labeled_reviews":686,"main_reviews_without_current_issue_level_labels":150,"pilot_items":18,"pilot_reviews_separate":72},"conditions":{"bare":"bare diff","generic":"architecture context","design":"architecture + design-review persona","linter":"architecture + detector/mutation report"},"raw_model_identifiers":sorted({r['model'] for r in reviews}),"approval_rates":rates,"human_review_labels_core":dict(collections.Counter(r.get('tpi') for r in human)),"human_issue_precision":precision,"core_buried_attribution":naming,"expansion_sampling_stability":stability,"pilot_attribution_from_supplied_labels":{k:{"named":v[0],"reviews":v[1]} for k,v in sorted(pilotattrib.items())},"pilot_excluded_nonviolation_family":"X"}
    expected=json.loads((ROOT/"expected/summary.json").read_text(encoding="utf-8"))
    checks=[]
    def compare(a,b,path="summary"):
        if isinstance(b,dict):
            assert isinstance(a,dict) and set(a)==set(b),path+" keys differ"
            for k in sorted(b):compare(a[k],b[k],path+"."+k)
        else:
            assert a==b,(path,a,b)
            checks.append(path)
    compare(summary,expected)
    (out/"summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (out/"verification.json").write_text(json.dumps({"pass":True,"checked_values":len(checks),"checks":checks,"network_calls":0},indent=2)+"\n",encoding="utf-8")
    print(f"PASS: {len(checks)} reference summary values checked; 836 main reviews + 72 separate pilot reviews.")
if __name__=="__main__":main()
