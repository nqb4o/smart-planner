# main.py

from fastapi import FastAPI
from pydantic import BaseModel, Field
from starlette.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import datetime
from agent.agentic_workflow import GraphBuilder
import uvicorn
import uuid
from typing import Dict, List

app = FastAPI(
    title="Smart Travel Planner API",
    description="API for the Agentic AI Travel Planner",
    version="1.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conversations: Dict[str, any] = {}


class Message(BaseModel):
    """Represents a single message in the chat history."""
    role: str
    content: str


class QueryRequest(BaseModel):
    """Request body now accepts a list of messages."""
    # Thay vì 'query: str', chúng ta nhận toàn bộ lịch sử
    messages: List[Message] = Field(...)
    conversation_id: str = Field(None)


@app.get("/")
async def read_root():
    return {"message": "Chào mừng bạn đến với ứng dụng lên kế hoạch Smart Travel Planner"}


@app.post("/query")
async def query_travel_agent(request: QueryRequest):
    try:
        log_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n--- [main.py] {log_time} ---")
        print(f"[main.py] LOG: Received query: '{request.messages[-1].content}'")

        conversation_id = request.conversation_id
        if not conversation_id or conversation_id not in conversations:
            conversation_id = str(uuid.uuid4())
            print(f"[main.py] LOG: New conversation started. ID: {conversation_id}")
            graph_builder = GraphBuilder(model_provider="google")
            react_app = graph_builder()
            conversations[conversation_id] = react_app
        else:
            print(f"[main.py] LOG: Continuing conversation. ID: {conversation_id}")
            react_app = conversations[conversation_id]

        langchain_messages = []
        for msg in request.messages:
            role = "ai" if msg.role == "assistant" else "user"
            langchain_messages.append((role, msg.content))

        input_data = {"messages": langchain_messages}
        print(f"[main.py] LOG: Invoking agent graph with full conversation history...")

        final_output = ""
        for chunk in react_app.stream(input_data):
            for key, value in chunk.items():
                if key == "agent" and value.get("messages"):
                    final_output = value["messages"][-1].content

        print(f"[main.py] LOG: Final answer extracted: {final_output[:150]}...")
        print(f"--- [main.py] End of Request ---")

        return {"answer": final_output, "conversation_id": conversation_id}

    except Exception as e:
        print(f"[main.py] ERROR: An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
