#Rivaldo Lumelino, Alexandr Voronovich
#CSC 36000 – Final Project
#Problem 1
#How can agents communicate and coordinate when network is poor (urban congestion or rural coverage gaps)?
#Without solution → collisions, inefficiency, unsafe behavior
import random
import math
from collections import deque
#Agent Class
class Agent:
    def __init__(self, agent_id, x, y):
        self.id = agent_id  # save agent id
        self.x = x  # x coordinate
        self.y = y  # y coordinate
        self.vx = 0  # x velocity
        self.vy = 0  # y velocity
        self.known_positions = {}  # dictionary to store the last known positions from messages
        self.sensor_range = 5.0
        self.received_current_step = []  # buffer for messages received during current tick (tick = one time step in the simulation)

        self.logs = []  # store human-readable reasoning messages
        self.prev_vx = 0  # previous x velocity
        self.prev_vy = 0  # previous y velocity

    def get_position(self):  # helper: return current position as tuple
        return (self.x, self.y)  # return x and y

    def update_velocity(self):  # choose a new velocity by random position
        # store previous velocity so we can detect turns later
        self.prev_vx = self.vx
        self.prev_vy = self.vy
        self.vx = random.uniform(-1, 1)  # set vx to random float between -1 to 1
        self.vy = random.uniform(-1, 1)  # set vy to random float between -1 to 1

    def move(self):  # update the position according to velocity
        self.x += self.vx  # increment x by vx
        self.y += self.vy  # increment y by vy

    def sense_agents(self, agents):  # This function lets an agent detect other agents near them even if communication fails
        sensed = []  # this is just an empty list, where we will store all nearby agents
        for agent in agents:  # iterate through all agents passed in
            if agent.id == self.id:  # skip sensing ourselves
                continue  # continue to next agent

            dist = math.dist(self.get_position(), agent.get_position())  # compute Euclidean distance (straight-line distance)
            if dist <= self.sensor_range:  # if within sensor range
                sensed.append((agent.id, agent.get_position()))  # append (id, pos)
        return sensed  # return list of sensed agents

    def create_message(self):  # prepare a message to be sent
        return {  # return a dictionary representing the message
            "from": self.id,  # sender id
            "pos": (self.x, self.y),  # current position
            "intent": (self.vx, self.vy)  # intended movement vector
        }

    def receive_message(self, msg):  # call when a message is delivered to the agent
        # append message to buffer. When messages arrive during the tick, we temporarily store them here
        self.received_current_step.append(msg)

    def process_received(self, current_time):
        # process messages buffered during this tick (current_time passed in for logging)
        if not self.received_current_step:
            return

        senders = []
        for msg in self.received_current_step:
            sender = msg["from"]
            self.known_positions[sender] = msg["pos"]
            senders.append(sender)

        # add interpretability log
        self.logs.append((current_time, f"Received messages from agents {sorted(senders)}"))

        # clear buffer after processing
        self.received_current_step = []

    def decide_action(self, current_time, agents):
        # decide action based on available information and add logs
        if not self.known_positions:
            sensed = self.sense_agents(agents)

            if not sensed:
                # slow down (no info)
                old = (self.vx, self.vy)
                self.vx *= 0.2
                self.vy *= 0.2
                self.logs.append(
                    (current_time,
                     f"Slowed down due to no messages and no sensed agents. "
                     f"Velocity {old} -> ({self.vx:.2f},{self.vy:.2f})")
                )
            else:
                # reacted to sensed agent
                sid, spos = sensed[0]
                self.logs.append(
                    (current_time,
                     f"No messages, but sensed agent {sid} at {spos}. Adjusting motion.")
                )
        else:
            known = sorted(self.known_positions.keys())
            self.logs.append(
                (current_time, f"Has comm info from agents {known}. Using it for navigation.")
            )

        # detect if large turn happened (compare current velocity with previous)
        dv = math.hypot(self.vx - self.prev_vx, self.vy - self.prev_vy)
        if dv > 0.7:
            self.logs.append(
                (current_time,
                 f"Large turn detected (Δv={dv:.2f}). "
                 f"({self.prev_vx:.2f},{self.prev_vy:.2f}) -> ({self.vx:.2f},{self.vy:.2f})")
            )

        # update prev_vx/prev_vy for next tick's comparison (important)
        self.prev_vx = self.vx
        self.prev_vy = self.vy
