from unittest import TestCase
from unittest.mock import patch, call, Mock

from guet.commands.usercommands.addcommitter.factory import AddCommitterFactory, ADD_COMMITTER_HELP_MESSAGE
from guet.commands.strategies.cancellable_strategy import CancelableCommandStrategy
from guet.committers.committer import Committer
from guet.context.context import Context
from guet.settings.settings import Settings


@patch('guet.commands.command_factory.Context')
@patch('builtins.print')
class TestAddCommitterFactory(TestCase):

    def test_returns_cancelable_strategy_if_given_initials_match_already_present_committer(self, mock_print,
                                                                                           mock_context):
        mock_committers = Mock()
        context: Context = mock_context.instance.return_value
        context.committers = mock_committers
        mock_committers.all.return_value = [Committer(initials='initials', name='name', email='email')]

        subject = AddCommitterFactory()
        response = subject.build(['add', 'initials', 'name', 'email'], Settings())
        self.assertIsInstance(response.strategy, CancelableCommandStrategy)

    def test_execute_prints_error_message_when_too_many_arguments_are_given(self, mock_print,
                                                                            mock_context):
        initials = 'usr'
        name = 'user'
        email = 'user@localhost'

        command = AddCommitterFactory().build(['add', initials, name, email, 'extra'], Settings())
        command.execute()

        mock_print.assert_called_once_with('Too many arguments.')

    def test_execute_prints_the_error_message_and_help_message_when_there_are_not_enough_args(self, mock_print,
                                                                                              mock_context):
        command = AddCommitterFactory().build(['guet', 'initials', 'name'], Settings())
        command.execute()

        calls = [
            call('Not enough arguments.'),
            call(''),
            call(ADD_COMMITTER_HELP_MESSAGE)
        ]
        mock_print.assert_has_calls(calls)

    def test_get_short_help_message(self, mock_print, mock_context):
        self.assertEqual('Add committer to the list of available committers',
                         AddCommitterFactory().short_help_message())


@patch('guet.commands.command_factory.Context')
class TestBuildLocal(TestCase):

    @patch('guet.commands.usercommands.addcommitter.factory.AddCommitterLocallyStrategy')
    def test_uses_add_local_strategy_when_given_local_flag(self, mock_strategy, mock_context):
        instance: Context = mock_context.instance.return_value
        initials = 'initials'
        name = 'name'
        email = 'email'
        command = AddCommitterFactory().build(['add', '--local', initials, name, email], Settings())
        self.assertEqual(command.strategy, mock_strategy.return_value)
        mock_strategy.assert_called_with(initials, name, email, project_root=instance.project_root_directory,
                                         committers=instance.committers)
