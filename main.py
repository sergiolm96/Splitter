import argparse
import re
from splitter import Splitter

def main():
    # Lee los miembros y los gastos desde el archivo de entrada
    (members, expenses) = parse_input_file(args.input_file)
    
    # Crea una instancia de Splitwise y calcula las transacciones necesarias
    splitwise = Splitter(members, expenses)
    transactions = splitwise.split_expense()
    
    # Imprime las transacciones calculadas
    print_output(transactions)

def parse_input_file(input_file):
    with open(input_file, 'r') as f:
        read_data = f.readlines()
        members = read_data[0]
        # Procesa la lista de miembros, eliminando comas y saltos de línea
        members_list = re.sub('[,\n]', '', members).split()

        expenses = []
        for line in read_data[2:]:
            expenses.append(line)
        expenses_list_temp = [re.sub('[\n]', '', x).split() for x in expenses]
        # Convierte la lista de gastos a una lista de tuplas (nombre, cantidad, descripción)
        expenses_list = [(x[0], float(x[1]), x[2]) for x in expenses_list_temp]

        # Imprime los datos de entrada
        print('-' * 75)
        print("ENTRADA")
        print("Leyendo archivo de entrada", args.input_file)
        print("Miembros de entrada", members_list)
        print("Gastos de entrada", expenses_list)
        print('-' * 75)

        return members_list, expenses_list

def print_output(transactions):
    # Imprime las transacciones calculadas
    print('-' * 75)
    print("SALIDA")
    for x in transactions:
        print(x[0], '->', x[1], x[2])
    print('-' * 75)

if __name__ == '__main__':
    print("*" * 75)
    print("DISTRIBUCIÓN DE GASTOS SPLITWISE")

    parser = argparse.ArgumentParser(description=
            'Dividir gastos entre los miembros. Leer archivo de entrada desde la línea de comandos.')
    parser.add_argument(
        "--input_file", type=str, help='Nombre del archivo de entrada.')
    args = parser.parse_args()

    if args.input_file:
        main()
    else:
        print("¡No se proporcionó un archivo de entrada! Por favor, consulte los usos. Saliendo.")

    print("*" * 75)
