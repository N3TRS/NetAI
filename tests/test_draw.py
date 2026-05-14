import asyncio
from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

VALID_DRAW_PAYLOAD = {"prompt": "dibuja un rectángulo", "sessionId": "session-abc"}


# ── /draw endpoint ────────────────────────────────────────────────────────────

def test_draw_success():
    with patch("app.controllers.draw_controller.drawAnalysis", new=AsyncMock(return_value="Rectángulo dibujado.")):
        response = client.post("/draw", json=VALID_DRAW_PAYLOAD)
    assert response.status_code == 200
    assert response.json() == {"status": "success", "response": "Rectángulo dibujado."}


def test_draw_empty_prompt_returns_422():
    response = client.post("/draw", json={"prompt": "", "sessionId": "session-abc"})
    assert response.status_code == 422


def test_draw_whitespace_prompt_returns_422():
    response = client.post("/draw", json={"prompt": "   ", "sessionId": "session-abc"})
    assert response.status_code == 422


def test_draw_empty_session_id_returns_422():
    response = client.post("/draw", json={"prompt": "dibuja", "sessionId": ""})
    assert response.status_code == 422


def test_draw_whitespace_session_id_returns_422():
    response = client.post("/draw", json={"prompt": "dibuja", "sessionId": "  "})
    assert response.status_code == 422


def test_draw_missing_fields_returns_422():
    response = client.post("/draw", json={"prompt": "dibuja"})
    assert response.status_code == 422


def test_draw_analysis_error_returns_500():
    with patch(
        "app.controllers.draw_controller.drawAnalysis",
        new=AsyncMock(side_effect=RuntimeError("agent failed")),
    ):
        response = client.post("/draw", json=VALID_DRAW_PAYLOAD)
    assert response.status_code == 500


# ── drawAnalysis unit ─────────────────────────────────────────────────────────

def _mock_board_session(tools):
    @asynccontextmanager
    async def _ctx():
        yield tools

    return _ctx


def test_draw_analysis_returns_agent_output():
    mock_tools = [MagicMock()]
    mock_agent = AsyncMock()
    mock_agent.ainvoke.return_value = {
        "messages": [MagicMock(content="Diagrama creado exitosamente.")]
    }

    with (
        patch("app.analysis.drawAnalysis.board_session", _mock_board_session(mock_tools)),
        patch("app.analysis.drawAnalysis.create_agent", return_value=mock_agent),
    ):
        from app.analysis.drawAnalysis import drawAnalysis
        result = asyncio.run(drawAnalysis("dibuja un cuadro", "session-xyz"))

    assert result == "Diagrama creado exitosamente."


def test_draw_analysis_returns_fallback_when_no_messages():
    mock_tools = [MagicMock()]
    mock_agent = AsyncMock()
    mock_agent.ainvoke.return_value = {"messages": []}

    with (
        patch("app.analysis.drawAnalysis.board_session", _mock_board_session(mock_tools)),
        patch("app.analysis.drawAnalysis.create_agent", return_value=mock_agent),
    ):
        from app.analysis.drawAnalysis import drawAnalysis
        result = asyncio.run(drawAnalysis("dibuja algo", "session-xyz"))

    assert result == "Diagrama creado en la pizarra."


def test_draw_analysis_propagates_exception():
    mock_tools = [MagicMock()]
    mock_agent = AsyncMock()
    mock_agent.ainvoke.side_effect = RuntimeError("LLM failed")

    with (
        patch("app.analysis.drawAnalysis.board_session", _mock_board_session(mock_tools)),
        patch("app.analysis.drawAnalysis.create_agent", return_value=mock_agent),
    ):
        from app.analysis.drawAnalysis import drawAnalysis
        with pytest.raises(RuntimeError, match="LLM failed"):
            asyncio.run(drawAnalysis("dibuja algo", "session-xyz"))


# ── board_client unit ─────────────────────────────────────────────────────────

def test_board_session_yields_tools():
    mock_tools = [MagicMock(name="draw_shape")]

    @asynccontextmanager
    async def mock_http(*args, **kwargs):
        yield (AsyncMock(), AsyncMock(), lambda: None)

    mock_session = AsyncMock()
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=False)
    mock_session.initialize = AsyncMock()

    with (
        patch("app.mcp.board_client.streamablehttp_client", mock_http),
        patch("app.mcp.board_client.ClientSession", return_value=mock_session),
        patch("app.mcp.board_client.load_mcp_tools", new=AsyncMock(return_value=mock_tools)),
    ):
        from app.mcp.board_client import board_session

        async def run():
            async with board_session() as tools:
                return tools

        result = asyncio.run(run())

    assert result == mock_tools
