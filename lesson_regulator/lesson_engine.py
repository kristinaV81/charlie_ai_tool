from lesson_regulator.models import LessonState
from lesson_regulator.utils.response_utils import respond
from lesson_regulator.utils.lesson_utils import _assign_lesson_stage, _is_word_left, _evaluate_user_attempt, _should_switch_word, _switch_word

DEFAULT_WORDS = ["cat", "dog", "bird"]


def start_lesson(words: list[str] | None = None) -> LessonState:
    """

    :param words: list of words to learn
    :return: lesson state
    """
    return LessonState(words=words or DEFAULT_WORDS)

def step(state: LessonState, user_input: str) -> dict:
    """

    :param state: lesson state
    :param user_input: user answer
    :return:
    {
    "message": "Charlie question",
    "stage": "practice/greeting",
    "current_word": "cat",
    "completed_words": ["cat"],
    "turns_on_current_word": 2,
    "evaluation": "partial",
    "lesson_done": False
}
    """
    stage_response = _assign_lesson_stage(state)
    if stage_response is not None:
        return stage_response

    current_word = _is_word_left(state)
    if current_word is not None:
        return current_word

    evaluation_label, evaluation_reason = _evaluate_user_attempt(state, user_input)

    if _should_switch_word(state):
        return _switch_word(
            state=state,
            user_input=user_input,
            evaluation_label=evaluation_label,
            evaluation_reason=evaluation_reason,
        )

    return respond(
        state,
        event="continue_lesson",
        user_input=user_input,
        evaluation=evaluation_label,
        evaluation_reason=evaluation_reason,
    )
