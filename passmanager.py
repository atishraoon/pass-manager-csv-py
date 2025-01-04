import os
import pandas as pd
import sys
import json

TODO_FILE = "data.csv"
DEFAULT_COLUMNS = ["id", "title", "username", "password"]

def clear_console():
    """Clears the console."""
    os.system('cls' if os.name == 'nt' else 'clear')


def read_from_csv():
    if os.path.exists(TODO_FILE):
        return pd.read_csv(TODO_FILE)
    else:
        return pd.DataFrame(columns=DEFAULT_COLUMNS)

def save_to_csv(df):
    df.reset_index(drop=True, inplace=True)
    df["id"] = df.index
    df.to_csv(TODO_FILE, index=False)

def add_todo():
    title = input("Enter the title: ")
    username = input("Type username: ")
    password = input("Type password: ")

    new_todo = {"title": title, "username": username, "password": password}
    df = read_from_csv()
    df = pd.concat([df, pd.DataFrame([new_todo])], ignore_index=True)
    save_to_csv(df)

def print_all_todos(df=None):
    clear_console()
    df = df if df is not None else read_from_csv()
    if df.empty:
        print("No todos available.")
    else:
        # Define column widths
        id_width = 3
        title_width = 27
        username_width = 45
        password_width = 24

        # Print table header
        print("+----+----------------------------+----------------------------------------------+-------------------------+")
        print("| ID |            Title           |                Username                      |      Password           |")
        print("+----+----------------------------+----------------------------------------------+-------------------------+")
            
        # Print rows
        for _, row in df.iterrows():
            id_cell = str(row["id"]).ljust(id_width)
            title_cell = str(row["title"]).ljust(title_width)
            username_cell = str(row["username"]).ljust(username_width)
            password_cell = str(row["password"]).ljust(password_width)
            print(f"| {id_cell}| {title_cell}| {username_cell}| {password_cell}|")
        
        # Print table footer
        print("+----+----------------------------+----------------------------------------------+-------------------------+")

def update_todo():
    try:
        df = read_from_csv()
        if df.empty:
            print("No todos to update.")
            return

        todo_id = int(input("Enter the ID of the todo to update: "))
        if 0 <= todo_id < len(df):
            print("Leave a field blank to keep the current value.")
            new_title = input(f"Enter new title (current: {df.at[todo_id, 'title']}): ").strip() or df.at[todo_id, 'title']
            new_username = input(f"Enter new username (current: {df.at[todo_id, 'username']}): ").strip() or df.at[todo_id, 'username']
            new_password = input(f"Enter new password (current: {df.at[todo_id, 'password']}): ").strip() or df.at[todo_id, 'password']

            df.at[todo_id, 'title'] = new_title
            df.at[todo_id, 'username'] = new_username
            df.at[todo_id, 'password'] = new_password

            save_to_csv(df)
        else:
            print("Invalid todo ID.")
    except ValueError:
        print("Invalid input.")

def delete_todo():
    try:
        df = read_from_csv()
        if df.empty:
            print("No todos to delete.")
            return

        print_all_todos(df)
        todo_id = int(input("Enter the ID of the todo to delete: "))
        if 0 <= todo_id < len(df):
            df = df.drop(index=todo_id).reset_index(drop=True)
            save_to_csv(df)
        else:
            print("Invalid todo ID.")
    except ValueError:
        print("Invalid input.")

def search_todos(search_term):
    df = read_from_csv()
    results = df[df["title"].str.contains(search_term, case=False, na=False)]
    if results.empty:
        print("No matching todos found.")
    else:
        print_all_todos(results)
        sys.exit(0)

def export_to_json():
    df = read_from_csv()
    json_data = df.to_dict(orient="records")
    json_file = os.path.join(os.path.expanduser("~"), "Desktop", "todos.json")
    with open(json_file, "w") as file:
        json.dump(json_data, file, indent=4)
    print(f"Todos exported to {json_file}")

def show_options():
    while True:
        user_choice = input("Type 'A' to add, 'D' to delete, 'U' to update, 'S' to search, 'Q' to quit: ").upper()
        if user_choice == 'A':
            add_todo()
        elif user_choice == 'D':
            delete_todo()
        elif user_choice == 'U':
            update_todo()
        elif user_choice == 'S':
            search_term = input("Enter search term: ")
            search_todos(search_term)
        elif user_choice == 'Q':
            break
        else:
            print("Command not found.")

        print_all_todos()

def is_this_first_time():
    df = read_from_csv()
    if df.empty:
        print("Welcome to CLI Password Manager App")
        add_todo()
        print_all_todos()
    else:
        print_all_todos()

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[32;1m")

    if len(sys.argv) > 1 and sys.argv[1].lower() == 'json':
        export_to_json()
    else:
        is_this_first_time()
        show_options()
