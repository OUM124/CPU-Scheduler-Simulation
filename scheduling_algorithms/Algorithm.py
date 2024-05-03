from assets.Job import Job
from assets.Queue import Queue


class Algorithm:
    def __init__(self, workQueue):
        self.readyQueue = Queue()
        self.currentJob = None
        self.busy = False
        self.list = workQueue.getCopy()
        self.list.OrderedByArrive()
        self.gantt_chart = []
        self.delay = 0

    def nextStep(self, simulationTime):
        self.updateReadyQueue(simulationTime)  # Ensures the ready queue is updated
        if not self.busy:
            if not self.readyQueue.isEmpty():
                self.busy = True
                self.setCurrentJob()  # Sets the current job from the ready queue
                print(f"Current job set: {self.currentJob.jobNumber if self.currentJob else 'No Job'}")
        current_job, busy = self.workInCPU(simulationTime)  # This should return a tuple
        return current_job, busy

    def workInCPU(self, simulationTime):
        if self.currentJob is None:
            return None, self.busy
        self.currentJob.jobWorked(simulationTime)
        if self.currentJob.getRemainTime() == 0:
            print(f"Job {self.currentJob.jobNumber} finished at time {simulationTime}")
            self.currentJob = None
            self.busy = False
        return self.currentJob, self.busy


    def updateReadyQueue(self, simulationTime):
        i = 0
        while i < self.list.size():
            temp = self.list.getJob(i)
            if temp.arrivalTime == simulationTime:
                self.readyQueue.addJob(temp)
                #temp.totalWait += simulationTime - temp.arrivalTime 
                self.list.removeJob(i)
               
            else:
                i += 1

    def setCurrentJob(self):
        if not self.readyQueue.isEmpty():
            self.currentJob = self.readyQueue.getJob(0)
            self.readyQueue.removeJob(0)
        else:
            self.currentJob = None
        

    def isFinished(self):
        return self.list.isEmpty() and self.readyQueue.isEmpty() and not self.busy and self.currentJob is None
    def getGanttChart(self):
        return self.gantt_chart
    
    def checkDelay(self):
        if self.delay:
            self.gantt_chart.append(['##', self.delay]) 
            self.delay = 0
    