import os, json, time, csv
from typing import List, Dict, Any
import pandas as pd
from tqdm import tqdm

from retail_router.router import RetailRouter

def load_golden(path: str) -> List[Dict[str, Any]]:
    items = []
    with open(path, "r") as f:
        for line in f:
            items.append(json.loads(line))
    return items

def contains_all(text: str, needles: List[str]) -> bool:
    low = text.lower()
    return all(n.lower() in low for n in needles)

def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Set OPENAI_API_KEY in your environment.")

    model = os.getenv("ROUTER_MODEL", "gpt-4o-mini")
    embed_model = os.getenv("EMBED_MODEL", "text-embedding-3-small")
    top_k = int(os.getenv("TOP_K", "4"))

    router = RetailRouter(model=model, embed_model=embed_model, top_k=top_k)
    goldens = load_golden("retail_router/evals/golden.jsonl")

    rows = []
    for g in tqdm(goldens, desc="Evaluating"):
        r = router.decide_and_execute(g["query"])

        picked_tool = r.get("tool_name")
        answer = r.get("answer","")
        ok = r.get("ok", False)

        tool_match = int(picked_tool == g["expected_tool"])
        answer_contains = int(contains_all(answer, g["must_contain"]))

        rows.append({
            "qid": g["qid"],
            "expected_tool": g["expected_tool"],
            "picked_tool": picked_tool,
            "tool_match": tool_match,
            "must_contain": ";".join(g["must_contain"]),
            "answer_contains": answer_contains,
            "ok": int(ok)
        })

    df = pd.DataFrame(rows)
    df.to_csv("results.csv", index=False)

    tool_acc = df["tool_match"].mean()
    ans_acc = df["answer_contains"].mean()
    print(f"Tool Selection Accuracy: {tool_acc:.3f}")
    print(f"Answer Must-Contain Rate: {ans_acc:.3f}")
    print("Wrote results.csv")

if __name__ == "__main__":
    main()
