import threading


class Manager:

    def start(self):
        threading.Thread(target=self.run)

    def run(self):
        print("run Manager")
