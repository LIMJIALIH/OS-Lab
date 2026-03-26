class Job:
    def __init__(self,name, order):
        self.name = name
        self.burst_time = 0
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0
        self.order = order

    def __lt__(self, other):
        if self.burst_time == other.burst_time:
            return self.order < other.order
        return self.burst_time < other.burst_time

def main():
    no_jobs = int(input("Enter the number of jobs:"))
    jobs = [Job(i+1, i) for i in range(no_jobs)]

    for job in jobs:
        job.burst_time = int(input(f"Enter burst time for job {job.name}:"))

    # Sort jobs based on burst time
    jobs.sort()  # This will use the __lt__ method defined in the Job class to sort by burst time and then by order

    jobs_order = []
    current_time = 0
    total_turnaroundTime = 0
    total_waitingTime = 0

    for job in jobs:

        current_job = job
        current_job.completion_time = current_time + current_job.burst_time
        current_job.turnaround_time = current_job.completion_time
        current_job.waiting_time = current_job.turnaround_time - current_job.burst_time

        total_turnaroundTime += current_job.turnaround_time
        total_waitingTime += current_job.waiting_time

        current_time = current_job.completion_time
        jobs_order.append(current_job)

    print("\n{:<6}{:<15}{:<18}{:<15}{:<18}".format(
        "Job", "Burst Time", "Completion Time", "Waiting Time", "Turnaround Time"
    ))

    for job in jobs_order:
        print("{:<6}{:<15}{:<18}{:<15}{:<18}".format(
            job.name,
            job.burst_time,
            job.completion_time,
            job.waiting_time,
            job.turnaround_time
        ))
    print(f"\nAverage Waiting Time: {total_waitingTime/no_jobs:.2f}")
    print(f"Average Turnaround Time: {total_turnaroundTime/no_jobs:.2f}")

if __name__ == "__main__":
    main()