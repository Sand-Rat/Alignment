from smush import chinese_smush
import sys

if __name__ == "__main__":
    with open(sys.argv[1], "r", encoding="utf-8") as inp:
        with open(sys.argv[2], "w", encoding='utf-8') as outp:
            for line in inp:
                outp.write(chinese_smush(line) + "\n")