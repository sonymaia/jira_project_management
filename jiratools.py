from atlassian import Jira
from dotenv import load_dotenv
from pathlib import os
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Carregar variáveis de ambiente de um arquivo .env
load_dotenv('.env')


class JiraTools(Jira):
    def __init__(self):
        self.jira_url = str(os.getenv('JIRA_URL'))
        self.token = str(os.getenv('TOKEN'))
        self.email = str(os.getenv('EMAIL'))
        self.jira = None

    def connect(self):
        try:  
            # Criar objeto JIRA
            self.jira = Jira(
                url= self.jira_url,
                username=self.email,
                password=self.token,
                verify_ssl=False
            )
            print("Conexão com o Jira estabelecida com sucesso!")

        except Exception as e:
            print(f"Falha na conexão com o Jira: {str(e)}")
        
        return self.jira

    def close(self):
        if self.jira is not None:
            self.jira.close()
            print("Conexão com o Jira encerrada.")

    def create_issue(self, project_key, summary, description):
        pass
    
