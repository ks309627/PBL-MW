from FC500Com import FC500Com
from LoggingHandler import ErrorLogger
from PySide6.QtCore import QTimer

import asyncio

class MeasureProcess:
    
    def __init__(self):
        self.logger = ErrorLogger()
        
        self.loop = asyncio.get_event_loop()
        self.cycle = self.loop.create_task(self.MeasureCycle())

    def StopCycle(self):
        self.cycle.cancel()

    async def MeasureCycle(self):
        try:
            while True:
                self.A()
                QTimer.singleShot(500, lambda:(
                self.B(),
                QTimer.singleShot(500,lambda:(
                self.C()
                ))))
                break
        except asyncio.CancelledError:
            self.logger.log_info("Safety Mushroom Pressed")

    def A(self):
        self.logger.log_info("A")
    def B(self):
        self.logger.log_info("B")
    def C(self):
        self.logger.log_info("C")

    # async def long_running_function():
    #     try:
    #         while True:
    #             print("Function is running...")
    #             await asyncio.sleep(1)
    #     except asyncio.CancelledError:
    #         print("Function was cancelled!")

    # async def main():
    #     task = asyncio.create_task(long_running_function())
    #     await asyncio.sleep(5)  # Let the function run for 5 seconds
    #     task.cancel()
    #     await task  # Wait for the cancellation to complete

    # asyncio.run(main())