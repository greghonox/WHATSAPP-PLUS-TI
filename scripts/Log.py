from scripts.Padroes import DateTime

def log(func):
	def method(*args, **kargs):
		try:
			argumentos = func(*args, **kargs)
			log = argumentos[0] if(isinstance(argumentos, tuple)) else argumentos
			dialog = DateTime() + log + " "

			try: tipo = argumentos[1]
			except: tipo = True
			
			try: log = argumentos[2]
			except: log = None

			Log(msg=dialog, tipo=tipo, guiLog=log)
			return argumentos
		except Exception as erro: return f"ERRO EM GERAR LOG {func} --- {args}"
	return method

class Log:
	def __init__(self, msg, tipo=True, arq=r'log.txt', guiLog=None):
		try:
			self.arq = arq			
			tipo = " -- INFORMACAO" if(tipo) else " -- CUIDADO"
			msg = '{:<200}'.format(msg[:200])
			dialog = DateTime() +' '+ msg + tipo
			self.log(dialog)	
			if(guiLog): guiLog.emit(msg)
		except Exception as erro: 
			msg = f"ERRO OCORRIDO EM IMPRIMIR LOG({erro}) -- {msg}"
			print(msg)
   
	def log(self, msg):  
		print(msg)
		with open(self.arq, 'a') as arq: arq.write(msg+'\n')
