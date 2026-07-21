# المسار: fallacy_analyzer/fallacy_analyzer/__init__.py

"""
حزمة تحليل المغالطات المنطقية (Fallacy Analyzer Package)
"""

from .decision_tree import LogicalFallacyClassifier
from .nlp_pipeline import ArgumentNLPPipeline

__version__ = "1.0.0"
__all__ = ["LogicalFallacyClassifier", "ArgumentNLPPipeline"]