import warnings
from typing import Union, List
from abc import ABC, abstractmethod


class BaseEvaluator(ABC):
    def __init__(self, candidates: List, references: List) -> None:
        self.candidates = candidates
        self.references = references

    @staticmethod
    def padding(
        candidates: List[str], references: List[str]
    ) -> Union[List[str], List[str]]:
        """_summary_

        Args:
            candidates (List[str]): The response generated from the LLM
            references (List[str]): The response to be measured against

        Returns:
            Union[List[str], List[str]]: Ensures equal length of `candidates` and `references`
        """
        _msg = str(
            """
            The length of references and candidates (hypothesis) are not same.
            """
        )
        warnings.warn(_msg)
        max_length = max(len(candidates), len(references))
        candidates.extend([""] * (max_length - len(candidates)))
        references.extend([""] * (max_length - len(references)))
        return candidates, references

    @staticmethod
    def list_to_string(l: List) -> str:
        assert (
            len(l) >= 1
        ), "Ensure the length of the message is greater than or equal to 1"

        return str(l[0])

    @abstractmethod
    def get_score(self) -> float:
        """
        Method to calculate the final result of the score function.

        Returns:
            Floating point value of the chosen evaluation metric.
        """
