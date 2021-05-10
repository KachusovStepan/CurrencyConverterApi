from services.exchange_rate_repository import ExchangeRateRepository


class CurrencyConverter:
    def __init__(self, exrate_repo: ExchangeRateRepository):
        self.exrate_repo = exrate_repo

    def convert(self, curr_from, curr_to, amount):
        factor = self.exrate_repo.get_rates(curr_from, curr_to)
        converted = amount * factor
        return converted
