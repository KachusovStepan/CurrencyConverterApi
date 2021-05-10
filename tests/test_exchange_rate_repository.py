import unittest

from services.exchange_rate_repository import ExchangeRateRepository


class ExchangeRateRepositoryTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.test_currencies = [
            {"USD": {"EUR": 0.1}},
            {"USD": {"EUR": 0.5}},
            {"USD": {"RUB": 0.5}}
        ]

    def test_merge_rates_updates_currency(self):
        repo = ExchangeRateRepository()
        repo.merge_rates(self.test_currencies[0])
        actual_rate = repo.get_rates("USD", "EUR")
        self.assertEqual(actual_rate, self.test_currencies[0]["USD"]["EUR"])

    def test_merge_rates_remain_unchanged_currencies(self):
        repo = ExchangeRateRepository()
        repo.merge_rates(self.test_currencies[0])
        repo.merge_rates(self.test_currencies[2])
        actual_rate = repo.get_rates("USD", "EUR")
        self.assertEqual(actual_rate, self.test_currencies[0]["USD"]["EUR"])

    def test_merge_rates_remain_can_invalidate_currencies(self):
        repo = ExchangeRateRepository()
        repo.merge_rates(self.test_currencies[0])
        repo.merge_rates(self.test_currencies[2], False)
        actual_rate = repo.get_rates("USD", "EUR")
        self.assertIsNone(actual_rate)

    def test_get_rates_by_base_returns_all_rates(self):
        repo = ExchangeRateRepository()
        repo.merge_rates(self.test_currencies[0])
        actual_rates = repo.get_rates_by_base("USD")
        self.assertDictEqual(actual_rates, self.test_currencies[0]["USD"])

    def test_get_rates_by_base_returns_None_if_not_present(self):
        repo = ExchangeRateRepository()
        actual_rates = repo.get_rates_by_base("USD")
        self.assertIsNone(actual_rates)


if __name__ == '__main__':
    unittest.main()
