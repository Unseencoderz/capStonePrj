import requests


# metrics placeholders (import from prometheus_client in the runtime environment)
try:
from prometheus_client import Counter
TOOL_ERRORS = Counter('tool_errors_total', 'Number of tool invocation errors')
except Exception:
# fallback dummy
class DummyCounter:
def inc(self, n=1):
return
TOOL_ERRORS = DummyCounter()




def jira_tool_create(action: Dict[str, Any]) -> Dict[str, Any]:
payload = {
"action_id": action.get("id", ""),
"title": (action.get("text", "") or "")[:240],
"description": action.get("text", "") or "",
"owner": action.get("owner") or "",
"due": action.get("due") or ""
}
try:
r = requests.post(f"{TOOL_SERVER}/jira/create", json=payload, timeout=5)
r.raise_for_status()
return r.json()
except Exception as e:
try:
TOOL_ERRORS.inc()
except Exception:
pass
return {"ticket_id": f"SIM-FALLBACK-{action.get('id','')[:8]}", "url": None, "action_id": action.get('id')}




def repo_search_tool(query: str, top_k: int = 3) -> List[Dict[str, Any]]:
payload = {"query": query, "top_k": top_k}
try:
r = requests.post(f"{TOOL_SERVER}/repo/search", json=payload, timeout=5)
r.raise_for_status()
return r.json().get("results", [])
except Exception:
return []




def calendar_create_tool(title: str, start: str, end: str, attendees: List[str] = None) -> Dict[str, Any]:
payload = {"title": title, "start": start, "end": end, "attendees": attendees or []}
try:
r = requests.post(f"{TOOL_SERVER}/calendar/create", json=payload, timeout=5)
r.raise_for_status()
return r.json()
except Exception:
return {"event_id": "SIM-EVT-0000", "link": None}