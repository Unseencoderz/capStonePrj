# === FILE: main_agents.py ===
"""
main_agents.py
Instantiates agents, memory, and wiring for the agent API.
"""
from agents import TranscriptNormalizer, ContextEnricher, ActionExtractor, Controller
from tools import jira_tool_create, repo_search_tool
from memory_store import memory
from approvals import approval_store, controller_store_pending, approve_and_create, defer_approval


# instantiate components
normalizer = TranscriptNormalizer()
enricher = ContextEnricher(repo_search_fn=repo_search_tool, memory_retrieval_fn=memory.query)
extractor = ActionExtractor()


# ticket creator uses tools.jira_tool_create
ctrl = Controller(normalizer=normalizer, enricher=enricher, extractor=extractor, ticket_creator_fn=jira_tool_create)


# convenience exports
__all__ = ["ctrl", "controller_store_pending", "approval_store", "approve_and_create", "defer_approval"]


# === END FILE: main_agents.py ===