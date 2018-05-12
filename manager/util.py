import threading


class Util:

    def start(self):
        threading.Thread(target=self.run)

    def run(self):
        print("###0")
