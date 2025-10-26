import unittest
from unittest.mock import patch, MagicMock
from taskrunner import cli
import sys

class TestCli(unittest.TestCase):

    @patch('sys.argv', ['taskrunner', 'list'])
    @patch('taskrunner.manager.list_tasks')
    def test_list_command(self, mock_list_tasks):
        cli.main()
        mock_list_tasks.assert_called_once()

    @patch('sys.argv', ['taskrunner', 'add', 'new_task'])
    @patch('taskrunner.manager.add_task')
    def test_add_command(self, mock_add_task):
        cli.main()
        mock_add_task.assert_called_once_with('new_task')

    @patch('sys.argv', ['taskrunner', 'remove', '1'])
    @patch('taskrunner.manager.remove_task')
    def test_remove_command(self, mock_remove_task):
        cli.main()
        mock_remove_task.assert_called_once_with(1)

    @patch('sys.argv', ['taskrunner', 'run'])
    @patch('taskrunner.manager.run_monitor')
    def test_run_command(self, mock_run_monitor):
        cli.main()
        mock_run_monitor.assert_called_once()

if __name__ == '__main__':
    unittest.main()