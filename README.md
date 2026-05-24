```python
import os

readme_content = """# 🏙️ Tirtha | City Assistant & System Automation Agent

A polished, secure, and production-ready **Streamlit** AI assistant powered by **LangChain** and **Mistral AI (`mistral-large-latest`)**. This agent utilizes advanced tool binding, custom session state orchestration, and an interactive **Human-in-the-Loop (HITL)** approval workflow to securely handle sensitive local operating system commands alongside real-time web lookups.

---

## 🚀 Key Architectural Breakthroughs

Developing agentic applications within an event-driven web framework like Streamlit presents unique state management challenges. This codebase explicitly solves a common production bottleneck: **The Mistral API Order Validation Mismatch (`HTTP 400`)**.

### The Challenge
The Mistral AI API enforces a strict, immutable sequence arrangement constraint on its conversation history:
$$\\text{HumanMessage} \\longrightarrow \\text{AIMessage (with tool\\_calls)} \\longrightarrow \\text{ToolMessage}$$
If a user submits a fresh input query, or if the web framework force-refreshes while an explicit `tool_call` is outstanding without an immediate, matching `ToolMessage` reply, the state becomes contaminated, throwing an invalid request sequence error.

### The Solution: Primitive-Safe Interception Layer
This architecture completely bypasses framework lifecycle limitations by applying an **isolated primitive state layer**:
1. **Primitive Storage:** Instead of keeping volatile LangChain/LangGraph memory objects in session state across hot-reloads, the conversation is stored strictly as primitive Python dictionaries (`{"role": "user", "content": "..."}`).
2. **Just-in-Time Context Construction:** The application maps these primitives into strict LangChain object instances (`HumanMessage`, `AIMessage`, `ToolMessage`) *only* at the precise microsecond of model execution via `build_api_context()`.
3. **Persistent UI Interception Lock:** When Mistral requests a tool call, the processing engine freezes the user's `st.chat_input` field, blocks routine loop execution, and caches the metadata inside a secure state key (`st.session_state.pending_action`). The interface yields control to a customized HTML/CSS warning container, forcing the operator to explicitly choose to **Approve** or **Deny** the local execution before any further text queries can be evaluated.

---

## 🛠️ Complete Feature & Functional Toolset

The agent is equipped with a mixed pipeline of web-based diagnostic APIs and sensitive system-level functions:

* **⛅ Get Weather (`get_weather`):** Communicates with the external OpenWeather API to fetch current conditions, wind/metric temperatures, and humidity percentages for any requested geographic location.
* **🔍 Get News (`get_news`):** Utilizes the high-performance `TavilyClient` engine to parse deep-web crawls, compiling real-time news summaries and raw source URLs for a specified city.
* **📁 Explore Local Directories (`explore_folder`):** Safely navigates local physical disks, validating directory existence, checking filesystem permissions, and outputting complete directory structural arrays via optimized `os.listdir()` mapping layouts.
* **🖥️ System Shutdown (`shutdown_pc`):** Forces active cross-platform browser instances (`Chrome`, `Edge`, `Firefox`, `Brave`) to terminate using system-level task management utilities (`taskkill` on Windows / `pkill` on macOS & Linux), then registers an asynchronous system-level hardware shutdown instruction scheduled to execute following a safe 60-second delay buffer.

---

## 🎨 Visual System Architecture & Dataflow

The diagram below maps how the system handles user interactions, manages state locks, and formats payloads to satisfy Mistral's order protocols:


```

```text



```


<img width="1408" height="768" alt="Gemini_Generated_Image_jcef9bjcef9bjcef" src="https://github.com/user-attachments/assets/69f19dd4-54b0-4d57-bf0d-ee03515ad2b5" />

                                          

```

---

## ⚙️ Installation & Local Setup Guide

### 1. Clone the Project Repository
```bash
git clone [https://github.com/your-username/tirtha-city-assistant.git](https://github.com/your-username/tirtha-city-assistant.git)
cd tirtha-city-assistant

```

### 2. Configure Your Virtual Environment

```bash
# Initialize Python environment
python -m venv .venv

# Activate environment (Windows)
.venv\\Scripts\\activate

# Activate environment (macOS/Linux)
source .venv/bin/activate

```

### 3. Install All Project Dependencies

```bash
pip install streamlit langchain langchain-mistralai tavily-python requests python-dotenv

```

### 4. Inject Your Environment Variables

Create a standard secure `.env` file directly inside the root directory layout of the repository:

```env
MISTRAL_API_KEY="your-mistral-ai-api-key"
TAVILY_API_KEY="your-tavily-search-client-api-key"
OPENWEATHER_API_KEY="your-openweather-developer-api-key"

```

### 5. Launch the Web Server Platform

```bash
streamlit run app.py

```

---

## 🛡️ Operational Safeguards

* **Explicit Human Sanity Check:** No local operating system execution path can trigger implicitly. Even if the LLM enters an autonomous chain, the visual window blocks input collection until an explicit hardware operator action is registered.
* **Failure Isolation Context:** If a user chooses to deny an option, the system gracefully feeds an explicit `ToolMessage(content="Error: Operation denied by user intervention")` trace signature back to the model. This allows the AI agent to dynamically catch the refusal, adjust its conversational plan, and apologize without entering an unhandled script execution fault loop.
"""


```

### ✨ Document Features & Highlights
* **Deep Architectural Breakdown:** Explicitly details the **"Mistral API Order Validation Mismatch (`HTTP 400`)"** problem and explains the exact engineering fix implemented in the code (using a primitive-safe session layer to isolate state changes between web engine refreshes).
* **Granular Component Mapping:** Outlines every single functional tool bound to the system (`get_weather`, `get_news`, `explore_folder`, and `shutdown_pc`) alongside its cross-platform fallback mechanisms.
* **Integrated Mathematical and Logical Flow:** Demonstrates how Mistral's required sequencing structure ($\text{HumanMessage} \rightarrow \text{AIMessage} \rightarrow \text{ToolMessage}$) is met using the `build_api_context()` method.
* **Complete High-Resolution Text Diagram:** Features an exact structural flowchart embedded cleanly via Markdown, documenting how the variables `chat_history` and `pending_action` manipulate state loops across `st.rerun()` calls.
* **Quick-Start Deployment Instructions:** Contains comprehensive local setup details, dependency listings, `.env` parameter configurations, and hardware activation instructions.

```
