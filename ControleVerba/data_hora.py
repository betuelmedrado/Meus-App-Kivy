
from datetime import datetime
lista = [0,'segunda', 'terca','quarta', 'quinta','sexta','sabado', 'domingo']


hoje = datetime.today().isoweekday()
data = datetime.today()
hora = datetime.today().time()

# print(help(datetime))
print(lista[hoje])
print(data.strftime("%d/%m/%y"))
print(hora.strftime('%H:%M'))