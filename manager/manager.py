import threading


class Manager:

    def start(self):
        thread = threading.Thread(target=self.run)
        thread.start()

    def run(self):
        print("run Manager")
