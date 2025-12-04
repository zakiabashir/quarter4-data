---
id: 0001
title: Initialize Physical AI Textbook Constitution
stage: constitution
date: 2025-12-04
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 002-ai-native-textbook
user: user
command: /sp.constitution
labels: ["initialization", "constitution", "physical-ai-textbook"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:

---

## Prompt

sp.constitution:
You are creating a full technical textbook using Spec-Kit Plus.
Purpose: Teach students Physical AI, Humanoid Robotics, ROS 2, Gazebo, Unity, NVIDIA Isaac, VLA, and AI-native textbook systems.

Primary Objectives:
1. Produce a complete multi-chapter textbook following the given chapter outline.
2. Ensure all content is accurate, actionable, industry-standard, and deeply technical.
3. Make the book compatible with Docusaurus + Context7 MCP + RAG chatbot integration.
4. All chapters contain:
   – Concepts
   – Diagrams (ASCII or Mermaid)
   – Python/ROS2 code
   – Simulation steps
   – Isaac workflows
   – Real vs Sim discussions
   – Labs and quizzes
5. Add personalization and Urdu translation hooks.
6. Deliver perfect GitHub-ready output.

Global Rules:
– Use simple, clear, authoritative tone.
– All explanations must start from fundamentals → expert-level mastery.
– Every chapter ends with Practical Labs + Exercises.
– Follow all Spec-Kit patterns (constitution → s

## Response snapshot

Initialized the project constitution with core principles and governance for the 'Physical AI & Humanoid Robotics Textbook'.

## Outcome

- ✅ Impact: Constitution file created and updated.
- 🧪 Tests: None
- 📁 Files: .specify/memory/constitution.md
- 🔁 Next prompts: None
- 🧠 Reflection: Successfully created the initial constitution for the project, incorporating user-defined objectives and rules.

## Evaluation notes (flywheel)

- Failure modes observed: `create-phr.sh` script failed, requiring manual PHR creation.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Fix `create-phr.sh` or ensure template is always present.
