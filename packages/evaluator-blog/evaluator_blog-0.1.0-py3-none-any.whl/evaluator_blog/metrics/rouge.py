import warnings
from typing import List, Union, Dict, Callable, Tuple, Optional
from ..evaluator import BaseEvaluator
from rouge_score import rouge_scorer


class RougeScore(BaseEvaluator):
    def __init__(
        self,
        candidates: List,
        references: List,
        rouge_types: Optional[Union[str, Tuple[str]]] = [
            "rouge1",
            "rouge2",
            "rougeL",
            "rougeLsum",
        ],
        use_stemmer: Optional[bool] = False,
        split_summaries: Optional[bool] = False,
        tokenizer: Optional[Callable] = None,
    ) -> None:
        super().__init__(candidates, references)

        # Default `rouge_types` is all, else the user specified
        if isinstance(rouge_types, str):
            self.rouge_types = [rouge_types]
        else:
            self.rouge_types = rouge_types

        # Enable `use_stemmer` to remove word suffixes to improve matching capability
        self.use_stemmer = use_stemmer

        # If enabled checks whether to add newlines between sentences for `rougeLsum`
        self.split_summaries = split_summaries

        # Enable `tokenizer` if user defined or else use the `rouge_scorer` default
        # https://github.com/google-research/google-research/blob/master/rouge/rouge_scorer.py#L83
        if tokenizer:
            self.tokenizer = tokenizer
        else:
            self.tokenizer = None
            _msg = str(
                """
                Utilizing the default tokenizer
                """
            )
            warnings.warn(_msg)

    def get_score(self) -> Dict:
        """
        Returns:
            Dict: JSON value of the evaluation for the corresponding metric
        """
        scorer = rouge_scorer.RougeScorer(
            rouge_types=self.rouge_types,
            use_stemmer=self.use_stemmer,
            tokenizer=self.tokenizer,
            split_summaries=self.split_summaries,
        )

        return scorer.score(self.list_to_string(self.candidates), self.list_to_string(self.references))
