
def get_share_price(symbol):
    # Mock implementation for testing - returns fixed prices
    prices = {'AAPL': 150.0, 'TSLA': 700.0, 'GOOGL': 2800.0}
    return prices.get(symbol, 0.0)

class Account:
    def __init__(self, account_id: str, initial_deposit: float) -> None:
        self.account_id = account_id
        self.initial_deposit = initial_deposit
        self.balance = initial_deposit
        self.holdings = {}
        self.transaction_history = []
        self._record_transaction('initial_deposit', amount=initial_deposit)

    def deposit(self, amount: float) -> None:
        self.balance += amount
        self._record_transaction('deposit', amount=amount)

    def withdraw(self, amount: float) -> bool:
        if amount <= self.balance:
            self.balance -= amount
            self._record_transaction('withdraw', amount=amount)
            return True
        return False

    def buy_shares(self, symbol: str, quantity: int) -> bool:
        price_per_share = get_share_price(symbol)
        total_cost = price_per_share * quantity
        if self.balance >= total_cost:
            self.balance -= total_cost
            self.holdings[symbol] = self.holdings.get(symbol, 0) + quantity
            self._record_transaction('buy', symbol, quantity, total_cost)
            return True
        return False

    def sell_shares(self, symbol: str, quantity: int) -> bool:
        if self.holdings.get(symbol, 0) >= quantity:
            price_per_share = get_share_price(symbol)
            total_revenue = price_per_share * quantity
            self.holdings[symbol] -= quantity
            self.balance += total_revenue
            self._record_transaction('sell', symbol, quantity, total_revenue)
            if self.holdings[symbol] == 0:
                del self.holdings[symbol]  # Remove entry if zero shares
            return True
        return False

    def get_portfolio_value(self) -> float:
        value = self.balance
        for symbol, quantity in self.holdings.items():
            value += get_share_price(symbol) * quantity
        return value

    def get_profit_or_loss(self) -> float:
        return self.get_portfolio_value() - self.initial_deposit

    def get_holdings(self) -> dict:
        return self.holdings

    def get_transaction_history(self) -> list:
        return self.transaction_history

    def _record_transaction(self, transaction_type: str, symbol: str = '', quantity: int = 0, amount: float = 0.0) -> None:
        transaction = {
            'type': transaction_type,
            'symbol': symbol,
            'quantity': quantity,
            'amount': amount,
        }
        self.transaction_history.append(transaction)
