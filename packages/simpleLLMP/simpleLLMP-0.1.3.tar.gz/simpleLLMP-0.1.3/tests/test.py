import unittest
from simpleLLMP import SimpleLLMP

class TestSimpleLLMP(unittest.TestCase):
    def setUp(self):
        self.llmp = SimpleLLMP()
        self.llmp.setup(api_key="your-api-key", model_version="gpt-4")

    def test_generate(self):
        prompt = "Hello, how are you?"
        response = self.llmp.generate(prompt)
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)

    def test_add_to_history(self):
        self.llmp.add_to_history("user", "Hello")
        self.llmp.add_to_history("assistant", "Hi there!")
        self.assertEqual(len(self.llmp.conversation_history), 2)
        self.assertEqual(self.llmp.conversation_history[0]['role'], "user")
        self.assertEqual(self.llmp.conversation_history[0]['content'], "Hello")

    def test_reset_conversation(self):
        self.llmp.add_to_history("user", "Hello")
        self.llmp.reset_conversation()
        self.assertEqual(len(self.llmp.conversation_history), 0)

if __name__ == '__main__':
    unittest.main()

