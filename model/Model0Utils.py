from collections import deque

import numpy as np

from model.Model0 import logger


def calculate_price(stablecoin_amount_in_pool, money_amount_in_pool):
    return money_amount_in_pool / stablecoin_amount_in_pool


def float_equal(a, b, config):
    return abs(a - b) < config.eps


# This is a high-efficient implementation of the risk queue
# It can be used to calculate the average risk with O(1) time complexity
# The aggregate time complexity of a single simulation is no more than O(n)
class RiskQueue:

    def __init__(self, simulation_time_interval, max_time_span, simulation_time_unit_timedelta):
        self.queue = deque()
        self.sum = 0
        self.simulation_time_interval = simulation_time_interval
        self.max_time_span = max_time_span
        self.simulation_time_unit_timedelta = simulation_time_unit_timedelta

    def add(self, time, risk):
        self.queue.append((time, risk))
        self.sum += risk

    def get_average(self, now_simulation_time):
        if len(self.queue) == 0:
            logger.warning("The risk_queue is empty.")
            return 0

        earliest_time = now_simulation_time - self.max_time_span
        while self.queue[0][0] < earliest_time:
            self.sum -= self.queue[0][1]
            self.queue.popleft()
        return self.sum / (len(self.queue) * (self.simulation_time_interval / self.simulation_time_unit_timedelta))


class LogNormalVariable:

    def __init__(self, phi, omega):
        self.phi = phi
        self.omega = omega

    def sample(self):
        if self.omega == 0:
            return self.phi
        elif self.phi == 0:
            return 0
        else:
            return np.random.lognormal(self.phi, self.omega)


