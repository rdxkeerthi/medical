from exercises.lip_exercise import RabbitCatchGame
from exercises.tongue_exercise import TongueExercise
from exercises.jaw_exercise import JawExercise

def main():
    print("Choose an exercise:")
    print("1. Lip Exercise")
    print("2. Tongue Exercise")
    print("3. Jaw Exercise")
    print("4. Rabbit Catch Game")
    
    choice = input("Enter your choice: ")

    if choice == '1':
        LipExercise().run()
    elif choice == '2':
        TongueExercise().run()
    elif choice == '3':
        JawExercise().run()
    elif choice == '4':
        RabbitCatchGame().run()
    else:
        print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
