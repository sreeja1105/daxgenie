from fastapi.testclient import TestClient

import api


def test_generate_endpoint(monkeypatch):
    # Mock the LLM call to avoid external network calls during tests
    monkeypatch.setattr(api, "call_gemini", lambda prompt: "MOCK_GENERATE_RESPONSE")
    # Disable auth for tests (SERVICE_API_KEY not set)
    monkeypatch.setenv("SERVICE_API_KEY", "")
    client = TestClient(api.app)
    r = client.post("/generate", json={"text": "Calculate YoY growth for Sales"})
    assert r.status_code == 200
    assert r.json()["result"] == "MOCK_GENERATE_RESPONSE"


def test_explain_endpoint(monkeypatch):
    monkeypatch.setattr(api, "call_gemini", lambda prompt: "MOCK_EXPLAIN_RESPONSE")
    monkeypatch.setenv("SERVICE_API_KEY", "")
    client = TestClient(api.app)
    r = client.post("/explain", json={"text": "CALCULATE(SUM(Sales[Amount]), ... )"})
    assert r.status_code == 200
    assert r.json()["result"] == "MOCK_EXPLAIN_RESPONSE"


def test_rate_limit(monkeypatch):
    """Test that rate limiting kicks in after limit is exceeded."""
    monkeypatch.setattr(api, "call_gemini", lambda prompt: "MOCK_RESPONSE")
    monkeypatch.setenv("SERVICE_API_KEY", "")
    monkeypatch.setenv("RATE_LIMIT_PER_MIN", "2")  # Set low limit for test
    client = TestClient(api.app)
    # Clear rate store to start fresh
    api._rate_store.clear()
    # First request should succeed
    r1 = client.post("/generate", json={"text": "test1"})
    assert r1.status_code == 200
    # Second request should succeed
    r2 = client.post("/generate", json={"text": "test2"})
    assert r2.status_code == 200
    # Third request should be rate limited
    r3 = client.post("/generate", json={"text": "test3"})
    assert r3.status_code == 429
