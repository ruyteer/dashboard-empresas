import streamlit as st
from functions.get_pdf_data import get_pdf_data
from generate_ci import generate_ci
import os
import convertapi
import tempfile

st.set_page_config(layout='wide', page_title="Automatizador de CI", page_icon="🌎", initial_sidebar_state="collapsed")

st.sidebar.title('Páginas')
st.sidebar.page_link("app.py", label='Empresas', icon='🏠')
st.sidebar.page_link("pages/ci-automation.py", label='Automatizador de CI', icon='🌎')

st.title('Automatizador de CI')


if "items" not in st.session_state:
    st.session_state["items"] = [{"quantidade": "", "descricao": "", "preco": ""}]


def add_item():
    st.session_state["items"].append({"quantidade": "", "descricao": "", "preco": ""})


def remove_item(index):
    st.session_state["items"].pop(index)


pdf_path = st.file_uploader("Carregue sua PODF ou REQDF aqui", type=["pdf"])

if pdf_path is not None:
    try:
      
        st.subheader("Formulário para Gerar CI")
        data = get_pdf_data(pdf_path)

        with st.form(key='ci-generator'):
            col1, col2, col3 = st.columns(3)
            code = col1.text_input("Código da Requisição", value=data['codigo_requisicao'])
            solicitant = col2.text_input("Solicitante", value=data['solicitante'])
            destination = col3.text_input("Local de Entrega", value=data['local_entrega'])

            col4, col5, col6 = st.columns(3)
            file_code = col4.text_input("Código da CI", placeholder="174")
            date = col5.text_input("Data", placeholder="01 de janeiro")
            amount = col6.text_input("Valor Total", value=data['valor_total'])

            company = st.text_input("Empresa", value=data['empresa'])
            justify = st.text_area("Justificativa da Compra", value=data['justificativa'])
            reason = st.text_area("Motivo da Compra", value=data['justificativa'])
            file_name = st.text_input(
                "Nome do Arquivo",
                value=f"CI - COMPRAS - DF00 (NUMERO) .2024 - {data['codigo_requisicao']} - DESCRICAO - {data['local_entrega']}"
            )

            
            st.subheader("Itens:")
            for idx, item in enumerate(st.session_state["items"]):
                cols = st.columns(4)
                item["quantidade"] = cols[0].text_input("Quantidade", value=item["quantidade"], key=f"quantidade_{idx}")
                item["descricao"] = cols[1].text_input("Descrição", value=item["descricao"], key=f"descricao_{idx}")
                item["preco"] = cols[2].text_input("Preço", value=item["preco"], key=f"preco_{idx}")
                
    
                if cols[3].form_submit_button(f"Remover {idx + 1}", type="secondary"):
                    remove_item(idx)
                    st.rerun()
            
            

        
            if st.form_submit_button("Adicionar Item"):
                add_item()
                st.rerun()
  
            
      
            submit_button = st.form_submit_button('Gerar CI')

            name_file = f"{file_name}.docx"
            word_output_path = os.path.join("uploads", name_file)

            if submit_button:
                st.toast("Formulário enviado com sucesso!")
                

                

                data = {
                      'codigo_requisicao': code,
                      'solicitante': solicitant,
                      'local_entrega': destination,
                      'justificativa': justify,
                      'valor_total': str(amount),
                      'motivo': reason,
                      'cod_arq': file_code,
                      'date': date,
                      'name_file': file_name,
                      'empresa': company,
                      'itens': st.session_state['items']
                }

                generate_ci(data=data, word_output_path=word_output_path)

                
        if word_output_path is not None:
            
            convertapi.api_credentials = 'secret_PYmspYXG8HzmXldH'

             
            converted_pdf = os.path.join("uploads", f"{file_name}.pdf")
            image_pdf = os.path.join("preloads", f"{file_name}.png")


            convertapi.convert('png', {'File': word_output_path}, from_format='docx').save_files(image_pdf)
            convertapi.convert('pdf', {'File': word_output_path}, from_format='docx').save_files(converted_pdf)

            st.image(image_pdf, width=500)
            
            with open(converted_pdf, "rb") as pdf_file:
                pdf_bytes = pdf_file.read()

            st.download_button(
                label="Baixar em formato PDF",
                data=pdf_bytes,
                file_name=f"{file_name}.pdf",
                mime="application/pdf"
            )

            with open(word_output_path, "rb") as file:
                        file_bytes = file.read()

            st.download_button(
                        label='Baixar em formato WORD',
                        file_name=name_file,
                        data=file_bytes,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )

            with st.form(key="merge_pdf"):
                submit = st.form_submit_button("Juntar PDF - PO e CI")

                if submit:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
                            temp_pdf.write(pdf_path.read())
                            temp_pdf_path = temp_pdf.name

                    merged_pdf = os.path.join("merged", f'{file_name}.pdf')
                    convertapi.convert('merge', {'Files': [converted_pdf, temp_pdf_path]}, from_format='pdf').save_files(merged_pdf)

                    with open(merged_pdf, "rb") as merged_file:
                            merged_pdf_bytes = merged_file.read()

                    st.download_button(
                            label="Baixar Arquivos Mesclados",
                            data=merged_pdf_bytes,
                            file_name=f"{file_name}.pdf",
                            mime="application/pdf"
                        )
                     

    except Exception as e:
        st.error(f"Ocorreu um erro ao carregar o arquivo: {e}")

else:
    st.info("Por favor, carregue um arquivo para gerar sua CI.")
