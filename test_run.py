from lesson_regulator.lesson_engine import start_lesson, step

def main() -> None:
    state = start_lesson()

    response = step(state, "")
    print(f"Charlie: {response['message']}")

    while state.stage != "finished":
        user_input = input("You: ")
        response = step(state, user_input)
        print(f"Charlie: {response['message']}")
        print(
            f"[stage={response['stage']}, "
            f"current_word={response['current_word']}, "
            f"completed={response['completed_words']}, "
            f"attempts={response['attempts']}, "
            f"evaluation={response['evaluation']}]"
        )

        if state.stage == "goodbye":
            response = step(state, "")
            print(f"Charlie: {response['message']}")


if __name__ == "__main__":
    main()