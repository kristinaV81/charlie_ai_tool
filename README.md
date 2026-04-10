# Word Learning Chatbot

A lesson starts with a list of target words, keeps one current focus word in the state,
and asks the LLM to generate a short child-friendly reply for that word. 
After each child response, a second LLM call evaluates the answer as `silence`, `off_topic`, `partial`, 
or `correct` based on the current focus word and lesson goal. 
The engine increases counters for the current word, keeps chat history, and moves to the next word only 
after enough successful answers. When there are no words left, the lesson switches to the goodbye stage and then finishes.

## Lesson state

The main state object is `LessonState`.

It stores these fields:
- `stage`: current lesson stage. Possible values: `greeting`, `practice`, `goodbye`, `finished`
- `words`: list of lesson words
- `current_word_index`: index of the current word in the list
- `turns_on_current_word`: how many attempts were made on the current word
- `successful_turns_on_current_word`: how many answers were accepted as `correct` for current word
- `max_turns_per_word`: how many correct answers are needed before switching to the next word
- `completed_words`: words that were already finished
- `chat_history`: recent dialogue history used for the next LLM response

There is also a computed property:
- `current_word`: returns the current focus word or `None` if the list is finished

## Answer types

The evaluator returns exactly one label:
- `silence`: the child says nothing (send space)
- `off_topic`: something unrelated to the current word or task
- `partial`: the answer is incomplete, sentence is not full
- `correct`: the child gives full sentence as an answer

## How the LLM decides between `partial` and `correct`

The evaluator receives the child response, the current focus word, the full word list,
and the lesson goal. 
It returns `partial` when the answer is relevant but incomplete, 
for example a one-word answer. 

It returns `correct` when the answer is relevant enough for the current lesson step, 
even if the grammar is not perfect.

## How to run

Export your Groq API key first:

```bash
export GROQ_API_KEY="your_api_key_here"
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit app:

```bash
streamlit run app.py
```
