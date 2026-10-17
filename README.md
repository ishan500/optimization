# Opti AI Agent 🚀

**Opti AI Agent** is a lightweight, terminal-native operations research studio powered by local artificial intelligence. Designed to bridge the gap between traditional mathematical modeling and modern agentic workflows, this tool solves complex industrial optimization problems locally, securely, and 100% free of cost—requiring zero cloud APIs, web dashboards, or paid subscriptions.

### ✨ Core Features
- **Transportation Problem Suite:** Simultaneously runs and benchmarks **Northwest Corner**, **Least Cost Method**, and **Vogel’s Approximation Method (VAM)**, instantly exposing cost efficiencies and performance gaps.
- **Assignment Optimizer:** Solves resource allocation problems using the high-performance **Hungarian Algorithm** via SciPy.
- **Job Sequencing & Scheduling:** Implements **Johnson’s Rule** to process $n$ jobs across 2 machines, minimizing total makespan and production idle time.
- **Local AI Consultant:** Connects natively with **Ollama (`qwen2.5:3b`)** to stream real-time, professional analytical briefings explaining algorithm variances directly inside your terminal.

### 🛠️ Tech Stack & Architecture
- **Language:** Python 
- **Math Engines:** NumPy, SciPy
- **AI Agent Core:** Local LLM via Ollama (`qwen2.5:3b`)
- **Environment:** VS Code Terminal-optimized CLI (Lightning-fast execution on consumer hardware)

### 🚀 Quick Start
1. Clone the repository and navigate to the `optimization` folder.
2. Install dependencies: `pip install numpy scipy ollama`
3. Ensure Ollama is running (`ollama serve`).
4. Launch your agent: `python main.py`

Built for engineers, students, and operations researchers who want a fast, elegant, and entirely offline optimization assistant.
