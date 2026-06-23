

# I Slashed 90% Tokens for My Multi-Agent | HEADROOM AI + MiniCPM5 1B

[![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-blue.svg)](https://ollama.com)
[![Headroom](https://img.shields.io/badge/Headroom--AI-Context_Compression-green.svg)](https://github.com/chopratejas/headroom)
[![Platform](https://img.shields.io/badge/Platform-Windows_PowerShell-orange.svg)]()

A minimal, high-efficiency Multi-Agent Swarm demonstration illustrating how to use `headroom-ai` to compress context passed between local Ollama models. By applying intelligent context compression, this swarm minimizes token counts, lowers RAM usage, and drastically improves inference speeds for downstream LLMs in agent pipelines.

---

## 🛠️ Tech Stack

*   **Runtime**: Python 3.10+
*   **Context Layer**: `headroom-ai` (using the `smart_crusher` strategy)
*   **Inference Engine**: Ollama (Running locally)
*   **Swarm Agents**:
    *   **Executor Agent**: `minicpm5:1b` (1.3B parameters, highly detailed outputs)
    *   **Reviewer Agent**: `granite4.1:3b` (3B parameters, robust security/code review)
*   **Communication**: Lightweight HTTP calls via `requests`

---

## 🚀 Setup Steps

Assumes a completely clean Windows system. Follow these steps sequentially:

### 1. Install & Launch Ollama
1. Download and run the installer from the [Official Ollama Website](https://ollama.com/download/windows).
2. Open Windows PowerShell and ensure the Ollama service is active.

### 2. Pull the Agent Models
Run the following PowerShell commands to download the required models locally:
```powershell
ollama pull minicpm5:1b
ollama pull granite4.1:3b
```

### 3. Clone and Setup Environment
Navigate to your project directory and install python requirements:
```powershell
# Create a virtual environment (optional but recommended)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install project dependencies
pip install -r requirements.txt
```

---

## 🏃 Run Steps

Execute the agent swarm pipeline from your active PowerShell console:

```powershell
python agent_swarm.py
```

---

## 🧪 Test Steps (Verification)

To verify the setup worked correctly:
1. **Console Verification**: Check your PowerShell console output. You should see distinct blocks for **Phase 1 (Executor Response)**, **Phase 2 (Compressed Content)**, **Phase 3 (Reviewer Response)**, and the calculated **Token Savings**.
2. **Artifact Verification**: Confirm that `output.md` has been successfully created in the root directory.
3. **Savings Calculation**: Ensure that the printed token savings ratio corresponds to the word counts of the raw and compressed outputs.

---

## 📂 File Structure & Code Explanation

*   `requirements.txt`: Defines direct dependencies required by the swarm (`headroom-ai[all]` and `requests`).
*   `agent_swarm.py`: Contains the core swarm workflow:
    *   Queries `minicpm5:1b` for the transaction handler architecture.
    *   Initializes headroom's native `SmartCrusher` to compress the executor's output.
    *   Passes only the compressed output to `granite4.1:3b` for a code review.
    *   Outputs comparative token savings and saves the entire log to `output.md`.
---

## 💡 Use Cases

1.  **Local Agent Pipelines**: Reducing context overhead for chain-of-thought agent workflows running on low-resource hardware.
2.  **Long-Document Summarization**: Collapsing long RAG documents before passing them to a reviewer model.
3.  **Low-Latency Code Review**: Compressing large source files or multi-file diffs before triggering review agents.
4.  **Edge Compute Orchestration**: Saving CPU/GPU compute cycles on local machines by dropping unnecessary context tokens.
5.  **Multi-turn Chat History**: Compressing historical dialogue context to prevent context window saturation in long-running agent chats.

---

## 🔮 Future Feature Ideas

1.  **Dynamic Strategy Selector**: Auto-detect content types (JSON, code, logs) to dynamically route them to the best compressor.
2.  **Cross-Agent Memory (CCR)**: Store original uncompressed logs in a local cache allowing the reviewer to fetch on-demand details.
3.  **Parallel Agent Execution**: Execute multiple reviewer sub-agents simultaneously on compressed sub-tasks.
4.  **Token Cost Estimator**: Track cumulative token savings over multiple runs and project API cost reductions.
5.  **Interactive Swarm Dashboard**: A local web interface visualizer showing real-time token compression and pipeline latency.

---

## 🏷️ Keywords & SEO
`headroom-ai` | `Multi-Agent Swarm` | `Context Compression` | `Local LLMs` | `Ollama` | `MiniCPM5 1B` | `Granite 4.1 3b` | `Token Optimization` | `LLM Prompt Savings` | `Smart Crusher` | `Agent Orchestration` | `AI Cost Reduction`

