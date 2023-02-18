from aiohttp.web_exceptions import HTTPConflict, HTTPBadRequest, HTTPNotFound
from aiohttp_apispec import request_schema, response_schema

from app.quiz.models import Answer
from app.quiz.schemes import (
    ThemeSchema, QuestionSchema,
)
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


class ThemeAddView(AuthRequiredMixin, View):
    @request_schema(ThemeSchema)
    @response_schema(ThemeSchema)
    async def post(self):
        title = self.data["title"]
        if await self.store.quizzes.get_theme_by_title(title):
            raise HTTPConflict
        theme = await self.store.quizzes.create_theme(title=title)
        return json_response(data=ThemeSchema().dump(theme))


class ThemeListView(AuthRequiredMixin, View):
    async def get(self):
        themes = await self.store.quizzes.list_themes()
        return json_response(
            data={"themes": [ThemeSchema().dump(theme) for theme in themes]}
        )


class QuestionAddView(AuthRequiredMixin, View):
    @request_schema(QuestionSchema)
    @response_schema(QuestionSchema)
    async def post(self):
        title = self.data["title"]
        theme_id = self.data["theme_id"]
        answers = self.data["answers"]

        count = 0
        for answer in answers:
            if answer["is_correct"]:
                count += 1

        if count != 1 or len(answers) == 1:
            raise HTTPBadRequest
        if len(answers) == 0 or len(answers) == 1:
            raise HTTPBadRequest
        if await self.store.quizzes.get_theme_by_id(theme_id) is None:
            raise HTTPNotFound
        if await self.store.quizzes.get_question_by_title(title):
            raise HTTPConflict

        question = await self.store.quizzes.create_question(
            title=title, theme_id=theme_id, answers=[
                Answer(
                    title=answer["title"],
                    is_correct=answer["is_correct"]
                ) for answer in answers
            ])
        return json_response(data=QuestionSchema().dump(question))


class QuestionListView(AuthRequiredMixin, View):
    @response_schema(QuestionSchema)
    async def get(self):
        theme_id = None
        if self.request.query:
            theme_id = self.request.query["theme_id"]
        if theme_id is None:
            questions_all = await self.store.quizzes.list_questions()
            q = [QuestionSchema().dump(question) for question in questions_all]
            return json_response(
                data={
                    "questions": q
                }
            )
        raw_questions = await self.store.quizzes.list_questions(theme_id)
        q_ = [QuestionSchema().dump(question) for question in raw_questions]
        return json_response(
            data={
                "questions": q_
            }
        )
