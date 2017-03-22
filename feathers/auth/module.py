from drongo import HttpResponseHeaders, HttpStatusCodes
from drongo.utils import dict2

from .actions import AuthActions
from .backend import AuthMongoBackend
from .views import AuthViews


class Auth(object):
    def __init__(self, app, backend='mongo', base_url='auth',
                 api_base_url='/api/auth', connection=None):
        self.app = app
        self.base_url = base_url
        self.api_base_url = api_base_url

        if backend == 'mongo':
            self.backend = AuthMongoBackend(connection)

        self.views = AuthViews(self)
        self.actions = AuthActions(self)

    def user_exists(self, username):
        return self.backend.user_exists(username)

    def create_user(self, username, password, active=False):
        return self.backend.create_user(username, password, active=active)

    def verify_login(self, username, password):
        return self.backend.verify_login(username, password)

    def update_user(self, username, fields={}):
        return self.backend.update_user(username, fields)

    def authenticate_user(self, request, response, username):
        self.update_user(username, {
            'last_login': datetime.utcnow()
        })
        request.context.session.auth.user = dict2(
            username=username,
            authenticated=True
        )

    def logout(self, request):
        request.context.session.auth.user = dict2(
            username='anonymus',
            authenticated=False
        )

    def add_error_message(self, request, message):
        request.context.session.auth.messages.setdefault('error', []).append(
            message
        )
