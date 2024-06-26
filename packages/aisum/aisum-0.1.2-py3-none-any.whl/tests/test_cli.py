import unittest
from click.testing import CliRunner
from aisum.cli import main

class TestCli(unittest.TestCase):

    def test_main(self):
        runner = CliRunner()
        result = runner.invoke(main, input='This is a long text to be summarized.')
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Summarize this', result.output)

if __name__ == '__main__':
    unittest.main()
