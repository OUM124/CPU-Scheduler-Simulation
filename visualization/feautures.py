import random
from assets.Job import Job
from typing import List, Union
from .Table import Table


# Function to print job information/features in a table
def print_in_table(jobQueue):
    if jobQueue.getJob(0).getStart():
        # Sort by start time
        jobQueue.OrderedByStartTime()

    dictJobs = []
    for job in jobQueue.mainList:
        dictJobs.append(job.getDict())

    # Create and display jobs with a table
    table = Table()  # Assuming Table is already defined somewhere
    table.addData(dictJobs)
    table.display()


# Function to print job information/features outside of a table
def print_off_table(jobQueue):
    n = jobQueue.size()

    total_time = 0
    for job in jobQueue.mainList:
        if total_time < job.getFinish():
            total_time = job.getFinish()

    throughput = total_time / n

    # Calculate average metrics 
    avg_start_time = sum(job.getStart() for job in jobQueue.mainList) / n
    avg_turnaround_time = sum(job.getTurnaround(job.finish) for job in jobQueue.mainList) / n
    avg_waiting_time = sum(job.getWaitTime(job.finish) for job in jobQueue.mainList) / n
    #avg_response_time = sum(job.getResponseTime() for job in jobs) / n

    # Output
    print("Average Start Time        : {:.2f}".format(avg_start_time))
    print("Average Turnaround Time   : {:.2f}".format(avg_turnaround_time))
    print("Average Waiting Time      : {:.2f}".format(avg_waiting_time))
    print("Throughput                : {:.2f} second\n".format(throughput))


# Function to print Gantt chart
def printGanttChart(gantt_chart):
    if not gantt_chart:
        print("Gantt chart is empty")
        return

    print("Gantt Chart:")

    border = ' '
    for job in gantt_chart:
        border += '__' * job[1] + ' '

    label = '|'
    for job in gantt_chart:
        space = '_' * (job[1] - 1)
        label += space + job[0] + space + '|'

    print(border)
    print(label)

    time = 0
    print(time, end="")
    for job in gantt_chart:
        print('  ' * (job[1]), end='')
        time += job[1]

        if time > 9:
            print("\b", end="")
            
        print(time, end="")

    print()



def compute_average_metrics(processes_dict):
    """Compute average metrics for each algorithm."""
    avg_metrics = {}
    for algorithm_name, processes in processes_dict.items():  # Iterate over dictionary items
        total_wait_time = 0
        total_turnaround_time = 0
        total_response_time = 0
        total_throughput = 0 
        num_processes = 0  # Initialize the count of valid processes 

        for process in processes:
            if process is not None and isinstance(process, Job):  # Check if the process is valid
                total_wait_time += process.totalWait
                total_turnaround_time += (process.finish - process.arrivalTime)
                total_response_time += (process.start - process.arrivalTime)
                num_processes += 1  # Increment the count of valid processes

        if num_processes > 0:  # Check if there are valid processes to compute metrics
            # Compute average metrics
            avg_wait_time = total_wait_time / num_processes
            avg_turnaround_time = total_turnaround_time / num_processes
            avg_response_time = total_response_time / num_processes
            avg_throughput = total_throughput / num_processes

            # Store average metrics for the algorithm
            avg_metrics[algorithm_name] = {
                'Avg Wait Time': avg_wait_time,
                'Avg Turnaround Time': avg_turnaround_time,
                'Avg Response Time': avg_response_time,
                'Throughput': avg_throughput
            }

    return avg_metrics

def print_comparison_table(avg_metrics):
    if not avg_metrics:
        print("No data to display")
        return

    header = "| {:<30} | {:<20} | {:<25} | {:<20} | {:<20} |".format(
        "Algorithm", "Avg Wait Time", "Avg Turnaround Time", "Avg Response Time", "Throughput" 
    )
    separator = "-" * len(header)
    print(separator)
    print(header)
    print(separator)

    for algorithm_name, metrics in avg_metrics.items():  # Use .items() to iterate over dictionary items
        row = "| {:<30} | {:<20.2f} | {:<25.2f} | {:<20.2f} | {:<20.2f} |".format(
            algorithm_name,
            metrics['Avg Wait Time'],
            metrics['Avg Turnaround Time'],
            metrics['Avg Response Time'],
            metrics['Throughput']
        )
        print(row)
        print(separator)

