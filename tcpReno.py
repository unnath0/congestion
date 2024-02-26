import matplotlib.pyplot as plt
import numpy as np

class TCP_Reno:
    np.random.seed(100)
    def __init__(self, cwnd_initial=1, max_cwnd=15, ssthresh=65535, loss_rate=0.1, rtt=1):
        self.cwnd = cwnd_initial  # Initial congestion window size
        self.max_cwnd = max_cwnd  # Maximum congestion window size
        self.ssthresh = ssthresh  # Slow start threshold
        self.time = [0]  # Time intervals
        self.cwnd_values = [self.cwnd]  # Congestion window size over time
        self.loss_rate = loss_rate  # Packet loss rate
        self.rtt = rtt  # Round-trip time
        self.dupacks = 0  # Number of duplicate acknowledgments received

    def simulate(self, num_iterations=20):
        for i in range(num_iterations):
            # Simulate packet loss
            if np.random.rand() < self.loss_rate:
                self.ssthresh = self.cwnd / 2  # Adjust slow start threshold
                self.cwnd = self.ssthresh + 3  # Set congestion window size after loss
                self.dupacks = 3  # Simulate receiving three duplicate ACKs
            else:
                # Slow start phase
                if self.dupacks <= 0:
                    self.cwnd += 1
                    if self.cwnd >= self.ssthresh:
                        self.dupacks = -1  # Start congestion avoidance
                # Congestion avoidance phase
                else:
                    self.dupacks -= 1
                    self.cwnd += 1 / self.cwnd  # Additive increase
            # Ensure congestion window does not exceed maximum size
            self.cwnd = min(self.cwnd, self.max_cwnd)
            # Record time and congestion window size
            self.time.append(self.time[-1] + self.rtt)
            self.cwnd_values.append(self.cwnd)

    def plot_congestion_window(self):
        plt.plot(self.time, self.cwnd_values, marker='o')
        plt.title('TCP Reno Congestion Window Size Over Time')
        plt.xlabel('Time (s)')
        plt.ylabel('Congestion Window Size')
        plt.grid(True)
        plt.show()

    def plot_throughput(self):
        # Exclude the first element of time to avoid division by zero
        throughput = [self.cwnd_values[i] / self.time[i] for i in range(1, len(self.time))]
        time = self.time[1:]  # Exclude the first element of time
        plt.plot(time, throughput, marker='o')
        plt.title('TCP Reno Throughput Over Time')
        plt.xlabel('Time (s)')
        plt.ylabel('Throughput (packets/s)')
        plt.grid(True)
        plt.show()


    def plot_packet_loss(self):
        packet_loss = [1 if np.random.rand() < self.loss_rate else 0 for _ in range(len(self.time))]
        plt.plot(self.time, packet_loss, marker='o')
        plt.title('TCP Reno Packet Loss Over Time')
        plt.xlabel('Time (s)')
        plt.ylabel('Packet Loss (1 = loss, 0 = no loss)')
        plt.grid(True)
        plt.show()

    def plot_rtt(self):
        rtt_values = [self.rtt] * len(self.time)
        plt.plot(self.time, rtt_values, marker='o')
        plt.title('TCP Reno Round-Trip Time (RTT) Over Time')
        plt.xlabel('Time (s)')
        plt.ylabel('RTT (s)')
        plt.grid(True)
        plt.show()

# Simulate TCP Reno
tcp_reno = TCP_Reno(loss_rate=0.1, rtt=0.1)
tcp_reno.simulate(num_iterations=20)

# Visualize congestion window size over time
tcp_reno.plot_congestion_window()

# Visualize throughput over time
tcp_reno.plot_throughput()

# Visualize packet loss over time
tcp_reno.plot_packet_loss()

# Visualize round-trip time (RTT) over time
tcp_reno.plot_rtt()
