import unittest
from unittest.mock import patch, mock_open, call
from taskrunner import manager
import os

class TestManager(unittest.TestCase):

    @patch('taskrunner.manager.write_tasks')
    @patch('taskrunner.manager.read_tasks', return_value=['task1', 'task2'])
    def test_add_task_existing(self, mock_read_tasks, mock_write_tasks):
        manager.add_task('task1')
        mock_write_tasks.assert_not_called()

    @patch('taskrunner.manager.write_tasks')
    @patch('taskrunner.manager.read_tasks', return_value=['task1', 'task2'])
    def test_add_task_new(self, mock_read_tasks, mock_write_tasks):
        manager.add_task('new_task')
        mock_write_tasks.assert_called_once_with(['task1', 'task2', 'new_task'])

    @patch('builtins.print')
    @patch('taskrunner.manager.read_tasks', return_value=['task1', 'task2'])
    def test_list_tasks(self, mock_read_tasks, mock_print):
        manager.list_tasks()
        mock_print.assert_any_call('0 : task1')
        mock_print.assert_any_call('1 : task2')

    @patch('builtins.print')
    @patch('taskrunner.manager.read_tasks', return_value=[])
    def test_list_tasks_empty(self, mock_read_tasks, mock_print):
        manager.list_tasks()
        self.assertTrue(any("No tasks found" in call[0][0] for call in mock_print.call_args_list))

    @patch('taskrunner.manager.write_tasks')
    @patch('taskrunner.manager.read_tasks', return_value=['task1', 'task2'])
    @patch('taskrunner.manager.load_pids', return_value={})
    @patch('taskrunner.manager.save_pids')
    def test_remove_task(self, mock_save_pids, mock_load_pids, mock_read_tasks, mock_write_tasks):
        manager.remove_task(1)
        mock_write_tasks.assert_called_once_with(['task2'])

    @patch('builtins.print')
    @patch('taskrunner.manager.read_tasks', return_value=['task1', 'task2'])
    def test_remove_task_invalid_index(self, mock_read_tasks, mock_print):
        manager.remove_task(3)
        self.assertTrue(any("Invalid task index" in call[0][0] for call in mock_print.call_args_list))

if __name__ == '__main__':
    unittest.main()
