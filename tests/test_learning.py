from app.learning import LearningEngine

def test_waits_for_sample():
    result = LearningEngine().evaluate(clicks=5, conversions=1, revenue=1.0)
    assert result.action == "collect_more_data"

def test_pauses_zero_conversion():
    result = LearningEngine().evaluate(clicks=30, conversions=0, revenue=0.0)
    assert result.action == "pause_experiment"


def test_revises_negative_profit():
    result = LearningEngine().evaluate(clicks=50, conversions=2, revenue=1.0, spend=2.0)
    assert result.action == "revise_strategy"

def test_retains_positive_profit():
    result = LearningEngine().evaluate(clicks=50, conversions=2, revenue=4.0, spend=1.0)
    assert result.action == "retain_and_test"
