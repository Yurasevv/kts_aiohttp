import typing

from app.store.admin.accessor import AdminAccessor
from app.store.database.database import Database

if typing.TYPE_CHECKING:
    from app.web.app import Application


class Store:
    def __init__(self, app: "Application"):
        from app.store.quiz.accessor import QuizAccessor
        self.admins = AdminAccessor(app)
        self.quizzes = QuizAccessor(app)


def setup_store(app: "Application"):
    app.database = Database()
    app.store = Store(app)
