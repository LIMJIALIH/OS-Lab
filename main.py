# Create a function to implement the First-Come, First-Served (FCFS) scheduling algorithm.
# The function should take a list of jobs and their corresponding burst times as input
def FCFS(jobs, burst_time):
    n = len(jobs)
    start_time = [0] * n
    waiting_time = [0] * n
    turnaround_time = [0] * n
    completion_time = [0] * n
    # create arrays to store start time, waiting time, turnaround time, and completion time for each job

    # initialize the first job's start time, waiting time, completion time, and turnaround time
    start_time[0] = 0
    waiting_time[0] = 0
    completion_time[0] = burst_time[0]
    turnaround_time[0] = burst_time[0]

    # calculate start time, waiting time, completion time, and turnaround time for each subsequent job
    for i in range(1, n):
        start_time[i] = completion_time[i-1]
        completion_time[i] = start_time[i] + burst_time[i]
        turnaround_time[i] = completion_time[i]
        waiting_time[i] = turnaround_time[i] - burst_time[i]

    # print the results in a tabular format
    print(f"{'Job':<10}{'Burst':<10}{'Start':<10}{'Completion':<15}{'Waiting':<10}{'Turnaround':<15}")
    print("-" * 70)

    for i in range(n):
        print(f"{jobs[i]:<10}{burst_time[i]:<10}{start_time[i]:<10}{completion_time[i]:<15}{waiting_time[i]:<10}{turnaround_time[i]:<15}")

    average_waiting_time = sum(waiting_time) / n
    average_turnaround_time = sum(turnaround_time) / n
    print(f"Average Waiting Time: {average_waiting_time:.2f}")
    print(f"Average Turnaround Time: {average_turnaround_time:.2f}")

def main():
    # prompt the user to enter job names and their corresponding burst times until they indicate they are done
    jobs = []
    burst_time = []
    while True:
        job = input("Enter job name ('done' to finish):")
        if job.lower() == 'done':
            break
        jobs.append(job)
        burst = int(input("Enter burst time for the job:"))
        while burst < 0:
            print("Burst time cannot be negative. Please enter a valid burst time.")
            burst = int(input("Enter burst time for the job:"))
        burst_time.append(burst)

    FCFS(jobs,burst_time)

if __name__ == "__main__":
    main()