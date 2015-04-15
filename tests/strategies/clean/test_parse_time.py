#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_clean_ti_strategies
----------------------------------

Tests for `clean_ti_strategies` module.
"""
from __future__ import unicode_literals
import unittest
import nose
import arrow
import json
import os
from functools import wraps
import re

from xlseries.strategies.clean.parse_time import ParseComposedQuarterTime1
from xlseries.strategies.clean.parse_time import ParseComposedQuarterTime2
from xlseries.strategies.clean.parse_time import ParseComposedMonthTime1
from xlseries.strategies.clean.parse_time import ParseComposedMonthTime2
from xlseries.strategies.clean.parse_time import ParseSimpleTime
from xlseries.utils.case_loaders import load_parameters_case
from xlseries.utils.path_finders import abs_path


def load_case_number():
    """Decorate a test loading the case number taken from test name."""

    def fn_decorator(fn):
        last_word = fn.__name__.split("_")[-1]
        case_num = last_word.replace("case", "").strip()

        @wraps(fn)
        def fn_decorated(*args, **kwargs):
            kwargs["case_num"] = case_num
            fn(*args, **kwargs)

        return fn_decorated
    return fn_decorator


# @unittest.skip("skip")
class ParseSimpleTimeTest(unittest.TestCase):

    def test_parse_simple_time_case1(self):
        params = load_parameters_case(1)
        value = "17-12.09"
        last_time = None
        # raise Exception(params[0])
        new_value = ParseSimpleTime._parse_time(value, last_time, params[0])

        exp_value = arrow.get(2009, 12, 17)

        self.assertEqual(new_value, exp_value)


class ParseComposedTimeTest(unittest.TestCase):

    def parse_time_values(self, strategy, values, params):

        last_time = None

        new_values = []
        for value in values:
            # print value.encode("utf-8", "ignore")
            new_time = strategy._parse_time(value,
                                            last_time, params)
            new_values.append(new_time)
            last_time = new_time

        return new_values

    def run_parse_time_case(self, case_num, strategy):
        """Run a parse time test case using provided strategy.

        Args:
            case_num: Number of case to load.
            strategy: Strategy to parse the case.
        """
        case = "test_case" + unicode(case_num)

        with open(os.path.join(abs_path("original"),
                               "parse_time.json")) as f:
            values = json.load(f)[case]

        with open(os.path.join(abs_path("expected"),
                               "parse_time.json")) as f:
            exp_vals = json.load(f)[case]
            exp_vals = [eval(value) for value in exp_vals]

        rule = re.compile("(\d)")
        case_num_int = int(rule.match(case_num).group())
        params = load_parameters_case(case_num_int)

        new_values = self.parse_time_values(strategy, values, params)

        msg = " ".join([str(case), ":", str(new_values),
                        "are not equal to", str(exp_vals)])
        assert new_values == exp_vals, msg

    @load_case_number()
    # @unittest.skip("skip")
    def test_parse_time_case3(self, case_num):
        """Parse a list of time values using _parse_time method."""
        self.run_parse_time_case(case_num, ParseComposedQuarterTime1)

    @load_case_number()
    # @unittest.skip("skip")
    def test_parse_time_case4(self, case_num):
        """Parse a list of time values using _parse_time method."""
        self.run_parse_time_case(case_num, ParseComposedQuarterTime2)

    @load_case_number()
    # @unittest.skip("skip")
    def test_parse_time_case5(self, case_num):
        """Parse a list of time values using _parse_time method."""
        self.run_parse_time_case(case_num, ParseComposedMonthTime1)

    @load_case_number()
    # @unittest.skip("skip")
    def test_parse_time_case5b(self, case_num):
        """Parse a list of time values using _parse_time method."""
        self.run_parse_time_case(case_num, ParseComposedMonthTime2)

    @load_case_number()
    @unittest.skip("skip")
    def test_parse_time_case6(self, case_num):
        """Parse a list of time values using _parse_time method."""
        # TODO: Implement a strategy for this case!
        self.run_parse_time_case(case_num, None)

    @load_case_number()
    @unittest.skip("skip")
    def test_parse_time_case6b(self, case_num):
        """Parse a list of time values using _parse_time method."""
        # TODO: Implement a strategy for this case!
        self.run_parse_time_case(case_num, None)

if __name__ == '__main__':
    nose.run(defaultTest=__name__)
    # unittest.main()
