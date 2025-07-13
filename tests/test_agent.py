import pytest
import asyncio
from unittest.mock import Mock, patch
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from mcp_bugbounty_agent.agent import BugBountyResearchAgent

@pytest.fixture
def agent():
    return BugBountyResearchAgent(premium=False, use_docker=False)

@pytest.fixture
def premium_agent():
    return BugBountyResearchAgent(api_key="test-key", premium=True, use_docker=False)

def test_agent_initialization(agent):
    assert agent.premium == False
    assert agent.use_docker == False
    assert agent.session_id is not None
    assert len(agent.session_id) == 8

def test_premium_agent_initialization(premium_agent):
    assert premium_agent.premium == True
    assert premium_agent.api_key == "test-key"

def test_validate_premium_access_free(agent):
    # Free tier should have limited access
    for _ in range(5):  # Try more than 3 times
        access = agent.validate_premium_access()
        if not access:
            break
    assert not access  # Should be denied after 3 uses

def test_validate_premium_access_premium(premium_agent):
    # Premium should always have access
    for _ in range(10):
        assert premium_agent.validate_premium_access() == True

@pytest.mark.asyncio
async def test_orchestrate_research_basic(agent):
    result = await agent.orchestrate_research("TestTarget", ["idor"])
    
    assert "session_id" in result
    assert "target" in result
    assert result["target"] == "TestTarget"
    assert "vulnerability_count" in result
    assert result["vulnerability_count"] >= 0

@pytest.mark.asyncio
async def test_orchestrate_research_premium(premium_agent):
    result = await premium_agent.orchestrate_research("TestTarget", ["idor", "auth_bypass"])
    
    assert "execution_plan" in result  # Premium feature
    assert "session_id" in result
    assert result["target"] == "TestTarget"

def test_generate_burp_payloads(agent):
    payloads = agent._generate_burp_payloads("idor", "user_id")
    
    assert "intruder_payload" in payloads
    assert "repeater_template" in payloads
    assert "methodology" in payloads
    assert "user_id" in payloads["intruder_payload"]

def test_estimate_bounty_potential(agent):
    mock_analysis = {
        "vulnerabilities": [
            type('MockVuln', (), {
                'severity': 'HIGH',
                'title': 'Test Vulnerability',
                'confidence': 0.8
            })()
        ]
    }
    
    bounty_range = agent._estimate_bounty_potential(mock_analysis)
    
    assert "min" in bounty_range
    assert "max" in bounty_range
    assert "confidence" in bounty_range
    assert bounty_range["min"].startswith("$")
    assert bounty_range["max"].startswith("$")

def test_save_session(agent, tmp_path):
    # Add some data to session log
    agent.session_log.append({"test": "data"})
    
    filename = str(tmp_path / "test_session.json")
    result_filename = agent.save_session(filename)
    
    assert result_filename == filename
    assert os.path.exists(filename)

if __name__ == "__main__":
    pytest.main([__file__])
