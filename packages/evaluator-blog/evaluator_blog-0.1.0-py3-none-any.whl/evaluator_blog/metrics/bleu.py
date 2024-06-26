from typing import List, Callable, Optional
from src.evaluator_blog.evaluator import BaseEvaluator

from nltk.translate.bleu_score import corpus_bleu, SmoothingFunction

"""
BLEU implementation from NLTK
"""


class BLEUScore(BaseEvaluator):
    def __init__(
        self,
        candidates: List[str],
        references: List[str],
        weights: Optional[List[float]] = None,
        smoothing_function: Optional[Callable] = None,
        auto_reweigh: Optional[bool] = False,
    ) -> None:
        """
        Calculate BLEU score (Bilingual Evaluation Understudy) from
        Papineni, Kishore, Salim Roukos, Todd Ward, and Wei-Jing Zhu. 2002.
        "BLEU: a method for automatic evaluation of machine translation."
        In Proceedings of ACL. https://aclanthology.org/P02-1040.pdf

            Args:
                weights (Optional[List[float]], optional): The weights that must be applied to each bleu_score. Defaults to None.
                smoothing_function (Optional[Callable], optional): A callable function to overcome the problem of the sparsity of training data by adding or adjusting the probability mass distribution of words. Defaults to None.
                auto_reweigh (Optional[bool], optional): Uniformly re-weighting based on maximum hypothesis lengths if largest order of n-grams < 4 and weights is set at default. Defaults to False.
        """
        super().__init__(candidates, references)

        # Check if `weights` is provided
        if weights is None:
            self.weights = [1, 0, 0, 0]
        else:
            self.weights = weights

        # Check if `smoothing_function` is provided
        # If `None` defaulted to method0
        if smoothing_function is None:
            self.smoothing_function = SmoothingFunction().method0
        else:
            self.smoothing_function = smoothing_function

        # If `auto_reweigh` enable it
        self.auto_reweigh = auto_reweigh

    def get_score(
        self,
    ) -> float:
        """
        Calculate the BLEU score for the given candidates and references.

        Args:
            candidates (List[str]): List of candidate sentences
            references (List[str]): List of reference sentences
            weights (Optional[List[float]], optional): Weights for BLEU score calculation. Defaults to (1.0, 0, 0, 0)
            smoothing_function (Optional[function]): Smoothing technique to for segment-level BLEU scores

        Returns:
            float: The calculated BLEU score.
        """
        # Check if the length of candidates and references are equal
        if len(self.candidates) != len(self.references):
            self.candidates, self.references = self.padding(
                self.candidates, self.references
            )

        # Calculate the BLEU score
        return corpus_bleu(
            list_of_references=self.references,
            hypotheses=self.candidates,
            weights=self.weights,
            smoothing_function=self.smoothing_function,
            auto_reweigh=self.auto_reweigh,
        )
