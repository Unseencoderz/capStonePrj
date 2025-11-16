from fastapi import FastAPI
from pydantic import BaseModel

# Import the components from your notebook workflow
from main_agents import (
    ctrl,
    controller_store_pending,
    approval_store,
    approve_and_create,
    defer_approval
)

app = FastAPI(
    title="Actionable Meeting Agent API",
    description="Runs multi-agent meeting analysis + approvals",
    version="1.0.0"
)

class TranscriptRequest(BaseModel):
    text: str
    create_tickets: bool = False

@app.post("/run")
def run_agent(req: TranscriptRequest):
    """Full pipeline run: normalize, enrich, extract, and optionally create tickets."""
    result = ctrl.run(req.text, create_tickets=req.create_tickets)
    return result

class PauseRequest(BaseModel):
    text: str

@app.post("/pending")
def create_pending(req: PauseRequest):
    """Pause mode: store pending approvals."""
    return controller_store_pending(ctrl, req.text)

@app.get("/pending")
def list_pending():
    return approval_store.list_pending()

class ApprovalRequest(BaseModel):
    reason: str = None

@app.post("/approve/{approval_id}")
def approve(approval_id: str):
    res = approve_and_create(approval_id, ctrl.ticket_creator_fn)
    return res

@app.post("/defer/{approval_id}")
def defer(approval_id: str, req: ApprovalRequest):
    return defer_approval(approval_id, req.reason)
