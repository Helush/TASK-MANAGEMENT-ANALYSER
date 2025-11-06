
import sys # Used for reading the input fom command line
import re
import matplotlib.pyplot as plt

class Team:
    def __init__(self, code, name):
        # Team constructor initializes each data member
        self.code = code
        self.name = name
        self.members: list[Member] = []

    def add_member(self, member):
        # Adds a new member to the Team
        self.members.append(member)

    def isManagerExperiencedWith(self, expertise):
        for member in self.members: # Checks if the member is a Manager and whether that manager has the expertise
            if isinstance(member, Manager) and member.expertise == expertise:
                return True
        return False

    def getUrgentTasks(self):
        # Method that returns all the urgent tasks in a Team
        urgent_tasks = []
        for member in self.members: # Added all urgent tasks from all the members
            urgent_tasks.extend(member.getUrgentTasks())
        return urgent_tasks

    def getWorkload(self):
        # Method that returns the total workload (hours) in a team
        total_workload = 0
        for member in self.members: # Adding the total estimated hours of all tasks assigned to this each member
            total_workload += member.getWorkload()
        return total_workload

    def getBusiestMember(self):
        # Method that returns the busiest team member of the team
        busiest_member = None
        max_hours = 0
        for member in self.members:
            workload = member.getWorkload()
            if workload > max_hours: # Comparing the workload of each team member
                max_hours = workload
                busiest_member = member # Assigning member was the max_hours as the busiest member
        return busiest_member

    def getTasksByProperty(self, name, value):
        # Returns a list of tasks assigned to this team, which contains the given name and value
        all_tasks = []
        for member in self.members:
            all_tasks += member.getTasksByProperty(name, value)
        return all_tasks

class Task:
    def __init__(self, code = "0", name = "Undefined"):
        # Task constructor initializes code, name, tags and properties
        self.code = code
        self.name = name
        self.tags = []
        self.properties = {}

    def addTag(self, tag):
        # Adds a new tag to the list
        self.tags.append(tag)

    def addProperty(self, name, value):
        # Method to add a new property to the dictionary
        self.properties[name] = value

    def getEstimatedHours(self):
        # Returns the estimated hours of a given task
        return int(self.properties["estimatedhours"])

    def isUrgent(self):
        # Method that determines whether a tag is urgent or not
        for tag in self.tags:
            if tag == "urgent":
                return True
        return False

    def hasProperty(self, name, value):
        # Method that checks whether a task has a given property with the given name and value
        if name in self.properties:
            if self.properties[name]== value:
                return True
        return False

    def __str__(self):
        # Return the Task object formatted as in the example:
        # [V1] Set up CICD pipeline  #devops  #estimatedhours:18  #complexity:high
        result = f"[{self.code}] {self.name}"

        # Append tags in the form #tag
        if self.tags:
            result += "  " + " ".join(f"#{tag}" for tag in self.tags)

        # Append properties in the form #name:value
        if self.properties:
            result += "  " + " ".join(f"#{name}:{value}" for name, value in self.properties.items())

        return result



class Member:
    def __init__(self, name, username):
        # Initializes the name, username, tasks of a Member
        self.name = name
        self.username = username
        self.task: list[Task] = []

    def addTask(self, task):
        # Appends a new task
        self.task.append(task)

    def getTasksByProperty(self, name, value):
        # Returns all the tasks that contains the given property name and value
        matched_tasks = []
        for task in self.task:
            if task.hasProperty(name, value):
                matched_tasks.append(task) # Appends matching tasks with the given property name and value
        return matched_tasks

    def getUrgentTasks(self):
        # Returns a list of tasks assigned to this member that are tagged as urgent
        urgent_tasks = []
        for task in self.task:
            if task.isUrgent():  # isUrgent() checks whether the task has the "urgent" tag
                urgent_tasks.append(task)
        return urgent_tasks

    def getWorkload(self):
        # Returns the total estimated workload assigned to each member
        total_hours = 0
        for task in self.task:
            total_hours += task.getEstimatedHours() # getEstimatedHours() returns the estimated workload for each task
        return total_hours

    def __str__(self):
        # Returns the string representation of Member
        return "{} <{}>".format(self.name, self.username)


class Manager(Member):
    def __init__(self, name, username):
        # Initializes each data member of Manager
        # Member constructor takes the name and username
        Member.__init__(self, name, username)
        self.expertise = []

    def addTask(self, task):
        # Appends a new task for manager
        self.task.append(task)
        for tag in task.tags: # Updating their expertise with the tags of the task
            if tag not in self.expertise:
                self.expertise.append(tag)

    def __str__(self):
        # Returns the string representation of Manager
        return "{} <{}>".format(self.name, self.username)

def printManagersByExpertise(teams): # option 1 in menu
    expertise = input("Enter expertise to search for: ").strip().lower() # Ask user to give the expertise to search
    found = False
    for team in teams: # Look for each team
        for member in team.members: # Look for each member in team
            if isinstance(member, Manager) and expertise in member.expertise: # If the member is manager and expertise matches
                found = True # Found the matching Manager with expertise
                print(f"\nManager: {member}") # Print manager information along with expertises and all tasks assigned to that manager
                print(f"Expertise: {', '.join(member.expertise)}")
                for t in member.task:
                    print("   -", t)

    if not found:
        print("\nNo manager found with expertise:", expertise)

def printUrgentTasks(teams): # option 2 in menu
    for team in teams:
        if team.getUrgentTasks(): # Gets urgent task(s) of each team
            print(team.name+":", end="\n") # Prints team's name along with urgent task(s)
            for t in team.getUrgentTasks():
                print(" ", t, end="\n\n")
        else:
            print("No urgent tasks for Team " + team.name, end="\n\n")


