from browser import document, ajax, html, bind, window, alert


class Member():
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.uf = data['uf']
        self.cep = data['cep']
        self.member = data['member']


def showData(req):
    data = eval(req.text)
    member = Member(data)

    document['user-title'].text = f'Você tem acesso a conteúdo do nível: {member.member}'
    document['user-content'].text = f'Conteúdo virá aqui \/'


def ajaxRestrito():
    req = ajax.Ajax()
    req.bind('complete', showData)
    req.open('POST', '/template_restrito/', True)
    req.set_header('content-type', 'application/x-www-form-urlencoded')
    req.send({})


ajaxRestrito()
