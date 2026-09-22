import uuid
from .models import Experiment

class ExperimentManager:
    def create(self, offer_id: str, channel: str, variant: str) -> Experiment:
        return Experiment(str(uuid.uuid4()), offer_id, channel, variant)

    def update(self, experiment: Experiment, *, impressions=0, clicks=0,
               conversions=0, revenue=0.0) -> Experiment:
        experiment.impressions += impressions
        experiment.clicks += clicks
        experiment.conversions += conversions
        experiment.revenue += revenue
        return experiment
