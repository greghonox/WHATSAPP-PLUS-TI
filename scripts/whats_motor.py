from os import getcwd
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class WhatsApp:
    def main(self):
        self.dr = self.iniciliazar_driver()
        self.dr.get("https://web.whatsapp.com/")
        self.rodando = True
        self.verifica_entrada()
        
    def verifica_entrada(self):
        """ AGUARDA A LEITURA DO QR CODE """
        contagem = 0
        while True and self.rodando:
          try:
              print(f"AGUARDANDO LEITURA DO QR CODE {contagem}")
              contagem += 1
              if(self.dr.find_element_by_class_name("Ui--U").text == "Mantenha seu celular conectado"): return True
          except Exception as erro: pass
          sleep(1)

    def iniciliazar_driver(self):
        return webdriver.Chrome(executable_path=getcwd() + r'\chromedriver.exe')
        
    def enviar(self, numero, mensagem, anexo, log):
        self.log = log
        
        def enviarAnexo():
            if(anexo != ''):
                self.navegar([{'att': '//*[@id="main"]/footer/div[1]/div[1]/div[2]/div/div/span', 'op': 'find_element_by_xpath', 'ac': 'click()'}])
                sleep(3)
                try:
                    tipos = {ex: '1' for ex in 'AVI,MPE,MP4,MKV,WMV,FLV,JPG,GIF,PNG,avi,mpe,mp4,mkv,wmv,flv,jpg,gif,png'.split(',')}
                    for ex in 'DOC,DOCX,PDF,XLS,XLSX,EXE,ZIP,RAR,XML,PPT,PPTX,doc,docx,pdf,xls,xlsx,exe,zip,rar,xml,ppt,pptx'.split(','): tipos[ex] = '3' 

                    try: tipo = tipos[anexo.split('.')[-1]]
                    except: tipo = '1'

                    try:self.dr.find_element_by_xpath(f"""//*[@id="main"]/header/div[3]/div/div[2]/span/div/div/ul/li[{tipo}]/button/input""").send_keys(anexo)
                    except: 
                        try: self.dr.find_element_by_xpath(f"""//*[@id="main"]/footer/div[1]/div[1]/div[2]/div/span/div/div/ul/li[{tipo}]/button/input""").send_keys(anexo)
                        except: pass

                    self.navegar([{'att': '//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div', 'op': 'find_element_by_xpath', 'ac': "click()"}], 5)
                    self.log(f"ENVIANDO ANEXO: {anexo} PARA {numero}  COM SUCESSO")
                except Exception as erro: print(f"ERRO EM ANEXAR({anexo}): {erro}")
                
        self.ok = False
        self.verifica_alerta()
        self.dr.get(f"https://api.whatsapp.com/send?phone=55{numero}&text={mensagem}")
        print('TENTANDO ENTRAR NA PAGINA DE ESCRITA DE MENSAGEM')
        for c in range(30):
            for e, _ in enumerate(["""//*[@id="action-button"]""", """//*[@id="fallback_block"]/div/div/a"""]): 
                try:
                    sleep(1)
                    if self.verificar_pagina_mensagem(): break
                    self.dr.find_element_by_xpath(_).click()
                    if e == 1: break
                except: print(f'TENTANDO ENVIAR {_} {c}/30')

        enviarAnexo()
    
    def verificar_pagina_mensagem(self):
        try: 
            if 'nova conversa' in self.dr.find_element_by_xpath('//*[@id="side"]/div[1]/div/div').text:
                return True
        except: ...
        
        try: 
            if 'telefone compartilhado' in self.dr.find_element_by_xpath('//*[@id="app"]/div[1]/span[2]/div[1]/span/div[1]/div/div/div/div/div[1]').text:
                return True
        except: return False
        
    def enviarEnter(self):
        try: 
            self.verificarWhatsFora()
            self.dr.find_element_by_xpath("""//*[@id="main"]/footer/div[1]/div[2]/div/div[2]""").send_keys(Keys.ENTER)
            self.ok = True
            return True
        except: return False
                
    def verifica_alerta(self):
        sleep(2)
        try: self.dr.switch_to.alert.accept()
        except: pass

    def parar(self): 
        try:self.dr.close()
        except: pass

    def verificarWhatsFora(self):
        contagem = 0
        while True:
            try:
                if(not self.dr.find_element_by_xpath('//*[@id="app"]/div/div/div/div/div/div/div[1]').text == 'Tentando conectar ao celular'):
                    self.log(f"O TELEFONE ESTA DESCONECTADO, TENTATIVA:{contagem}", False)
                    contagem += 1
                return True                
            except: return True

    def fecharWhats(self):
        try:
            self.dr.quit()
            self.dr.close()
        except Exception as erro: print(f"ERRO EM FECHAR O CHROME DRIVER {erro}")

    def navegar(self, campos, tempo=2):
        """ 
        ESSA É A FUNÇÃO MAIS BEM ELABORADA QUE EXISTE NESSE CODIGO.
        COM ELA VOCÊ PODE CHAMAR O DRIVER PARA NAVEGAR PELA PAGINA SEM TER QUE 
        DEFINE EXCEÇÕES E VERIFICAÇÕES.
        O USO DELA É PREENCHENDO DESSA FORMA:
        self.navegar([{'att': 'CAMINHO_XPATH', 'op': 'find_element_by_xpath', 'ac': 'click()'}])
        self.navegar([{'att': 'CLASSE NAME', 'op': 'find_element_by_class_name', 'ac': 'click()'}])
        .... ENTRE OUTROS METODOS PARA MANIPULAR O SELENIUM.
        UMA COISA NÃO EXPLICADA AQUI É QUE VOCÊ PODE DEFINIR VARIOS PASSOS ASSIM:

        self.nevegar([{'att': 'CAMINHO_XPATH', 'op': 'find_element_by_xpath', 'ac': 'click()'},
                      {'att': 'CLASSE NAME', 'op': 'find_element_by_class_name', 'ac': 'click()'},
                      {'att': 'CAMINHO_XPATH', 'op': 'find_element_by_xpath', 'ac': 'click()'},
                      {'att': 'CLASSE NAME', 'op': 'find_element_by_class_name', 'ac': 'click()'}])
        """
        for c in campos:
          try:  
              sleep(tempo)
              exe = f"self.dr.{c['op']}('{c['att']}').{c['ac']}"
              eval(exe); #print(exe)
          except Exception as erro: print(f"ERRO NO COMANDO:{exe} -- ({c['att']}) -- {erro}")

