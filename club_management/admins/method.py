class Percentage:
    def __init__(self, value, total):
        self.value = value
        self.total = total
        self.percentage = round((self.value / self.total * 100), 1)
