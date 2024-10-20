import random
# Number of servers
NUM_SERVERS = 5
class Server:
    def __init__(self, id):
        self.id = id
        self.available_resources = random.randint(50, 100)  # Randomly initialize resources for each server

    def __str__(self):
        return f"Server {self.id}: {self.available_resources} resources available"
    
# Initialize the servers
servers = [Server(i) for i in range(1, NUM_SERVERS + 1)]

def assign_task_to_server(task_weight):
    # Sort servers in descending order
    servers.sort(key=lambda s: s.available_resources, reverse=True)

    # Find a server with enough available resources to handle the task
    for server in servers:
        if server.available_resources >= task_weight:
            server.available_resources -= task_weight
            print(f"\nTask of weight {task_weight} assigned to Server {server.id}")
            return server.id
        else:
            raise Exception("Server Busy") 
        
while True:
    try:
        # Input the task weight from the user
        user_input = input("\nEnter the task weight (or type 'exit' to quit): ")
        if user_input.lower() == 'exit':
            print("\nExiting the task assignment system.")
            break
        task_weight = int(user_input)
        
        # Try to assign the task to an appropriate server
        assign_task_to_server(task_weight) 
        # Print the resources after assignment
        print("\nServer resources (after assignment):")
        for server in servers:
            print(server)
    except ValueError:
        print("Invalid input! Please enter a valid task weight or 'exit' to quit.")
    except Exception as e:
        print(e)
