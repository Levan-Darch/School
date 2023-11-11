from melipayamak import Api


def send_sms(to, text):
    username = '19927145149'
    password = '9BOG6'
    print(1)
    api = Api(username, password)
    sms = api.sms()
    print(2)
    _from = '50004001145149'
    print(3)
    response = sms.send(to, _from, text)
    print(4)
    print(response)


"""
def send_sms(to, text):
    print(to)
    print(text)
"""