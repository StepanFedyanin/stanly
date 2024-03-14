from mw_calc.models import BaseChunk
from django.db import models


class Chunk(BaseChunk):
    test = models.CharField(max_length=255, blank=True)
