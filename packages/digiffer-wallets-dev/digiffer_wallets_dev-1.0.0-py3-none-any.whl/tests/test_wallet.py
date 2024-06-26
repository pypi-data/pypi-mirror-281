# tests/test_wallet.py

import unittest
from digiffer_wallets_dev.wallet import DigifferWallet # type: ignore

class TestDigifferWallet(unittest.TestCase):
    def setUp(self):
        self.wallet = DigifferWallet("http://example.com", "12345")

    def test_create_wallet(self):
        with self.assertRaises(Exception) as context:
            self.wallet.create_wallet({})
        self.assertTrue('Error createwallet' in str(context.exception))

    # Add more tests for other methods

if __name__ == '__main__':
    unittest.main()
