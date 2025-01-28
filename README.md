<div align="center">
  <img src="assets/logo.png" alt="kubepilot Logo" />
</div>

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Clone the Repository](#clone-the-repository)
  - [Install Dependencies](#install-dependencies)
  - [Setup Ollama LLM Backend](#setup-ollama-llm-backend)
- [Usage](#usage)
  - [Running the Agent](#running-the-agent)
- [Future Work](#future-work)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Overview

**kubepilot** is a Kubernetes Site Reliability Engineering (SRE) assistant designed to streamline the diagnosis and troubleshooting of Kubernetes issues. As Kubernetes is a general computing platform often used to run AI workflows, kubepilot leverages the power of a Language Model (LLM) with reasoning capabilities to operate infrastructure. Using a ReAct (Reasoning + Action) agent pattern, kubepilot interacts with Kubernetes tools to analyze k8s resource statuses, logs, events, and more, providing actionable insights and recommendations to maintain the health and performance of your Kubernetes clusters.

It is important to note that **kubepilot** is a proof-of-concept (PoC) project aimed at showcasing the feasibility of automating operations with minimal human intervention. The focus is on diagnosis workflows only, achieved by running read-only tools without any mutation. This project is not intended for production use but rather to demonstrate the potential of such an approach.

## Features

- **Automated Diagnosis:** Quickly identify and diagnose issues within Kubernetes pods using intelligent analysis.
- **ReAct Agent Pattern:** Utilizes a multi-step reasoning process to interact with Kubernetes tools and gather necessary information.
- **LLM Integration:** Integrates with Ollama-based Language Models (e.g., `deepseek-r1:8b`) for natural language understanding and response generation.
- **Configurable Logging:** Flexible logging setup allowing logs to be directed to the console, files, or both based on configuration.
- **Extensible Tooling:** Supports various Kubernetes tools including `kubectl_get`, `kubectl_describe`, `kubectl_logs`, `kubectl_events`, `kubectl_top_pods`, and `kubectl_top_nodes`.
- **Robust Error Handling:** Gracefully handles malformed responses and communication issues with the LLM backend.

## Architecture

kubepilot follows a modular architecture comprising the following components:

- **Agent:** A single agent implements the ReAct pattern, enabling multi-step reasoning and interaction with the LLM and Kubernetes tools. It coordinates diagnosis tasks efficiently by combining language model reasoning with Kubernetes-specific operations.
- **LLM Backend:** Communicates with an LLM provider (e.g., a local Ollama server) to generate responses based on prompts and tool outputs.
- **Tools:** Interfaces with Kubernetes commands (`kubectl`) to gather necessary data.
- **Prompts:** Defines system prompts guiding the LLM's behavior and response structure.
- **Logging:** Provides configurable logging to monitor and debug agent operations.

## Installation

### Prerequisites

Before installing kubepilot, ensure you have the following prerequisites:

- **Python 3.13+**
- **Kubernetes Cluster:** Access to a Kubernetes cluster with `kubectl` configured and appropriate permissions. For reproducibility, a k3s cluster setup is available in the `environments/` directory of this repository, which includes all necessary steps and configurations.
- **Ollama Server:** Running Ollama server with the required model (`deepseek-r1:8b`) installed.

### Clone the Repository

Clone the kubepilot repository to your local machine:

```bash
git clone https://github.com/jingairpi/kubepilot.git
cd kubepilot
```

### Install Dependencies

Install the required Python packages using `poetry`

```bash
poetry lock
poetry install
```

Note: It's recommended to use a virtual environment to manage dependencies.

### Setup Ollama LLM Backend

Ensure that the Ollama server is installed and running. By default, Ollama listens on [http://localhost:11434](http://localhost:11434). Verify that the required model (`deepseek-r1:8b`) is installed and active.

#### Verify Ollama Server

```bash
lsof -i -P -n | grep LISTEN | grep ollama
```

#### Expected Output

```bash
ollama    50772 <user_name>    3u  IPv4 0x450c1db0784f9fda      0t0    TCP 127.0.0.1:11434 (LISTEN)
```

## Usage

### Running the Agent

To diagnose a specific Kubernetes pod, use the `scripts/demo.py` script with the `--query` argument.

```bash
python scripts/demo.py --query "Diagnose the pod with name network-issue in the default namespace"
```

## Future Work

There are several identified key areas for enhancement to improve **kubepoilot**'s **usability**, **scalability**, **diagnostic accuracy**, and **integration capabilities**, advancing it it beyond PoC. The following initiatives are prioritized to ensure kubepilot remains a powerful and reliable Kubernetes SRE assistant:

### Domain Knowledge Base with Retrieval-Augmented Generation (RAG)

Integrate a comprehensive Kubernetes-specific knowledge base using RAG. This will enable kubepilot to dynamically access and utilize up-to-date information, enhancing diagnostic accuracy and providing more informed recommendations without the need for extensive model retraining.

### Multi-Agent Architecture

Transition to a multi-agent architecture by decomposing the monolithic agent into specialized agents focused on distinct Kubernetes domains (e.g., Networking, Storage, Compute). This modular approach will improve scalability, maintainability, and the depth of diagnostics, allowing kubepilot to handle complex scenarios more efficiently.

### Enhanced Tooling and Integrations

Expand kubepilot's capabilities by supporting a broader range of kubectl commands and integrating with third-party Kubernetes tools such as Helm, Prometheus, and Grafana. These enhancements will enable more comprehensive diagnostics and provide users with a wider array of management and monitoring options.

### User Interface Improvements

Develop a user-friendly web-based dashboard alongside enhancing the existing Command-Line Interface (CLI). These improvements will offer real-time monitoring, interactive diagnostics, and a more intuitive user experience, making kubepilot accessible to both technical and non-technical users.

## Contributing

Contributions are welcome! Whether you're fixing bugs, improving documentation, or adding new features, your input is valuable.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For questions, issues, or contributions, please contact [jingairpi@gmail.com](mailto:jingairpi@gmail.com).
