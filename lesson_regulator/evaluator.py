import json
from typing import Literal, TypedDict

from llm_tools.evaluation_prompt import EVALUATION_SYSTEM_PROMPT
from llm_tools.llm_client import generate_raw_completion


EvaluationLabel = Literal["silence", "off_topic", "partial", "correct"]


class EvaluationResult(TypedDict):
    label: EvaluationLabel
    reason: str


def evaluate_with_llm(
    user_input: str,
    target_words: list[str],
    current_word: str | None,
    lesson_goal: str = "The child should use the target word in a full sentence.",
) -> EvaluationResult:
    """

    :param user_input: user answer
    :param target_words: words to learn
    :param current_word: current word we are practising
    :param lesson_goal: what to expect from user
    :return:
        answer classification, reason of classification from llm
    """
    user_prompt = f"""
                        Target words: {target_words}
                        Current focus word: {current_word}
                        Lesson goal: {lesson_goal}
                        
                        Child response:
                        {user_input!r}
                        
                        Classify the child's response.
                        Return JSON only.
                    """

    raw = generate_raw_completion(
        system_prompt=EVALUATION_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        temperature=0,
        max_tokens=120,
    )

    try:
        data = json.loads(raw)
        label = data.get("label", "partial")
        reason = data.get("reason", "")

        if label not in {"silence", "off_topic", "partial", "correct"}:
            label = "partial"
        print(f'label: {label}, reason: {reason}')
        return {
            "label": label,
            "reason": reason,
        }
    except Exception:
        return {
            "label": "partial",
            "reason": "Fallback: could not parse evaluator output.",
        }

def evaluate_answer(user_input: str, target_word: str, all_words: list[str]) -> dict:
    return evaluate_with_llm(user_input=user_input, target_words=all_words, current_word=target_word)
