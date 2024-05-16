# import liblary yang dibutuhkan
import glob
import time
import sys
sys.path.append("scheduling_algorithms")

# import model

from assets.Job import Job

from assets.Queue import Queue
from visualization.feautures import print_in_table, print_off_table, printGanttChart,compute_average_metrics,print_comparison_table
from scheduling_algorithms.FCFS import FCFS
from scheduling_algorithms.SJF import SJF
from scheduling_algorithms.PriorityRR import PriorityRoundRobin

from scheduling_algorithms.Priority import Priority
#from scheduling_algorithms.PriorityPreemptive import PriorityPreemptive
from scheduling_algorithms.RR import RR

def run_all_processes(processes):
    # Define a dictionary to store completed processes for each algorithm
    processes_dict = {}

    # Run each scheduling algorithm and store completed processes
    fcfs = FCFS(processes) # Reset processes before running the algorithm
    run_scheduler(fcfs, processes)
    processes_dict["FCFS"] = fcfs.completed_processes
    

    sjf = SJF(processes)
    reset_processes(processes)  # Reset processes before running the algorithm
    run_scheduler(sjf, processes)
    processes_dict["SJF"] = sjf.completed_processes

    priority = Priority(processes)
    reset_processes(processes)  # Reset processes before running the algorithm
    run_scheduler(priority, processes)
    processes_dict["Priority"] = priority.completed_processes

    rr = RR(processes, quantum)
    reset_processes(processes)  # Reset processes before running the algorithm
    run_scheduler(rr, processes)
    processes_dict["RR"] = rr.completed_processes

    print(processes_dict)

    return processes_dict

def reset_processes(processes):
    """Reset all processes in the queue."""
    for process in processes.mainList:
        process.reset()


def run_scheduler(scheduler, work_queue):
    simulationTime = 0
    while not scheduler.isFinished():
        current_job, cpu_busy = scheduler.nextStep(simulationTime)
        
        if current_job:
            print(f"Processing Job {current_job.jobNumber} at time {simulationTime}")
       
        elif current_job is None and  not work_queue.isEmpty() : 
            scheduler.delay +=1
            print("No job is being processed at time", simulationTime)
        # the current job is none but the queue still have some elements inside   
        simulationTime += 1
        
        if not cpu_busy:
            continue

    
    work_queue.showQueue(simulationTime)

def printInfo(processes, ganttChart=None):
    # display information in table
    print_in_table(processes)

    # display information off table
    print_off_table(processes)

    if ganttChart:
        # display gantt chart
        printGanttChart(ganttChart)

# MAIN PROGRAM 
# ========================

# read data file .txt 
txt_files = glob.glob("test-case/*.txt")

schedulingAlgorithms = ["FCFS (First Come First Served)",
                        "SJF (Shortest Job First)",
                        "Priority Scheduling (Non-Preemptive)",
                        "RR (Round Robin)",
                        "RR & Priority (Round Robin & Priority)"
                        ]

# Display
print()
print('-' * 35 + " Simulation Scheduling Algorithm " + '-' * 35, end="\n\n")

