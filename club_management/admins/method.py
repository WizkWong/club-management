class UserTaskPercentage:
    def __init__(self, total_completes, total):
        self.total_completes = total_completes
        self.total = total
        self.percentage = round((self.total_completes / self.total * 100), 1)
