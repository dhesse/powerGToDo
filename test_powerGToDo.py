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

class TestAzureToDo(TestCase):

    @patch("powerGToDo.requests.get")
    @patch("powerGToDo.get_config", new=MagicMock(return_value={'access_token': 'foo123'}))
    def test_constructor(self, get_mock):
        todo = AzureToDo()
        get_mock.assert_called_with(todo.LISTS_URL, headers={'Authorization': 'foo123'})