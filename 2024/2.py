from pathlib import Path
from helpers import read_file, parse_to_matrix, Matrix


class MatrixExtended(Matrix):
    def count_safe_rows(self):
        count = 0
        for row in self.matrix:
            row_safe = self.is_row_safe(row=row)

            if row_safe:
                # print(row)
                count += 1

        return count

    def count_safe_rows_with_one_mistake(self):
        count = 0

        for row in self.matrix:
            # print(row)
            row_safe = self.is_row_safe(row=row)

            if row_safe:
                # print(row)
                count += 1
            else:
                # now check by removing 1 number

                for i in range(len(row)):
                    new_row = row[::]
                    new_row.pop(i)
                    # print(new_row)

                    row_safe = self.is_row_safe(row=new_row)
                    if row_safe:
                        # print(new_row)
                        count += 1
                        break
            # print()

        return count

    def is_row_safe(self, row):
        row_reversed = row[::-1]
        row_sorted = sorted(row)

        if (
            row_sorted == row or row_reversed == row_sorted
        ):  # or row_sorted != row_reversed:
            pass
        else:
            return False

        for i, num in enumerate(row):
            if i > (len(row) - 2):
                continue

            # print(i, num)
            next_num = row[i + 1]

            level_diff = abs(num - next_num)
            if level_diff < 1 or level_diff > 3:
                return False

        return True


PATH = Path(__file__)
YEAR = str(PATH).split("\\")[-2]
DATA = read_file(f"./{YEAR}/{PATH.name.split('.')[0]}.txt")


def part1():
    matrix = MatrixExtended(DATA)
    # print(matrix)

    num_safe_rows = matrix.count_safe_rows()
    return num_safe_rows


def part2():
    matrix = MatrixExtended(DATA)
    # print(matrix)

    num_safe_rows = matrix.count_safe_rows_with_one_mistake()
    return num_safe_rows


def main():
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")


main()
