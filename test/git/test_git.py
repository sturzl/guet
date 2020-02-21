from os.path import join
from unittest import TestCase
from unittest.mock import Mock, patch, call

from guet.git.git import Git

path_to_git = '/path/to/.git'


def _mock_hook(path: str, *, is_guet_hook: bool = True):
    mock = Mock()
    mock.path = path
    mock.is_guet_hook.return_value = is_guet_hook
    return mock


@patch('guet.git._hook_loader.Hook')
class TestGit(TestCase):

    def test_init_loads_all_possible_hooks(self, mock_hook):
        pre_commit_content = Mock()
        post_commit_content = Mock()
        commit_msg_content = Mock()
        pre_commit_alongside_content = Mock()
        post_commit_alongside_content = Mock()
        commit_msg_alongside_content = Mock()

        expected_hooks = [pre_commit_content, post_commit_content, commit_msg_content,
                          pre_commit_alongside_content, post_commit_alongside_content, commit_msg_alongside_content]

        mock_hook.side_effect = expected_hooks

        git = Git(path_to_git)

        mock_hook.assert_has_calls([
            call(join(path_to_git, 'hooks', 'pre-commit'), create=False),
            call(join(path_to_git, 'hooks', 'post-commit'), create=False),
            call(join(path_to_git, 'hooks', 'commit-msg'), create=False),
            call(join(path_to_git, 'hooks', 'pre-commit-guet'), create=False),
            call(join(path_to_git, 'hooks', 'post-commit-guet'), create=False),
            call(join(path_to_git, 'hooks', 'commit-msg-guet'), create=False)
        ])
        self.assertListEqual(expected_hooks, git.hooks)

    def test_init_swallows_file_not_found_error(self, mock_hook):
        mock_hook.side_effect = [FileNotFoundError(), FileNotFoundError(), FileNotFoundError(), FileNotFoundError(),
                                 FileNotFoundError(), FileNotFoundError()]

        git = Git(path_to_git)

        self.assertListEqual([], git.hooks)

    def test_hooks_present_returns_true_when_all_normal_hooks_present(self, mock_hook):
        git = Git(path_to_git)
        git.hooks = [
            _mock_hook(join(path_to_git, 'hooks', 'pre-commit')),
            _mock_hook(join(path_to_git, 'hooks', 'post-commit')),
            _mock_hook(join(path_to_git, 'hooks', 'commit-msg'))
        ]
        self.assertTrue(git.hooks_present())

    def test_hooks_present_returns_false_if_normal_hooks_have_non_guet_content(self, mock_hook):
        git = Git(path_to_git)
        git.hooks = [
            _mock_hook(join(path_to_git, 'hooks', 'pre-commit')),
            _mock_hook(join(path_to_git, 'hooks', 'post-commit'), is_guet_hook=False),
            _mock_hook(join(path_to_git, 'hooks', 'commit-msg'))
        ]
        self.assertFalse(git.hooks_present())

    def test_hooks_present_returns_true_when_normal_hooks_have_non_guet_content_but_dash_hooks_are_present(self, _):
        git = Git(path_to_git)
        git.hooks = [
            _mock_hook(join(path_to_git, 'hooks', 'post-commit'), is_guet_hook=False),
            _mock_hook(join(path_to_git, 'hooks', 'pre-commit-guet')),
            _mock_hook(join(path_to_git, 'hooks', 'post-commit-guet')),
            _mock_hook(join(path_to_git, 'hooks', 'commit-msg-guet'))
        ]
        self.assertTrue(git.hooks_present())

    def test_hooks_present_when_all_dash_guet_hooks_are_present(self, mock_hook):
        git = Git(path_to_git)
        git.hooks = [
            _mock_hook(join(path_to_git, 'hooks', 'pre-commit-guet')),
            _mock_hook(join(path_to_git, 'hooks', 'post-commit-guet')),
            _mock_hook(join(path_to_git, 'hooks', 'commit-msg-guet'))
        ]
        self.assertTrue(git.hooks_present())

    def test_non_guet_hooks_present_returns_true_if_any_hooks_have_non_guet_contnet(self, mock_hook):
        git = Git(path_to_git)
        non_guet_hook = Mock()
        non_guet_hook.is_guet_hook.return_value = False
        guet_hook = Mock()
        guet_hook.is_guet_hook.return_value = True
        git.hooks = [non_guet_hook]
        self.assertTrue(git.non_guet_hooks_present())

    def test_non_guet_hooks_present_returns_false_if_all_hooks_have_guet_content(self, mock_hook):
        git = Git(path_to_git)
        guet_hook = Mock()
        guet_hook.is_guet_hook.return_value = True
        git.hooks = [guet_hook]
        self.assertFalse(git.non_guet_hooks_present())

    def test_non_guet_hook_present_returns_false_when_no_hooks_present(self, mock_hook):
        git = Git(path_to_git)
        git.hooks = []
        self.assertFalse(git.non_guet_hooks_present())

    def test_create_hooks_adds_new_files(self, mock_hook):
        git = Git(path_to_git)
        git.hooks = []

        mock_hook.reset_mock()
        pre_commit_hook = Mock()
        post_commit_hook = Mock()
        commit_msg_hook = Mock()
        expected_hooks = [pre_commit_hook, post_commit_hook, commit_msg_hook]
        mock_hook.side_effect = expected_hooks

        git.create_hooks()

        self.assertListEqual(expected_hooks, git.hooks)

        mock_hook.assert_has_calls([
            call(join(path_to_git, 'hooks', 'pre-commit'), create=True),
            call(join(path_to_git, 'hooks', 'post-commit'), create=True),
            call(join(path_to_git, 'hooks', 'commit-msg'), create=True),
        ])

        pre_commit_hook.save.assert_called()
        post_commit_hook.save.assert_called()
        commit_msg_hook.save.assert_called()

    def test_create_hooks_adds_new_alongside_hooks(self, mock_hook):
        git = Git(path_to_git)
        git.hooks = []

        mock_hook.reset_mock()
        pre_commit_hook = Mock()
        post_commit_hook = Mock()
        commit_msg_hook = Mock()
        expected_hooks = [pre_commit_hook, post_commit_hook, commit_msg_hook]
        mock_hook.side_effect = expected_hooks

        git.create_hooks(alongside=True)

        self.assertListEqual(expected_hooks, git.hooks)

        mock_hook.assert_has_calls([
            call(join(path_to_git, 'hooks', 'pre-commit-guet'), create=True),
            call(join(path_to_git, 'hooks', 'post-commit-guet'), create=True),
            call(join(path_to_git, 'hooks', 'commit-msg-guet'), create=True),
        ])

        pre_commit_hook.save.assert_called()
        post_commit_hook.save.assert_called()
        commit_msg_hook.save.assert_called()
