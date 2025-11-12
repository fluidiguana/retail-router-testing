import os, json, time, math, uuid
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple
import numpy as np

from openai import OpenAI
from .tools import TOOLS

def cosine(a: np.ndarray, b: np.ndarray) -> float:
    denom = (np.linalg.norm(a) * np.linalg.norm(b)) or 1e-9
    return float(np.dot(a, b) / denom)

@dataclass
class ToolSpec:
    name: str
    description: str
    schema: Dict[str, Any]
    embedding: np.ndarray

class RetailRouter:
    def __init__(self, model: str = "gpt-4o-mini", embed_model: str = "text-embedding-3-small", top_k: int = 4):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model
        self.embed_model = embed_model
        self.top_k = top_k
        self._tool_specs: List[ToolSpec] = []
        texts = [f"{t.name}: {t.description}" for t in TOOLS]
        embs = self.client.embeddings.create(model=self.embed_model, input=texts).data
        for t, e in zip(TOOLS, embs):
            self._tool_specs.append(ToolSpec(
                name=t.name, description=t.description, schema=t.schema,
                embedding=np.array(e.embedding, dtype=np.float32)
            ))

    def _retrieve_tools(self, query: str) -> List[ToolSpec]:
        q_emb = self.client.embeddings.create(model=self.embed_model, input=query).data[0].embedding
        q_emb = np.array(q_emb, dtype=np.float32)
        scored = [(cosine(q_emb, ts.embedding), ts) for ts in self._tool_specs]
        scored.sort(key=lambda x: x[0], reverse=True)
        return [ts for _, ts in scored[: self.top_k]]

    def _format_tool_options(self, tool_specs: List[ToolSpec]) -> List[Dict[str, Any]]:
        return [{
            "type":"function",
            "function": {
                "name": ts.name,
                "description": ts.description,
                "parameters": ts.schema
            }
        } for ts in tool_specs]

    def decide_and_execute(self, query: str) -> Dict[str, Any]:
        cands = self._retrieve_tools(query)
        tools_for_llm = self._format_tool_options(cands)

        sys = "You are a precise retail assistant. Pick exactly one tool from the provided functions and return the best arguments. Do not invent fields."
        messages = [
            {"role":"system","content":sys},
            {"role":"user","content":query}
        ]
        
        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools_for_llm,
                tool_choice="required"
            )
        except Exception as e:
            return {"ok": False, "error": f"API call failed: {str(e)}"}

        message = resp.choices[0].message
        
        # Check for tool calls
        if not message.tool_calls or len(message.tool_calls) == 0:
            return {"ok": False, "error": "No tool selected by model."}

        tool_call = message.tool_calls[0]
        tool_name = tool_call.function.name
        tool_args = json.loads(tool_call.function.arguments)

        tool_map = {t.name: t for t in TOOLS}
        if tool_name not in tool_map:
            return {"ok": False, "error": f"Unknown tool '{tool_name}' chosen."}

        tool_handler = tool_map[tool_name].handler
        tool_result = tool_handler(tool_args)

        # Synthesize final answer
        # Convert message to dict format for the API
        assistant_msg = {"role": "assistant", "content": message.content}
        if message.tool_calls:
            assistant_msg["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": tc.type,
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                } for tc in message.tool_calls
            ]
        
        synth_messages = [
            {"role":"system","content":"Answer succinctly for a retail operator. Include critical numbers and the action to take."},
            {"role":"user","content":query},
            assistant_msg,
            {"role":"tool","name":tool_name,"content":json.dumps(tool_result)}
        ]
        
        try:
            synth = self.client.chat.completions.create(
                model=self.model,
                messages=synth_messages
            )
            final_text = synth.choices[0].message.content or ""
        except Exception as e:
            return {"ok": False, "error": f"Synthesis failed: {str(e)}", "tool_name": tool_name, "tool_result": tool_result}

        return {
            "ok": True,
            "tool_name": tool_name,
            "tool_args": tool_args,
            "tool_result": tool_result,
            "answer": final_text.strip()
        }
