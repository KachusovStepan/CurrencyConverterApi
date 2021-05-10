import unittest

from services.currency_converter import CurrencyConverter
from services.exchange_rate_repository import ExchangeRateRepository


class ExchangeRateRepositoryTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.test_currency = {"USD": {"EUR": 0.5}}

    def test_convert(self):
        repo = ExchangeRateRepository()
        repo.merge_rates(self.test_currency)
        converter = CurrencyConverter(repo)
        actual_new_amount = converter.convert("USD", "EUR", 10)
        self.assertEqual(actual_new_amount, 5)


if __name__ == '__main__':
    unittest.main()
