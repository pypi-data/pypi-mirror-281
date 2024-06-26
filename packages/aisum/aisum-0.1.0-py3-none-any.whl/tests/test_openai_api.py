import unittest
from unittest.mock import patch
from aisum.openai_api import summarize_text

class TestOpenaiAPi(unittest.TestCase):

    @patch('openai.Completion.create')
    def test_summarize_text(self, mock_create):
        mock_create.return_value.choices = [{"text": "Summary"}]
        summary = summarize_text("This is a long text to be summarized.")
        self.assertEqual(summary, "Summary")

if __name__ == '__main__':
    unittest.main()
