import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta, date

def tendency_line_check_accumulated(tendency_line, total_items, addition):
    if tendency_line < total_items:
        return tendency_line + addition
    else:
        return tendency_line
    
    
def burnup(start_date, child_issues):
    # Dados fornecidos
    num_weeks = 60

    

    dates = []
    backlog_cumulative_list = []
    delivered_cumulative_list = []
    deliveries_by_period_list = []
    
    #intervalor entre as datas para os cálculos
    interval = timedelta(days=7)
    
    for i in range(num_weeks):
        backlog_cumulative = 0
        delivery_cumulative = 0
        
        if len(dates) == 0:
            dates.append(start_date)
        
        else:
            dates.append(dates[i-1] + interval)
        
        for issue in child_issues:        
            creared_date_child = datetime.strptime(issue['fields']['created'], '%Y-%m-%dT%H:%M:%S.%f%z').date()
            
            conclusion_date_child = None
            if issue['fields']['resolutiondate'] != None:
                conclusion_date_child = datetime.strptime(issue['fields']['resolutiondate'], '%Y-%m-%dT%H:%M:%S.%f%z').date()

            if len(dates) == 1:
                if creared_date_child < dates[i]:
                    backlog_cumulative += 1
                    
            else:
                if  creared_date_child <= dates[i]:
                        backlog_cumulative += 1
    
    
    
            if conclusion_date_child != None  and conclusion_date_child <= dates[i] and issue['fields']['resolution']['name'] == "Done":
                delivery_cumulative +=1
                
            elif conclusion_date_child != None  and conclusion_date_child <= dates[i] and issue['fields']['resolution']['name'] != "Done":
                backlog_cumulative -= 1 
                          

        backlog_cumulative_list.append(backlog_cumulative)  
        
        if dates[i] <= date.today() + interval:   
            if len(delivered_cumulative_list) == 0:
                deliveries_by_period_list.append(delivery_cumulative)
            else:
                deliveries_by_period_list.append(delivery_cumulative-delivered_cumulative_list[-1])
                
            delivered_cumulative_list.append(delivery_cumulative)
            
            
            
        else:
            delivered_cumulative_list.append(0)   
        
        
        
    print(backlog_cumulative_list)
    print(delivered_cumulative_list)
    print(deliveries_by_period_list)
    print(dates)
    print(len(dates))
    print(len(backlog_cumulative_list)) 
    print(len(delivered_cumulative_list)) 
    print(len(deliveries_by_period_list))         
        
        
        
        
    optimistic_line = []
    realistic_line = []
    pessimistic_line = []

    optimistic_cumulative = 0
    realistic_cumulative = 0
    pessimistic_cumulative = 0
       
    
    percentile_50 = np.percentile(deliveries_by_period_list, 50)
    percentile_75 = np.percentile(deliveries_by_period_list, 75)
    percentile_90 = np.percentile(deliveries_by_period_list, 90)
    total_items = backlog_cumulative_list[-1]
    
    
    for i in range(num_weeks):
    
        if i < len(deliveries_by_period_list):
            optimistic_line.append(delivered_cumulative_list[i])
            realistic_line.append(delivered_cumulative_list[i])
            pessimistic_line.append(delivered_cumulative_list[i])
        else:            
            optimistic_cumulative = tendency_line_check_accumulated(optimistic_line[-1], total_items, percentile_90)
            realistic_cumulative = tendency_line_check_accumulated(realistic_line[-1], total_items, percentile_75)
            pessimistic_cumulative = tendency_line_check_accumulated(pessimistic_line[-1], total_items, percentile_50)

            optimistic_line.append(optimistic_cumulative)
            realistic_line.append(realistic_cumulative)
            pessimistic_line.append(pessimistic_cumulative)
            

        
    # Plotagem do gráfico
    plt.bar(dates, delivered_cumulative_list, label='Entregas')
    # Adiciona as legendas com o número nas colunas
    for i, value in enumerate(delivered_cumulative_list):
        plt.text(dates[i], value, str(value), ha='center', va='bottom')
    plt.plot(dates, pessimistic_line[:len(dates)], label='Pessimista', color="red")
    plt.plot(dates, realistic_line[:len(dates)], label='Realista', color="blue")
    plt.plot(dates, optimistic_line[:len(dates)], label='Otimista', color="green")
    plt.plot(dates, backlog_cumulative_list[:len(dates)] , label='Backlog', color="orange", linewidth=2)
    plt.xlabel('Data')
    plt.ylabel('Itens Concluídos')
    plt.title('Gráfico de Burnup')
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()
