from aiohttp.web_exceptions import HTTPForbidden
from aiohttp_apispec import request_schema, response_schema
from aiohttp_session import new_session, get_session

from app.admin.models import Admin
from app.admin.schemes import AdminSchema
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


class AdminLoginView(View):
    @request_schema(AdminSchema)
    @response_schema(AdminSchema, 200)
    async def post(self):
        data = await self.request.json()
        admin_from_db = await self.store.admins.get_by_email(data["email"])
        if not admin_from_db:
            raise HTTPForbidden
        session = await new_session(request=self.request)
        admin = AdminSchema().dump(admin_from_db)
        session["admin"] = admin
        return json_response(data=admin)


class AdminCurrentView(AuthRequiredMixin, View):
    @response_schema(AdminSchema, 200)
    async def get(self):
        return json_response(AdminSchema().dump(self.request.admin))
