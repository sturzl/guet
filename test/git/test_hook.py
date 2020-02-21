from unittest import TestCase
from unittest.mock import patch

from guet.git.errors import NotGuetHookError
from guet.git.hook import Hook, GUET_HOOK_FILE


@patch('guet.git.hook.read_lines', return_value=GUET_HOOK_FILE)
class TestHook(TestCase):

    def test_reads_content_to_hook(self, mock_read_lines):
        hook = Hook('/path/to/.git/hooks/name')
        mock_read_lines.assert_called_with('/path/to/.git/hooks/name')
        self.assertEqual(mock_read_lines.return_value, hook.content)

    def test_is_guet_hook_returns_whether_hook_matches_guet_content(self, mock_read_lines):
        mock_read_lines.return_value = ['Other', 'Content']
        hook = Hook('/path/to/.git/hooks/name')
        self.assertFalse(hook.is_guet_hook())

    def test_works_with_specific_content(self, mock_read_lines):
        mock_read_lines.return_value = ['#! /usr/bin/env python3', 'from guet.hooks import manage', 'import sys',
                                        'manage(sys.argv[0])']
        try:
            Hook('/path/to/.git/hooks/name')
            pass
        except (NotGuetHookError, FileNotFoundError):
            self.fail('Should successfully create hook.')

    def test_init_with_create_flag_catches_file_not_found_error_and_save_content_to_default(self, mock_read_lines):
        mock_read_lines.side_effect = FileNotFoundError()
        hook = Hook('/path/to/.git/hooks/name', create=True)
        self.assertEqual(GUET_HOOK_FILE, hook.content)

    def test_init_with_create_flag_overwrites_already_present_content(self, mock_read_lines):
        mock_read_lines.return_value = ['Other', 'Content']
        hook = Hook('/path/to/.git/hooks/name', create=True)
        self.assertEqual(GUET_HOOK_FILE, hook.content)

    @patch('guet.git.hook.chmod')
    @patch('guet.git.hook.stat')
    @patch('guet.git.hook.write_lines')
    def test_save_writes_lines_to_file(self, mock_write_lines, mock_stat, mock_chmod, mock_read_lines):
        mock_read_lines.side_effect = FileNotFoundError()
        path = '/path/to/.git/hooks/name'
        hook = Hook(path, create=True)
        hook.save()
        mock_write_lines.assert_called_with(path, hook.content)

    @patch('guet.git.hook.chmod')
    @patch('guet.git.hook.stat')
    @patch('guet.git.hook.write_lines')
    def test_save_chmods_file_to_executable(self, mock_write_lines, mock_stat, mock_chmod, mock_read_lines):
        mock_read_lines.side_effect = FileNotFoundError()
        path = '/path/to/.git/hooks/name'
        hook = Hook(path, create=True)
        hook.save()
        mock_chmod.assert_called_with(path, mock_stat.return_value.st_mode | 0o111)
