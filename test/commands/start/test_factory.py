import unittest
from unittest.mock import patch

from guet.commands.start.factory import StartCommandFactory
from guet.settings.settings import Settings


@patch('guet.commands.command_factory.Context')
@patch('guet.commands.start.factory.Git')
class TestStartCommandFactoryMethod(unittest.TestCase):

    @patch('guet.commands.start.factory.git_path_from_cwd', return_value='/path')
    @patch('guet.commands.start.factory.PromptUserForHookTypeStrategy')
    @patch('guet.commands.start.factory.StrategyCommand')
    def test_returns_prompt_strategy_if_hooks_present(self, mock_command, mock_prompt_strategy, _2, mock_git,
                                                      mock_context):
        mock_git.return_value.non_guet_hooks_present.return_value = True
        command = StartCommandFactory().build(['start'], Settings())
        mock_prompt_strategy.assert_called_once_with('/path', mock_context.instance.return_value)
        mock_command.assert_called_once_with(mock_prompt_strategy.return_value)
        self.assertEqual(command, mock_command.return_value)

    @patch('guet.commands.start.factory.git_path_from_cwd', return_value='/path')
    @patch('guet.commands.start.factory.CreateHookStrategy')
    @patch('guet.commands.start.factory.StrategyCommand')
    def test_returns_create_strategy_if_no_hooks_present(self, mock_command, mock_create_strategy, _2, mock_git,
                                                         mock_context):
        mock_git.return_value.non_guet_hooks_present.return_value = False
        command = StartCommandFactory().build(['start'], Settings())
        mock_create_strategy.assert_called_once_with('/path', mock_context.instance.return_value)
        mock_command.assert_called_once_with(mock_create_strategy.return_value)
        self.assertEqual(command, mock_command.return_value)

    @patch('guet.commands.start.factory.git_path_from_cwd', return_value='/path')
    @patch('guet.commands.start.factory.CreateAlongsideHookStrategy')
    @patch('guet.commands.start.factory.StrategyCommand')
    def test_returns_command_with_create_alongside_strategy_if_given_dash_a(self, mock_command,
                                                                            mock_alongside_strategy,
                                                                            _2, _3, mock_context):
        command = StartCommandFactory().build(['start', '-a'], Settings())
        mock_alongside_strategy.assert_called_once_with('/path', mock_context.instance.return_value)
        mock_command.assert_called_once_with(mock_alongside_strategy.return_value)
        self.assertEqual(command, mock_command.return_value)

    @patch('guet.commands.start.factory.git_path_from_cwd', return_value='/path')
    @patch('guet.commands.start.factory.CreateHookStrategy')
    @patch('guet.commands.start.factory.StrategyCommand')
    def test_returns_command_with_create_new_strategy_if_given_dash_o(self, mock_command,
                                                                      create_hook_strategy,
                                                                      _2, _3, mock_context):
        command = StartCommandFactory().build(['start', '-o'], Settings())
        create_hook_strategy.assert_called_once_with('/path', mock_context.instance.return_value)
        mock_command.assert_called_once_with(create_hook_strategy.return_value)
        self.assertEqual(command, mock_command.return_value)

    @patch('guet.commands.start.factory.git_path_from_cwd', return_value='/path')
    @patch('guet.commands.start.factory.CreateHookStrategy')
    @patch('guet.commands.start.factory.StrategyCommand')
    def test_returns_command_with_create_new_strategy_if_given_dash_dash_overwrite(self, mock_command,
                                                                                   create_hook_strategy,
                                                                                   _2, _3, mock_context):
        command = StartCommandFactory().build(['start', '--overwrite'], Settings())
        create_hook_strategy.assert_called_once_with('/path', mock_context.instance.return_value)
        mock_command.assert_called_once_with(create_hook_strategy.return_value)
        self.assertEqual(command, mock_command.return_value)

    @patch('guet.commands.start.factory.git_path_from_cwd', return_value='/path')
    @patch('guet.commands.start.factory.CreateAlongsideHookStrategy')
    @patch('guet.commands.start.factory.StrategyCommand')
    def test_returns_command_with_create_alongside_strategy_if_given_dash_dash_alongside(self, mock_command,
                                                                                         mock_alongside_strategy,
                                                                                         _2, _3, mock_context):
        command = StartCommandFactory().build(['start', '--alongside'], Settings())
        mock_alongside_strategy.assert_called_once_with('/path', mock_context.instance.return_value)
        mock_command.assert_called_once_with(mock_alongside_strategy.return_value)
        self.assertEqual(command, mock_command.return_value)

    def test_get_short_help_message(self, _1, _2):
        self.assertEqual('Start guet usage in the repository at current directory',
                         StartCommandFactory().short_help_message())
