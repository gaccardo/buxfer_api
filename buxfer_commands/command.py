import settings
from api import buxfer


class BuxferCommand( object ):

    def do_connect(self):
        ba = buxfer.BuxferAPI()
        ba.login(user = settings.USER,
            password = settings.PASS)

        return ba
