
import sys
import re
import matplotlib.pyplot as plt

class Team:
    def __init__(self, code, name):
        self.code = code
        self.name = name
        self.members: list[Member] = []

    def add_member(self, member):
        self.members.append(member)

    def isManagerExperiencedWith(self, expertise):
        for member in self.members:
            if isinstance(member, Manager) and member.expertise == expertise:
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
        return int(self.properties["estimatedhours"])

    def isUrgent(self):
        for tag in self.tags:
            if tag == "urgent":
                return True
        return False

    def hasProperty(self, name, value):
        if name in self.properties:
            if self.properties[name]== value:
                return True
        return False

    def __str__(self):
        result = f"[{self.code}] {self.name}"

        if self.tags:
            result += "  " + " ".join(f"#{tag}" for tag in self.tags)

        # Add properties (as name:value)
        if self.properties:
            result += "  " + " ".join(f"#{name}:{value}" for name, value in self.properties.items())


        return result


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
            if task.hasProperty(name, value):
                matched_tasks.append(task)
        return matched_tasks

    def getUrgentTasks(self):
        urgent_tasks = []
        for task in self.task:
            if task.isUrgent():
                urgent_tasks.append(task)
        return urgent_tasks

    def getWorkload(self):
        total_hours = 0
        for task in self.task:
            total_hours += task.getEstimatedHours()
        return total_hours

    def __str__(self):
        return "{} <{}>".format(self.name, self.username)


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
        return "{} <{}>".format(self.name, self.username)

def printManagersByExpertise(teams): # option 1 in menu
    expertise = input("Enter expertise to search for: ").strip().lower()
    found = False
    for team in teams:
        for member in team.members:
            if isinstance(member, Manager) and expertise in member.expertise:
                found = True
                print(f"\nManager: {member}")
                print(f"Expertise: {', '.join(member.expertise)}")
                for t in member.task:
                    print("   -", t)

    if not found:
        print("\nNo manager found with expertise:", expertise)

def printUrgentTasks(teams): # option 2 in menu
    for team in teams:
        if team.getUrgentTasks():
            print(team.name+":", end="\n")
            for t in team.getUrgentTasks():
                print(" ", t, end="\n\n")
        else:
            print("No urgent tasks for Team " + team.name, end="\n\n")


def printTeamWorkloads(teams): #option 3 in menu
    team_names = []
    team_workloads = []
    for team in teams:
        workload = team.getWorkload()
        if workload != 0:
            team_names.append(team.name)
            team_workloads.append(workload)
    plt.pie(team_workloads, labels=team_names)
    plt.title('Team Workloads')
    plt.show()


def printBusiestMembers(teams):
    for team in teams:
        busy_member = team.getBusiestMember()
        if busy_member:
            print(team.name + ":", end="\n")
            print(busy_member)
            if isinstance(busy_member, Manager):
                print("Expertise: ", end="")
                print(','.join(busy_member.expertise))
            for task in busy_member.task:
                print(task)
            print("\n")

        else:
            print("No busy members in team " + team.name, end="\n\n")



def printTasksByProperty(teams, name, value): # option 5 in menu
    for team in teams:
        tasks = team.getTasksByProperty(name, value)
        if len(tasks) != 0:
            print(f"\n{team.name}:")
            for task in tasks:
                print(" ", task)
            print("\n")
        else:
            print(f"No such tasks in team {team.name}", end="\n")


if __name__ == "__main__":
    filename = sys.argv[1]
    try:
        file = open(filename, "r")
    except IOError:
        print("File could not be opened")
        exit(1)

    print("\n\n")
    for i in range (len(sys.argv)):
       print("argument %s" %sys.argv[i])

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

    print("Data loaded successfully.")
    while True: #menu loop
        print("\nMenu Options:\n1. Print Manager by Expertise\n2. Print Urgent Tasks\n3. Print Team Workloads\n4. Print Busiest Members\n5. Print Tasks by Property\n0. Exit\n")
        option = input("Enter your choice: ")
        match option:
            case "1":
                printManagersByExpertise(teams)
            case "2":
                printUrgentTasks(teams)
            case "3":
                printTeamWorkloads(teams)
            case "4":
                printBusiestMembers(teams)
            case "5":
                property_name = input("Enter property name: ").lower()
                property_value = input("Enter property value: ").lower()
                printTasksByProperty(teams, property_name, property_value)
            case "0":
                print("Exiting.")
                break
            case _:
                print("Invalid Option. Try again.")

