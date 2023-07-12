from typing import Any
import requests
import json
from dateutil.parser import parse
import progressbar
import os
import pickle
import itertools
import sys
from typing import Callable

class Task:

    def __init__(self, parent: "TodoList", title: str, id: str, createdDateTime: object, **args):
        
        self.parent = parent
        self.title = title
        self.created = parse(createdDateTime)
        self.id = id
        self.args = args

class TodoList:

    def __init__(self, task_list_gen: Callable[["TodoList"], list[Task]],
                 displayName: str, id: str, **args):
        
        self.name = displayName
        self.id = id
        self.args = args
        self.tasks = task_list_gen(self)

class AzureToDo:

    GRAPH_URL = "https://graph.microsoft.com/v1.0/me/todo/"
    LISTS_URL = GRAPH_URL + "lists"

    def __init__(self):
        config = json.load(open("config.json"))
        self.headers = {"Authorization": config['access_token']}
        list_raw = requests.get(self.LISTS_URL, headers=self.headers)
        self.lists = [TodoList(self.get_tasks, **a)
        for a in progressbar.progressbar(list_raw.json()['value'])]
    
    def get_tasks(self, parent: TodoList) -> list[Task]:
        tasks_raw = requests.get(self.LISTS_URL + f"/{parent.id}/tasks", headers=self.headers)
        return [Task(parent, **t) for t in tasks_raw.json()['value']]
    
    def forget_token(self) -> None:
        del self.config['access_token']

class CLI:

    def __init__(self, todo):
        
        self.todo = todo
        self.actions = {'l': {'desc': "Show ToDo lists", 'a': self.show_lists},
                        's': {'desc': "Show stale tasks", 'a': self.stale},
                        'q': {'desc': "quit", 'a': self.quit},
                        'h': {'desc': "Show help mesage", 'a': self.help}}
        
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        
        while True:
            fn = self.actions.get(
                input("choose action (h for help, Ctrl+C to quit): "),
                {'a': self.help})['a']()

    def show_lists(self) -> None:
        for n, l in enumerate(self.todo.lists):
            print(f"({n:4}) {l.name}")
    
    def help(self) -> None:
        print("available commands:")
        for a in self.actions:
            print(f"{a}: {self.actions[a]['desc']}")
    
    def stale(self) -> None:
        N = int(input("How many stale tasks to show (default: 20)") or 20)
        all_tasks = [t for t in itertools.chain.from_iterable(l.tasks for l in self.todo.lists) if t.args['status'] != 'completed']
        all_tasks.sort(key=lambda t: t.created)
        for t in all_tasks[:N]:
            print(f"{t.created} -> {t.title} | {t.parent.name}")

    def quit(self) -> None:
        sys.exit(0)

if __name__ == "__main__":

    pf = 'tasks.pickle'
    if os.path.exists(pf):
        tasks = pickle.load(open(pf, 'rb'))
    else:
        tasks = AzureToDo()
        tasks.forget_token()
        with open(pf, 'wb') as bf:
            pickle.dump(tasks, bf)
    CLI(tasks)()
