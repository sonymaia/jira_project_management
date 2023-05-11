from  jiratools import JiraTools
from datetime import datetime, date
from graphicsplotly import burnup

def main():
    project_status()
    

    
def project_status(): 
    jira = JiraTools().connect()
    
    #issue_id = input("Digite o Id da issue: ")
    issue_id = 'BOAC-652'
    
    #Pega as informaçoes da Issue Pai
    jql_request = f'issuekey = {issue_id}'
    iniciative = jira.jql(jql_request)

    #print(iniciative) 
    
    duedateIssue = iniciative['issues'][0]['fields']['duedate']
    startdate = iniciative['issues'][0]['fields']['customfield_10015']
    
    
    duedateIssue = datetime.strptime(duedateIssue, '%Y-%m-%d').date()
    startdate = datetime.strptime(startdate, '%Y-%m-%d').date()
    
    diasFaltante = (duedateIssue - date.today()).days
        
    
    #Pega as informaçoes das issues filhas
    jql_child_issues = f'issuekey in portfolioChildIssuesOf({issue_id} ) and issuetype in (story)'
    child_issues = jira.jql(jql_child_issues)

    total_issues = len(child_issues['issues'])
    total_done = 0
    
    
    for issue in child_issues['issues']:
        
        #print( 'key:', issue['key'])
        #print( 'summary:', issue['fields']['summary'])
        ##print( 'created:', issue['fields']['created'])
        #print( 'resolutiondate:', issue['fields']['resolutiondate'])
        
        if issue['fields']['resolution'] != None: 
            total_done += 1 
            #print( 'resolution:', issue['fields']['resolution']['name'])
        #else:
        #    print( 'resolution:', issue['fields']['resolution'])
            
            
        
        #print( 'issuetype:', issue['fields']['issuetype']['name'])
        
    print('======================================')
 
    burnup(startdate, child_issues['issues'])
    

    
    

    # conclusao = (total_done*100)/total_issues

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