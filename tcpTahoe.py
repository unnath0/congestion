import matplotlib.pyplot as plt
import numpy as np

class TCP_Tahoe:
    np.random.seed(100)
    def __init__(self, cwnd_initial=1, max_cwnd=15, ssthresh=65535, loss_rate=0.1, rtt=1):
        self.cwnd = cwnd_initial  # Initial congestion window size
        self.max_cwnd = max_cwnd  # Maximum congestion window size
        self.ssthresh = ssthresh  # Slow start threshold
        self.time = [0]  # Time intervals
        self.cwnd_values = [self.cwnd]  # Congestion window size over time
        self.loss_rate = loss_rate  # Packet loss rate
        self.rtt = rtt  # Round-trip time

    def simulate(self, num_iterations=20):
        for i in range(num_iterations):
            # Simulate packet loss
            if np.random.rand() < self.loss_rate:
                self.ssthresh = self.cwnd / 2  # Adjust slow start threshold
                self.cwnd = 1  # Set congestion window size after loss
            else:
                # Slow start phase
                if self.cwnd < self.ssthresh:
                    self.cwnd *= 2
                # Congestion avoidance phase
                else:
                    self.cwnd += 1 if self.cwnd < self.max_cwnd else 0
            # Cap congestion window size to maximum value
            self.cwnd = min(self.cwnd, self.max_cwnd)
            # Record time and congestion window size
            self.time.append(self.time[-1] + self.rtt)
            self.cwnd_values.append(self.cwnd)

    def plot_congestion_window(self):
        plt.plot(self.time, self.cwnd_values, marker='o')
        plt.title('TCP Tahoe Congestion Window Size Over Time')
        plt.xlabel('Time (s)')
        plt.ylabel('Congestion Window Size')
        plt.grid(True)
        plt.show()

    def plot_throughput(self):
        # Exclude the first element of time to avoid division by zero
        throughput = [self.cwnd_values[i] / self.time[i] for i in range(1, len(self.time))]
        time = self.time[1:]  # Exclude the first element of time
        plt.plot(time, throughput, marker='o')
        plt.title('TCP Tahoe Throughput Over Time')
        plt.xlabel('Time (s)')
        plt.ylabel('Throughput (packets/s)')
        plt.grid(True)
        plt.show()

    def plot_packet_loss(self):
        packet_loss = [1 if np.random.rand() < self.loss_rate else 0 for _ in range(len(self.time))]
        plt.plot(self.time, packet_loss, marker='o')
        plt.title('TCP Tahoe Packet Loss Over Time')
        plt.xlabel('Time (s)')
        plt.ylabel('Packet Loss (1 = loss, 0 = no loss)')
        plt.grid(True)
        plt.show()

    def plot_rtt(self):
        rtt_values = [self.rtt] * len(self.time)
        plt.plot(self.time, rtt_values, marker='o')
        plt.title('TCP Tahoe Round-Trip Time (RTT) Over Time')
        plt.xlabel('Time (s)')
        plt.ylabel('RTT (s)')
        plt.grid(True)
        plt.show()

# Simulate TCP Tahoe
tcp_tahoe = TCP_Tahoe(loss_rate=0.1, rtt=0.1)
tcp_tahoe.simulate(num_iterations=20)

# Visualize congestion window size over time
tcp_tahoe.plot_congestion_window()

# Visualize throughput over time
tcp_tahoe.plot_throughput()

# Visualize packet loss over time
tcp_tahoe.plot_packet_loss()

# Visualize round-trip time (RTT) over time
tcp_tahoe.plot_rtt()
