"""Render a Plumbline benchmark prompt from the stored templates."""
import argparse,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
SPEC=json.loads((ROOT/'prompts/conditions.json').read_text(encoding='utf-8'))
MODE_PROMPTS=SPEC['MODE_PROMPTS'];ARCH_BLURB=SPEC['ARCH_BLURB']
ARCH=json.loads((ROOT/'prompts/architecture.json').read_text(encoding='utf-8'))
def clip_diff(diff: str, limit: int = 9000) -> str:
    """Head+tail truncation: huge diffs exhaust the output budget (thinking
    tokens + long JSON) and yield empty reviews that would silently bias
    the clean-item false-positive denominator."""
    if len(diff) <= limit:
        return diff
    return (diff[:6000] +
            "\n\n[... diff truncated for length ...]\n\n" + diff[-2500:])

def review_prompt(item: dict, mode: str) -> list[dict]:
    linter = f"\n\n{linter_block}" if (mode == "linter" and
              (linter_block := item.get("linter"))) else ""
    # bare mode withholds the architecture blurb: the reviewer must infer
    # the project's structure from the diff alone (no priors supplied)
    context = "" if mode == "bare" else f"{ARCH_BLURB}\n\n"
    user = (f"{context}PR title: {item['title']}\n\n"
            f"```diff\n{clip_diff(item['diff'])}\n```{linter}\n\n"
            "Respond with ONLY a JSON object: "
            '{"verdict": "APPROVE"|"REQUEST_CHANGES", "issues": '
            '[{"category": "bug"|"architecture"|"dead_code"|"style"|'
            '"security", "description": "..."}], "praise": ["..."]}')
    return [{"role": "user", "content": user}]

def review_prompt_with_repo_context(item: dict, mode: str) -> list[dict]:
    blurb = ARCH[item.get("repo_key", "rentomatic")]
    linter = f"\n\n{linter_block}" if (mode == "linter" and
              (linter_block := item.get("linter"))) else ""
    context = "" if mode == "bare" else f"{blurb}\n\n"
    user = (f"{context}PR title: {item['title']}\n\n"
            f"```diff\n{item['diff']}\n```{linter}\n\n"
            "Respond with ONLY a JSON object: "
            '{"verdict": "APPROVE"|"REQUEST_CHANGES", "issues": '
            '[{"category": "bug"|"architecture"|"dead_code"|"style"|'
            '"security", "description": "..."}], "praise": ["..."]}')
    return [{"role": "user", "content": user}]

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('item');ap.add_argument('mode',choices=list(MODE_PROMPTS),nargs='?',default='bare');a=ap.parse_args()
    rows=[json.loads(l) for l in (ROOT/'data/items.jsonl').read_text(encoding='utf-8').splitlines() if l.strip()];it=next(r for r in rows if r['id']==a.item)
    use_repo_builder=(it['campaign']=='core_grid' and it['id'].startswith(('K4','D1'))) or (it['campaign']=='expansion' and it.get('repo_key','rentomatic')!='rentomatic')
    msg=review_prompt_with_repo_context(it,a.mode) if use_repo_builder else review_prompt(it,a.mode)
    print(json.dumps({'item':a.item,'mode':a.mode,'system_prompt_template':MODE_PROMPTS[a.mode],'user_messages':msg,'record_type':'rendered_prompt_template'},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
