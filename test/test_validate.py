import pytest

from validator.validate import validate


@pytest.mark.parametrize(
    "code,expected",
    [
        (
            """
def CorrectFunctionName():
    ...
            """,
            True,
        ),
        (
            """
def incorrect_function_name():
    ...
            """,
            False,
        ),
        (
            """
class CorrectClassName:
    ...
            """,
            True,
        ),
        (
            """
class incorrectClassName:
    ...
            """,
            False,
        ),
        (
            """
class CorrectClassName:
    def correct_function_name():
        ...
            """,
            True,
        ),
        (
            """
class CorrectClassName:
    def IncorrectFunctionName():
        ...
            """,
            False,
        ),
        (
            """
def CorrectFunctionName():
    class CorrectClassName():
        def correct_function_name():
            ...

class CorrectClassName():
    def correct_function_name():
        class CorrectClassName2():
            ...
            """,
            True,
        ),
        (
            """
async def incorrect_function_name():
    ...
            """,
            False,
        ),
        (
            """
package main

import "fmt"

func main() {
    fmt.Println("Hello, 世界")
}
            """,
            False,
        ),
    ],
    ids=[
        "correct function name, outside of class",
        "incorrect function name, outside of class",
        "correct class name",
        "incorrect class name",
        "correct function name, inside of class",
        "incorrect function name, inside of class",
        "recursive",
        "async function",
        "syntax error",
    ],
)
def test_validate(code, expected):
    assert validate(code) == expected