# Network Simulator(handles message delays)
class Network:
    def __init__(self, network_type):
        self.network_type = network_type  # save what network is using urban, suburban, rural
        # Set network behavior based on type
        if network_type == "v2x":
            self.drop_prob = 0.01  # 5% messages lost
            self.delay_range = (1, 1)  # messages arrive in 1-3 steps (small delay)
            
        elif network_type == "mqtt":
            self.drop_prob = 0.10  # 5% messages lost
            self.delay_range = (3, 8)  # messages arrive in 1-3 steps (small delay)
            
        elif network_type == "urban":
            self.drop_prob = 0.05  # 5% messages lost
            self.delay_range = (1, 3)  # messages arrive in 1-3 steps (small delay)

        elif network_type == "suburban":
            self.drop_prob = 0.10  # 10% messages are lost
            self.delay_range = (2, 6)  # messages arrive in 2-6 steps (medium delay)

        elif network_type == "rural":
            self.drop_prob = 0.30  # 30% message loss
            self.delay_range = (5, 15)  # messages arrive in 5-15 steps (long delay)

        else:
            raise ValueError("Invalid Network Settings")  # error if wrong network name is used

        # Message Queue
        self.queue = []  # list to store messages waiting to be delivered: tuples (deliver_time, agent, msg)
        self.time = 0  # keeps track of the current simulation time

        self.comm_success = 0  # how many messages were delivered successfully
        self.comm_attempts = 0  # how many messages were attempted to send
        self.collisions = 0  # how many collisions happened

    # This function simulates sending messages (now correctly inside the class)
    def broadcast(self, sender, msg, agents):
        for agent in agents:  # loop through all agents
            if agent.id == sender.id:  # skip sending a message to ourselves
                continue

            self.comm_attempts += 1  # count that a message was attempted

            if random.random() < self.drop_prob:
                continue  # message is lost, do not deliver it

            delay = random.randint(*self.delay_range)  # choose random delay within allowed range
            deliver_time = self.time + delay  # time when message should arrive
            # append tuple: (deliver_time, recipient_agent, msg)
            self.queue.append((deliver_time, agent, msg))

    # Deliver messages that are ready
    def deliver_messages(self):
        # find all messages whose deliver_time <= current time
        ready = [item for item in self.queue if item[0] <= self.time]

        for deliver_time, agent, msg in ready:
            agent.receive_message(msg)  # give the message to the agent
            self.comm_success += 1  # count successful delivery
            # remove this message from the queue
            self.queue.remove((deliver_time, agent, msg))
#ENVIRONMENT CLASS
class Environment:
    # Create Agents and network
    def __init__(self, num_agents, network_type, steps=100):
        self.interpretability_log = {}
        self.agents = [
            Agent(
                agent_id=i,  # give each agent ID
                x=random.uniform(0, 50),  # random starting x position
                y=random.uniform(0, 50)  # random y position
            )
            for i in range(num_agents)  # repeat for all agents
        ]

        self.network = Network(network_type)  # create a network with chosen type
        self.steps = steps  # how many time steps to simulate

    # Collision Checker must be a method of Environment
    def check_collisions(self):
        positions = {}  # store positions we have seen
        for agent in self.agents:
            pos = (round(agent.x, 1), round(agent.y, 1))  # round position to 1 decimal

            if pos in positions:  # if another agent already has this spot
                self.network.collisions += 1  # count a collision
            else:
                positions[pos] = agent.id  # store this position

    # main simulation loop as a method of Environment
    def run(self):
        for step in range(1, self.steps + 1):
            # Agents pick a new velocity
            for agent in self.agents:
                agent.update_velocity()

            # Agents send messages
            for agent in self.agents:
                msg = agent.create_message()
                self.network.broadcast(agent, msg, self.agents)

            # Network delivers messages
            self.network.deliver_messages()

            # Agents process messages they received (pass current network time)
            for agent in self.agents:
                agent.process_received(self.network.time)

            # Agents decide actions (interpretability happens here)
            for agent in self.agents:
                agent.decide_action(self.network.time, self.agents)

            # Agents move according to velocities
            for agent in self.agents:
                agent.move()

            # Check if agents collide
            self.check_collisions()

            # collect and clear agent logs into environment-level store
            self.interpretability_log[step] = []
            for agent in self.agents:
                for entry in agent.logs:
                    self.interpretability_log[step].append((agent.id, entry[0], entry[1]))
                agent.logs = []

            # Move time forward
            self.network.time += 1

            # log output every 10 steps
            if step % 10 == 0:
                print(
                    f"[step {step}] time={self.network.time} "
                    f"queue={len(self.network.queue)} "
                    f"comm_success={self.network.comm_success}/{self.network.comm_attempts} "
                    f"collisions={self.network.collisions}"
                )

        return {
            "network_type": self.network.network_type,
            "steps": self.steps,
            "agents": len(self.agents),
            "comm_success": self.network.comm_success,
            "comm_attempts": self.network.comm_attempts,
            "collisions": self.network.collisions,
            "logs": self.interpretability_log,
        }
#Demo
if __name__ == "__main__":
    random.seed(42)
    env = Environment(num_agents=8, network_type="suburban", steps=50)
    results = env.run()

    print("\n=========== SIMULATION SUMMARY ===========")
    print(f"Network type:    {results['network_type']}")
    print(f"Total steps:     {results['steps']}")
    print(f"Agents:          {results['agents']}")
    print(f"Messages sent:   {results['comm_attempts']}")
    print(f"Messages received:  {results['comm_success']}")
    print(f"Collisions:      {results['collisions']}")
    print("==========================================")

    print("\n==== SAMPLE INTERPRETABILITY LOGS (first 5 steps) ====")
    for t in range(1, 6):
        entries = results["logs"].get(t, [])
        print(f"\n--- Time step {t}, {len(entries)} events ---")
        for (agent_id, tick, text) in entries[:5]:
            print(f"[Agent {agent_id}] {text}")
