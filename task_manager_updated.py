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
            print()
            print("***LOGIN***")
            current_user = input("Username: ").strip()
            current_password = input("Password: ").strip()
            if current_user not in super().get_users().keys():
                print(f"{'-'*20}")
                print("User does not exist!")
                print(f"{'-'*20}")
                continue
            elif super().get_users()[current_user] != current_password:
                print(f"{'-'*20}")
                print("Wrong password!")
                print(f"{'-'*20}")
                continue
            else:
                print(f"{'-'*20}")
                print("Login successful!")
                print(f"{'-'*20}")
                logged_in = True
        return current_user

    def register(self):
        '''Register a new user to the 'user.txt' file.'''

        isExisting = False
        while not isExisting:
            new_username = input("New Username: ")
            if new_username in super().get_users().keys():
                print(f"{'-'*20}")
                print("The username is already in use and please enter another username!")
                print(f"{'-'*20}")
                continue
            else:
                isExisting = True

        new_password = input("New Password: ")

        users = {}
        isConfirmed = False
        while not isConfirmed:
            confirm_password = input("Confirm Password: ")
            if confirm_password != new_password:
                print(f"{'-'*20}")
                print("Passwords do not match! Please re-enter password.")
                print(f"{'-'*20}")
                continue
            else:
                print(f"{'-'*20}")
                print("New user is registered successfully!")
                print(f"{'-'*20}")
                users[new_username] = new_password

                user_file = []
                for key in users:
                    user_file.append(f"{key};{users[key]}")
                super()._write("\n".join(user_file))
                
                isConfirmed = True


class Task(File):

    has_been_completed = False

    def mark_as_completed(self):
        self.has_been_completed = True

    def get_task(self):
        _tasks = []
        read_tasks = [item for item in super()._read("tasks.txt") if item != ""]
        for item in read_tasks:
            task = {}
            task['username'] = item.split(";")[0]
            task['title'] = item.split(";")[1]
            task['description'] = item.split(";")[2]
            task['due_date'] = datetime.strptime(item.split(';')[3], DATETIME_STRING_FORMAT)
            task['assigned_date'] = datetime.strptime(item.split(';')[4], DATETIME_STRING_FORMAT)
            task['completed'] = True if item.split(";")[5] == "Yes" else False
            
            _tasks.append(task)
        return _tasks
    
    def add_task(self):
        """Add the tasks into the file"""

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
                print(f"{'-'*20}")
                print("Invalid datetime format. Please use the format specified")
                print(f"{'-'*20}")
        
        # Add the tasks into a list.
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
        
        # Write the tasks into the file.
        task_to_write = []
        for task in _tasks:
            task_content = [
                task['username'],
                task['title'],
                task['description'],
                task['due_date'].strftime(DATETIME_STRING_FORMAT), 
                task['assigned_date'].strftime(DATETIME_STRING_FORMAT), 
                "Yes" if task['completed'] else "No"
            ]
            task_to_write.append(";".join(task_content))
        super()._write("\n".join(task_to_write))
        print("Task successfully added.")
        return task_to_write

    def view_all(self, tasks):
        for task in tasks:
            print()
            display = f"{'-'*60}\n"
            display += f"Task: \t{task['title']}\n"
            display += f"Assigned to: \t{task['username']}\n"
            display += f"Date Assigned: \t {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"  
            display += f"Due Date: \t {task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n" 
            display += f"Take Complete?: \t {task['completed']}\n"
            display += f"Task Description: \n   {task['description']}\n"
            display += f"{'-'*60}\n"
            print(f"{display}")

    def view_mine(self, tasks, curr_user):
        count = 0
        for task in tasks:

            # Using 'count' as a number to identify the task
            count += 1
            if task['username'] == curr_user:
                print()
                display = ""
                display += f"Task Number(#): {str(count)}\n"
                display += f"{'-'*60}\n"
                display += f"Task: \t {task['title']}\n"
                display += f"Assigned to: \t {task['username']}\n"
                display += f"Date Assigned: \t {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"  
                display += f"Due Date: \t {task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n" 
                display += f"Take Complete?: \t {task['completed']}\n"
                display += f"Task Description: \n   {task['description']}\n"
                display += f"{'-'*60}\n"
                print(f"{display}")


if __name__ == '__main__':
    
    # with open("tasks.txt", "r") as file:
    #     contents = file.readlines()
    # print(contents[0])
    # print(contents[0].split(";"))

    # #print(contents[0].split(";")[5])
    # print(contents[0].split(";")[5].strip("\n").replace("No", "Yes"))
    # file.close()
    # exit()

    # Create tasks.txt file if it doesn't exist
    task_file = File("tasks.txt")
    task_file.create()
    
    # Read tasks.txt and get the tasks
    task = Task("tasks.txt")
    tasks = task.get_task()

    #====Login Section====
    '''This code reads usernames and password from the user.txt file to 
        allow a user to login.
    '''

    # Create user.txt if it doesn't exist
    user_file = File("user.txt")
    user_file.create("admin;password")
    
    # User login
    user = User("user.txt")
    current_user = user.log_in()
    
    # presenting the menu to the user
    while True:
        print()
        menu = input('''Select one of the following Options below:
  re - Register a user
  ad - Add a task
  va - View all tasks
  vm - View my task
  ds - Display statistics
  ex - Exit
    ::>>> ''').lower()
        
        # Register a user
        if menu == "re":
            user.register()
        
        # Add a task
        elif menu == "ad":
            task.add_task()
        
        # View all tasks
        elif menu == "va":
            task.view_all(tasks)
        
        # View my task
        elif menu == "vm":
            my_task = task.view_mine(tasks, current_user)

            option = input("Enter the task number to choose a task or '-1' to return to the main menu: ")

            if option == "-1":
                menu
            else:
                pass

        # Display statistics to admin user          
        elif menu == "ds":
            if current_user == "admin":
                print("-----------------------------------")
                print(f"Number of users: \t\t {len(user.get_users().keys())}")
                print(f"Number of tasks: \t\t {len(tasks)}")
                print("-----------------------------------") 

        # Exit the program   
        elif menu == "ex":
            print(f"{'-'*15}")
            print('Goodbye!!!')
            print(f"{'-'*15}")
            exit()
        
        # Invalid input
        else:
            print("You have made a wrong choice. Please try again!")

        