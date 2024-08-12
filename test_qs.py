import pytest
import pathlib
import pandas as pd
import numpy as np
from HW5_q1 import QuestionnaireAnalysis

def test_valid_input():
    fname = pathlib.Path(__file__).parent / "data.json"
    q = QuestionnaireAnalysis(fname)
    assert q.filename == fname

def test_str_input():
    fname = str(pathlib.Path(__file__).parent / "data.json")
    q = QuestionnaireAnalysis(fname)
    assert q.filename == fname

def test_missing_file():
    fname = pathlib.Path("teststs.fdfd")
    with pytest.raises(ValueError):
        QuestionnaireAnalysis(fname)

def test_data_attr_exists():
    fname = "data.json"
    q = QuestionnaireAnalysis(fname)
    q.read_data()
    assert hasattr(q, 'data')

def test_data_attr_is_df():
    fname = "data.json"
    q = QuestionnaireAnalysis(fname)
    q.read_data()
    assert isinstance(q.data, pd.DataFrame)

def test_correct_age_distrib_hist():
    fname = "data.json"
    q = QuestionnaireAnalysis(fname)
    q.read_data()
    hist, _ = q.show_age_distrib()
    truth = np.load("tests_data/q1_hist.npz")
    assert np.array_equal(hist, truth['hist'])

def test_correct_age_distrib_edges():
    fname = "data.json"
    q = QuestionnaireAnalysis(fname)
    q.read_data()
    _, bin_edges = q.show_age_distrib()
    truth = np.load("tests_data/q1_hist.npz")
    assert np.array_equal(bin_edges, truth['bin_edges'])

def test_email_validation():
    truth = pd.read_csv("tests_data/q2_email.csv")
    fname = "data.json"
    q = QuestionnaireAnalysis(fname)
    q.read_data()
    q.remove_rows_without_mail()
    pd.testing.assert_frame_equal(q.data, truth)

def test_fillna_rows():
    truth = np.load("tests_data/q3_fillna.npy")
    fname = "data.json"
    q = QuestionnaireAnalysis(fname)
    q.read_data()
    q.fill_na_with_mean()
    np.testing.assert_array_equal(q.data.to_numpy(), truth)

def test_fillna_df():
    truth = pd.read_csv("tests_data/q3_fillna.csv")
    fname = "data.json"
    q = QuestionnaireAnalysis(fname)
    q.read_data()
    q.fill_na_with_mean()
    pd.testing.assert_frame_equal(q.data, truth)

def test_score_exists():
    fname = "data.json"
    q = QuestionnaireAnalysis(fname)
    q.read_data()
    q.score_subjects()
    assert 'score' in q.data.columns

def test_score_dtype():
    fname = "data.json"
    q = QuestionnaireAnalysis(fname)
    q.read_data()
    q.score_subjects()
    assert q.data['score'].dtype == np.dtype('int64')

def test_score_results():
    truth = pd.read_csv('tests_data/q4_score.csv', index_col=0).astype("UInt8").squeeze()
    fname = "data.json"
    q = QuestionnaireAnalysis(fname)
    q.read_data()
    q.score_subjects()
    pd.testing.assert_series_equal(q.data['score'], truth['score'])

def test_correlation():
    truth = pd.read_csv("tests_data/q5_corr.csv").set_index(["gender", "age"])
    fname = "data.json"
    q = QuestionnaireAnalysis(fname)
    q.read_data()
    correlation = q.data.corr()
    pd.testing.assert_frame_equal(correlation, truth)
