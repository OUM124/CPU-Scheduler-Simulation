from matplotlib import pyplot as plt
from .Algorithm import Algorithm

class SJF(Algorithm):
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
        if not self.busy:
            if self.readyQueue.isEmpty():
                return None, self.busy
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
        return current_job, busy
    
    

    def workInCPU(self, simulationTime):
        if self.currentJob is None:
            return None, self.busy
        
        if self.currentJob.start is None:  # Check if start time is None
            self.currentJob.start = simulationTime  # Set start time if not set
    
        if self.currentJob.getRemainTime() == 0:
            print(f"Job {self.currentJob.jobNumber} finished at time {simulationTime}")
            self.completed_processes.append(self.currentJob)  # Append the completed process
            self.checkDelay()
            self.gantt_chart.append(['P'+ str(self.currentJob.jobNumber),
                                    self.currentJob.burst])
            self.currentJob = None
            self.busy = False
            if not self.readyQueue.isEmpty():
                    self.setCurrentJob()  # Immediately set the next job if available
                    self.busy = True
                    self.currentJob.setRemainTime(self.currentJob.getRemainTime() - 1)  # Decrease remaining time by 1 for the next job

        else : 
            self.currentJob.jobWorked(simulationTime)    
        return self.currentJob, self.busy

    def updatePlot(self):
        self.ax.clear()

        # Create Gantt bars and generate legend labels dynamically
        colors = {'Idle': 'gray'}  # Initialize colors dictionary with Idle
        running_processes = set()
        start_time = 0
        for process, time in self.gantt_chart_info:
            if process == 'Idle':
                continue  # Skip adding idle time to the legend
            running_processes.add(process)
            if process not in colors:  # Check if process is not in colors dictionary
                colors[process] = plt.cm.tab10(len(colors))  # Generate a new color for the process
            color = colors[process]
            self.ax.barh(y=0, width=time, left=start_time, height=0.5, align='center', color=color)
            start_time += time
        
        # Add legend outside the loop for only running processes
        legend_handles = [(plt.Rectangle((0,0),1,1, color=color), process) for process, color in colors.items() if process in running_processes]
        self.ax.legend([handle for handle, _ in legend_handles], [process for _, process in legend_handles], loc='upper right')

        # Set labels and ticks
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Process')
        self.ax.set_yticks([])
        self.ax.set_title('Gantt Chart')
