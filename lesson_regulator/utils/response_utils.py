from lesson_regulator.models import LessonState
from lesson_regulator.utils.response_builder import build_message


def make_response(
    state: LessonState,
    message: str,
    evaluation: str | None = None,
    evaluation_reason: str | None = None,
) -> dict:
    """
    function to return a response

    :param state: lesson state
    :param message: Charlie message
    :param evaluation: classification on answer
    :param evaluation_reason: reason of classification from llm
    :return:
    """
    return {
        "message": message,
        "stage": state.stage,
        "current_word": state.current_word,
        "completed_words": list(state.completed_words),
        "turns_on_current_word": state.attempt_on_current_word,
        "evaluation": evaluation,
        "lesson_done": state.stage == "finished",
    }


def change_word(state: LessonState) -> str | None:
    """

    :param state: lesson state
    :return:
        next word to learn/ practise
    """
    current_word = state.current_word

    if current_word is None:
        return None

    if current_word not in state.completed_words:
        state.completed_words.append(current_word)

    state.current_word_index += 1

    # reset counters
    state.attempt_on_current_word = 0
    state.successful_attempts_on_current_word = 0

    if state.current_word_index >= len(state.words):
        return None

    return state.current_word


def respond(
    state: LessonState,
    event: str,
    user_input: str | None = None,
    evaluation: str | None = None,
    evaluation_reason: str | None = None,
) -> dict:
    """
    :param state: lesson state
    :param event: lesson started/finished/continue
    :param user_input: user answer
    :param evaluation: llm evaluation label
    :param evaluation_reason: reason of evaluation label from llm
    :return:
        dict with Lesson state and attempts info
    """
    message = build_message(
        event=event,
        state=state,
        user_input=user_input,
        evaluation_label=evaluation,
    )

    state.chat_history.append({"role": "assistant", "content": message})

    return make_response(
        state=state,
        message=message,
        evaluation=evaluation,
        evaluation_reason=evaluation_reason,
    )
