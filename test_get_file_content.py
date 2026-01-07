import os
from functions.get_file_content import get_file_content

def test_get_file_content() -> None:

    # TEST 1
    result = get_file_content("calculator", "main.py")
    print(result)

    # TEST 2
    result = get_file_content("calculator", "pkg/calculator.py")
    print(result)

    # TEST 3
    result = get_file_content("calculator", "bin/cat")
    print(result)

    # TEST 4
    result = get_file_content("calculator", "pkg/does_not_exist.py")
    print(result)

if __name__ == "__main__":
    test_get_file_content()