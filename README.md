# CPU Scheduler Simulation

## Overview
The CPU Scheduler Simulation program provides a detailed simulation of various scheduling algorithms to understand their behavior and impact on system performance. 

## Features
- *Multiple Scheduling Algorithms*: Includes First-Come, First-Served (FCFS), Shortest Job First (SJF), Priority Scheduling (Non-Preemptive), Round Robin (RR), and a Priority Scheduling with Round Robin.
- *Dynamic Input Options*: Users can manually input process details or import them from a test case file or generate randomply
- *Comprehensive Outputs*: The simulation provides detailed outputs including Gantt charts, process tables, and performance metrics.
- *Customizable Parameters*: Users can set parameters like quantum for Round Robin scheduling directly through the interface.

## Prerequisites
- Python 3.x
- No external libraries are required for the basic functions. However, if additional features are used, they may require external Python packages.

## Installation
1. Download the source code.
2. Ensure Python is installed on your system.

## Running the Program
Navigate to the directory containing main.py and run the following command:
YAML
python main.py

## Usage
Upon running the program, users will be presented with options to either manually input process details or import them from a file. The main options are:

1. *Manual Input*: Enter details such as arrival time, burst time, and priority for each process.
2. *Import Test Case*: Load processes from a predefined .txt file located in the test-case directory.
3. *Exit*: Terminate the program.

### Simulation Steps:
- *Choose the input method*: Decide whether to input data manually or import from a file.
- *Select the scheduling algorithm*: Choose from the list of available scheduling algorithms.
- *View the simulation results*, which include:
  - *Gantt chart visualization*: Provides a graphical representation of process scheduling.
  - *Detailed tables*: Shows metrics such as process start, finish, turnaround, waiting, and response times.
- *Adjust scheduling parameters* (if applicable), like quantum time for the Round Robin algorithm.

## Scheduling Algorithms
- *FCFS (First Come First Served)*: Processes are handled based on their arrival time.
- *SJF (Shortest Job First)*: Processes are sorted and executed based on their burst time.
- *Priority Scheduling (Non-Preemptive)*: Processes are executed according to their priority.
- *Round Robin (RR)*: Each process receives a fixed time slice in a rotating order.
- *Priority with Round Robin*: Processes are first grouped by priority, and Round Robin is applied within each group.

## File Structure
- main.py: The main program file.
- scheduling_algorithms/: Directory containing different scheduling algorithm implementations.
- assets/: Contains classes like Job and Queue for process management.
- visualization/: Contains functions to print tables and Gantt charts.
- test-case/: Directory for sample data files used for import.



## Input:
- *Job number*: string
- *Arrival time*: int
- *Burst time*: int
- *Priority*: int (for Priority Scheduling)
- *Quantum*: int (for Round Robin)

## Test Case:
Input test case using a .txt data file, example format:
YAML
#JobID #ArriveTime #BurstTime #Priority
0 0 12 3
1 19 6 4
2 13 9 4
3 4 1 5
4 8 6 2
5 8 2 6
6 10 10 1
2 #quantum


### Features

#### In the Table:
- *Start Time*: The time when execution by the CPU starts.
- *Finish Time*: The time when execution is completed.
- *Turnaround Time*: The time from arrival to completion.  
  Turnaround Time = Finish Time - Arrival Time
- *Waiting Time*: The time spent waiting in the ready queue.  
  Waiting Time = Turnaround Time - Burst Time
- *Response Time*: The time from arrival until the first execution.  
  Response Time = Start Time - Arrival Time

#### Off the Table:
- *Throughput*:  
  Throughput = Total Time / Number of Processes
- *Average Start Time*:  
  Average Start Time = Sum of Start Times / Number of Processes
- *Average Turnaround Time*:  
  Average Turnaround Time = Sum of Turnaround Times / Number of Processes
- *Average Waiting Time*:  
  Average Waiting Time = Sum of Waiting Times / Number of Processes
- *Average Response Time*:  
  Average Response Time = Sum of Response Times / Number of Processes

*Note: *Total Time refers to the total execution time for all processes, and Number of Processes refers to the total number of executed processes.

### Gantt Chart Example:
yaml
 ________ __ __________ ______________ ______ ____
|___P1___|P2|____P0____|______P4______|__P3__|_P5_|
0        4  5         10             17     20   22


## Simulation:
1. *Input Data* : Load your process data for simulation.

2. *Process Algorithm* : Choose among 5 scheduling algorithms.

3. *Output Features*: Each algorithm displays output features in table, off table, and through a Gantt chart.
