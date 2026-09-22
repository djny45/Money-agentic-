from app.learning import LearningEngine

def test_waits_for_sample():
    result = LearningEngine().evaluate(clicks=5, conversions=1, revenue=1.0)
    assert result.action == "collect_more_data"

def test_pauses_zero_conversion():
    result = LearningEngine().evaluate(clicks=30, conversions=0, revenue=0.0)
    assert result.action == "pause_experiment"
