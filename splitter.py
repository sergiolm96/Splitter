class Splitter:
    def __init__(self, members, expenses):
        # Inicializa los miembros y los gastos
        self.members = members
        self.expenses = expenses

    def calculate_per_member_share(self):
        # Calcula el total de los gastos y luego el gasto promedio por miembro
        sum_of_expenses = float(sum([x[1] for x in self.expenses]))
        return sum_of_expenses / len(self.members)

    def calculate_per_member_balances(self):
        # Calcula el balance de cada miembro comparando lo que pagó con el gasto promedio
        each_share = self.calculate_per_member_share()
        balances = {}
        for member in self.members:
            expense_of_member = sum([x[1] for x in self.expenses if x[0] == member])
            balances[member] = round(expense_of_member - each_share, 2)
        return balances

    def calculate_borrowers_and_lenders_balances(self):
        # Clasifica a los miembros en prestamistas (lenders) y prestatarios (borrowers)
        lenders = {}
        borrowers = {}
        member_balances = self.calculate_per_member_balances()
        for member, balance in member_balances.items():
            if balance > 0:
                lenders[member] = balance
            elif balance < 0:
                borrowers[member] = balance

        return borrowers, lenders

    def split_expense(self):
        # Optimiza el cálculo de las transacciones necesarias para equilibrar los gastos
        (borrowers, lenders) = self.calculate_borrowers_and_lenders_balances()
        transactions = []
        
        # Convertir diccionarios a listas de tuplas y ordenarlas
        borrowers = sorted(borrowers.items(), key=lambda x: x[1])
        lenders = sorted(lenders.items(), key=lambda x: x[1], reverse=True)

        i, j = 0, 0
        while i < len(borrowers) and j < len(lenders):
            borrower, borrowed_amt = borrowers[i]
            lender, lend_amt = lenders[j]

            # La cantidad que el prestatario va a pagar al prestamista
            amount_to_pay = min(-borrowed_amt, lend_amt)
            
            transactions.append((borrower, lender, amount_to_pay))
            
            # Actualizar los montos prestados y tomados
            borrowed_amt += amount_to_pay
            lend_amt -= amount_to_pay

            # Actualizar las listas
            if borrowed_amt == 0:
                i += 1
            else:
                borrowers[i] = (borrower, borrowed_amt)

            if lend_amt == 0:
                j += 1
            else:
                lenders[j] = (lender, lend_amt)

        return transactions
