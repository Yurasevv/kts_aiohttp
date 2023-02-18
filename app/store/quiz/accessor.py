from typing import Optional

from app.base.base_accessor import BaseAccessor
from app.quiz.models import Theme, Question, Answer
from app.quiz.schemes import QuestionSchema, AnswerSchema


class QuizAccessor(BaseAccessor):
    async def create_theme(self, title: str) -> Theme:
        theme = Theme(id=self.app.database.next_theme_id, title=str(title))
        self.app.database.themes.append(theme)
        return theme

    async def get_theme_by_title(self, title: str) -> Optional[Theme]:
        for t in self.app.database.themes:
            if title == t.title:
                return t
        return None

    async def get_theme_by_id(self, id_: int) -> Optional[Theme]:
        for t in self.app.database.themes:
            if id_ == t.id:
                return t
        return None

    async def list_themes(self) -> list[Theme]:
        return self.app.database.themes

    async def get_question_by_title(self, title: str) -> Optional[Question]:
        for q in self.app.database.questions:
            if q.title == title:
                return q
        return None

    async def create_question(
            self, title: str, theme_id: int, answers: list[Answer]
    ) -> Question:
        question = Question(
            title=title,
            id=self.app.database.next_question_id,
            theme_id=theme_id,
            answers=answers
        )
        self.app.database.questions.append(question)
        return question

    async def list_questions(self, theme_id: Optional[int] = None) -> list[Question]:
        questions = []
        for question in self.app.database.questions:
            if not theme_id:
                questions.append(question)
            elif theme_id and str(question.theme_id) == theme_id:
                questions.append(question)
        return questions
