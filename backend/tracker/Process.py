import psutil
import datetime as dt
import time

class Process:
    def __init__(self, title: str):
        self.__title = title
        self.__start_time = psutil.process_iter([])
        self.__end_time = None
        self.__snapshot = None
        self.__running = False



    ## GETTERS ##
    def get_title(self):
        return self.__title
    
    def get_start_time(self):
        return self.__start_time
    
    def get_end_time(self):
        return self.__end_time
    
    def get_snapshot(self):
        return self.__snapshot
    
    def get_process(self, processes):
        for proc in processes:
            if proc.info["name"] == self.__title:
                return proc
        return None
    
    def get_is_running(self, processes):
        self.set_running(self.__is_running(processes))
        return



    ## SETTERS ##
    def set_start_time(self, processes):
        proc = self.get_process(processes)
        if proc:
            self.__start_time = dt.datetime.fromtimestamp(proc.info["create_time"])
        return self.__start_time

    def set_snapshot(self, processes):
        proc = self.get_process(processes)
        if proc:
            self.__snapshot = {
                "name": proc.info["name"],
                "create_time": dt.datetime.fromtimestamp(proc.info["create_time"]),
                "cpu_times": proc.info["cpu_times"],
                "time_of_snapshot": dt.datetime.now()
            }

    def set_end_time(self):
        self.__end_time = self.__snapshot["time_of_snapshot"] if self.__snapshot else dt.datetime.now()
        return self.__end_time
    
    def set_running(self, state: bool):
        self.__running = state
        return self.__running

    

    ## PRIVATE METHODS ##
    def __is_running(self, processes):
        for proc in processes:
            if self.get_title().lower() in proc.info["name"].lower():
                self.set_running(True)
                print(f"[200]{self.get_title()} is running")
                return self.__running
        print(f"[404]{self.get_title()} is not running")
        self.set_running(False)
        self.set_end_time()
        return self.__running


