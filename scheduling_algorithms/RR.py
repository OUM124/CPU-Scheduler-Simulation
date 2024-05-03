from matplotlib import pyplot as plt
from .Algorithm import Algorithm

class RR(Algorithm):
    def __init__(self, work_queue, quantum):
        super().__init__(work_queue)
        self.quantum = quantum  # Quantum time for the algorithm
        self.process_time = 0  # Remaining quantum time for a specific job
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

    def nextStep(self, simulation_time):
        # Update the ready queue with any new arrivals
        self.initializePlot()  # Initialize the plot if not already done
        self.updateReadyQueue(simulation_time)

        # If the CPU is not busy and there is no current job, try to load a new job
        if not self.busy and not self.currentJob:
            if not self.readyQueue.isEmpty():
                self.setCurrentJob()
                self.process_time = min(self.quantum, self.currentJob.getRemainTime())
                self.busy = True

            else:
                return None, False  # No job to process, CPU is not busy

        # Check if the job has finished or the quantum time has expired
        if self.currentJob and self.currentJob.getRemainTime() == 0:
            self.gantt_chart_info.append(('P' + str(self.currentJob.jobNumber), self.quantum - self.process_time))
            self.currentJob = None
            self.busy = False

        if self.process_time <= 0 and self.currentJob:
            # Job still has remaining time, re-queue it
            self.gantt_chart_info.append(('P' + str(self.currentJob.jobNumber), self.quantum))
            self.readyQueue.addJob(self.currentJob)
            self.currentJob = None
            self.busy = False

        # Load the next job if available
        if not self.busy and not self.readyQueue.isEmpty():
            self.setCurrentJob()
            self.process_time = min(self.quantum, self.currentJob.getRemainTime())
            self.busy = True

        # Process the current job if there is one
        if self.currentJob:
            self.workInCpu(simulation_time)

        self.updatePlot()  # Update the plot
        plt.pause(0.5)  # Pause to slow down the execution speed

        return self.currentJob, self.busy
    

    
    def workInCpu(self, simulation_time):
        """Process the current job in the CPU for one simulation time step."""
        
        if self.currentJob:
            if not self.busy:
                self.delay +=1
            if self.process_time == self.quantum :
                if self.currentJob.remaining == 0 :
                    pass
                elif self.currentJob.remaining < self.quantum:
                    self.checkDelay()
                    self.gantt_chart.append(['P'+ str(self.currentJob.jobNumber),
                                        self.currentJob.remaining])
                else:
                    self.checkDelay()
                    self.gantt_chart.append(['P'+ str(self.currentJob.jobNumber),
                                      self.quantum])
            if self.currentJob.getRemainTime() == 0:
                
                print(f"Job {self.currentJob.jobNumber} finished at time {simulation_time}")
                self.completed_processes.append(self.currentJob)  # Append the completed process

                self.currentJob = None
                self.busy = False  # Mark CPU as not busy because the job is finished
            else:
                self.currentJob.jobWorked(simulation_time)
                self.process_time -= 1  # Decrement the remaining quantum time

    def updatePlot(self):
        self.ax.clear()

        # Create Gantt bars and generate legend labels dynamically
        colors = {}  # Initialize colors dictionary
        start_time = 0
        for process, time in self.gantt_chart_info:
            if process not in colors:  # Check if process is not in colors dictionary
                colors[process] = plt.cm.tab10(len(colors))  # Generate a new color for the process
            color = colors[process]
            self.ax.barh(y=0, width=time, left=start_time, height=0.5, align='center', color=color)
            start_time += time

        # Add legend outside the loop
        legend_handles = [(plt.Rectangle((0, 0), 1, 1, color=color), process) for process, color in colors.items()]
        self.ax.legend([handle for handle, process in legend_handles], [process for handle, process in legend_handles], loc='upper right')

        # Set labels and ticks
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Process')
        self.ax.set_yticks([])
        self.ax.set_title('Gantt Chart')
