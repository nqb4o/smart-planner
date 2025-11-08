# app.py

import streamlit as st
import requests
import uuid

BASE_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Ứng dụng Agentic AI Lập Kế Hoạch Du Lịch Thông Minh",
    page_icon="🌍",
    layout="wide",
)

st.title("🌍 Trợ lý Du lịch Thông minh")
st.markdown(
    "Chào mừng bạn! Tôi có thể giúp bạn lên kế hoạch cho chuyến đi mơ ước. Hãy bắt đầu bằng cách cho tôi biết điểm đến của bạn.")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = str(uuid.uuid4())

for msg in st.session_state.messages:
    role_icon = "🧑" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=role_icon):
        st.markdown(msg["content"])

if user_input := st.chat_input("Ví dụ: Lên kế hoạch đi Đà Lạt 3 ngày 2 đêm"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_input)

    try:
        print(f"\n--- [app.py] LOG: User input: '{user_input}' ---")
        with st.spinner("Trợ lý đang suy nghĩ..."):
            payload = {
                "messages": st.session_state.messages,
                "conversation_id": st.session_state.conversation_id
            }
            print(f"[app.py] LOG: Sending request to backend with full history...")
            response = requests.post(f"{BASE_URL}/query", json=payload)
            print(f"[app.py] LOG: Received response with status code: {response.status_code}")

        with st.chat_message("assistant", avatar="🤖"):
            if response.status_code == 200:
                response_data = response.json()
                print(f"[app.py] LOG: Raw JSON response from backend: {response_data}")

                raw_answer = response_data.get("answer", "Xin lỗi, đã có lỗi xảy ra.")

                parsed_text = ""
                if isinstance(raw_answer, list) and raw_answer:
                    first_item = raw_answer[0]
                    if isinstance(first_item, dict) and 'text' in first_item:
                        parsed_text = first_item['text']
                    else:
                        parsed_text = str(raw_answer)
                elif isinstance(raw_answer, str):
                    parsed_text = raw_answer
                else:
                    parsed_text = str(raw_answer)

                st.session_state.conversation_id = response_data.get("conversation_id")

                st.markdown(parsed_text)

                st.session_state.messages.append({"role": "assistant", "content": parsed_text})
            else:
                error_message = f"❌ Lỗi: {response.status_code} - {response.text}"
                st.error(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})

    except requests.exceptions.RequestException as e:
        error_message = f"⚠️ Lỗi kết nối đến máy chủ: {e}"
        st.error(error_message)
        st.session_state.messages.append({"role": "assistant", "content": error_message})
    except Exception as e:
        error_message = f"⚠️ Đã xảy ra lỗi không mong muốn: {e}"
        print(f"[app.py] ERROR: Frontend request failed: {e}")
        st.error(error_message)
        st.session_state.messages.append({"role": "assistant", "content": error_message})
