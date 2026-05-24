import streamlit as st
from dotenv import load_dotenv
import os
import requests
import subprocess
import platform
import time
from langchain_mistralai import ChatMistralAI
from langchain.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from tavily import TavilyClient
load_dotenv()
# =====================================================================
# 1. Page Configuration & Styling
# =====================================================================
st.set_page_config(
    page_title="Tirtha | City Assistant",
    page_icon="🏙️",
    layout="centered"
)

st.markdown("""
<style>
    div.stButton > button:first-child {
        border-radius: 8px;
        font-weight: 500;
    }
    .approval-container {
        background-color: rgba(255, 193, 7, 0.15);
        border-left: 5px solid #ffc107;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# =====================================================================
# 2. Tools Definition
# =====================================================================
load_dotenv()

@tool
def get_weather(city: str) -> str:
    """Get current Weather of a City"""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if str(data.get('cod')) != '200':
            return f"Error: {data.get('message', 'Could not Fetch Weather')}"
        temp = data['main']['temp']
        desc = data['weather'][0]["description"]
        humi = data['main']["humidity"]
        return f'weather in {city}: {desc}, {temp} C ,{humi}%'
    except Exception as e:
        return f"Error fetching weather: {str(e)}"

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def get_news(city: str) -> str:
    """Get latest news about the city"""
    try:
        response = tavily_client.search(query=f"latest news in {city}", search_depth='basic', max_results=3)
        result = response.get("results", [])
        if not result:
            return f"No news found for {city}"
        news_list = [f"{r.get('title', 'no title')}\n {r.get('url', '')}\n {r.get('content', '')[:100]}...." for r in result]
        return f"Latest news in {city}:\n\n" + "\n\n".join(news_list)  
    except Exception as e:
        return f"Error fetching news: {str(e)}"

@tool
def explore_folder(folder_path: str) -> str:
    """Opens a local system directory path and lists out all sub-folders and files inside it."""
    normalized_path = os.path.abspath(folder_path)
    if not os.path.exists(normalized_path):
        return f"Error: The target path '{folder_path}' does not exist on this computer."
    if not os.path.isdir(normalized_path):
        return f"Error: The target path '{folder_path}' is a file, not a directory folder."
    try:
        items = os.listdir(normalized_path)
        if not items:
            return f"The folder '{normalized_path}' is currently empty."
        return f"Successfully accessed folder: '{normalized_path}'\n\nContents:\n" + "\n".join([f" - {item}" for item in items])
    except PermissionError:
        return f"Error: Access denied. Missing permissions to read inside '{normalized_path}'."
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def shutdown_pc() -> str:
    """Forcefully closes all open browser windows/tabs and schedules a complete system shutdown after a 60-second delay."""
    os_type = platform.system().lower()
    try:
        if "windows" in os_type:
            browsers = ["chrome.exe", "msedge.exe", "firefox.exe", "brave.exe"]
            for browser in browsers:
                subprocess.run(["taskkill", "/F", "/IM", browser], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif "linux" in os_type or "darwin" in os_type:
            browsers = ["chrome", "firefox", "msedge", "brave"]
            for browser in browsers:
                subprocess.run(["pkill", "-f", browser], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(1)
    except Exception:
        pass

    try:
        if "windows" in os_type:
            subprocess.run(["shutdown", "/s", "/t", "60", "/f"], check=True)
            return "All major web browser tabs have been closed! The PC is scheduled to completely power down in 60 seconds."
        elif "linux" in os_type or "darwin" in os_type: 
            subprocess.run(["sudo", "shutdown", "-h", "+1"], check=True)
            return "All browser tasks terminated. System shutdown scheduled to trigger in 1 minute."
        else:
            return f"Error: Unsupported OS type architecture ('{os_type}')."
    except Exception as e:
        return f"Error: Failed to issue OS shutdown command: {str(e)}"

tools_map = {
    "get_weather": get_weather,
    "get_news": get_news,
    "explore_folder": explore_folder,
    "shutdown_pc": shutdown_pc
}

# =====================================================================
# 3. LLM Setup & Session Management
# =====================================================================
SYSTEM_PROMPT = "You are a helpful city assistant. If anyone asks you what your name is, you say your name is Tirtha."

llm = ChatMistralAI(model="mistral-large-latest", temperature=0.7).bind_tools(list(tools_map.values()))

# We store simple primitive types to avoid layout contamination errors
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "pending_action" not in st.session_state:
    st.session_state.pending_action = None

# Helper to build standard clean payload contexts for Mistral
def build_api_context():
    formatted = [HumanMessage(content=SYSTEM_PROMPT)]
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            formatted.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            if msg.get("tool_calls"):
                formatted.append(AIMessage(content=msg["content"], tool_calls=msg["tool_calls"]))
            else:
                formatted.append(AIMessage(content=msg["content"]))
        elif msg["role"] == "tool":
            formatted.append(ToolMessage(content=msg["content"], tool_call_id=msg["tool_call_id"], name=msg["name"]))
    return formatted

# =====================================================================
# 4. UI Rendering Layout
# =====================================================================
st.title("🏙️ Tirtha | City Assistant")
st.caption("Powered by LangChain, MistralAI & Tavily")
st.divider()

# Render chat items out beautifully
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
    elif msg["role"] == "assistant" and msg["content"]:
        with st.chat_message("assistant"):
            st.markdown(msg["content"])

# Process Interceptions cleanly
if st.session_state.pending_action:
    action_info = st.session_state.pending_action
    
    st.markdown(
        f"""
        <div class="approval-container">
            <strong>⚠️ Security Intervention Required</strong><br>
            The execution agent is requesting permission to run local tool: <code>{action_info['name']}</code> with parameters: <code>{action_info['args']}</code>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Approve Action", use_container_width=True, type="primary"):
            with st.spinner(f"Executing {action_info['name']}..."):
                target_tool = tools_map[action_info['name']]
                tool_result_str = target_tool.invoke(action_info['args'])
                
                # Directly append tool answer following tool request sequence
                st.session_state.chat_history.append({
                    "role": "tool",
                    "content": str(tool_result_str),
                    "tool_call_id": action_info['id'],
                    "name": action_info['name']
                })
                st.session_state.pending_action = None
                
                # Generate final summary reply
                final_ai_response = llm.invoke(build_api_context())
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": final_ai_response.content
                })
            st.rerun()
            
    with col2:
        if st.button("❌ Deny Action", use_container_width=True):
            st.session_state.chat_history.append({
                "role": "tool",
                "content": "Error: Operation denied by user intervention.",
                "tool_call_id": action_info['id'],
                "name": action_info['name']
            })
            st.session_state.pending_action = None
            
            final_ai_response = llm.invoke(build_api_context())
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": final_ai_response.content
            })
            st.rerun()

# Receive routine user text inputs
elif user_input := st.chat_input("Ask about weather, news, files..."):
    with st.chat_message("user"):
        st.markdown(user_input)
        
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    with st.chat_message("assistant"):
        with st.spinner("Tirtha is thinking..."):
            response = llm.invoke(build_api_context())
            
            if response.tool_calls:
                # Save the tool call details directly alongside the AIMessage request 
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response.content,
                    "tool_calls": response.tool_calls
                })
                call = response.tool_calls[0]
                st.session_state.pending_action = {
                    "name": call["name"],
                    "args": call["args"],
                    "id": call["id"]
                }
            else:
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response.content
                })
                st.markdown(response.content)
                
    st.rerun()