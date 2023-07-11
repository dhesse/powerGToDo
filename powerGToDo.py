from typing import Any
import requests
import json
import dateutil
import progressbar
import os
import pickle
import itertools

class Task:

    def __init__(self, title: str, id: str, createdDateTime: object, **args):
        
        self.title = title
        self.created = dateutil.parser.parse(createdDateTime)
        self.id = id
        self.args = args

class TodoList:

    def __init__(self, tasks: list[Task], displayName: str, id: str, **args):
        
        self.tasks = tasks
        self.name = displayName
        self.id = id
        self.args = args

class AzureToDo:

    GRAPH_URL = "https://graph.microsoft.com/v1.0/me/todo/"
    LISTS_URL = GRAPH_URL + "lists"

    def __init__(self):
        config = json.load(open("config.json"))
        self.headers = {"Authorization": config['access_token']}
        list_raw = requests.get(self.LISTS_URL, headers=self.headers)
        self.lists = [TodoList(self.get_tasks(a['id']), **a) for a in progressbar.progressbar(list_raw.json()['value'])]
    
    def get_tasks(self, list_id: str) -> list[Task]:
        tasks_raw = requests.get(self.LISTS_URL + f"/{list_id}/tasks", headers=self.headers)
        return [Task(**t) for t in tasks_raw.json()['value']]

class CLI:

    def __init__(self, todo):
        
        self.todo = todo
        self.actions = {'l': {'desc': "Show ToDo lists", 'a': self.show_lists},
                        's': {'desc': "Show stale tasks", 'a': self.stale},
                        'h': {'desc': "Show help mesage", 'a': self.help}}
        
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        
        while True:
            self.actions[input("choose action (h for help, Ctrl+C to quit): ")]['a']()

    def show_lists(self) -> None:
        for n, l in enumerate(self.todo.lists):
            print(f"({n:4}) {l.name}")
    
    def help(self) -> None:
        print("available commands:")
        for a in self.actions:
            print(f"{a}: {self.actions[a]['desc']}")
    
    def stale(self) -> None:
        all_tasks = list(itertools.chain.from_iterable(l.tasks for l in self.todo.lists))
        all_tasks.sort(key=lambda t: t.created)
        for t in all_tasks[:10]:
            print(f"{t.created} -> {t.title}")

if __name__ == "__main__":

    pf = 'tasks.pickle'
    if os.path.exists(pf):
        tasks = pickle.load(open(pf, 'rb'))
    else:
        tasks = AzureToDo()
        with open(pf, 'wb') as bf:
            pickle.dump(tasks, bf)
    CLI(tasks)()