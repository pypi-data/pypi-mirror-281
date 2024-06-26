from unittest.mock import Mock, patch

import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

import psp_validation.cv_validation.analyze_traces as test_module


def test__filter_traces():
    t = np.arange(0, 100, 0.1)
    t_stim = 60
    traces = np.random.random((2, len(t))) * 30 - 70
    spike = test_module.SPIKE_TH + np.random.random()
    spike_idx = np.random.choice(np.where(t > t_stim)[0])
    traces[0, spike_idx] = spike  # add late spike

    # check that the trace with a late spike is filtered out
    res = test_module._filter_traces(t, traces, t_stim)
    assert res.shape == (1, len(t))
    assert_array_equal(res, [traces[1]])

    # check that None is return if all traces filtered out
    traces[:, spike_idx] = spike
    res = test_module._filter_traces(t, traces, t_stim)
    assert res is None


def test__get_jackknife_traces():
    traces = np.hstack((np.eye(11), np.zeros((11, 1))))
    expected = np.hstack((np.full((11, 11), 0.1) - np.eye(11) * 0.1, np.full((11, 1), 0)))

    res = test_module._get_jackknife_traces(traces)
    assert_array_equal(res, expected)


@patch.object(test_module, "_get_jackknife_traces", new=Mock())
@patch.object(test_module, "_get_peak_amplitudes")
def test_calc_cv(mock_get_amplitudes):
    np.random.seed(1)
    amplitudes = np.random.random(10)
    mock_get_amplitudes.return_value = amplitudes

    expected = np.std(amplitudes) / np.mean(amplitudes)
    assert_allclose(test_module.calc_cv(None, None, None, None, "current", jk=False), expected)

    # Since JK_var = (n-1)/n * SUM_SQUARES, and Var = 1/n * SUM_SQUARES
    expected = np.sqrt(len(amplitudes) - 1) * np.std(amplitudes) / np.mean(amplitudes)
    assert_allclose(test_module.calc_cv(None, None, None, None, "current", jk=True), expected)
