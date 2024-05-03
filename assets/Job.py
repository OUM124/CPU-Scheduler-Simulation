import random


class Job:
    def __init__(self, jobNumber, arrivalTime=None, burst=None, priority=None):
        self.jobNumber = jobNumber  # job ID
        self.arrivalTime = arrivalTime if arrivalTime is not None else random.randint(0, 6) if jobNumber != 1 else 0
        self.burst = burst if burst is not None else random.randint(1, 30)
        self.start = None
        self.priority = priority if priority is not None else random.randint(1, 8)
        self.finished = False  # show if job is finished or not
        self.finish = 0  # finish time
        self.remaining = self.burst
        self.totalWait = 0
        self.in_queue = False
        self.turnAround_time=0
    def getBurstTimeRemaining(self):
        return self.remaining
    def reset(self):
        self.start = None
        self.finished = False
        self.finish = 0
        self.remaining = self.burst
        self.totalWait = 0

    def getName(self):
        return 'P'+ str(self.jobNumber)
    def setPriority(self,priority):
        self.priority = priority
    def updateWaitTime(self, simulationTime):
        # Update wait time only if the job has not started processing yet
        return self.getTurnaround(simulationTime) - (self.burst - self.getRemainTime())
    def jobWorked(self, simulationTime):
        if self.burst == self.remaining:  # First work
            self.start = simulationTime
        self.remaining -= 1
        if self.remaining == 0:  # Check for completion
            self.finish = simulationTime +1
            self.finished = True
        
    def copyJob(self):
        temp = Job(self.jobNumber, self.arrivalTime, self.burst, self.priority)
        temp.finished = self.finished
        temp.start = self.start
        temp.finish = self.finish
        return temp

    def getClearCopyJob(self):
        return Job(self.jobNumber, self.arrivalTime, self.burst, self.priority)

    def getPercent(self):
        return int((self.burst - self.getRemainTime()) * 100 / self.burst)

    def getWaitTime(self, simulationTime):
        return self.getTurnaround(simulationTime) - (self.burst - self.getRemainTime())
    

    def getRemainTime(self):
        return self.remaining

    def getTurnaround(self, simulationTime):
        if self.finished:
            return self.finish - self.arrivalTime
        if simulationTime > self.arrivalTime:
            return simulationTime - self.arrivalTime
        return 0

    def getFinish(self):
        return self.finish if self.finished else 0

    def getStart(self):
        return self.start

    def setRemainTime(self, remaining):
        self.remaining = remaining

    def setFinish(self, finish):
        self.finish = finish

    def setStart(self, start):
        self.start = start

    def isFirst(self, other):
        if self.arrivalTime == other.arrivalTime:
            return self.jobNumber < other.jobNumber
        return self.arrivalTime < other.arrivalTime

    def isShort(self, other):
        if self.burst == other.burst:
            return self.isFirst(other)
        return self.burst < other.burst

    def isPrior(self, other):
        if self.priority == other.priority:
            return self.isFirst(other)
        return self.priority < other.priority

    def isShortRemain(self, other):
        if self.remaining == other.remaining:
            return self.isFirst(other)
        return self.remaining < other.remaining
    
    def ShowData(self):
        print("Showing job data")
        if self is None:
            print("Empty job")
            return
        print("# =", self.jobNumber, ", arrive =", self.arrivalTime, ", burst =", self.burst)
    def updateMetrics(self, simulationTime):
        if self.start is None:
            self.start = simulationTime
        if self.remaining > 0:
            self.remaining -= 1
        if self.remaining == 0 and not self.finished:
            self.finish = simulationTime + 1
            self.finished = True
        if not self.finished:
            self.totalWait = simulationTime - self.arrivalTime - (self.burst - self.remaining - 1)
    def getDict(self):
        # Create a dictionary with job attributes
        job_dict = {
            'JobNumber': self.jobNumber,
            'ArrivalTime': self.arrivalTime,
            'BurstTime': self.burst,
            'Priority': self.priority,
            'StartTime': self.start,
            'FinishTime': self.finish,
            'TurnaroundTime': self.getTurnaround(self.finish),  # Calculate turnaround time using finish time
            'WaitingTime': self.getWaitTime(self.finish),  # Calculate waiting time using finish time
        }

        # Remove None values from the dictionary
        job_dict = {key: value for key, value in job_dict.items() if value is not None}

        return job_dict
