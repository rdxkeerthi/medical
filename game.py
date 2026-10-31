import subprocess

def run_python_file(option):
    if option == "1":
        file_path = "/home/sec/mini_project/Priyanka_project/FlappyBird/main.py"
    elif option == "2":
        file_path = "/home/sec/mini_project/Priyanka_project/Maze-Game/tonge.py"
    elif option == "3":
        file_path = "/home/sec/mini_project/Priyanka_project/src/main.py"
    else:
        print("Invalid option selected!")
        return

    try:
        subprocess.run(["python3", file_path])
    except Exception as e:
        print(f"Error running the file: {e}")

def main():
    print("Select a project to run:")
    print("1. Mandible Movement Practice Birdie on the Breeze")
    print("2. Lingual exercise game Maze Master Challenge")
    print("3. Oral Muscle Exercise game Bunny's Catching Eggs")

    choice = input("Enter your choice (1, 2, or 3): ")
    run_python_file(choice)

if __name__ == "__main__":
    main()
