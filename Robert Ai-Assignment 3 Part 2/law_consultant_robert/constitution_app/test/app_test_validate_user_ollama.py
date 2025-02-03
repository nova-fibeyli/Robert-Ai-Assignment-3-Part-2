import pytest
from constitution_app.app import stream_chat
from utils.question_handler import get_multi_queries, reciprocal_rank_fusion

def test_stream_chat():
    """Ensures stream_chat() runs without crashing and returns default response for unrecognized input."""
    result = stream_chat("llama3.2", [{"role": "user", "content": "HELP"}])
    assert "I didn’t catch that" in result, "Chatbot should return a default response when it doesn't understand the input."

def test_stream_chat_no_constitution_retrieval():
    """Ensures chatbot does not retrieve content from constitution.json for irrelevant input."""
    result = stream_chat("llama3.2", [{"role": "user", "content": "Tell me a joke."}])
    assert "Article" not in result, "Chatbot should not retrieve legal content for non-legal queries."

def test_multi_query_generation():
    queries = get_multi_queries("What is constitutional law?")
    assert len(queries) == 5, "Multi-query should return exactly 5 queries."

def test_reciprocal_rank_fusion():
    mock_results = [[{"content": "Law A"}, {"content": "Law B"}], 
                    [{"content": "Law B"}, {"content": "Law C"}]]
    fused_results = reciprocal_rank_fusion(mock_results)
    assert len(fused_results) > 0, "RAG Fusion should return ranked documents."
    assert fused_results[0]["content"] in ["Law A", "Law B", "Law C"], "Results should be relevant."