from  jiratools import JiraTools
from datetime import datetime, date
from graphics.graphicsplotly import burnup
import requests


def main():
    project_status()
    

    
def project_status(id): 
    jira = JiraTools().connect()
    #issue_id = 'BOAC-652'
    issue_id = id
    
    try:
        #Pega as informaçoes da Issue Pai
        jql_request = f'issuekey = {issue_id}'
        iniciative = jira.jql(jql_request)

    except requests.exceptions.HTTPError as e:
        # Tratamento para o erro HTTPError específico
        print("Ocorreu um erro HTTP:", e)
        # Realize ações adicionais de tratamento, se necessário
        # Redireciona para uma página de sucesso ou outra página
        return e

    except Exception as e:
        # Tratamento genérico para outras exceções que possam ocorrer
        print("Ocorreu um erro:", e)
        return e

        
    #print("Resultado", iniciative) 
    
    duedateIssue = iniciative['issues'][0]['fields']['duedate']
    startdate = iniciative['issues'][0]['fields']['customfield_10015']
    summary = iniciative['issues'][0]['fields']['summary']

    
    
    duedateIssue = datetime.strptime(duedateIssue, '%Y-%m-%d').date()
    startdate = datetime.strptime(startdate, '%Y-%m-%d').date()
    
    
    
    # Get the information of the child Issues
    jql_child_issues = f'issuekey in portfolioChildIssuesOf({issue_id} ) and issuetype in (story)'
    child_issues = jira.jql(jql_child_issues)

    total_issues = len(child_issues['issues'])
    total_done = 0
    total_declined = 0
    
    
    for issue in child_issues['issues']:
        
        #print( 'key:', issue['key'])
        #print( 'summary:', issue['fields']['summary'])
        ##print( 'created:', issue['fields']['created'])
        #print( 'resolutiondate:', issue['fields']['resolutiondate'])
        
        if issue['fields']['resolution'] != None: 
            total_done += 1 
            if issue['fields']['resolution']['name'] != "Done":
                total_declined += 1 

    
            #print( 'resolution:', issue['fields']['resolution']['name'])
            #print( 'issuetype:', issue['fields']['issuetype']['name'])
        
    print('======================================')

    total_issues = total_issues - total_declined
    total_done = total_done - total_declined

    days_left = (duedateIssue - date.today()).days
    completion_percentage = (total_done*100)/total_issues
        
    dict_project_data = {'issue_id': issue_id,
                         'summary': summary,
                         'days_left': days_left,
                         'completion_percentage': completion_percentage,
                         'total_done': total_done,
                         'total_issues': total_issues,
                         'duedateIssue': duedateIssue
                        }
    
    #build the burnup chart
    dict_chart_data = burnup(startdate, child_issues['issues'], duedateIssue)
    dict_project_data.update(dict_chart_data)    

    return dict_project_data
    

    
    

     

    # print('======================================')
    # print(f"""
    # Data prometida:{duedateIssue}
    # Faltam {diasFaltante} dias para a entrega
    # Total de itens filhos(stories):{total_issues}
    # Total Done:{total_done}
    # Conclusão de {conclusao:.2f}% da Issue {issue_id}
    # """)
    
    # response = input("Gostaria de fazer uma nova pesquisa? 1=Sim 2=Não  ")
    # if response == "1":
    #     main()
        
    
if __name__ == "__main__":
    main()