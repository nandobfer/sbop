from datetime import datetime, timedelta, date
from src.config import TIMELIMIT, database_auth
from src.mysql_handler import Mysql


class Connection():
    def __init__(self, ip, data):
        self.ip = ip
        self.id = data[0]
        self.user = data[1]
        self.password = data[2]
        self.name = data[3]
        self.uf = data[4]
        self.member = data[5]
        self.cep = data[6]
        self.email = data[7]
        self.telefone = data[8]
        self.celular = data[9]
        self.endereco = data[10]
        self.numero = data[11]
        self.complemento = data[12]
        self.bairro = data[13]
        self.cidade = data[14]
        self.pais = data[15]
        self.crm = data[16]
        self.curriculum = data[17]
        self.pessoa = data[18]

        self.expira = datetime.now() + timedelta(minutes=TIMELIMIT)

    def isExpired(self):
        if not datetime.now() < self.expira:
            return True


class Session():
    def __init__(self):
        self.connections = []
        self.member_list = []
        self.database = Mysql()
        self.database.connect(database_auth)
        self.getMembers()

    def getMembers(self):
        try:
            if not self.database.connection.is_connected():
                self.reconnectDatabase()
        except:
            pass

        self.member_list = []
        members = self.database.fetchTable(0, 'Membros')

        for member in members:
            data = {
                'id': member[0],
                'user': member[1],
                'name': member[3],
                'uf': member[4],
                'member': member[5],
                'cep': member[6],
                'email': member[7],
                'telefone': member[8],
                'celular': member[9],
                'endereco': member[10],
                'numero': member[11],
                'complemento': member[12],
                'bairro': member[13],
                'cidade': member[14],
                'pais': member[15],
                'crm': member[16],
                'curriculum': member[17],
                'pessoa': member[18]
            }
            self.member_list.append(data)

    def reconnectDatabase(self):
        self.database.connect(database_auth)

    def getConnection(self, ip):
        for connection in self.connections:
            if connection.ip == ip:
                if not connection.isExpired():
                    return connection
                else:
                    self.connections.remove(connection)

    def login(self, user, password, ip):
        try:
            data = self.database.fetchTable(1, 'Membros', 'USU??RIO', user)[0]
            if data:
                if password == data[2]:
                    id = data[0]

                    # check if user is already logged and update it' connection if it exists
                    is_logged = self.getConnection(ip)
                    if is_logged and is_logged.id == id:
                        self.connections.remove(is_logged)

                    self.connections.append(Connection(ip, data))
                    return str(id)
        except Exception as error:
            print(error)
            return None

    def signup(self, data):
        try:
            usuario = self.database.fetchTable(
                1, 'Membros', 'USU??RIO', data['usuario'])[0]
            if usuario:
                return 'Usu??rio j?? cadastrado', False

            email = self.database.fetchTable(
                1, 'Membros', 'EMAIL', data['email'])[0]
            if email:
                return 'E-mail j?? cadastrado', False

        except:
            data.update({'id': len(self.member_list)})
            self.database.insertMember(data)
            self.member_list.append(data)
            return 'Usu??rio cadastrado', True

    def get_blog(self, membro):
        try:
            blog_list = self.database.fetchTable(0, 'Blog', 'MEMBRO', membro)
            if blog_list:
                return blog_list
        except:
            return None

    def blogPost(self, data):
        id = len(self.database.fetchTable(0, 'Blog'))
        date = datetime.now()
        date = f'{date.day}/{date.month}/{date.year} - {date.hour}:{date.minute}'
        data = (id, data['member'], data['title'],
                data['content'], data['author'], date)
        self.database.insertPost(data)
