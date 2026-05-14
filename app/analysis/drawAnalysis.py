import logging
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from app.mcp.board_client import board_session

logger = logging.getLogger("netai")

DRAW_SYSTEM = """Eres un asistente de dibujo para una pizarra colaborativa Excalidraw.
El sessionId del tablero es: {session_id}

Tienes acceso a herramientas para dibujar en la pizarra:
- draw_shape: dibuja rectángulos, elipses o diamantes
- draw_text: agrega texto
- draw_arrow: dibuja flechas entre puntos
- add_elements: agrega elementos Excalidraw crudos
- get_board_state: obtiene el estado actual del tablero
- clear_board: limpia el tablero

IMPORTANTE: Siempre usa sessionId="{session_id}" en TODAS las llamadas a herramientas.

Cuando el usuario pide dibujar algo:
1. Planifica la distribución en el canvas (empieza en x=100, y=100, usa espaciado de ~150px)
2. Usa las herramientas para construir el diagrama paso a paso
3. Confirma qué dibujaste con una descripción breve

Responde en español. No expliques el proceso, solo confirma el resultado final."""


async def drawAnalysis(prompt: str, session_id: str) -> str:
    async with board_session() as tools:
        llm = ChatGroq(
            model="llama-3.3-70b-versatile", temperature=0.0, max_retries=2, timeout=60
        )
        system_msg = DRAW_SYSTEM.format(session_id=session_id)
        agent = create_agent(llm, tools, system_prompt=system_msg)

        try:
            result = await agent.ainvoke({"messages": [("human", prompt)]})
            messages = result.get("messages", [])
            last = messages[-1] if messages else None
            output = getattr(last, "content", None) if last else None
            return output or "Diagrama creado en la pizarra."
        except Exception as e:
            logger.error("drawAnalysis error: %s", e)
            raise
