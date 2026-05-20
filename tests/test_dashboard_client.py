from dashboard import api_client


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self) -> None:
        return None

    def json(self):
        return self.payload


def test_dashboard_fetch_helpers(monkeypatch) -> None:
    calls = []

    def fake_get(url, headers, timeout):
        calls.append((url, headers, timeout))
        if url.endswith("/security/summary"):
            return FakeResponse({"total_events": 1, "by_event_type": {}, "by_severity": {}})
        return FakeResponse([{"event_type": "LOGIN_FAILURE"}])

    monkeypatch.setattr(api_client.requests, "get", fake_get)

    summary = api_client.fetch_summary("token", "http://api.test")
    events = api_client.fetch_events("token", "http://api.test")

    assert summary["total_events"] == 1
    assert events[0]["event_type"] == "LOGIN_FAILURE"
    assert calls[0][1] == {"Authorization": "Bearer token"}
