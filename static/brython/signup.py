from browser import document, ajax, html, bind, window, alert

button = document['signup-button']
password = document['senha']
password_confirmation = document['confirme-senha']


@bind('.senha', 'blur')
def validate(ev):
    if password.value == password_confirmation.value:
        button.disabled = False
        document['error'].text = ''
    else:
        button.disabled = True
        document['error'].text = 'Senhas não conferem'


# só aceita input numerico no input type text
@bind('#cep', 'input')
def cep(ev):
    try:
        int(document['cep'].value[-1:])
        if len(document['cep'].value) == 5:
            document['cep'].value += '-'
    except:
        document['cep'].value = document['cep'].value[:-1]
