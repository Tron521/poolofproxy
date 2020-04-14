from get import getter
from app import app
from multiprocessing import Process
from test import tester
import time
TESTER_CYCLE = 20
GETTER_CYCLE = 20
TESTER_ENABLED = True
GETTER_ENABLED = False
API_ENABLED = True


class scheduler(object):
    def schedule_tester(self, cycle=TESTER_CYCLE):
        self.tester = tester()
        while True:
            print("  测试器开始运行  ")
            self.tester.run()
            time.sleep(cycle)

    def schedule_getter(self, cycle=GETTER_CYCLE):
        self.getter = getter()
        while True:
            print("  测试器开始运行  ")
            self.getter.run()
            time.sleep(cycle)

    def schedule_app(self):
        app.run()

    def run(self):
        print("代理池开始运行")
        if TESTER_ENABLED:
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()
        if GETTER_ENABLED:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()
        if API_ENABLED:
            app_process = Process(target=self.schedule_app)
            app_process.start()


scheduler = scheduler()
scheduler.run()
