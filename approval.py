# === FILE: approvals.py ===


# convenience functions
approval_store = RedisApprovalStore(redis_client)


# helper to store pending approvals using the store
def controller_store_pending(controller, raw_transcript: str):
norm = controller.normalizer.normalize(raw_transcript)
enriched = controller.enricher.enrich(norm)
actions = controller.extractor.extract(enriched)
approval_ids = []
for a in actions:
aid = approval_store.store_pending(a)
approval_ids.append(aid)
logger.info(json.dumps({"event":"approval_stored", "approval_id": aid, "action_id": a["id"]}))
return {"approvals_created": approval_ids, "count": len(approval_ids)}


# approve helper
from tools import jira_tool_create


def approve_and_create(approval_id: str, ticket_creator_fn = None):
payload = approval_store.get(approval_id)
if not payload:
return None
if payload["status"] != "pending":
return payload
action = payload["action"]
ticket = None
if ticket_creator_fn:
ticket = ticket_creator_fn(action)
else:
ticket = jira_tool_create(action)
patch = {"status": "created", "ticket": ticket, "approved_ts": int(time.time())}
updated = approval_store.update(approval_id, patch)
logger.info(json.dumps({"event":"approval_approved", "approval_id": approval_id, "ticket": ticket}))
return updated




def defer_approval(approval_id: str, reason: str = None):
payload = approval_store.get(approval_id)
if not payload:
return None
patch = {"status": "deferred", "notes": reason, "deferred_ts": int(time.time())}
updated = approval_store.update(approval_id, patch)
logger.info(json.dumps({"event":"approval_deferred", "approval_id": approval_id, "reason": reason}))
return updated


# === END FILE: approvals.py ===