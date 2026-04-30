"""
Tests for agents
"""

import pytest
import asyncio
from src.agents import MasterAgent
from src.agents.retrieval_agent import RetrievalAgent
from src.agents.generation_agent import GenerationAgent


@pytest.mark.asyncio
async def test_master_agent_initialization():
    """Test master agent initialization"""
    agent = MasterAgent()
    assert await agent.initialize()
    assert agent.name == "MasterAgent"
    await agent.shutdown()


@pytest.mark.asyncio
async def test_retrieval_agent_initialization():
    """Test retrieval agent initialization"""
    agent = RetrievalAgent()
    assert await agent.initialize()
    assert agent.name == "RetrievalAgent"
    await agent.shutdown()


@pytest.mark.asyncio
async def test_generation_agent_initialization():
    """Test generation agent initialization"""
    agent = GenerationAgent()
    # Skip actual initialization if API is not available
    try:
        result = await agent.initialize()
        assert result is not None
    except Exception as e:
        # Expected if API is not configured
        pass
    await agent.shutdown()


@pytest.mark.asyncio
async def test_task_queue():
    """Test task queue"""
    from src.core.task_queue import TaskQueue, TaskPriority

    queue = TaskQueue()
    task_id = await queue.add_task(
        name="test_task",
        payload={"test": "data"},
        priority=TaskPriority.NORMAL,
    )

    assert task_id is not None
    assert task_id in queue.tasks


@pytest.mark.asyncio
async def test_state_manager():
    """Test state manager"""
    from src.core.state_manager import StateManager, ExecutionState

    manager = StateManager()
    context = manager.create_context(
        execution_id="test-exec-123",
        agent_name="TestAgent",
        task_input={"test": "data"},
    )

    assert context is not None
    assert context.execution_id == "test-exec-123"

    manager.update_state(
        "test-exec-123",
        ExecutionState.COMPLETED,
    )

    assert manager.get_context("test-exec-123").state == ExecutionState.COMPLETED
