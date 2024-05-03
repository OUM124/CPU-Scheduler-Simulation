from collections import deque
from assets.Job import Job

class PriorityRoundRobin:
    def __init__(self, processes, quantum):
        self.processes = processes
        self.quantum = quantum
        self.current_time = 0
        self.priority_queues = {1: deque(), 2: deque(), 3: deque(), 4: deque()}
        self.counter = 0
        self.gantt_chart = []

    def check_for_new_arrivals(self):
        for process in self.processes:
            if process.arrivalTime <= self.current_time and not process.in_queue and not process.finished:
                if process.priority not in self.priority_queues:
                    self.priority_queues[process.priority] = deque()  # Create a new queue if it doesn't exist
                self.priority_queues[process.priority].append(process)
                process.in_queue = True


    def update_queue(self):
        # Serve the lowest numerical priority first, which is considered the highest priority
        for priority in sorted(self.priority_queues.keys()):
            queue = self.priority_queues[priority]
            if queue:
                process = queue.popleft()
                if process.start is None:
                    process.start = self.current_time
                execution_time = min(self.quantum, process.remaining)
                if process.remaining == 0:
                    pass
                elif process.remaining < self.quantum:
                    self.gantt_chart.append(['P'+ str(process.jobNumber),
                                    process.remaining])
                else :
                    self.gantt_chart.append(['P'+ str(process.jobNumber),
                                    self.quantum])

                for _ in range(execution_time):
                    print(f"Processing Job {process.jobNumber} at time {self.current_time}")
                    process.remaining -= 1
                    
                    self.current_time += 1

                    if process.remaining == 0:
                        break
                
                if process.remaining == 0:
                    process.finished = True
                    process.in_queue = False
                    process.finish= self.current_time
                    process.turnAround_time = process.finish - process.arrivalTime
                    process.waiting_time = process.finish- process.arrivalTime - process.burst
                    print(f"Job {process.jobNumber} finished at time {self.current_time}")
                

                else :
                    
                    queue.append(process)  # Re-enqueue the process if it's not complete
                
                return  # Exit after processing one time slice

    def run(self):
        while any(not q.finished for q in self.processes):
            self.check_for_new_arrivals()
            self.update_queue()
        print("No job is being processed at time", self.current_time)
        
    def getGanttChart(self):
        return self.gantt_chart


