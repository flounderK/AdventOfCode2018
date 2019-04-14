import re

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


print(order_string)

