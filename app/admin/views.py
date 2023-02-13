from app.web.app import View
from app.web.utils import json_response


class AdminLoginView(View):
    async def post(self):
        data = await self.request.json()
        admin = await self.store.admins.get_by_email(data["email"])
        return json_response(data = {"email =" : admin.email})



class AdminCurrentView(View):
    async def get(self):
        raise NotImplementedError
