from pushover import Pushover

class Message:
    def push(message, title):
        api_token = "a9uvbwxa8j2gcmfw6z95hzj95wkhwp"
        user_key = "uEgiVanmYFdcXEXhMHFfowMRpYci2u"

        po = Pushover(api_token)
        po.user(user_key)

        msg = po.msg(message)

        msg.set("title", title)

        po.send(msg)

  