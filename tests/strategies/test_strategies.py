#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_strategies

Tests for `strategies` module.
"""

from __future__ import unicode_literals
import unittest
import nose
import pandas as pd
from functools import wraps

from xlseries.strategies.discover.parameters import Parameters
from xlseries.utils.case_loaders import load_original_case
from xlseries.utils.case_loaders import load_parameters_case
from xlseries.utils.case_loaders import load_expected_case
from xlseries.utils.data_frame import compare_period_ranges
from xlseries.utils.data_frame import compare_data_frames
from xlseries.strategies.strategies import ParameterDiscovery


# @unittest.skip("skip")
class ParameterDiscoveryTestCase(unittest.TestCase):

    # @unittest.skip("skip")

    def test_get_period_ranges(self):

        test_wb = load_original_case(2)
        params = load_parameters_case(2)
        strategy_obj = ParameterDiscovery(test_wb, params)
        ws = strategy_obj.wb.active

        pr_d = pd.period_range("20020304", "20140410", freq="D")
        pr_m = pd.period_range("20020301", "20140301", freq="M")

        period_ranges = list(strategy_obj._get_period_ranges(ws, params))

        self.assertTrue(compare_period_ranges(pr_d, period_ranges[0]))
        self.assertTrue(compare_period_ranges(pr_m, period_ranges[1]))

    def test_generate_attempts(self):
        params = Parameters({
            "alignment": "vertical",
            "headers_coord": ["B1", "C1"],
            "data_starts": 2,
            "data_ends": 256,
            "frequency": "M",
            "time_header_coord": "A1",
            "time_multicolumn": True,
            "time_composed": True,
            "time_alignment": 0,
            "continuity": True,
            "blank_rows": True,
            "missings": None,
            "missing_value": None,
            "series_names": None
        })

        non_discovered = ["missings"]
        attempts = ParameterDiscovery._generate_attempts(non_discovered,
                                                         params)
        p1 = Parameters({
            "alignment": "vertical",
            "headers_coord": ["B1", "C1"],
            "data_starts": 2,
            "data_ends": 256,
            "frequency": "M",
            "time_header_coord": "A1",
            "time_multicolumn": True,
            "time_composed": True,
            "time_alignment": 0,
            "continuity": True,
            "blank_rows": True,
            "missings": True,
            "missing_value": None,
            "series_names": None
        })
        p2 = Parameters({
            "alignment": "vertical",
            "headers_coord": ["B1", "C1"],
            "data_starts": 2,
            "data_ends": 256,
            "frequency": "M",
            "time_header_coord": "A1",
            "time_multicolumn": True,
            "time_composed": True,
            "time_alignment": 0,
            "continuity": True,
            "blank_rows": True,
            "missings": False,
            "missing_value": None,
            "series_names": None
        })

        self.assertEqual(len(attempts), 2)

        for param_name in attempts[0]:
            self.assertEqual(p1[param_name], attempts[0][param_name])
        for param_name in attempts[1]:
            self.assertEqual(p2[param_name], attempts[1][param_name])

    def test_param_combinations_generator(self):

        missings_dict = {
            "missings": [True, False],
            "blank_rows": [True, False]
        }
        exp_combinations = [
            {"missings": True, "blank_rows": True},
            {"missings": True, "blank_rows": False},
            {"missings": False, "blank_rows": True},
            {"missings": False, "blank_rows": False}
        ]

        combs = list(ParameterDiscovery._param_combinations_generator(
            missings_dict))

        for exp_comb in exp_combinations:
            self.assertIn(exp_comb, combs)
        for comb in combs:
            self.assertIn(comb, exp_combinations)


if __name__ == '__main__':
    # unittest.main()
    nose.run(defaultTest=__name__)
