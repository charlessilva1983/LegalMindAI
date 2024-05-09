import requests
from pathlib import Path
import hashlib
import google.generativeai as genai

genai.configure(api_key="AIzaSyAwEYuuhqOPJ-VuWwlymOoITTko_2_r8Sk")

# Set up the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

def remover_zero_esquerda(numero):
    # Remove o zero à esquerda apenas se estiver na faixa de 01 a 09
    if len(numero) > 1 and numero[0] == '0':
        return numero[1:]
    return numero


# Aqui, tribunais é um dicionário que você precisa ter definido anteriormente
# Por exemplo:
tribunais = {
    1: {'link': '', 'nome': 'Supremo Tribunal Federal'},
    2: {'link': '', 'nome': 'Conselho Nacional de Justiça'},
    3: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_stj/_search', 'nome': 'Superior Tribunal de Justiça'},
    4: {
        1: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_trf1/_search', 'nome': 'Tribunal Regional Federal da 1a Região'},
        2: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_trf2/_search', 'nome': 'Tribunal Regional Federal da 2a Região'},
        3: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_trf3/_search', 'nome': 'Tribunal Regional Federal da 3a Região'},
        4: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_trf4/_search', 'nome': 'Tribunal Regional Federal da 4a Região'},
        5: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_trf5/_search', 'nome': 'Tribunal Regional Federal da 5a Região'},
        6: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_trf6/_search', 'nome': 'Tribunal Regional Federal da 6a Região'}
    },
    5: {
        0: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_tst/_search', 'nome': 'Tribunal Superior do Trabalho'},
        1: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_trt1/_search', 'nome': 'Tribunal Regional do Trabalho da 1 região'},
        2: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_trt2/_search', 'nome': 'Tribunal Regional do Trabalho da 2 região'},
        3: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_trt3/_search', 'nome': 'Tribunal Regional do Trabalho da 3 região'},
        4: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_trt4/_search', 'nome': 'Tribunal Regional do Trabalho da 4 região'},
        5: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_trt5/_search', 'nome': 'Tribunal Regional do Trabalho da 5 região'},
        6: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_trt6/_search', 'nome': 'Tribunal Regional do Trabalho da 6 região'},
        7: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_trt7/_search', 'nome': 'Tribunal Regional do Trabalho da 7 região'},
        8: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_trt8/_search', 'nome': 'Tribunal Regional do Trabalho da 8 região'},
        9: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_trt9/_search', 'nome': 'Tribunal Regional do Trabalho da 9 região'},
        10: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_trt10/_search', 'nome': 'Tribunal Regional do Trabalho da 10 região'},
        11: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_trt11/_search', 'nome': 'Tribunal Regional do Trabalho da 11 região'},
        12: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_trt12/_search', 'nome': 'Tribunal Regional do Trabalho da 12 região'},
        13: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_trt13/_search', 'nome': 'Tribunal Regional do Trabalho da 13 região'},
        14: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_trt14/_search', 'nome': 'Tribunal Regional do Trabalho da 14 região'},
        15: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_trt15/_search', 'nome': 'Tribunal Regional do Trabalho da 15 região'},
        16: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_trt16/_search', 'nome': 'Tribunal Regional do Trabalho da 16 região'},
        17: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_trt17/_search', 'nome': 'Tribunal Regional do Trabalho da 17 região'},
        18: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_trt18/_search', 'nome': 'Tribunal Regional do Trabalho da 18 região'},
        19: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_trt19/_search', 'nome': 'Tribunal Regional do Trabalho da 19 região'},
        20: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_trt20/_search', 'nome': 'Tribunal Regional do Trabalho da 20 região'},
        21: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_trt21/_search', 'nome': 'Tribunal Regional do Trabalho da 21 região'},
        22: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_trt22/_search', 'nome': 'Tribunal Regional do Trabalho da 22 região'},
        23: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_trt23/_search', 'nome': 'Tribunal Regional do Trabalho da 23 região'},
        24: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_trt24/_search', 'nome': 'Tribunal Regional do Trabalho da 24 região'}
    },
    6: {
        0: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_tse/_search', 'nome': 'Tribunal Superior Eleitoral'},
        1: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_tre-ac/_search', 'nome': 'Tribunal Regional Eleitoral do Acre'},
        2: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_tre-al/_search', 'nome': 'Tribunal Regional Eleitoral de Alagoas'},
        3: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_tre-ap/_search', 'nome': 'Tribunal Regional Eleitoral do Amapá'},
        4: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_tre-am/_search', 'nome': 'Tribunal Regional Eleitoral de Amazonas'},
        5: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_tre-ba/_search', 'nome': 'Tribunal Regional Eleitoral da Bahia'},
        6: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_tre-ce/_search', 'nome': 'Tribunal Regional Eleitoral do Ceará'},
        7: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_tre-df/_search', 'nome': 'Tribunal Regional Eleitoral do Distrito Federal'},
        8: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_tre-es/_search', 'nome': 'Tribunal Regional Eleitoral do Espírito Santo'},
        9: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_tre-go/_search', 'nome': 'Tribunal Regional Eleitoral de Goiás'},
        10: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_tre-ma/_search', 'nome': 'Tribunal Regional Eleitoral do Maranhão'},
        11: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_tre-mt/_search', 'nome': 'Tribunal Regional Eleitoral do Mato Grosso'},
        12: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_tre-ms/_search', 'nome': 'Tribunal Regional Eleitoral do Mato Grosso do Sul'},
        13: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_tre-mg/_search', 'nome': 'Tribunal Regional Eleitoral de Minas Gerais'},
        14: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_tre-pa/_search', 'nome': 'Tribunal Regional Eleitoral do Pará'},
        15: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_tre-pb/_search', 'nome': 'Tribunal Regional Eleitoral da Paraíba'},
        16: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_tre-pr/_search', 'nome': 'Tribunal Regional Eleitoral do Paraná'},
        17: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_tre-pe/_search', 'nome': 'Tribunal Regional Eleitoral de Pernambuco'},
        18: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_tre-pi/_search', 'nome': 'Tribunal Regional Eleitoral do Piauí'},
        19: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_tre-rj/_search', 'nome': 'Tribunal Regional Eleitoral do Rio de Janeiro'},
        20: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_tre-rn/_search', 'nome': 'Tribunal Regional Eleitoral do Rio Grande do Norte'},
        21: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_tre-rs/_search', 'nome': 'Tribunal Regional Eleitoral do Rio Grande do Sul'},
        22: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_tre-ro/_search', 'nome': 'Tribunal Regional Eleitoral de Rondônia'},
        23: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_tre-rr/_search', 'nome': 'Tribunal Regional Eleitoral de Roraima'},
        24: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_tre-sc/_search', 'nome': 'Tribunal Regional Eleitoral de Santa Catarina'},
        25: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_tre-se/_search', 'nome': 'Tribunal Regional Eleitoral de Sergipe'},
        26: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_tre-sp/_search', 'nome': 'Tribunal Regional Eleitoral de São Paulo'},
        27: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_tre-to/_search', 'nome': 'Tribunal Regional Eleitoral de Tocantins'}
    },
    7: {
        0: {'link': 'https://api-publica.datajud.cnj.jus.br/api_publica_stm/_search', 'nome': 'Tribunal Superior Militar'},
        1: {'link': '', 'nome': '1a Circunscrição Judiciária Militar'},
        2: {'link': '', 'nome': '2a Circunscrição Judiciária Militar'},
        3: {'link': '', 'nome': '3a Circunscrição Judiciária Militar'},
        4: {'link': '', 'nome': '4a Circunscrição Judiciária Militar'},
        5: {'link': '', 'nome': '5a Circunscrição Judiciária Militar'},
        6: {'link': '', 'nome': '6a Circunscrição Judiciária Militar'},
        7: {'link': '', 'nome': '7a Circunscrição Judiciária Militar'},
        8: {'link': '', 'nome': '8a Circunscrição Judiciária Militar'},
        9: {'link': '', 'nome': '9a Circunscrição Judiciária Militar'},
        10: {'link': '', 'nome': '10a Circunscrição Judiciária Militar'},
        11: {'link': '', 'nome': '11a Circunscrição Judiciária Militar'},
        12: {'link': '', 'nome': '12a Circunscrição Judiciária Militar'}
    }
}

