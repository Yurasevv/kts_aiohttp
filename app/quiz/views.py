from aiohttp.web_exceptions import HTTPConflict
from aiohttp_apispec import request_schema, response_schema

from app.quiz.schemes import (
    ThemeSchema,
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


class ThemeListView(View):
    async def get(self):
        themes = await self.store.quizzes.list_themes()
        return json_response(
            data={"themes": [ThemeSchema().dump(theme) for theme in themes]}
        )


class QuestionAddView(View):
    async def post(self):
        raise NotImplementedError


class QuestionListView(View):
    async def get(self):
        raise NotImplementedError
