from llm_tools.charlie_prompt import BASE_CHARLIE_PROMPT
from llm_tools.llm_client import generate_charlie_message
from lesson_regulator.models import LessonState


def build_message(
    event: str,
    state: LessonState,
    user_input: str | None = None,
    evaluation_label: str | None = None,
) -> str:

    messages = _build_messages_for_llm(
        state=state,
        event=event,
        user_input=user_input,
        evaluation_label=evaluation_label,
    )

    try:
        return generate_charlie_message(BASE_CHARLIE_PROMPT, messages)
    except Exception:
        return _fallback_message(
            event=event,
            current_word=state.current_word,
            evaluation_label=evaluation_label,
        )


def _build_messages_for_llm(
    state: LessonState,
    event: str,
    user_input: str | None = None,
    evaluation_label: str | None = None,
) -> list[dict]:
    messages: list[dict] = []

    for msg in state.chat_history[-8:]:
        messages.append(msg)

    context = (
        f"Target words: {state.words}. "
        f"Current focus word: {state.current_word}. "
        f"Completed words: {state.completed_words}. "
        f"Turns on current word: {state.attempt_on_current_word}/{state.max_attempts_per_word}."
    )

    if event == "lesson_started":
        messages.append(
            {
                "role": "user",
                "content": (
                    f"{context} "
                    f"Start the lesson with a playful hook. "
                    f"Focus on the current word. "
                    f"Ask one very short question or give one short sentence to repeat."
                ),
            }
        )
        return messages

    if event == "continue_lesson":
        messages.append(
            {
                "role": "user",
                "content": (
                    f"{context} "
                    f"The user said: '{user_input}'. "
                    f"The response classification is: '{evaluation_label}'. "
                    f"Continue the lesson. "
                    f"IMPORTANT: stay only on the current focus word '{state.current_word}' "
                    f"Do not move to the next word unless the event is 'switch_word'. "
                    f"If classification is 'partial', guide the child to a full sentence. "
                    f"If classification is 'silence', encourage gently and give a short model sentence. "
                    f"If classification is 'off_topic', gently bring the child back to the current word. "
                    f"if classification is 'off_topic' make a sentence including off_topic word plus {state.current_word}"
                    f"If classification is 'correct', praise the child and expand a little."
                ),
            }
        )

    if event == "switch_word":
        messages.append(
            {
                "role": "user",
                "content": (
                    f"{context} "
                    f"Move to the next target word: '{state.current_word}'. "
                    f"Start a new playful mini-task for this word."
                ),
            }
        )
        return messages

    if event == "lesson_completed":
        messages.append(
            {
                "role": "user",
                "content": (
                    f"{context} "
                    f"The lesson is complete. "
                    f"Say goodbye in a warm, playful, very short way."
                ),
            }
        )
        return messages

    messages.append(
        {
            "role": "user",
            "content": (
                f"{context} Continue the lesson in a short playful way."
            ),
        }
    )
    return messages


def _fallback_message(
    event: str,
    current_word: str | None,
    evaluation_label: str | None,
) -> str:
    if event == "lesson_started":
        return f"Hi! I am Charlie 🦊 Let’s practice word {current_word}!"

    if event == "switch_word":
        return f"Great job! Now let’s practise word {current_word} ✨"

    if event == "lesson_completed":
        return "Great job today! Bye-bye! 🦊✨"

    if evaluation_label == "silence":
        return f"That’s okay 🦊 Say: I see a {current_word}"

    if evaluation_label == "off_topic":
        return f"Let’s go back to {current_word} 🦊 Can you say a sentence?"

    if evaluation_label == "partial":
        return f"Nice try! Say a full sentence with {current_word} 🦊"

    return f"Great! Say one more sentence with {current_word} 🦊"
