# -*- coding: utf-8 -*-

from typing import List, Tuple


def get_filename(language: str) -> str:
    """Generate a filename for the analyzer to fix the language to use."""
    if language == "python":
        return "test.py"
    return "test.c"


def get_function_attrs(functions) -> List[Tuple]:
    """Generate a dictionary of attributes for each function in analysis results."""
    attrs:List[Tuple] = []
    for function in functions:
        attrs.append(
            (
                function.name,
                {
                    "Cyclomatic Complexity": function.cyclomatic_complexity,
                    "Lines of Code": function.nloc,
                    "Number of Parameters": function.parameter_count,
                    "Length": function.length,
                    "Fan In": function.fan_in,
                    "Fan Out": function.fan_out,
                    "Nesting Level": function.top_nesting_level,
                },
            )
        )
    return attrs
