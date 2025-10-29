class Team:
    def __init__(self, code, name):
        self.code =code
        self.name = name
        self.members: list[Member] = []
    def add_member(self, member):
        self.members.append(member)

    def isManagerExperiencedWith(self, experience):
        for member in self.members:
            if isinstance(member, Manager) and member.expertise == experience:
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
    def __init__(self, code = "O", name = "Undefined"):
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
        self.task = []

    def addTask(self, task):
        self.task.append(task)

    def getTasksByProperty(self, name, value):
        matchedTasks = []
        for task in self.task:
            if task.property[name] == value:
                matchedTasks.append(task)
        return matchedTasks

    def getUrgentTasks(self):
        urgentTasks = []
        for task in self.task:
            if task.property["Urgent"]:
                urgentTasks.append(task)
        return urgentTasks

    def getWorkload(self):
        totalHours = 0;
        for task in self.task:
            totalHours += task.getEstimatedHours()
        return totalHours

    def __str__(self):
        print("Name: " + self.name + "Username: " + self.username)



class Manager(Member):
    def __init__(self, name, username):
        """member constructor takes the name and username"""
        Member.__init__(self, name, username)
        self.expertise = []

    def addTask(self, task):
        self.task.append(task)
        for tag in task.tag:
            if tag not in self.expertise:
                self.expertise.append(tag)

    def __str__(self):
        print("Manager Name: " + self.name + "Manager Username: " + self.username)

if __name__ == "__main__":
    task1 = Task("B1", "API Development")
    task1.addTag("backend")
    task1.addTag("urgent")
    task1.addProperty("estimatedhours","20")
    task1.addProperty("priority","medium")


    print((task1.hasProperty("priority","medium")))
    print(task1)