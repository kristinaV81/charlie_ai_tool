from lesson_regulator.evaluator import evaluate_answer
from lesson_regulator.models import LessonState
from lesson_regulator.utils.response_utils import change_word, respond


def _assign_lesson_stage(state: LessonState) -> dict | None:
    """
    assign stage of the class and generate response
    :param state: lesson state
    :return: class stage
    """
    if state.stage == "finished":
        return {
            "message": "Lesson is already finished.",
            "stage": state.stage,
            "current_word": state.current_word,
            "completed_words": list(state.completed_words),
            "attempt_on_current_word": state.attempt_on_current_word,
            "evaluation": None,
            "evaluation_reason": None,
            "lesson_done": True,
        }

    if state.stage == "greeting":
        state.stage = "practice"
        return respond(state, event="lesson_started")

    if state.stage == "goodbye":
        state.stage = "finished"
        return respond(state, event="lesson_completed")

    if state.stage != "practice":
        return {
            "message": "Something went wrong with the lesson state.",
            "stage": state.stage,
            "current_word": state.current_word,
            "completed_words": list(state.completed_words),
            "attempt_on_current_word": state.attempt_on_current_word,
            "evaluation": None,
            "evaluation_reason": None,
            "lesson_done": state.stage == "finished",
        }

    return None


def _is_word_left(state: LessonState) -> dict | None:
    """
    check if we have more words to learn
    :param state: lesson state
    :return: word that left
    """
    if state.current_word is None:
        state.stage = "goodbye"
        return respond(state, event="lesson_completed")
    return None


def _evaluate_user_attempt(state: LessonState, user_input: str) -> tuple[str, str]:
    """
    evaluate user answer
    :param state: lesson state
    :param user_input: user answer
    :return:
        label (correct/partial correct/ off_topic/ silence)
        reason - a short reason why llm decided to classify answer like that
    """
    state.chat_history.append({"role": "user", "content": user_input})

    evaluation_result = evaluate_answer(
        user_input=user_input,
        target_word=state.current_word,
        all_words=state.words,
    )

    state.attempt_on_current_word += 1

    if evaluation_result["label"] == "correct":
        state.successful_attempts_on_current_word += 1

    return evaluation_result["label"], evaluation_result["reason"]


def _should_switch_word(state: LessonState) -> bool:
    """
    check if we should switch the word
    :param state: lesson state
    :return:
    """
    return state.successful_attempts_on_current_word >= state.max_attempts_per_word


def _switch_word( state: LessonState, user_input: str, evaluation_label: str, evaluation_reason: str, ) -> dict:
    """

    :param state: lesson state
    :param user_input: user answer
    :param evaluation_label: evaluation of the answer from llm
    :param evaluation_reason: reason of classification from llm
    :return:
         return {
        "message": message,
        "stage": state.stage,
        "current_word": state.current_word,
        "completed_words": list(state.completed_words),
        "turns_on_current_word": state.attempt_on_current_word,
        "evaluation": evaluation,
        "lesson_done": state.stage == "finished",
    }
    """
    next_word = change_word(state)

    if next_word is None:
        state.stage = "goodbye"
        return respond(
            state,
            event="lesson_completed",
            user_input=user_input,
            evaluation=evaluation_label,
            evaluation_reason=evaluation_reason,
        )

    return respond(
        state,
        event="switch_word",
        user_input=user_input,
        evaluation=evaluation_label,
        evaluation_reason=evaluation_reason,
    )
