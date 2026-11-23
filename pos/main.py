import sys
from pos.container import Container
from pos.ui.console import run


def demo(c: Container) -> None:
    f = c.facade
    alice = f.add_student("Alice")
    bob = f.add_student("Bob")
    test = f.add_criterion("Test", max_score=10, weight=0.4)
    lab = f.add_criterion("Lab", max_score=5, weight=0.6)

    f.evaluate(alice, test, 8)
    f.evaluate(alice, lab, 4)
    f.evaluate(bob, test, 6)

    print("Alice:", f.total(alice))
    print("Bob:  ", f.total(bob))

    f.export_totals("totals.csv")


if __name__ == "__main__":
    container = Container()
    if "--demo" in sys.argv:
        demo(container)
    else:
        run(container.facade)
