import pandas as pd
from functions.format_text import remover_acentos

def get_zone_services(igrejas_regioes, tabela_servicos):
    contagem_servicos = []

    # Inicializar contagem de serviços em zero para todas as igrejas e regiões
    for bloco, regioes in igrejas_regioes.items():
        for regiao in regioes:
            contagem_servicos.append({
                   
                    "Região": regiao["Região"],
                    "Igreja": regiao['Igrejas'],
                    "Serviços": 0
                })
          
      
                

    # Atualizar contagem com os dados da tabela de serviços
    for _, servico in tabela_servicos.iterrows():
        regiao = servico['Região']
        igreja = servico["Cenáculo"]

     
        
        # Encontra e atualiza a contagem para a igreja correspondenter
        for item in contagem_servicos:
            
          
            if remover_acentos(item["Região"].replace(" ", "").lower()) == regiao.replace(" ", "").lower():
                item["Serviços"] += 1
                

              
              
                    

    return pd.DataFrame(contagem_servicos)
