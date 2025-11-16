import json
import uuid
import logging
from typing import List, Dict, Any, Callable, Optional


logger = logging.getLogger("observability")


class TranscriptNormalizer:
# """Cleans transcript text, splits into segments."""
def normalize(self, raw_transcript: str) -> Dict[str, Any]:
lines = [ln.strip() for ln in raw_transcript.splitlines() if ln.strip()]
normalized = {"segments": [{"id": i, "text": lines[i]} for i in range(len(lines))], "meta": {"len": len(lines)}}
logger.info(json.dumps({"event":"normalize", "segments": len(lines)}))
return normalized


class ContextEnricher:
# """Adds repo / meeting history context via injected functions."""
def __init__(self, repo_search_fn: Optional[Callable[[str], List[Dict[str,Any]]]] = None, memory_retrieval_fn: Optional[Callable[[str], List[Dict[str,Any]]]] = None):
self.repo_search_fn = repo_search_fn
self.memory_retrieval_fn = memory_retrieval_fn


def enrich(self, normalized_transcript: Dict[str, Any]) -> Dict[str, Any]:
text = " ".join(seg["text"] for seg in normalized_transcript["segments"][:10])
repo_matches = []
if self.repo_search_fn:
try:
repo_matches = self.repo_search_fn(text)
except Exception as e:
logger.info(json.dumps({"event":"repo_search_error","error": str(e)}))
memory_ctx = []
if self.memory_retrieval_fn:
try:
memory_ctx = self.memory_retrieval_fn(text)
except Exception as e:
logger.info(json.dumps({"event":"memory_search_error","error": str(e)}))
enriched = {"normalized": normalized_transcript, "repo_matches": repo_matches, "memory_ctx": memory_ctx}
logger.info(json.dumps({"event":"enrich", "repo_hits": len(repo_matches), "memory_hits": len(memory_ctx)}))
return enriched


class ActionExtractor:
"""Extracts structured actions from enriched transcript. By default uses a simple heuristic.
You can replace the 'model' parameter with an LLM wrapper to improve extraction.
"""
def __init__(self, model: Any = None, default_confidence: float = 0.75):
self.model = model
self.default_confidence = default_confidence


def extract(self, enriched: Dict[str, Any]) -> List[Dict[str, Any]]:
segments = enriched.get("normalized", {}).get("segments", [])
actions = []
for seg in segments:
text = seg.get("text", "")
# Heuristic: TODO, action, action item, assign, please, will
lower = text.lower()
if lower.startswith(("todo", "action", "assign", "please", "reminder", "note:")) or "action item" in lower or "todo" in lower:
a = {
"id": str(uuid.uuid4()),
"text": text,
"owner": None,
"due": None,
"confidence": self.default_confidence,
"source_segment_id": seg.get("id")
}
actions.append(a)
logger.info(json.dumps({"event":"extract", "actions_found": len(actions)}))
return actions

