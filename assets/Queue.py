from assets.Job import Job
from typing import List, Union

class Queue:
    def __init__(self, jobs=None):
        if jobs is None:
            self.mainList = []
            self.number = 0
        elif isinstance(jobs, int):
            self.mainList = [None] * jobs
            self.number = jobs
        elif isinstance(jobs, list):
            self.mainList = jobs.copy()
            self.number = len(jobs)
        else:
            raise ValueError("Invalid type for jobs. Must be either an integer, a list of Job instances, or None.")
    def fill(self):
        for i in range(self.number):
            temp = Job(i + 1)  
            self.mainList[i] = temp

    def getJob(self, num):
        return self.mainList[num]

    def removeJob(self, num):
        del self.mainList[num]

    def addJob(self, job):
        self.mainList.append(job)

    def set(self, i, job):
        self.mainList[i] = job

    def isEmpty(self):
        return not self.mainList

    def size(self):
        return len(self.mainList)

    def clearQueue(self):
        self.mainList = []

    def OrderedByArrive(self):
        self.mainList.sort(key=lambda x: x.arrivalTime)

    def OrderedByShortest(self):
        self.mainList.sort(key=lambda x: x.burst)

    def OrderedByPriority(self):
        self.mainList.sort(key=lambda x: x.priority)

    def OrderedByShortRemain(self):
        self.mainList.sort(key=lambda x: x.remaining)

    def getCopy(self):
        return Queue([job for job in self.mainList])

    def getClearCopy(self):
        return Queue([job.getClearCopyJob() for job in self.mainList])
    def OrderedByStartTime(self):
        self.mainList.sort(key=lambda j: j.getStart())
    def showQueue(self, simulationTime):
        if self.isEmpty():
            print("Empty Queue")
            return
        print("number of jobs", self.size())
        print("#   Arrive   Burst   Priority   Start   Wait   Remain   Finish   Turn   % ")
        for temp in self.mainList:
            print(temp.jobNumber, temp.arrivalTime, temp.burst, temp.priority, temp.getStart(),
                  temp.getWaitTime(simulationTime), temp.getRemainTime(), temp.getFinish(),
                  temp.getTurnaround(simulationTime), temp.getPercent())

    def removeJob2(self, job):
        if job in self.mainList:
            self.mainList.remove(job)