class Hola:
    def __init__(self, mensaje: str):
        self.mensaje = mensaje

    def saludar(self):
        return f"Hola, {self.mensaje}!"


class Payment:
    def __init__(self, amount: float, currency: str):
        self.amount = amount
        self.currency = currency

    def process_payment(self):
        return f"Processing payment of {self.amount} {self.currency}"

    def refund_payment(self):
        return f"Refunding payment of {self.amount} {self.currency}"
