MESSAGES = {
    'hello_msg': """
        Здравствуй, {0}, нам очень приятно, что вы выбрали нашу новостную ленту!
    """,
    'err_msg': """Госпаде, я не понимаю что ты говоришь!""",
}


def message_form(success, message, **kwargs):
    return dict(**{'success': success, 'error': message}, **kwargs)
