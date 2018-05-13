import threading


class Manager:
    def __init__(self, models):
        """

        :type models: models
        """
        self.models = models

    def start(self):
        thread = threading.Thread(target=self.run)
        thread.start()

    def run(self):
        print("run Manager")
