from unittest import TestCase
from unittest.mock import MagicMock, patch
import datetime

from powerGToDo import TodoList, Task, AzureToDo


class TestToDoList(TestCase):

    def test_factory_is_called(self):

        factory = MagicMock(return_value=[])
        task_list = TodoList(factory, "foo", "bar")
        factory.assert_called_with(task_list)
        self.assertListEqual(task_list.tasks, [])


class TestTask(TestCase):

    def test_date_time_conversion(self):

        parent = MagicMock()
        task = Task(parent, "foo", "bar", "2010-10-20 20:51:52")
        self.assertEqual(task.created,
                         datetime.datetime(2010, 10, 20, 20, 51, 52))

    def test_tags(self):

        task = Task(MagicMock(), "This task has no tags.", "bar", "2010-10-10")
        self.assertListEqual(task.tags, [])

        task = Task(MagicMock(), "This task has #two cool #tags.",
                    "bar", "2010-10-10")
        self.assertListEqual(task.tags, ["two", "tags"])


class TestAzureToDo(TestCase):

    @patch("powerGToDo.requests.get")
    @patch("powerGToDo.get_config",
           new=MagicMock(return_value={'access_token': 'foo123'}))
    def test_constructor(self, get_mock):
        todo = AzureToDo()
        get_mock.assert_called_with(todo.LISTS_URL, headers={
                                    'Authorization': 'foo123'})

    @patch("powerGToDo.requests.get")
    @patch("powerGToDo.get_config")
    def test_porperties(self, *a):
        todo = AzureToDo()
        todo.config = {'projects': ['proj'],
                       'waiting': ['wf'], 'next_action': ['na']}
        todo.lists = [TodoList(MagicMock(retun_value=[]), 'proj', 'foo'),
                      TodoList(MagicMock(retun_value=[]), 'wf', 'foo'),
                      TodoList(MagicMock(retun_value=[]), 'na', 'foo')]
        self.assertListEqual(todo.projects, [todo.lists[0]])
        self.assertListEqual(todo.waiting, [todo.lists[1]])
        self.assertListEqual(todo.next_action, [todo.lists[2]])
