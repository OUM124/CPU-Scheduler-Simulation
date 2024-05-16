from matplotlib import pyplot as plt
from .Algorithm import Algorithm

class FCFS(Algorithm):
    def __init__(self, workQueue):
        super().__init__(workQueue)
        self.gantt_chart_info = []  # List to store process information for Gantt chart
        self.ax = None  # Placeholder for axes object
        self.completed_processes = []


    def initializePlot(self):
        if self.ax is None:
            self.fig, self.ax = plt.subplots()  # Create figure and axes for the plot
            self.ax.set_xlabel('Time')
            self.ax.set_ylabel('Process') 
            self.ax.set_yticks([])
            self.ax.set_title('Gantt Chart')

    def nextStep(self, simulationTime):
        self.initializePlot()  # Initialize the plot if not already done
        self.updateReadyQueue(simulationTime)
        if not self.busy and not self.readyQueue.isEmpty():
            self.busy = True
            self.setCurrentJob()
            print(f"Current job set: {self.currentJob.jobNumber if self.currentJob else 'No Job'}")
        current_job, busy = self.workInCPU(simulationTime)  # Ensure workInCPU returns a tuple
        
        # Update Gantt chart information
        if self.currentJob:
            self.gantt_chart_info.append((f'P{self.currentJob.jobNumber}', 1))
        else:
            self.gantt_chart_info.append(('Idle', 1))
        
        self.updatePlot()  # Update the plot
        plt.pause(0.5)  # Pause to slow down the execution speed
        if self.isFinished():
            self.completed_processes.append(self.currentJob) 
        return current_job, busy
    
    


    def workInCPU(self, simulationTime):
        if self.currentJob is None:
            return None, self.busy
        
        if self.currentJob.start is None:  # Check if start time is None
            self.currentJob.start = simulationTime  # Set start time if not set
        if not self.busy:
            self.delay +=1
        if self.currentJob.getRemainTime() == 0:  # Check if current job has finished
            self.checkDelay()
            print(f"Job {self.currentJob.jobNumber} finished at time {simulationTime}")
            self.gantt_chart.append(['P'+ str(self.currentJob.jobNumber),
                                    self.currentJob.burst])
            self.currentJob = None
            self.busy = False
            if not self.readyQueue.isEmpty():
                self.setCurrentJob()  # Immediately set the next job if available
                self.busy = True
                self.currentJob.setRemainTime(self.currentJob.getRemainTime() - 1)  # Decrease remaining time by 1 for the next job
        else: 
            self.currentJob.jobWorked(simulationTime)  

        return self.currentJob, self.busy

    def updatePlot(self):
        self.ax.clear()

        # Initialize colors and legend labels dictionaries
        colors = {}
        legend_labels = {}

        # Create Gantt bars
        start_time = 0
        for process, time in self.gantt_chart_info:
            # Check if color and legend label for the process already exist
            if process not in colors:
                colors[process] = plt.cm.tab10(len(colors) % 10)  # Assign color based on number of processes
                legend_labels[process] = f'Process {process[1:]}'  # Generate legend label for the process
            color = colors[process]

            # Create Gantt bar for the process
            self.ax.barh(y=0, width=time, left=start_time, height=0.5, align='center', color=color, label=None)
            start_time += time

        # Add legend outside the loop
        legend_handles = [(plt.Rectangle((0, 0), 1, 1, color=colors[process]), label) for process, label in legend_labels.items()]
        self.ax.legend([handle for handle, _ in legend_handles], [label for _, label in legend_handles], loc='upper right')

        # Set labels and ticks
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Process')
        self.ax.set_yticks([])
        self.ax.set_title('Gantt Chart')
