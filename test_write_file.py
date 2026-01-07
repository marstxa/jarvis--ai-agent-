import os
from functions.write_file import write_file

def test_write_file() -> None:

    # TEST 1
    result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print(result)

    # TEST 2
    result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print(result)

    # TEST 3
    result = write_file("calculator", "/tmp/temp.text", "this should not be allowed")
    print(result)

if __name__ == "__main__":
    test_write_file()