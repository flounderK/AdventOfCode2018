import re
import string


class Worker:
    ORDER_STRING = ""
    FINISHED_STEPS = set()

    def __init__(self, number):
        self.number = number
        self.working_on = ""
        self.working = False
        self.task_finished_time = 0
        self.time = 0
        self.assignment_log = list()

    def start_work(self, step):
        self.working_on = step
        self.working = True
        self.task_finished_time = self.time + (string.ascii_uppercase.find(step) + 1) + 60
        self.assignment_log.append(step)

    def tick(self):
        self.time += 1
        if self.working is True and self.task_finished_time == self.time:
            self.task_finished_time = 0
            self.working = False
            Worker.FINISHED_STEPS.add(self.working_on)
            Worker.ORDER_STRING += self.working_on
            self.working_on = ""

    def __repr__(self):
        return f"\nNumber: {self.number}\n" \
               f"Working on: {self.working_on}\n" \
               f"Working: {self.working}\n" \
               f"Task finished time: {self.task_finished_time}\n" \
               f"Time: {self.time}"


class WorkerPool:
    def __init__(self, number_of_workers):
        self.max_workers = number_of_workers
        self.elapsed_time = 0
        self.worker_available = True
        self.workers = list()
        self.create_workers()

    def create_workers(self):
        for i in range(1, self.max_workers + 1):
            self.workers.append(Worker(i))

    def find_available_worker(self):
        for i in self.workers:
            if i.working is False:
                return i
        return None

    def assign_work(self, step):
        available_worker = self.find_available_worker()
        if available_worker is None:
            return False
        available_worker.start_work(step)
        return True

    def tick(self):
        available_count = 0
        self.elapsed_time += 1
        for i in self.workers:
            i.tick()
            if i.working is False:
                available_count += 1
        if available_count < 1:
            self.worker_available = False

    def __repr__(self):
        return f"{self.workers}"


with open("Day7In.txt", "r") as f:
    content = [i.replace("\n", "") for i in f.readlines()]

relationships_dependents = dict()
all_steps = set()
for line in content:
    matches = re.match("Step ([A-Z]) must be finished before step ([A-Z]) can begin.", line).groups()
    ind_step, dep_step = matches
    all_steps.add(ind_step)
    all_steps.add(dep_step)
    if relationships_dependents.get(ind_step) is None:
        relationships_dependents[ind_step] = {dep_step}
    else:
        relationships_dependents[ind_step].add(dep_step)

first_steps = set()
for checked_step in relationships_dependents.keys():
    original_step = True
    for step in relationships_dependents.keys():
        if checked_step in relationships_dependents[step]:
            original_step = False

    if original_step is True:
        first_steps.add(checked_step)

last_step = (all_steps - set(relationships_dependents.keys())).pop()

# set up dict to show which steps are needed to be complete before each step starts

dependent_of_relationships = dict()
for checked_step in all_steps:
    dependent_of_relationships[checked_step] = set()
    for step in relationships_dependents.keys():
        if checked_step in relationships_dependents[step]:
            dependent_of_relationships[checked_step].add(step)


current_step = sorted(first_steps)[0]
order_string = current_step
step_options = first_steps.copy()
step_options.remove(current_step)
used_steps = {current_step}
while current_step != last_step:
    step_options = step_options.union(relationships_dependents[current_step]) - used_steps
    for step_option in sorted(step_options):
        prereq_met = True
        for prerequisite_step in dependent_of_relationships[step_option]:
            if prerequisite_step not in used_steps:
                prereq_met = False
                break
        if prereq_met is True:
            current_step = step_option
            break

    step_options.remove(current_step)
    used_steps.add(current_step)
    order_string += current_step


print(f"Part 1: {order_string}")

# Part 2
worker_pool = WorkerPool(5)
current_step = sorted(first_steps)[0]
worker_pool.assign_work(current_step)
step_options = first_steps.copy()
step_options.remove(current_step)
used_steps = set()
assigned_steps = {current_step}
step_options_log = list()
while used_steps != all_steps:
    for worker in worker_pool.workers:
        if worker.working_on != '' and relationships_dependents.get(worker.working_on) is not None:
            step_options = (step_options.union(relationships_dependents[worker.working_on]) -
                            used_steps.union(assigned_steps))

    step_options_log.append(step_options)
    worker_pool.tick()
    used_steps = used_steps.union(Worker.FINISHED_STEPS)
    for step_option in sorted(step_options):
        prereq_met = True
        for prerequisite_step in dependent_of_relationships[step_option]:
            if prerequisite_step not in used_steps:
                prereq_met = False
                break
        if prereq_met is True:
            current_step = step_option
            assigned = worker_pool.assign_work(step_option)
            if assigned is True:
                step_options.remove(step_option)
                assigned_steps.add(step_option)


total_elapsed_time = worker_pool.elapsed_time
# total_elapsed_time = total_elapsed_time + (60*len(Worker.ORDER_STRING))
print("Part 2:")
print(f"Elapsed time: {total_elapsed_time}")
print(Worker.ORDER_STRING)

