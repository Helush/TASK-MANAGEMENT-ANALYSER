
import sys
import re

class Team:
    def __init__(self, code, name):
        self.code = code
        self.name = name
        self.members: list[Member] = []

    def add_member(self, member):
        self.members.append(member)

    def isManagerExperiencedWith(self, expertise):
        for member in self.members:
            if isinstance(member, Manager) and member.expertise == expertise: #do we need to check instance since manager is already a member?
                return True
        return False

    def getUrgentTasks(self):
        urgent_tasks = []
        for member in self.members:
            urgent_tasks.extend(member.getUrgentTasks())
        return urgent_tasks

    def getWorkload(self):
        total_workload = 0
        for member in self.members:
            total_workload += member.getWorkload()
        return total_workload

    def getBusiestMember(self):
        busiest_member = None
        max_hours = 0
        for member in self.members:
            workload = member.getWorkload()
            if workload > max_hours:
                max_hours = workload
                busiest_member = member
        return busiest_member

    def getTasksByProperty(self, name, value):
        all_tasks = []
        for member in self.members:
            all_tasks += member.getTasksByProperty(name, value)
        return all_tasks

class Task:
    def __init__(self, code = "0", name = "Undefined"):
        self.code = code
        self.name = name
        self.tags = []
        self.properties = {}

    def addTag(self, tag):
        self.tags.append(tag)

    def addProperty(self, name, value):
        self.properties[name] = value

    def getEstimatedHours(self):
        return self.properties["estimatedhours"]

    def isUrgent(self):
        for tag in self.tags:
            if tag == "urgent":
                return True
        return False

    def hasProperty(self, name, value):
        if self.properties[name]== value:
                return True
        return False

    def __str__(self):
        return "code: {}, name: {}, tags: {}, properties: {}".format(self.code, self.name, self.tags, self.properties)


class Member:
    def __init__(self, name, username):
        self.name = name
        self.username = username
        self.task: list[Task] = []

    def addTask(self, task):
        self.task.append(task)

    def getTasksByProperty(self, name, value):
        matched_tasks = []
        for task in self.task:
            if task.properties[name] == value:
                matched_tasks.append(task)
        return matched_tasks

    def getUrgentTasks(self):
        urgent_tasks = []
        for task in self.task:
            if task.properties["Urgent"]:
                urgent_tasks.append(task)
        return urgent_tasks

    def getWorkload(self):
        total_hours = 0
        for task in self.task:
            total_hours += task.getEstimatedHours()
        return total_hours

    def __str__(self):
        return "Name: {} Username: {}".format(self.name, self.username)



class Manager(Member):
    def __init__(self, name, username):
        """member constructor takes the name and username"""
        Member.__init__(self, name, username)
        self.expertise = []

    def addTask(self, task):
        self.task.append(task)
        for tag in task.tags:
            if tag not in self.expertise:
                self.expertise.append(tag)

    def __str__(self):
        return "Manager Name: {} Manager Username: {}".format(self.name, self.username)


if __name__ == "__main__":
    try:
        file = open("data.txt", "r")
    except IOError:
        print("File could not be opened")
        exit(1)

    records = file.readlines()

    teams = []
    members = []
    managers = []
    tasks = []
    current_team = None

    for record in records:
        record = record.strip()
        if not record:
            continue  # skip empty lines

        member_match = re.match(r"^([\w\s]+)\s+<(\w+)>$", record)
        manager_match = re.match(r"^([\w\s]+)\s+<!(\w+)>$", record)
        team_match = re.match(r"^([\w\s]+)\s+<(\w+)>\s*->\s*([\w,]+)$", record)
        # [B1]API Development @ jdoe  # estimatedhours:20 #priority:high #backend #urgent
        task_match = re.match(r"^\[(\w+)]\s*([\w\s]+)\s+@\s*(\w+)\s*((?:#\S+\s*)*)$", record)

        if team_match:
            team_name, team_code, usernames_str = team_match.groups()
            current_team = Team(team_code, team_name)

            for uname in usernames_str.split(","):
                uname = uname.strip()
                for m in members + managers:
                    if m.username == uname:
                        current_team.add_member(m)
            teams.append(current_team)

        elif member_match:
            fullName, username = member_match.groups()
            member = Member(fullName.strip(), username)
            members.append(member)
            if current_team:
                current_team.add_member(member)

        elif manager_match:
            fullName, username = manager_match.groups()
            manager = Manager(fullName, username)
            managers.append(manager)
            if current_team:
                current_team.add_member(manager)

        elif task_match:
            task_code, task_name, assigned_user, tags = task_match.groups()
            task = Task(task_code.strip(), task_name.strip())

            if tags:
            # Extract all tags after '#', ignore empties, and strip whitespace
                tags_list = [t.strip() for t in tags.split('#') if t.strip()]
                for tag in tags_list:
                    if ':' in tag:
                        name, value = tag.split(':', 1)
                        task.addProperty(name, value)
                    else:
                        task.addTag(tag)
            for m in members + managers:
                    if m.username == assigned_user:
                        m.addTask(task)


    file.close()
    for team in teams:
        print(f"Team: {team.name}")
        for member in team.members:
            print(f"  Member: {member.username}")
            for task in member.task:
                print(f"    Task: {task}")
    while True: #menu loop
        print("Menu Options:\n1. Print Manager by Expertise\n2. Print Urgent Tasks\n3. Print Team Workloads\n4. Print Busiest Members\n5. Print Tasks by Property\n0. Exit\n")
        option = input("Enter your choice: ")
        match option:
            case "1":
                print("Print Manager by Expertise")
            case "2":
                print("Print Urgent Tasks")
            case "3":
                print("Print Team Workloads")
            case "4":
                print("Print Busiest Members")
            case "5":
                print("Print Tasks by Property")
            case "0":
                print("Exiting...")
                break
            case _:
                print("Invalid Option")

