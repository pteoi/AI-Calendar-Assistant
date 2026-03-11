import datetime
import asyncio
import contextlib


class Task:

    def __init__(
        self,
        name: str,
        deadline: datetime.datetime,
        description: str,
        repeatsWeekly: bool,
        isLate=False,
    ):
        self.name = name
        self.deadline = deadline
        self.description = description
        self.repeatsWeekly = repeatsWeekly
        self.isLate = isLate


class Event:

    def __init__(
        self,
        name: str,
        datetime: datetime.datetime,
        duration: int,
        description: str,
        repeatsWeekly: bool,
    ):
        self.name = name
        self.datetime = datetime
        self.duration = duration
        self.description = description
        self.repeatsWeekly = repeatsWeekly


class Agenda:

    def __init__(self):
        self.toDo = []
        self.onGoing = []
        self.late = []
        self.done = []
        self.events = []

    @property
    def scheduled(self):
        return (self.toDo, self.onGoing, self.late)

    def task_is_Scheduled(self, task: Task) -> bool:
        if any(task in l for l in self.scheduled):
            return True

        else:
            return False

    def add_task(self, task: Task) -> None:
        if self.task_is_Scheduled(task):
            print("Task already scheduled.")

        else:
            self.toDo.append(task)
            print("Task added succesfully.")

    def start_task(self, task: Task) -> None:
        if task in self.toDo:
            self.toDo.remove(task)
            self.onGoing.append(task)
            print(f"{task.name} is now on going.")

        else:
            print("There is no such task on to do list.")

    def complete_task(self, task: Task) -> None:
        if not self.task_is_Scheduled(task):
            print("Task is not scheduled.")

        else:
            for i in range(len(self.scheduled)):
                if task in self.scheduled[i]:
                    self.scheduled[i].remove(task)
                    self.done.append(task)
                    print(f"{task.name} is now done and removed from schedule.")
                    if task in self.late:
                        self.late.remove(task)
                        return

    async def late_task(self) -> None:
        while True:
            for bucket in self.scheduled:
                for task in bucket[:]:
                    if (
                        task.deadline < datetime.datetime.now()
                        and task not in self.late
                    ):
                        task.isLate = True
                        self.late.append(task)
                        print(f"{task.name} is now late.")
            await asyncio.sleep(60)

    def print_agenda(self) -> None:
        print("To Do:")
        for task in self.toDo:
            print(task.name)

        print("\nOn Going:")
        for task in self.onGoing:
            print(task.name)

        print("\nLate:")
        for task in self.late:
            print(task.name)

        print("\nDone:")
        for task in self.done:
            print(task.name)

        print("\nEvents:")
        for event in self.events:
            print(event.name)

    def schedule_event(self, event: Event) -> None:
        if any(
            event.datetime
            <= e.datetime
            < event.datetime + datetime.timedelta(minutes=event.duration)
            or e.datetime
            <= event.datetime
            < e.datetime + datetime.timedelta(minutes=e.duration)
            for e in self.events
        ):
            print("There is already an event scheduled for this time.")
        else:
            self.events.append(event)
            print(f"{event.name} added succesfully.")


async def interactive_loop(agenda: Agenda) -> None:
    while True:
        cmd = (
            (
                await asyncio.to_thread(
                    input, "\nCommand (addtask/addevent/start/done/show/quit): "
                )
            )
            .strip()
            .lower()
        )

        if cmd == "show":
            agenda.print_agenda()

        elif cmd == "addtask":
            name = await asyncio.to_thread(input, "Name: ")
            mins = int(
                await asyncio.to_thread(
                    input, "Deadline in how many minutes from now?: "
                )
            )
            deadline = datetime.datetime.now() + datetime.timedelta(minutes=mins)
            agenda.add_task(Task(name, deadline, "No description", False))

        elif cmd == "addevent":
            name = await asyncio.to_thread(input, "Name: ")
            duration = int(
                await asyncio.to_thread(input, "Event lasts for how long (minutes)?: ")
            )
            date = await asyncio.to_thread(
                input, "Event date and time (YYYY-MM-DD HH:MM): "
            )
            datetime_obj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
            agenda.schedule_event(
                Event(name, datetime_obj, duration, "No description", False)
            )

        elif cmd == "start":
            name = await asyncio.to_thread(input, "Task name to start: ")
            task = next((t for t in agenda.toDo if t.name == name), None)
            if task:
                agenda.start_task(task)
            else:
                print("Task not found in To Do.")

        elif cmd == "done":
            name = await asyncio.to_thread(input, "Task name to complete: ")
            task = next(
                (t for t in agenda.toDo + agenda.onGoing if t.name == name), None
            )
            if task:
                agenda.complete_task(task)
            else:
                print("Task not found in active lists.")

        elif cmd == "quit":
            break

        else:
            print("Unknown command.")


async def main():
    agenda = Agenda()

    watcher = asyncio.create_task(agenda.late_task())

    try:
        await interactive_loop(agenda)
    finally:
        watcher.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await watcher


if __name__ == "__main__":
    asyncio.run(main())
