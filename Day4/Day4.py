import re
import datetime 


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



