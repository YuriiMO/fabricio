import mock
import unittest2 as unittest

from fabric import api as fab

import fabricio
import fabricio.tasks

from fabricio import docker


class TestContainer(docker.Container):

    image = docker.Image('test')


class DecoratorsTestCase(unittest.TestCase):

    def test_skip_unknown_host(self):

        mocked_task = mock.Mock()

        @fabricio.skip_unknown_host
        def task():
            mocked_task()

        with fab.settings(fab.hide('everything')):
            fab.execute(task)
            mocked_task.assert_not_called()

            fab.execute(task, host='host')
            mocked_task.assert_called_once()

    def test_once_per_task(self):
        cases = dict(
            default=dict(
                all_hosts=[],
                command=None,
                infrastructure=None,
            ),
            same_infrastructure=dict(
                all_hosts=[],
                command=None,
                infrastructure='inf',
            ),
            same_command=dict(
                all_hosts=[],
                command='command',
                infrastructure=None,
            ),
            same_hosts=dict(
                all_hosts=['host1', 'host2'],
                command=None,
                infrastructure=None,
            ),
            complex=dict(
                all_hosts=['host1', 'host2'],
                command='command',
                infrastructure='inf',
            ),
        )
        for case, data in cases.items():
            with self.subTest(case=case):
                def real_method():
                    real_method.call_count += 1
                real_method.call_count = 0
                method = fabricio.once_per_task(real_method)
                with fab.settings(**data):
                    method()
                    method()
                self.assertEqual(1, real_method.call_count)

    def test_once_per_task_reset(self):
        method = fabricio.once_per_task(lambda x: x)
        method.set('value')
        method.reset()
        self.assertFalse(method.has_result())
        self.assertFalse(method.wait(0))
