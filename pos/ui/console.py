from pos.app.facade import AppFacade
from pos.domain.errors import DomainError


MENU = """\
1. Add student
2. Add criterion
3. Add evaluation
4. Show student evaluations
5. Total student score
6. Export scores to CSV
7. List of students and criterions
0. Exit"""


def run(facade: AppFacade) -> None:
    while True:
        print(MENU)
        choice = input("> ").strip()
        try:
            if choice == "0":
                return
            elif choice == "1":
                name = input("Student name: ")
                print("Student id:", facade.add_student(name))
            elif choice == "2":
                name = input("Criterion name: ")
                mx = float(input("Max score: "))
                w = float(input("Weight (0..1]: "))
                print("Criterion id:", facade.add_criterion(name, mx, w))
            elif choice == "3":
                sid = input("Student id: ")
                cid = input("Criterion id: ")
                val = float(input("Score: "))
                print("Evaluation id:", facade.evaluate(sid, cid, val))
            elif choice == "4":
                sid = input("Student id: ")
                for ev in facade.list_evaluations(sid):
                    print(ev)
            elif choice == "5":
                sid = input("Student id: ")
                print(facade.total(sid))
            elif choice == "6":
                path = input("Path to csv: ")
                facade.export_totals(path)
            elif choice == "7":
                for s in facade.list_students(): print("S", s)
                for c in facade.list_criteria(): print("C", c)
            else:
                print("Unknown action")
        except DomainError as e:
            print("Domain error:", e)
        except ValueError as e:
            print("Invalid input:", e)