# SIMULATION
while True:
    
    print("Select input type:")
    print("1. Manual")
    print("2. Import test case")
    print("3. Generate Randomly")
    print("0. Exit")
    print('=' * 30)
    print("Enter number:")
    choice = int(input("-> "))
    print('-' * 10, end="\n\n")

    processes = Queue()
    if choice == 1:
        # manual input
        n = int(input("Enter how many processes: "))
        for i in range(n):
            arrive_time = int(input("Enter Arrive Time: "))
            burst_time = int(input("Enter Burst Time: "))
            job_priority = int (input("Enter Priority: "))
            processes.addJob(Job(jobNumber=i, arrivalTime = arrive_time, burst=burst_time, priority = job_priority))

    elif choice == 2:
        # input test case data file .txt

        # Prompt the user to enter the filename
        filename = input("Enter the filename (including path if necessary): ")

        try:
            # Open the file and read the data
            with open(filename, 'r') as f:
                data = f.readlines()

            # Process the data
            for line in data:
                values = line.strip().split()
                if len(values) == 4:
                    name, arrival_time, burst_time, priority = values
                    processes.addJob(Job(name[1], int(arrival_time), int(burst_time), int(priority)))
                elif len(values) == 3:
                    name, arrival_time, burst_time = values
                    processes.addJob(Job(name[1], int(arrival_time), int(burst_time)))
                else:
                    pass

            
            n = processes.size()  

        except FileNotFoundError:
            print("File not found. Please make sure the filename and path are correct.")
            continue
    elif choice == 3:
        # generate data randomly
        n = int(input("Enter the number of processes: "))
        processes = Queue(n)
        processes.fill()

    elif choice == 0:
            break

    else:
            print("[!]> Invalid choice <[!]", end="\n\n")
            continue

    if processes:

        print("Input Process:")
        print_in_table(processes)

        while True:
            print("Scheduling Algorithms:")
            for i, algorithm in enumerate(schedulingAlgorithms):
                print(f"{i+1}. {algorithm}")
            #print("7. Compare all Scheduling Algorithms")    
            print("0. Exit")
            print('=' * 30)
            print("Enter number:")
            choice = int(input("-> "))
            print('-' * 10, end="\n\n")

            if choice == 3:
                if not processes.getJob(0).priority:
                    print("Enter Priority:")
                    print("Name Arrive Burst Priority")
                    for process in processes:
                        print(f"{process.getName()}   {process.arrivalTime}      {process.burst}     ", end="")
                        process.setPriority(int(input()))
                
                print()

            elif choice == 4 or choice == 5:
                set_quantum = input("Set quantum: ")
                
                if set_quantum:
                    quantum = int(set_quantum)

            # Process
            # ===================================================

            if choice != 0 and choice < 7:
                for i in range(4):
                    print('.' * (i+1))
                    time.sleep(0.2)
                print()
            
            if choice == 1:
                # process FCFS (First Come First Served) algorithm
                fcfs = FCFS(processes)
                run_scheduler(fcfs, processes)
                print('-' * 35 + " FCFS (First Come First Served) " + '-' * 35)
                # display information 
                printInfo(processes, fcfs.getGanttChart())
                

            elif choice == 2:
                # process SJF (Shortest Job First) 
                sjf = SJF(processes)
                run_scheduler(sjf, processes)

                print('-' * 35 + " SJF (Shortest Job First) " + '-' * 35)

                # display information 
                printInfo(processes, sjf.getGanttChart())

            elif choice == 3:
                if processes.getJob(0).priority:
                    priority = Priority(processes)
                    run_scheduler(priority, processes)
                    print('-' * 35 + " Priority " + '-' * 35)

                    # display information
                    printInfo(processes, priority.getGanttChart())

                else:
                    print("[!]> The input process has no priority <[!]")

            elif choice == 4:
                # process RR (Round Robin) 
                rr = RR(processes, quantum)
                run_scheduler(rr, processes)

                print('-' * 35 + " RR (Round Robin) " + '-' * 35)

                # display information
                printInfo(processes, rr.getGanttChart())


            elif choice == 5:
                if processes.getJob(0).priority:
                    processList = processes.mainList
                    priority_RR =PriorityRoundRobin(processList,quantum)
                    priority_RR.run()
                    print('-' * 35 + " Priority " + '-' * 35)

                    # display information
                    printInfo(processes, priority_RR.getGanttChart())
                    

                else:
                    print("[!]> The input process has no priority <[!]")

            elif choice == 6:
                # process RR (Round Robin) 
                rr = RR(processes, quantum)
                rr.run()
                processes = rr.getCompletedProcesses()

                print('-' * 35 + " RR (Round Robin) " + '-' * 35)

                # display information
                printInfo(processes, rr.getGanttChart())

            elif choice == 0:
                break
            elif choice == 7:
                # Prompt the user to set the quantum value
                set_quantum = input("Set quantum: ")
                if set_quantum:
                    quantum = int(set_quantum)
                processes_dict = run_all_processes(processes)
                # Ensure there are completed processes to compare
                avg_metrics = compute_average_metrics(processes_dict)  # Compute average metrics for each algorithm
                print_comparison_table(avg_metrics)  # Print the comparison table
            else:
                print("[!]> Invalid choice <[!]")
            
            print()
            print('-' * 100, end="\n\n")

            # ===================================================
            # reset
            for process in processes.mainList:
                process.reset()
                
    else:
        print("[!]> No process to run <[!]")


# Input
# -----------
# test case 
"""
processes = [
    Process("P0", 5, 3, 2),
    Process("P1", 4, 0, 3),
    Process("P2", 1, 1, 2),
    Process("P3", 3, 5, 4),
    Process("P4", 7, 3, 3),
    Process("P5", 2, 8, 1),
]
quantum = 2
n = len(processes)
"""
