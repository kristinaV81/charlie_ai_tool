from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class LessonState:
    """
    Lesson entity with main arguments
    """
    stage: str = "greeting"  # greeting | practice | goodbye | finished
    words: List[str] = field(default_factory=lambda: ["cat", "dog", "bird"])
    current_word_index: int = 0
    attempt_on_current_word: int = 0
    successful_attempts_on_current_word: int = 0
    max_attempts_per_word: int = 3
    completed_words: List[str] = field(default_factory=list)
    chat_history: List[Dict[str, str]] = field(default_factory=list)

    @property
    def current_word(self) -> str | None:
        if 0 <= self.current_word_index < len(self.words):
            return self.words[self.current_word_index]
        return None