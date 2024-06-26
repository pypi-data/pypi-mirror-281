from evaluator_blog import RougeScore

candidate = "it is dog"
reference = "it's dog"


def test_rouge_score():
    rg = RougeScore(
        candidates=candidate,
        references=reference,
    )
    assert type(rg.get_score()) == dict
