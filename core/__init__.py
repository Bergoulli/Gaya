import datetime

class SystemInfo:
    def __init__(self):
        pass

    @staticmethod
    def get_time():
        now = datetime.datetime.now()
        resposta = 'São {} horas e {} minutos'.format(now.hour, now.minute)
        return resposta
    
    @staticmethod
    def get_date():
        now = datetime.datetime.now()
        res = (f'Hoje é dia {now.day} de {now.strftime("%B")} de {now.year}')
        return res