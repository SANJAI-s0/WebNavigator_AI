from webnavigator_ai.agent.memory import AgentMemory


def test_agent_memory_store_and_retrieve(tmp_path):
    memory_path = tmp_path / "memory.json"
    memory = AgentMemory(path=str(memory_path))

    memory.remember_query("python selenium", "https://example.com")
    memory.remember_query("github", "https://github.com")

    assert memory.recall_query("python selenium") == "https://example.com"
    assert memory.recall_query("github") == "https://github.com"
    assert memory.recall_query("unknown") is None
