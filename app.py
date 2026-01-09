import streamlit as st
import pickle
import numpy as np


# Carrega o modelo treinado
with open('modelo_fraude.pkl', 'rb') as file: 
    fraud_model = pickle.load(file)

st.title("detector de Fraude em Transações")
st.write("Este modelo utiliza Regressão Logística para identificar possíveis fraudes em transações financeiras.")

valor_transacao = st.number_input("Valor da Transação (em dólares):", min_value=0.0, max_value=100000.0, value=50.0)
tempo_conta = st.number_input("Tempo de Conta (em meses desde a criação da conta", min_value=0, max_value=120, value=6)
num_transacoes_ult_30d = st.number_input("Número de Transações nos Últimos 30 Dias:", min_value=0, max_value=1000, value=3)

pais_origem_options = {
    "Brasil": 0,    
    "EUA": 1,
    "Outros": 2
}

pais_origem_escolhido = st.selectbox("País de Origem da Transação:", options=list(pais_origem_options.keys()))
pais_origem= pais_origem_options[pais_origem_escolhido]

if st.button("Verificar Fraude"):   
    input_data = np.array([[valor_transacao, tempo_conta, num_transacoes_ult_30d, pais_origem]])
    prediction = fraud_model.predict(input_data)    
    if prediction[0] == 1:
        st.error("Alerta: A transação é suspeita de fraude!")
    else:
        st.success("A transação parece legítima.")
    #probabilidade de fraude
    probabilidade = fraud_model.predict_proba(input_data)[0][1]
    st.write(f"Probabilidade de Fraude: {probabilidade:.2%}")
    
    #probabilidade de não fraude
    probabilidade_nao_fraude = fraud_model.predict_proba(input_data)[0][0]
    st.write(f"Probabilidade de Transação Legítima: {probabilidade_nao_fraude:.2%}")
    
else:
    st.write("Preencha os dados acima e clique em 'Verificar Fraude' para analisar a transação.")
    
    