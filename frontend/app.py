import streamlit as st
import requests
import pandas as pd

st.set_page_config(layout="wide")
st.image("logo.png", width=200)
st.title("Gerenciamento de Produtos")

def show_response_message(response):
    if response.status_code == 200:
        st.success("Operação realizada com sucesso!")
    else:
        try:
            data = response.json()
            if isinstance(data["detail"], list):
                errors = "\n".join([error["msg"] for error in data ["dewtail"]])
                st.error(f"Erro: {errors}")
            else:
                st.serror(f"Erro: {data['Detail']}")
        except ValueError:
            st.error("Erro desconhecido. Não foi possível codificar a resposta")

#CRIAR PRODUTO
with st.expander("Adicionar um Novo Produto"):
    with st.form("new_product"):
        name = st.text_input("Nome do Produto")
        description = st.text_area("Descrição do Produto")
        price = st.number_input("Preço", min_value = 0.01, format="%f")
        categoria = st.selectbox(
            "Categoria",
            ["Eletrônico", "Eletrodoméstico", "Móveis", "Roupas", "Calçados"],
        )
        email_fornecedor = st.text_input("Email do Fornecedor")
        submit_button = st.form_submit_button("Adicionar Produto")

        if submit_button:
            response = requests.post(
                "http://backend:8000/products/",
                json={
                    "name": name,
                    "description": description,
                    "price": price,
                    "categoria": categoria,
                    "email_fornecedor": email_fornecedor,
                },
            )
            show_response_message(response)

# VISUALIZAR PRODUTOS
with st.expander("Visualizar Produtos"):
    if st.button("Exibir Todos os Produtos"):
        response = requests.get("http://backend:8000/products/")
        if response.status_code == 200:
            product = response.json()
            df = pd.DataFrame(product)

            df = df[
                [
                    "id",
                    "name",
                    "price",
                    "categoria",
                    "email_fornecedor",
                    "created_at",
                ]
            ]

            #EXIBE O DATAFRAME SEM O ÍNIDICE
            st.write(df.to_html(index=False), unsafe_allow_html=True)
        else:
            show_response_message(response)

#OBTER DETALHES DE UM PRODUTO
with st.expander("Obter Detalhes de um Produto"):
    get_id = st.number_input("ID do Produto", min_value=1, format="%d")
    if st.button("Buscar Produto"):
        response = requests.get(f"http://backend:8000/products/{get_id}")
        if response.status_code == 200:
            product = response.json()
            df = pd.DataFrame([product])

            df = df[
                [
                    "id",
                    "name",
                    "price",
                    "categoria",
                    "email_fornecedor",
                    "created_at",
                ]
            ]

            #EXIBE O DATAFRAME SEM O INDICE
            st.write(df.to_html(index=False), unsafe_allow_html=True)
        else:
            show_response_message(response)

# DELETAR PRODUTO
with st.expander("Deletar Produto"):
    delete_id = st.number_input("ID do Produto para Deletar", min_value=1, format="%d")
    if st.button("Deletar Produto"):
        response = requests.delete(f"htt://backend:8000/products/{delete_id}")
        show_response_message(response)

#ATUALIZAR PRODUTO
with st.expander("Atualizar Produto"):
    with st.form("uptdate_product"):
        uptdate_id = st.number_input("ID do Produto", min_value=1, format="%d")
        new_name = st.text_input("Novo Nome do Produto")
        new_description = st.text_area("Nova Descrição do Produto")
        new_price = st.number_input("Novo Preço", min_value = 0.01, format="%f")
        new_categoria = st.selectbox(
            "Nova Categoria",
            ["Eletrônico", "Eletrodoméstico", "Móveis", "Roupas", "Calçados"],
        )
        new_email_fornecedor = st.text_input("Novo Email do Fornecedor")
        update_button = st.form_submit_button("Atualizar Produto")

        if update_button:
            update_data = {}
            if new_name:
                update_data["name"] = new_name
            if new_description:
                update_data["description"] = new_description
            if new_price > 0:
                update_data["price"] = new_price
            if new_email_fornecedor:
                update_data["email_fornecedor"] = new_email_fornecedor
            if new_categoria:
                update_data["categoria"] = new_categoria

            
            if update_data:
                response = requests.put(
                    f"http://backend:8000/products/{uptdate_id}", json=update_data
                )
            show_response_message(response)
