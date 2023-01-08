import ast, argparse


class Antiplagiat:
    def __init__(self):
        parser = argparse.ArgumentParser()  #используем argparse для работы через консоль
        parser.add_argument('input_name', type=str)
        parser.add_argument('output_name', type=str)
        self.args = parser.parse_args()
        self.results = []  #список полученных результатов

    def levenstein(self, A, B):
        n = len(A)
        m = len(B)
        F = [[i + j if i * j == 0 else 0 for j in range(m + 1)] for i in range(n + 1)]
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                if A[i - 1] == B[j - 1]:
                    F[i][j] = F[i - 1][j - 1]
                else:
                    F[i][j] = 1 + min(F[i][j - 1], F[i - 1][j], F[i - 1][j - 1])
        return 1 - F[n][m] / m  #получаем редакционное расстояние(насколько похожи два текста)

    def check_levenstein(self, first_file, second_file):
        with open(first_file, 'r') as first:
            tree_first = ast.dump(ast.parse(first.read()))  #преобразуем первый код в абстрактное синтаксическое дерево(ast)
        first.close()

        with open(second_file, 'r') as second:
            tree_second = ast.dump(ast.parse(second.read()))  #преобразуем второй код в абстрактное синтаксическое дерево(ast)
        second.close()

        self.results.append(str(self.levenstein(tree_first, tree_second)))

    def open_input_file(self):
        with open(self.args.input_name, 'r') as input_file: #открываем файл с расположением сравниваемых кодов
            for i in input_file.readlines():
                first_file = i.split()[0]
                second_file = i.split()[1]
                self.check_levenstein(first_file, second_file)

    def open_output_file(self):
        with open(self.args.output_name, 'w') as output_file:
            for i in self.results:
                output_file.write(i + '\n')  #записываем полученные результаты в выходной файл


run = Antiplagiat()
run.open_input_file()
run.open_output_file()
