import threading
from sim import Sim
from slam import Slam
from interface import Interface


def bringup_sim(interface: Interface) -> None:
    sim = Sim(interface)
    sim_thread = threading.Thread(target=sim.start)
    sim_thread.start()


def bringup_slam(interface: Interface) -> None:
    slam = Slam(interface)
    slam.start()


def main() -> None:
    interface = Interface()
    bringup_sim(interface)
    bringup_slam(interface)


if __name__ == '__main__':
    main()
