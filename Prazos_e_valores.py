import streamlit as st
import pandas as pd
import datetime
from math import floor, ceil

#Configurações da página
st.set_page_config(

    page_title="Prazos e valores"
)

st.title("PRAZOS E VALORES")

st.divider()
#input data base
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

with col1:
    data_base = st.date_input("Data Base:", datetime.date.today(), format="DD/MM/YYYY")
with col2:
    qtidade_de_pagamentos = st.number_input("Quantidade de pagamentos:", value = 3, min_value= 1,placeholder= "Digite a quantidade de pagamentos")
with col3:
    valor_total = st.number_input("Valor total:", value = 0.0, min_value=0.0,step=1.0,placeholder= "Digite o valor total")
with col4:
    intervalo_entre_pagamentos = st.number_input("Intervalo entre os pagamentos:", value = 30, step = 15, min_value= 1,placeholder= "Digite o intervalor entre os pagamentos")

def divisor(data_base, qtidade_de_pagamentos, intervalo_entre_pagamentos, valor_total):
    lista_valores = list()
    lista_datas = list()
    lista_numero_do_pagamento = list()
    valor_de_incremento_datas = intervalo_entre_pagamentos

    for data in range(qtidade_de_pagamentos):
        lista_datas.append(data_base + datetime.timedelta(days=valor_de_incremento_datas))
        valor_de_incremento_datas += intervalo_entre_pagamentos
        temp = "PAG " + str(data + 1)
        lista_numero_do_pagamento.append(temp)

    valor_restante = valor_total
    qtidade_de_parcelas_restantes = qtidade_de_pagamentos
    valor_pago = 0
    
    valor_base = valor_total // qtidade_de_pagamentos
    resto = valor_total % qtidade_de_pagamentos
    for data in range(qtidade_de_pagamentos):
        lista_valores.append(valor_base)
    
    lista_valores.sort(reverse=True)

    while True:
        if resto >= 1:
            lista_valores[-1] += 1
            resto -= 1
        else:
            lista_valores[-1] += resto
            break
        lista_valores.sort(reverse=True)
    lista_valores.sort(reverse=True)
    return lista_datas, lista_valores, lista_numero_do_pagamento



lista_datas, lista_valores, lista_numero_do_pagamento = divisor(data_base, qtidade_de_pagamentos, intervalo_entre_pagamentos, valor_total)

# Função para formatar a data no formato DD/MM/YYYY
def formatar_data(data):
    return data.strftime("%d/%m/%Y")

# Aplicar a formatação a cada data na lista
lista_datas_formatadas = [formatar_data(data) for data in lista_datas]

# Função para formatar valores como dinheiro
def formatar_dinheiro(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# Aplicar a formatação a todos os valores da lista
valores_formatados = [formatar_dinheiro(valor) for valor in lista_valores]

df = pd.DataFrame({
    "Data": lista_datas_formatadas,
    "Valor": valores_formatados
}, index=lista_numero_do_pagamento)

st.dataframe(df, width=1000)