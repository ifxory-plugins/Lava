from twisted.internet import reactor
from quarry.net.server import ServerProtocol, ServerFactory, Protocol
import requests
import secrets

class Lava(ServerProtocol):

    def player_joined(self):
        Protocol.player_joined(self)
        ServerProtocol.switch_protocol_mode(self, "play")
        self.log = self.factory.log
        self.log.info("User {0}({1}) authorized.".format(self.display_name, self.remote_addr.host))

        token = secrets.token_hex(5)
        headers = {"Authorization":"Bearer " + self.factory.token}
        data = {"key":token, "username":self.display_name, "uuid":self.uuid}
        try:
            r = requests.post(self.factory.api, headers=headers, data=data)
            if r.status_code != 200:
                self.factory.log.error("HTTPS API return status code: {0}".format(r.status_code))
                self.close("Internal Server Error.")
            elif r.status_code == 200:
                self.factory.log.success("HTTPS API auth request sucess: {0}".format(r.status_code))
            else:
                self.factory.log.info("HTTPS API return status code: {0}".format(r.status_code))
        except:
            self.factory.log.error("HTTPS API cannot be requested")
            self.close("Internal Server Error.")

        self.close("Your token is: {0}".format(token))

class Factory(ServerFactory):
    protocol = Lava

def start(log, args, image):
    factory = Factory()
    factory.log = log
    factory.motd = args.motd
    if(image):
        factory.icon_path = args.icon_path
    factory.secure_mode = args.secure_mode
    factory.api = args.api
    factory.token = args.api_token
    factory.listen(args.host, args.port)
    reactor.run()
