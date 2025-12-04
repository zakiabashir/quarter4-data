---
id: 0001
title: Initial Constitution for AI-Native Textbook
stage: constitution
date: 2025-12-04
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 001-ai-native-textbook
user: unknown
command: /sp.constitution
labels: [constitution, ai-native-textbook, spec-kit]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

sp.constitution """
You are an expert AI system with 20+ years of experience in book writing, robotics, and prompt engineering.
Your job is to generate a complete AI-Native textbook titled:

"Physical AI & Humanoid Robotics — An Agentic, Spec-Kit Native Textbook"

The book MUST follow the Spec-Kit pattern and MUST include the following chapters:

CHAPTER 1 — Introduction to Physical AI
Embodied intelligence
Digital vs Physical AI
Humanoid robotics landscape
Sensors overview (LIDAR, IMU, Cameras)

CHAPTER 2 — ROS 2: The Robotic Nervous System
ROS nodes, topics, services
rclpy integration with Python Agents
URDF basics
Building ROS packages

CHAPTER 3 — Digital Twin Simulation
Gazebo simulation
Unity high-fidelity simulation
Physics, gravity, collision
Sensor simulation

CHAPTER 4 — NVIDIA Isaac: The AI-Robot Brain
Isaac Sim
Isaac ROS
VSLAM
Perception and Navigation
Reinforcement learning

CHAPTER 5 — Vision-Language-Action (VLA)
Whisper voice-to-action
LLM-based cognitive planning
Natural language to ROS actions

CHAPTER 6 — Humanoid Robotics Development
Kinematics
Bipedal locomotion
Manipulation
Human-robot interaction

CHAPTER 7 — Building the AI-Native Textbook
Docusaurus setup
RAG chatbot integration
Context7 MCP server
OpenAI Agents SDK (ChatKit / FastAPI)
Qdrant + Neon Postgres

CHAPTER 8 — Personalization, Translation & Subagents
Add Urdu translation button
Add content personalization
Create Claude Code Subagents
Create reusable Agent Skills

CHAPTER 9 — Capstone Project
Autonomous Humanoid Robot
Voice command → plan → navigation → perception → manipulation
Real world or simulated deployment
Final evaluation

The textbook must include:
- Clear explanations
- Architecture diagrams (ASCII)
- Code samples (ROS2, rclpy, Gazebo, Isaac)
- Docusaurus-ready MDX format
- RAG chatbot integration instructions
- MCP Context7 server usage
- Clarification prompts
- Urdu translation prompts
- Personalization prompts
- Subagents & Skills definitions

The voice must be authoritative, clear, technical, and fully aligned with Spec-Kit culture.
"""

## Response snapshot

The project constitution for the AI-Native Textbook has been initialized, outlining core principles and governance for its development.

## Outcome

- ✅ Impact: The project's constitution was successfully created and written to `.specify/memory/constitution.md`, establishing the foundational principles for the "Physical AI & Humanoid Robotics — An Agentic, Spec-Kit Native Textbook".
- 🧪 Tests: none
- 📁 Files: One file (`.specify/memory/constitution.md`) was modified.
- 🔁 Next prompts: Review the updated constitution; Proceed with creating the feature specification.
- 🧠 Reflection: The initial constitution was created based on detailed user input, ensuring alignment with project goals and Spec-Kit methodologies.

## Evaluation notes (flywheel)

- Failure modes observed: The create-phr.sh script was not found, requiring manual PHR creation. The prompt for /sp.phr itself does not include the prompt text for the original command, requiring manual retrieval from the conversation history. Also, git user name is not available.
- Graders run and results (PASS/FAIL): null
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Ensure create-phr.sh script is available and executable. Enhance /sp.phr command to automatically capture the full preceding user prompt. Integrate git config user.name to auto-populate the USER field.
