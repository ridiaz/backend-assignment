from django.db import models

from django.conf import settings


# class Criteria:
#     questions = [
#         'In most ways my life is close to my ideal.',
#         'The conditions of my life are excellent.',
#         'I am satisfied with my life.',
#         'So far I have gotten the important things I want in life.',
#         'If I could live my life over, I would change almost nothing.',
#     ]


# Scoring and Interpretation Information
# Scores consist of a raw score (between 5 and 35). Higher scores represent higher life satisfaction.
# Scorers can be assigned into six well-being categories and interpretative text in provided for each. -

# - 30- 35 Extremely satisfied
# - 25 - 29 Satisfied
# - 20 - 24 Slightly satisfied
# - 15 - 19 Slightly dissatisfied
# - 10 - 14 Dissatisfied
# - 5 - 9 Extremely dissatisfied


class CheckIn(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    responses = models.JSONField(default=list)
    created = models.DateTimeField(auto_now_add=True)
