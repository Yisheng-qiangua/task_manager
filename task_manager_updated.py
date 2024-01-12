# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

class File:

    def __init__(self, filename):
        self.filename = filename

    def create(self, contents=""):
        """Create a file if it doesn't exist."""
        if not os.path.exists(self.filename):
            self._write(contents)
    
    def _read(self, filename):
        with open(filename, "r") as file:
            return file.read().split("\n")
        
    def _write(self, contents):
        with open(self.filename, "a") as file:
            return file.write(f"\n{contents}")
        
    def get_users(self):
        """Get users' details such as username and password from the file."""
        users = {}
        for item in self._read("user.txt"):
            username, password = item.split(';')
            users[username] = password
        return users

class User(File):

    def log_in(self):
        """Log in users using username and password"""

        logged_in = False
        while not logged_in:
            print("***LOGIN***")
            current_user = input("Username: ").strip()
            current_password = input("Password: ").strip()
            if current_user not in super().get_users().keys():
                print(f"{'-'*20}")
                print("User does not exist!")
                print(f"{'-'*20}")
                continue
            elif super().get_users()[current_user] != current_password:
                print("Wrong password!")
                continue
            else:
                print()
                print("Login successful!")
                logged_in = True
        return current_user

    def register(self):
        '''Register a new user to the 'user.txt' file.'''

        isExisting = False
        while not isExisting:
            new_username = input("New Username: ")
            if new_username in super().get_users().keys():
                print("The username is already in use and please enter another username!")
                continue
            else:
                isExisting = True

        new_password = input("New Password: ")

        users = {}
        isConfirmed = False
        while not isConfirmed:
            confirm_password = input("Confirm Password: ")
            if confirm_password != new_password:
                print("**Passwords do not match! Please re-enter to confirm password.**")
                continue
            else:
                print()
                print("New user is registered successfully!")
                users[new_username] = new_password

                user_file = []
                for key in users:
                    user_file.append(f"{key};{users[key]}")
                super()._write("\n".join(user_file))
                
                isConfirmed = True


class Task(File):

    def get_task(self):
        tasks = []
        read_tasks = [item for item in super()._read("tasks.txt") if item != ""]
        for item in read_tasks:
            task = {}
            task['username'] = item.split(";")[0]
            task['title'] = item.split(";")[1]
            task['description'] = item.split(";")[2]
            task['due_date'] = f"{datetime.strptime(item.split(';')[3], DATETIME_STRING_FORMAT)}"
            task['assigned_date'] = f"{datetime.strptime(item.split(';')[4], DATETIME_STRING_FORMAT)}"
            task['completed'] = True if item.split(";")[5] == "Yes" else False
            
            tasks.append(task)
        return tasks
    
    def add_task(self):

        while True:
            assigned_user = input("Name of person assigned to task: ")
            if assigned_user not in super().get_users().keys():
                print("User does not exist. Please enter a valid username!")
                continue
            else:
                break
        
        title = input("Title of Task: ")
        description = input("Description of Task: ")

        while True:
            try:
                task_due = input("Due date of task (YYYY-MM-DD): ")
                due_date = datetime.strptime(task_due, DATETIME_STRING_FORMAT)
                break
            except ValueError:
                print("Invalid datetime format. Please use the format specified")
        
        _tasks = []
        new_task = {
            "username": assigned_user,
            "title": title,
            "description": description,
            "due_date": due_date,
            "assigned_date": date.today(),
            "completed": False
        }

        _tasks.append(new_task)

        task_to_write = []
        for task in _tasks:
            task_content = [
                task['username'],
                task['title'],
                task['description'],
                str(task['due_date']).split()[0],
                str(task['assigned_date']).split()[0],
                "Yes" if task['completed'] else "No"
            ]
            task_to_write.append(";".join(task_content))
        super()._write("\n".join(task_to_write))
        print("Task successfully added.")
        return _tasks

    def view_task(self, tasks):
        for task in tasks:
            print()
            display = f"{'-'*60}\n"
            display += f"Task: \t\t\t {task['title']}\n"
            display += f"Assigned to: \t\t {task['username']}\n"
            display += f"Date Assigned: \t\t {task['assigned_date']}\n" # 
            display += f"Due Date: \t\t {task['due_date']}\n" 
            display += f"Take Complete?: \t\t {task['completed']}\n"
            display += f"Task Description: \n   {task['description']}\n"
            display += f"{'-'*60}\n"
            print(f"{display}")

if __name__ == '__main__':

    task_file = File("tasks.txt")
    task_file.create()
    
    task = Task("tasks.txt")
    tasks = task.get_task()

    #====Login Section====
    '''This code reads usernames and password from the user.txt file to 
        allow a user to login.
    '''
    user_file = File("user.txt")
    user_file.create("admin;password")

    user = User("user.txt")
    current_user = user.log_in()

    while True:
        # presenting the menu to the user and 
        # making sure that the user input is converted to lower case.
        print()
        menu = input('''Select one of the following Options below:
    r  - Register a user
    a  - Add a task
    va - View all tasks
    vm - View my task
    ds - Display statistics
    e  - Exit
    ::>>> ''').lower()
        
        match menu:

            case "r":
                user.register()
            
            case "a":
                task.add_task()

            case "va":
                task.view_task(tasks)

            case "vm":
                count = 0
                for task in tasks:
                    count += 1
                    if task['username'] == current_user:
                        print()
                        display = f"{'-'*60}\n"
                        display += f"Task({count}): \t\t {task['title']}\n"
                        display += f"Assigned to: \t\t {task['username']}\n"
                        display += f"Date Assigned: \t\t {task['assigned_date']}\n"
                        display += f"Due Date: \t\t {task['due_date']}\n"
                        display += f"Take Complete?: \t\t {task['completed']}\n"
                        display += f"Task Description: \n   {task['description']}\n"
                        display += f"{'-'*60}\n"
                        print(f"{display}")

            case "ds":
                if current_user == "admin":
                    print("-----------------------------------")
                    print(f"Number of users: \t\t {len(user.get_users().keys())}")
                    print(f"Number of tasks: \t\t {len(tasks)}")
                    print("-----------------------------------") 
            
            case "e":
                print(f"{'-'*10}")
                print('Goodbye!!!')
                print(f"{'-'*10}")
                exit()

            case _:
                print("You have made a wrong choice. Please try again!")

        