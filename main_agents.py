# Extract your notebook logic into main_agents.py

# Create a file containing:

# TranscriptNormalizer

# ContextEnricher

# ActionExtractor

# Controller

# jira_tool_create_with_metrics

# repo_search_tool

# memory & vector store

# approval_store

# Any utilities

# For now, paste this minimal version:

from agents import TranscriptNormalizer, ContextEnricher, ActionExtractor, Controller
from tools import jira_tool_create_with_metrics, repo_search_tool
from memory_store import memory
from approvals import approval_store, controller_store_pending, approve_and_create, defer_approval

# Instantiate agents
normalizer = TranscriptNormalizer()
enricher = ContextEnricher(repo_search_fn=repo_search_tool, memory_retrieval_fn=memory.query)
extractor = ActionExtractor()

# Full controller
ctrl = Controller(
    normalizer=normalizer,
    enricher=enricher,
    extractor=extractor,
    ticket_creator_fn=jira_tool_create_with_metrics
)
