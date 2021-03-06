import unittest
from unittest.mock import patch, Mock
import guet
from guet.commands.usercommands.help.guet_usage import guet_usage
from guet.executor import Executor


@patch('guet.executor.already_initialized', return_value=True)
@patch('guet.executor.get_settings')
class TestCommandFactory(unittest.TestCase):

    def test_returns_command_with_settings_from_settings_file(self, mock_get_settings,
                                                              mock_already_init):
        builder_map = dict()
        mock_factory = Mock()
        builder_map['command'] = mock_factory

        command_factory = Executor(builder_map)
        args = ['command']
        command_factory.create(args)
        mock_factory.build.assert_called_with(args, mock_get_settings.return_value)

    @patch('builtins.print')
    def test_uses_command_builder_map_to_print_help_messages(self, mock_print, mock_get_settings,
                                                             mock_already_init):
        builder_map = dict()
        builder_map['command'] = Mock()
        command_factory = Executor(builder_map)
        result = command_factory.create([])
        result.execute()
        mock_print.assert_called_with(guet_usage(builder_map))

    @patch('builtins.print')
    def test_returns_command_that_prints_version_when_given_dash_dash_version_flag(self, mock_print,
                                                                                   mock_get_settings,
                                                                                   mock_already_init):
        builder_map = dict()
        builder_map['command'] = Mock()

        command_factory = Executor(builder_map)

        result = command_factory.create(['--version'])
        result.execute()
        mock_print.assert_called_with(f'{guet.__version__}')

    @patch('builtins.print')
    def test_returns_command_that_prints_version_when_given_dash_v(self, mock_print,
                                                                   mock_get_settings,
                                                                   mock_already_init):
        builder_map = dict()
        builder_map['command'] = Mock()

        command_factory = Executor(builder_map)

        result = command_factory.create(['-v'])
        result.execute()
        mock_print.assert_called_with(f'{guet.__version__}')

    @patch('builtins.print')
    def test_returns_command_that_prints_usage(self, mock_print,
                                               mock_get_settings,
                                               mock_already_init):
        builder_map = dict()
        builder_map['command'] = Mock()

        command_factory = Executor(builder_map)

        result = command_factory.create(['-h'])
        result.execute()
        mock_print.assert_called_with(guet_usage(builder_map))