def get_process_details(process_number):
    # Remove '.' e '-' do número do processo
    clean_process_number = process_number.replace('.', '').replace('-', '')
    
    # Extraindo os códigos de tipo de justiça e do tribunal, supondo que os índices estão corretos
    type_of_court_code = int(clean_process_number[13:14])  # Convertendo para int
    court_code = int(clean_process_number[14:16])  # Convertendo para int e removendo zeros à esquerda automaticamente

    # Acessando o dicionário de forma segura
    court_info = tribunais.get(type_of_court_code, {}).get(court_code, None)

    if court_info and court_info.get('link'):
        url = court_info['link']
        print(f"Type of court code: {type_of_court_code}")
        print(f"Court code: {court_code}")
        print(f"API URL: {url}")

        # Configuração da requisição HTTP
        headers = {
            'Authorization': 'APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==',
            'Content-Type': 'application/json',
            'x-li-format': 'json'
        }
        payload = {
            'query': {
                'match': {
                    'numeroProcesso': clean_process_number
                }
            }
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            results = response.json()
            processo = results['hits']['hits'][0]['_source']
            result = {
                'processo': processo,
                'tribunal': court_info['nome']
            }
            return result
        else:
            return {"error": "Erro ao consultar o processo."}
    else:
        return {"error": "Tribunal não encontrado ou link indisponível."}

print('Digite o Número do processo:')

process_number = input('Numero:')
# Exemplo de uso da função
result_process = get_process_details(process_number)

convo = model.start_chat(history=[
  {
    "role": "user",
    "parts": [f"Gere um relatorio a partir desses dados {result_process}"]
  },
])

convo.send_message("gere")
print(convo.last.text)
print('Como posso ajudar com esses dados?')
print('Caso não precise de mais nada só digitar ENCERRAR')

new_input = input('')

convo.send_message(new_input)
print(convo.last.text)


