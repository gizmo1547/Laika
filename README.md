# Laika

# Interpretable Multi-Agent Coordination Algorithms for Heterogeneous (Urban/Suburban/Rural) Autonomous Mobility Networks

**Authors**: Rivaldo Lumelino, Alexandr Voronovich  
**Course/Project**: CSC 36000: Modern Distributed Computing – Final Project  
**Date**: November 2025 
**GitHub Repo**: https://github.com/gizmo1547/Laika
**Google Colab**: [https://github.com/gizmo1547/Laika](https://colab.research.google.com/drive/1uNz9UnVD6ye_g6YHMB02sG19JYGzVOpL#scrollTo=8c81bc22)


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


🌐 Communication Models

The simulation compares five realistic network environments:

Network	Description
V2X	Near-real-time, very low packet loss
MQTT	Higher latency and moderate loss
Urban	Low delay, moderate reliability
Suburban	Medium delay and loss
Rural	High delay, high packet loss

Each message may be delayed, dropped, or discarded as stale.


📦 Task-Based Extension

To move beyond pure motion simulation, we added logistics tasks:

2 pickup locations

2 drop-off locations

Drones select the closest pickup

After delivery, they request a new task

This models real autonomous delivery scenarios.


🧩 Decision Algorithm (High-Level)

At every time step, each drone:

Processes received messages

Smooths neighbor positions (noise reduction)

Uses sensors if communication fails

Applies swarm rules:

Attraction (cohesion)

Repulsion (collision avoidance)

Steers toward task goal

Logs its reasoning

All decisions are local and asynchronous.


📊 Metrics Collected

The simulation evaluates:

Message delivery rate

Average communication delay

Collision count

Sensor fallback usage

Interpretability event count

Tasks completed

These metrics directly link network quality → behavior → performance.


🔍 Interpretability Engine (Key Contribution)

Every drone explains its behavior using human-readable logs, such as:

“No messages → slowed down”

“Using sensors to avoid collision”

“Steering toward pickup location”

“Large turn detected”

This addresses the black-box problem in autonomous systems.


🎥 Visualization

The project generates high-resolution MP4 videos showing:

Drone movement in real time

Pickup (red) and drop-off (green) locations

Drone state:

Blue = empty

Orange = carrying task

This provides visual validation of system behavior.


🧠 Distributed Systems Perspective

This project demonstrates key distributed systems concepts:

Asynchronous communication

No global clock

Fault tolerance via redundancy

Local autonomy under failure

Scalability to large swarms


🏁 Conclusion

This project presents a robust, interpretable, and realistic distributed drone system that adapts to unreliable communication while maintaining safety and task performance.

It bridges distributed systems theory, autonomous robotics, and real-world network constraints.
