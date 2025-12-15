# Laika

# Interpretable Multi-Agent Coordination Algorithms for Heterogeneous (Urban/Suburban/Rural) Autonomous Mobility Networks

**Authors**: Rivaldo Lumelino, Alexandr Voronovich  
**Course/Project**: CSC 36000 – Final Project  
**Date**: November 2025 
**GitHub Repo**: https://github.com/gizmo1547/Laika


### The 3 Core Problems We Solve

| # | Problem | Why It Matters in Real World |
| --- | ------- | --------------------------- |
| 1 | How can agents communicate and coordinate when network is poor (urban congestion or rural coverage gaps)? | Without solution → collisions, inefficiency, unsafe behavior | 
| 2 | How can agents adapt their strategy to completely different environments (city vs. rural) while staying safe and efficient? | One-size-fits-all policies fail dramatically in mixed networks |
| 3 | How can we design interpretable reinforcement learn ingmodels that explain their decisions inhuman understandable ways? | People should understand the agens |

CSC 36000: Modern Distributed Computing



Resilient Multi-Drone Coordination Under Network Constraints

This project simulates a distributed multi-drone system operating under realistic communication conditions.
We study how different network environments affect coordination, safety, interpretability, and task completion when drones act without centralized control.

The system is built as a fully decentralized simulation, inspired by real-world drone swarms, V2X systems, and IoT communication protocols.

📌 Project Motivation

Autonomous drones operate in environments where:

Communication is unreliable or delayed

Network quality varies by location (urban vs rural)

Decisions must remain safe without global knowledge

Human operators need explainable behavior

Key Question:

How do communication constraints influence swarm coordination, and how can local autonomy compensate for network failures?

🧠 System Overview

Each drone (agent):

Operates independently (no central controller)

Communicates asynchronously with neighbors

Falls back to local sensors when messages fail

Performs real tasks (pickup → delivery)

Logs its decisions for interpretability

The environment simulates realistic network delays, packet loss, and message staleness.

🤖 Agent Capabilities

Each drone has:

Position and velocity in a 2D space

Short-term memory for smoothing neighbor positions

Local sensing range (5 meters)

Task state machine:

IDLE

GO_TO_PICKUP

GO_TO_DROPOFF

Human-readable decision logs

Drones coordinate using only local information.
