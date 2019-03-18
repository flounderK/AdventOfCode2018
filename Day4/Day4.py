import re
import datetime 
import math

class record:
    def __init__(self, record_string):
        match = re.match(r"\[(.+)\] (.+)", 
                         record_string)
        self.datetime = datetime.datetime.strptime(match.groups()[0], 
                                                   "%Y-%m-%d %H:%M")
        self.action = match.groups()[1]
        self.record = record_string

    def __repr__(self):
        return self.record 


class guard:
    def __init__(self, number):
        self.number = number
        self.sleep_lengths = list()
        self.records = list()
        self.average_sleep_length = None
        self.total_sleep_minutes = 0
        # only minute matters, not hour
        self.minutes_spent_asleep = dict()

    def get_minutes_of_sleep(self, start, duration_delta):
        """takes in datetime objects"""
        duration_minutes = duration_delta.seconds / 60
        for minute in range(0, math.floor(duration_minutes)):
            minute_asleep = (start + datetime.timedelta(minutes=minute)).minute
            if self.minutes_spent_asleep.get(minute_asleep) is None:
                self.minutes_spent_asleep[minute_asleep] = 1
            else:
                self.minutes_spent_asleep[minute_asleep] += 1

    def collect_sleep_data(self):
        sleep_start = None
        sleep_end = None
        for rec in self.records:
            if rec.action == "falls asleep":
                sleep_start = rec.datetime
            if rec.action == "wakes up":
                sleep_end = rec.datetime
            if sleep_start is not None and sleep_end is not None:
                self.sleep_lengths.append(sleep_end - sleep_start)
                self.get_minutes_of_sleep(sleep_start, (sleep_end - sleep_start))
                sleep_start = None
                sleep_end = None
        
        for sleep_length in self.sleep_lengths:
            self.total_sleep_minutes += (sleep_length.seconds / 60)
        if len(self.sleep_lengths) > 0: 
            self.average_sleep_length = self.total_sleep_minutes / len(self.sleep_lengths)
        else:
            self.average_sleep_length = 0

    def __repr__(self):
        return self.number


with open("Day4In.txt", "r") as f:
    content = [i.replace("\n", "") for i in f.readlines()]


records = [record(i) for i in content]

records.sort(key=lambda x: x.datetime)

guards = dict()
guard_number = 0
for rec in records:
    action_match = re.match(r"Guard #(\d+) begins shift", rec.action)
    if action_match:
        guard_number = action_match.groups()[0]
    if guards.get(guard_number) is None:
        guards[guard_number] = guard(guard_number)
    guards[guard_number].records.append(rec)

for key in guards.keys():
    guards[key].collect_sleep_data()


best_guard_no_choice = 0
greatest_total_sleep = 0
for guard in guards.keys():
    if guards[guard].total_sleep_minutes > greatest_total_sleep:
        greatest_total_sleep = guards[guard].total_sleep_minutes
        best_guard_no_choice = guards[guard]

print(f"Guard number: {best_guard_no_choice}")

best_minute_choice = 0
highest_sleep_count = 0
for minute in guards[best_guard_no_choice.number].minutes_spent_asleep.keys():
    current_minute_count = guards[best_guard_no_choice.number].minutes_spent_asleep[minute]
    if current_minute_count > highest_sleep_count:
        best_minute_choice = minute
        highest_sleep_count = current_minute_count


print(f"Best minute: {best_minute_choice}")
answer = best_minute_choice * int(best_guard_no_choice.number)
print(f"Answer: {best_guard_no_choice.number} x {best_minute_choice} = {answer}")

