"""
Simple M/M/1/inf queue simulation
See https://en.wikipedia.org/wiki/M/M/1_queue
"""
import math
import random
from typing import Dict, List, Union


class Markovian:
    """
    A M/M/1/inf simulating class with implemented entry-service processes
    with single server and single queue, where arrivals 
    determined by a Poisson process and job service times
    have exponential distribution.
    """

    time_in_system: float = 0
    entry_times: List = []
    exit_times: List = []
    queue_sizes: List = []
    total_sizes: List = []
    waiting_times: List = []
    system_times: List = []
    shift_times: List = []

    def __init__(self,
                 lmbda: float,
                 mu: float) -> None:

        self.lmbda = lmbda
        self.mu = mu

    def get_service_time(self) -> float:
        """
        Generating exponentially distributed service time
        """
        return random.expovariate(self.mu)

    def get_entry_time(self) -> float:
        """
        Generating exponentially distributed entry time
        """
        return random.expovariate(self.lmbda)

    def _generate_entries(self, number_of_entries) -> None:
        """
        Generating all entries depending on entered
        number of queries
        """

        last_entry = 0

        for _ in range(number_of_entries):
            time_between_entries = self.get_entry_time()
            self.entry_times.append(last_entry + time_between_entries)
            last_entry += time_between_entries

    def run(self, number_of_queries: int) -> Dict[str, Union[float, List[float]]]:
        """
        The main function that runs the simulation of a queue
        """

        metrics = dict()

        self._generate_entries(number_of_queries)

        self.exit_times = [0] * number_of_queries
        self.shift_times = [0] * number_of_queries
        self.exit_times[0] = self.entry_times[0] + self.get_service_time()

        for i in range(1, number_of_queries - 1):
            service_time = self.get_service_time()
            self.shift_times[i] = max(
                self.exit_times[i - 1], self.entry_times[i])
            self.exit_times[i] = max(
                self.exit_times[i - 1], self.entry_times[i]) + service_time
            self.time_in_system += self.exit_times[i] - self.entry_times[i]

        total_moments = math.trunc(max(self.exit_times))

        self.queue_sizes = [0] * (total_moments + 1)
        self.total_sizes = [0] * (total_moments + 1)
        self.waiting_times = [0] * (total_moments + 1)
        self.system_times = [0] * (total_moments + 1)
        for i in range(number_of_queries):
            for j in range(math.ceil(self.entry_times[i]), math.trunc(self.shift_times[i]) + 1):
                self.queue_sizes[j] += 1
                self.waiting_times[j] += (j - self.entry_times[i])
            for j in range(math.ceil(self.entry_times[i]), math.trunc(self.exit_times[i]) + 1):
                self.total_sizes[j] += 1
                self.system_times[j] += (j - self.entry_times[i])

        metrics["Average Total Queries in System Per Moment"] = [
            sum(self.total_sizes[:i]) / (i + 1) for i in range(1, total_moments)]
        metrics["Average Queue Size Per Moment"] = [
            sum(self.queue_sizes[:i]) / (i + 1) for i in range(1, total_moments)]
        metrics["Average System Time Per Moment"] = [
            sum(self.system_times[:i]) / (i + 1) for i in range(1, total_moments)]
        metrics["Average Waiting Time Per Moment"] = [
            sum(self.waiting_times[:i]) / (i + 1) for i in range(1, total_moments)]
        metrics["Average Queue Size"] = sum(self.queue_sizes) / total_moments
        metrics["Average Total Queries"] = sum(
            self.total_sizes) / total_moments
        metrics["Average System Time"] = self.time_in_system / number_of_queries
        metrics["Average Waiting Time"] = sum(
            self.waiting_times) / total_moments

        return metrics