def printTeamWorkloads(teams): #option 3 in menu
    team_names = []
    team_workloads = []
    for team in teams: # Get workloads for each team and store workloads and teams accordingly
        workload = team.getWorkload()
        if workload != 0: # Only the teams with workloads > 0 will be displayed
            team_names.append(team.name)
            team_workloads.append(workload)
    plt.pie(team_workloads, labels=team_names) # Creates the pie chart, gives it a title
    plt.title('Team Workloads')
    plt.show()


def printBusiestMembers(teams): # Option 4 in menu
    for team in teams: # gets busiest member in each team
        busy_member = team.getBusiestMember()
        if busy_member: # if team has found the busiest member. Print team name, member's information,
            print(team.name + ":", end="\n")
            print(busy_member)
            if isinstance(busy_member, Manager): # if the member is manager, print expertise as well
                print("Expertise: ", end="")
                print(','.join(busy_member.expertise))
            for task in busy_member.task: # print each task of the busy member
                print(task)
            print("\n")

        else:
            print("No busy members in team " + team.name, end="\n\n")



def printTasksByProperty(teams, name, value): # Option 5 in menu
    for team in teams: # get tasks by their name and value
        tasks = team.getTasksByProperty(name, value)
        if len(tasks) != 0: # if task found
            print(f"\n{team.name}:")
            for task in tasks:
                print(" ", task)
            print("\n")
        else:
            print(f"No such tasks in team {team.name}", end="\n")


def loadData(filename = sys.argv[1]):
    try: # Attempt to open the file, handling the error by throwing an exception
        file = open(filename, "r")
    except IOError:
        print("File could not be opened")
        exit(1)

    records = file.readlines() # Read all lines and store them for processing
    # Creating object lists
    teams = []
    members = []
    managers = []
    tasks = []
    current_team = None # Keeps track of the team currently being processed

    for record in records: # Loop through every line to handle blank lines and new lines to get clean records
        record = record.strip()
        if not record:
            continue  # skip empty lines

        # Pattern matching for different record types
        member_match = re.match(r"^([\w\s]+)\s+<(\w+)>$", record) # Matches members with the format fullname, <username>
        manager_match = re.match(r"^([\w\s]+)\s+<!(\w+)>$", record) # Matches managers with the format fullname, <!username>
        team_match = re.match(r"^([\w\s]+)\s+<(\w+)>\s*->\s*([\w,]+)$", record) # Matches teams with the format [Team Name] <[team_code]> -> username1, username2 ...
        task_match = re.match(r"^\[(\w+)]\s*([\w\s]+)\s+@\s*(\w+)\s*((?:#\S+\s*)*)$", record) # Matches tasks with the format [[taskCode]] taskName @ username #propertyOrTag1 #propertyOrTag2 ...

        if team_match: # If the current line is matching team, capture necessary information and create a new team object
            team_name, team_code, usernames_str = team_match.groups()
            current_team = Team(team_code, team_name)
            # Add members/managers to this team if their usernames match
            for uname in usernames_str.split(","):
                uname = uname.strip()
                for m in members + managers:
                    if m.username == uname:
                        current_team.add_member(m)
            teams.append(current_team) # store the team in teams list

        # Create member
        elif member_match:
            fullName, username = member_match.groups()
            member = Member(fullName.strip(), username)
            members.append(member)
            if current_team:
                current_team.add_member(member)

        # Create manager
        elif manager_match:
            fullName, username = manager_match.groups()
            manager = Manager(fullName, username)
            managers.append(manager)
            if current_team:
                current_team.add_member(manager)

        # Create task and assign it
        elif task_match:
            task_code, task_name, assigned_user, tags = task_match.groups()
            task = Task(task_code.strip(), task_name.strip())

            if tags:
            # Extract all tags after '#', ignore empties, and strip whitespace
                tags_list = [t.strip() for t in tags.split('#') if t.strip()]
                for tag in tags_list:
                    if ':' in tag: # Property (name:value)
                        name, value = tag.split(':', 1)
                        task.addProperty(name, value)
                    else:
                        task.addTag(tag)
            for m in members + managers: # assigns task to the correct person
                    if m.username == assigned_user:
                        m.addTask(task)

    file.close() # Close the file
    print("Data loaded successfully.")
    return teams

# Start of the program execution
if __name__ == "__main__":
    teams = loadData()
    while True: # Menu loop
        print("\nMenu Options:\n1. Print Manager by Expertise\n2. Print Urgent Tasks\n3. Print Team Workloads\n4. Print Busiest Members\n5. Print Tasks by Property\n0. Exit\n")
        option = input("Enter your choice: ")
        match option:
            case "1": # Displays the full details of managers in the system which have specified expertise by user
                printManagersByExpertise(teams)
            case "2": # Prints the details of all tasks which are tagged urgent for each team
                printUrgentTasks(teams)
            case "3": # Displays a pie chart showing the workload in estimated hours for each team in system
                printTeamWorkloads(teams)
            case "4": # Prints the team member with the highest workload in estimated hours for each team
                printBusiestMembers(teams)
            case "5": # Prints the team name and all tasks assigned to that team which contain that specified property with the specified value given by user for each team
                property_name = input("Enter property name: ").strip().lower()
                property_value = input("Enter property value: ").strip().lower()
                printTasksByProperty(teams, property_name, property_value)
            case "0": # Exit case
                print("Exiting.")
                break
            case _: # Error handling for invalid menu option
                print("Invalid Option. Try again.")

