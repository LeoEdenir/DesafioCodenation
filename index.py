import requests
import json
import string
import hashlib

# faz a requisição HTTP
requisicao = "https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token=81c93fbacddc0a91448db75e669cca6cef000982"
r = requests.get(requisicao)

# transforma a requisição em objeto JSON
json_file = json.dumps(r.json())

# abre o arquivo e salva o conteúdo da requisição
arquivo = open("answer.json", "w")
arquivo.write(json_file)

# obtém o número de casas e o texto cifrado do arquivo
texto_cifrado = json.loads(json_file)['cifrado']
numero_casas = json.loads(json_file)['numero_casas']

arquivo.close()

# recebe alfabeto da biblioteca String
alfabeto = string.ascii_lowercase
texto_decifrado = ""

# faz a criografia de Júlio César
for i in texto_cifrado.lower():

    if i in alfabeto:

        index = alfabeto.index(i) - numero_casas
        if index < 0:
            index += len(alfabeto)

        texto_decifrado += alfabeto[index]

    else:
        texto_decifrado += i


# gera o resumo criptográfico em sha1
sha1 = hashlib.sha1(texto_decifrado.encode()).hexdigest()

print(texto_decifrado, sha1)

with open("answer.json", "r") as arquivo:
    arquivo_json = json.load(arquivo)
    arquivo_json['decifrado'] = texto_decifrado
    arquivo_json['resumo_criptografico'] = sha1

with open("answer.json", "w") as arquivo:
    arquivo_json = json.dumps(arquivo_json, indent=4)
    arquivo.write(arquivo_json)


# envia arquivo para a API
url = "https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token=81c93fbacddc0a91448db75e669cca6cef000982"
resposta = {'answer': open('answer.json', 'rb')}
r = requests.post(url, files=resposta)
