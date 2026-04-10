import streamlit as st

from lesson_regulator.lesson_engine import start_lesson, step


st.set_page_config(page_title="Charlie AI Lesson", page_icon="🦊", layout="centered")


def init_session() -> None:
    if "lesson_started" not in st.session_state:
        st.session_state.lesson_started = False

    if "lesson_state" not in st.session_state:
        st.session_state.lesson_state = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "last_response" not in st.session_state:
        st.session_state.last_response = None


def reset_lesson() -> None:
    st.session_state.lesson_started = False
    st.session_state.lesson_state = None
    st.session_state.chat_history = []
    st.session_state.last_response = None


def start_new_lesson() -> None:
    state = start_lesson(words=["cat", "dog", "bird"])
    first_response = step(state, "")

    st.session_state.lesson_started = True
    st.session_state.lesson_state = state
    st.session_state.last_response = first_response
    st.session_state.chat_history = [
        {"role": "assistant", "content": first_response["message"]}
    ]


def send_user_message(user_text: str) -> None:
    state = st.session_state.lesson_state
    if state is None:
        return

    st.session_state.chat_history.append({"role": "user", "content": user_text})

    response = step(state, user_text)
    st.session_state.last_response = response
    st.session_state.chat_history.append(
        {"role": "assistant", "content": response["message"]}
    )

    if state.stage == "goodbye":
        final_response = step(state, "")
        st.session_state.last_response = final_response
        st.session_state.chat_history.append(
            {"role": "assistant", "content": final_response["message"]}
        )


init_session()

st.title("Charlie AI 🦊")

with st.sidebar:
    st.subheader("Lesson logs")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Start lesson", use_container_width=True):
            start_new_lesson()

    with col2:
        if st.button("Reset", use_container_width=True):
            reset_lesson()

    st.divider()

    if st.session_state.lesson_state is not None:
        state = st.session_state.lesson_state

        st.subheader("Progress")
        st.write(f"**Stage:** {state.stage}")
        st.write(f"**Current word:** {state.current_word}")
        st.write(f"**Completed:** {', '.join(state.completed_words) if state.completed_words else '-'}")
        st.write(f"**All words:** {', '.join(state.words)}")

        if st.session_state.last_response is not None:
            st.divider()
            st.subheader("Last turn")
            st.write(f"**Attempts on current word:** {state.attempt_on_current_word}")
            st.write(f"**Evaluation:** {st.session_state.last_response['evaluation']}")
            st.write(f"**Lesson done:** {st.session_state.last_response['lesson_done']}")
    else:
        st.info("Start a lesson to see progress.")

st.divider()

chat_box = st.container()

with chat_box:
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if not st.session_state.lesson_started:
    st.info("Click **Start lesson** to begin.")
else:
    if st.session_state.lesson_state and st.session_state.lesson_state.stage != "finished":
        user_input = st.chat_input("Type the child's answer here...")

        if user_input is not None:
            send_user_message(user_input)
            st.rerun()
    else:
        st.success("Lesson finished. You can start a new one.")
