import os
from functions.get_files_info import get_files_info

def test_get_files_info() -> None:

    # TEST 1
    # Expected to print info of current directory
    result = get_files_info("calculator", ".")
    print("Result for current directory:\n")
    print(result)

    # TEST 2
    # Expected to print info of 'pkg' subdirectory
    result = get_files_info("calculator", "pkg")
    print("Result for 'pkg' directory:\n")
    print(result)

    # TEST 3
    # Expected to return error (outside permitted directory)
    result = get_files_info("calculator", "/bin")
    print("Result for '/bin' directory:\n")
    print(result)

    # TEST 4
    # Expected to return error (outside permitted directory)
    result = get_files_info("calculator", "../")
    print("Result for '../' directory:\n")
    print(result)

if __name__ == "__main__":
    test_get_files_info()