from abc import abstractmethod


class Plugin:
    @abstractmethod
    def connectivity_test(self):
        raise NotImplementedError()

    @abstractmethod
    def collect(self):
        raise NotImplementedError()

    def run(self):
        if self.connectivity_test():
            self.collect()
