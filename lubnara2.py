from abc import ABC, abstractmethod
from datetime import datetime
import logging

# Strategy pattern for payment method
class PaymentMethod(ABC):
    @abstractmethod
    def validate(self, payment_details):
        pass

    @abstractmethod
    def process_payment(self, amount):
        pass

class CreditCardPayment(PaymentMethod):
    def validate(self, payment_details):
        print("valedating credit card details")
        return True

    def process_payment(self, amount):
        
        return f"Credit card payment of ${amount} processed successfully"

class PayPalPayment(PaymentMethod):
    def validate(self, payment_details):
        print("valedating paypal account")
        return True

    def process_payment(self, amount):
        
        return f"PayPal payment of ${amount} processed successfully"

class CryptocurrencyPayment(PaymentMethod):
    def validate(self, payment_details):
        print("valedating cryptocurrency details")
        return True

    def process_payment(self, amount):
        
        return f"Cryptocurrency payment of ${amount} processed successfully"

# Discount strategy pattern
class Discount(ABC):
    @abstractmethod
    def apply_discount(self, amount):
        pass

class PercentageDiscount(Discount):
    def __init__(self, percentage):
        self.percentage = percentage

    def apply_discount(self, amount):
        return amount - (amount * self.percentage / 100)

class FixedAmountDiscount(Discount):
    def __init__(self, amount):
        self.amount = amount

    def apply_discount(self, amount):
        return amount - self.amount

# Transaction logger
class TransactionLogger:
    def __init__(self, log_file):
        self.log_file = log_file
        self.logger = logging.getLogger("TransactionLogger")
        self.logger.setLevel(logging.INFO)
        self.handler = logging.FileHandler(log_file)
        self.handler.setLevel(logging.INFO)
        self.formatter = logging.Formatter("%(asctime)s - %(message)s")
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)

    def log_transaction(self, amount, result):
        self.logger.info(f"Transaction: Amount: ${amount} - Result: {result}")

# Payment processor
class PaymentProcessor:
    def __init__(self, payment_method, discount=None, transaction_logger=None):
        self.payment_method = payment_method
        self.discount = discount
        self.transaction_logger = transaction_logger

    def process_payment(self, amount):
        if self.payment_method.validate("payment_details"):
            if self.discount:
                amount = self.discount.apply_discount(amount)
            result = self.payment_method.process_payment(amount)
            if self.transaction_logger:
                self.transaction_logger.log_transaction(amount, result)
            return result
        else:
            return "Invalid payment details"

# Currency convertor
class CurrencyConverter:
    def __init__(self):
        self.exchange_rates = {
            "USD": {"EUR": 0.84, "GBP": 0.76, "JPY": 109.23},
            "EUR": {"USD": 1.19, "GBP": 0.90, "JPY": 130.23},
            "GBP": {"USD": 1.32, "EUR": 1.11, "JPY": 144.23},
            "JPY": {"USD": 0.0092, "EUR": 0.0077, "GBP": 0.0069}
        }

    def convert(self, amount, from_currency, to_currency):
        if from_currency != to_currency:
            exchange_rate = self.exchange_rates[from_currency][to_currency]
            converted_amount = amount * exchange_rate
            return converted_amount
        else:
            return amount

    def get_exchange_rate(self, from_currency, to_currency):
        return self.exchange_rates[from_currency][to_currency]


# Main 
if __name__ == "__main__":
    transaction_logger = TransactionLogger("transaction.log")

    payment_processor = PaymentProcessor(CreditCardPayment(), transaction_logger=transaction_logger)
    print(payment_processor.process_payment(100))

    payment_processor = PaymentProcessor(PayPalPayment(), PercentageDiscount(10), transaction_logger)
    print(payment_processor.process_payment(100))

    payment_processor = PaymentProcessor(CryptocurrencyPayment(), FixedAmountDiscount(20), transaction_logger)
    print(payment_processor.process_payment(100))

    converter = CurrencyConverter()
    print(converter.convert(100, "USD", "EUR"))