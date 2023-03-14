"""
    Description (TODO)
"""
import random
from typing import Dict


class Markovian:
    """
        Description (TODO)
    """

    def __init__(self,
                 lmbda: float,
                 mu: float) -> None:

        self.lmbda = lmbda
        self.mu = mu

        self.current_customers = 0
        self.entry_probability = self.lmbda / (self.lmbda + self.mu)
        self.exit_probability = self.mu / (self.lmbda + self.mu)
        self.average_waiting_time = 0
        self.total_waiting_time = 0
        self.average_queue_size = 0
        self.total_customers = 0
        self.customers_per_event = []
        self.waiting_time_per_customer = []
        self.waiting_time_queue = []

        self.current_moment = 0
        self.real_queue = []

        self.event_types = ["service", "entry"]

    def _get_service_time(self) -> float:
        """
        Description (TODO)
        """
        return random.expovariate(self.mu)

    def _get_event_type(self) -> str:
        """
        Description (TODO)
        """
        return random.choices(self.event_types, [self.exit_probability, self.entry_probability])[0]

    def update_prob(self) -> None:
        """
        Description (TODO)
        """

        if self.current_customers == 0:
            self.entry_probability = 1
            self.exit_probability = 0
        else:
            self.entry_probability = self.lmbda / (self.lmbda + self.mu)
            self.exit_probability = self.mu / (self.lmbda + self.mu)

    def event(self) -> None:
        """
        Description (TODO)
        """

        self.update_prob()
        event = self._get_event_type()

        if event == "entry":
            self.current_customers += 1
            self.waiting_time_queue.append(0)
        else:
            self.current_customers -= 1
            service_time = self._get_service_time()
            self.waiting_time_per_customer.append(
                self.waiting_time_queue.pop(0))
            if len(self.waiting_time_queue) > 0:
                for i in range(len(self.waiting_time_queue)):
                    self.waiting_time_queue[i] += service_time

        self.customers_per_event.append(self.current_customers)

    def run(self, number_of_iterations: int) -> Dict[str, float]:
        """
        Description (TODO)
        """

        metrics = dict()

        for _ in range(number_of_iterations):
            self.event()

        metrics["Average Queue Size"] = sum(
            self.customers_per_event) / number_of_iterations
        metrics["Average Waiting Time"] = sum(
            self.waiting_time_per_customer) / len(self.waiting_time_per_customer)

        return metrics
