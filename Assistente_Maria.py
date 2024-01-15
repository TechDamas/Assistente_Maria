# para instalar todos os modulos
# pip install -r requirements.txt
import time
import openai  # pip install openai
import speech_recognition as sr  # pip install SpeechRecognition
import whisper  # pip install whisper-openai
import pyttsx3  # pip install pyttsx3
import os
import subprocess
import pexpect.popen_spawn
import sys
import unicodedata
import re
import sqlite3

# Inicialize aqui sua senha da API
openai.api_key='Insira aqui sua senha da API'

# caso nao queira falar "assistente" ou "Chat GPT"
sem_palavra_ativadora = False
# printa o total de tokens por interacao
debug_custo = True
# print de algumas informacoes para debug
debugar = False
# define qual gerador de texto
# escolher_stt = "whisper"
escolher_stt = "google"
# escolhe entrada por texto ou voz
entrada_por_texto = False
# falar ou nao
falar = True

if entrada_por_texto:
    sem_palavra_ativadora = True


def interpretar_numero(palavras):
    numeros_texto = {
        'um': '1',
        'dois': '2',
        'três': '3',
        'quatro': '4',
        'cinco': '5',
        'seis': '6',
        'sete': '7',
        'oito': '8',
        'nove': '9',
        'dez': '10'
    }

    for palavra in palavras:
        palavra = palavra.lower()
        if palavra in numeros_texto:
            return numeros_texto[palavra]

    return None


def remover_caracteres_especiais(texto):
    # Normaliza a string removendo os caracteres especiais
    texto_normalizado = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
    return texto_normalizado


def criar_tarefa_nova():
    caminho_programa = '.\gerenciador_de_tarefas.exe'
    talk('qual o nome da tarefa?')
    time.sleep(1)
    print('Fale alguma coisa:')

    try:
        audio_nome = r.listen(fonte)
        nome_tarefa = r.recognize_google(audio_nome, language="pt-BR")
        nome_tarefa = remover_caracteres_especiais(nome_tarefa)
        print(f'Nome da tarefa: {nome_tarefa}')
    except sr.UnknownValueError:
        print("Não foi possível entender o nome da tarefa.")
        talk("Não consegui entender o nome da tarefa. Por favor, tente novamente.")
        return
    except sr.RequestError as e:
        print(f"Erro na requisição ao serviço de reconhecimento de fala: {e}")
        talk("Houve um problema na requisição ao serviço de reconhecimento de fala. Por favor, tente novamente mais tarde.")
        return

    talk('qual a descrição dessa tarefa?')
    time.sleep(1)
    print('Fale alguma coisa:')

    try:
        audio_descricao = r.listen(fonte)
        desc_tarefa = r.recognize_google(audio_descricao, language="pt-BR")
        desc_tarefa = remover_caracteres_especiais(desc_tarefa)
        print(f'Descrição da tarefa: {desc_tarefa}')
    except sr.UnknownValueError:
        print("Não foi possível entender a descrição da tarefa.")
        talk("Não consegui entender a descrição da tarefa. Por favor, tente novamente.")
        return
    except sr.RequestError as e:
        print(f"Erro na requisição ao serviço de reconhecimento de fala: {e}")
        talk("Houve um problema na requisição ao serviço de reconhecimento de fala. Por favor, tente novamente mais tarde.")
        return

    processo = pexpect.popen_spawn.PopenSpawn (caminho_programa)
    processo.sendline(f'1\n{nome_tarefa}\n{desc_tarefa}\n6\n')

    talk('tarefa criada com sucesso')

def ler_tarefa():
    # Conectar-se ao banco de dados
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    # Exemplo: Se a tabela se chama "tarefas" e possui colunas "tarefa" e "descricao"
    cursor.execute('SELECT id, title, description, completed FROM tasks')

    # Recuperar todas as linhas
    tarefas = cursor.fetchall()

    # Mostrar as tarefas e descrições
    for tarefa in tarefas:
        numero_da_tarefa = tarefa[0]  # ID da tarefa
        titulo = tarefa[1]  # Título da tarefa
        descricao = tarefa[2]  # Descrição da tarefa
        completa = "Completa" if tarefa[3] else "Incompleta"  # Verifica se está completa

        talk(f"Número da Tarefa: {numero_da_tarefa}")
        talk(f"Título: {titulo}")
        talk(f"Descrição: {descricao}")
        talk(f"Status: {completa}")

    # Fechar conexão
    conn.close()

def deletar_tarefa():
    caminho_programa = '.\gerenciador_de_tarefas.exe'

    talk('qual o indice da tarefa?')
    time.sleep(1)
    print('Fale alguma coisa:')

    try:
        numeros = ["um", "dois", "três", "quatro", "cinco", "seis", "sete", "oito", "nove", "dez"]
        audio_nome = r.listen(fonte)
        palavra = r.recognize_google(audio_nome, language="pt-BR")
        print(f'Frase reconhecida: {palavra}')
        if not palavra:
            print("Não foi possível entender o indice da tarefa.")
            talk("Não consegui entender o nome da tarefa. Por favor, tente novamente.")
            return

        palavra = re.findall(r'\b(?:' + '|'.join (numeros) + r')\b', palavra)
        if palavra is None:
            print("Não foi possível encontrar um número na frase.")
            talk("Não consegui encontrar um número na frase. Por favor, tente novamente.")
            return

        indice_tarefa = interpretar_numero(palavra)
        print(f'Índice da tarefa: {indice_tarefa}')

    except sr.UnknownValueError:
        print("Não foi possível entender o indice da tarefa.")
        talk("Não consegui entender o nome da tarefa. Por favor, tente novamente.")
        return
    except sr.RequestError as e:
        print(f"Erro na requisição ao serviço de reconhecimento de fala: {e}")

    try:
        # Inicie o programa usando pexpect
        processo = pexpect.popen_spawn.PopenSpawn (caminho_programa)
        processo.sendline(f'5\n{indice_tarefa}\n6\n')
        talk('tarefa deletada com sucesso')
        print("Programa executado com sucesso!")
    except subprocess.CalledProcessError as e:
        mensagem_decodificada = e.output.decode (sys.getfilesystemencoding ())
        print(f"Erro ao executar o programa: {e.output.decode (sys.getfilesystemencoding ())}")


def marcar_tarefa():
    caminho_programa = '.\gerenciador_de_tarefas.exe'

    talk('qual o indice da tarefa?')
    time.sleep(1)
    print('Fale alguma coisa:')

    try:
        numeros = ["um", "dois", "três", "quatro", "cinco", "seis", "sete", "oito", "nove", "dez"]
        audio_nome = r.listen(fonte)
        palavra = r.recognize_google(audio_nome, language="pt-BR")
        print(f'Frase reconhecida: {palavra}')
        if not palavra:
            print("Não foi possível entender o indice da tarefa.")
            talk("Não consegui entender o nome da tarefa. Por favor, tente novamente.")
            return

        palavra = re.findall(r'\b(?:' + '|'.join(numeros) + r')\b', palavra)
        if palavra is None:
            print("Não foi possível encontrar um número na frase.")
            talk("Não consegui encontrar um número na frase. Por favor, tente novamente.")
            return


        indice_tarefa = interpretar_numero(palavra)
        print(f'Índice da tarefa: {indice_tarefa}')

    except sr.UnknownValueError:
        print("Não foi possível entender o indice da tarefa.")
        talk("Não consegui entender o nome da tarefa. Por favor, tente novamente.")
        return
    except sr.RequestError as e:
        print(f"Erro na requisição ao serviço de reconhecimento de fala: {e}")

    try:
        # Inicie o programa usando pexpect
        processo = pexpect.popen_spawn.PopenSpawn (caminho_programa)
        processo.sendline(f'5\n{indice_tarefa}\n6\n')
        talk ('tarefa atualizada com sucesso')
        print("Programa executado com sucesso!")
    except subprocess.CalledProcessError as e:
        mensagem_decodificada = e.output.decode (sys.getfilesystemencoding ())
        print(f"Erro ao executar o programa: {e.output.decode (sys.getfilesystemencoding ())}")


def atualizar_tarefa():
    caminho_programa = '.\gerenciador_de_tarefas.exe'

    talk('qual o indice da tarefa?')
    time.sleep(1)
    print('Fale alguma coisa:')

    try:
        numeros = ["um", "dois", "três", "quatro", "cinco", "seis", "sete", "oito", "nove", "dez"]
        audio_nome = r.listen(fonte)
        palavra = r.recognize_google(audio_nome, language="pt-BR")
        print(f'Frase reconhecida: {palavra}')
        if not palavra:
            print("Não foi possível entender o indice da tarefa.")
            talk("Não consegui entender o nome da tarefa. Por favor, tente novamente.")
            return

        palavra = re.findall(r'\b(?:' + '|'.join(numeros) + r')\b', palavra)
        if palavra is None:
            print("Não foi possível encontrar um número na frase.")
            talk("Não consegui encontrar um número na frase. Por favor, tente novamente.")
            return


        indice_tarefa = interpretar_numero(palavra)
        print(f'Índice da tarefa: {indice_tarefa}')

    except sr.UnknownValueError:
        print("Não foi possível entender o indice da tarefa.")
        talk("Não consegui entender o nome da tarefa. Por favor, tente novamente.")
        return
    except sr.RequestError as e:
        print(f"Erro na requisição ao serviço de reconhecimento de fala: {e}")

    talk('qual o novo nome da tarefa?')
    time.sleep(1)
    print('Fale alguma coisa:')

    try:
        audio_nome = r.listen(fonte)
        novo_nome = r.recognize_google(audio_nome, language="pt-BR")
        novo_nome = remover_caracteres_especiais(novo_nome)
        print(f'Nome da tarefa: {novo_nome}')
    except sr.UnknownValueError:
        print("Não foi possível entender o nome da tarefa.")
        talk("Não consegui entender o nome da tarefa. Por favor, tente novamente.")
        return
    except sr.RequestError as e:
        print(f"Erro na requisição ao serviço de reconhecimento de fala: {e}")
        talk("Houve um problema na requisição ao serviço de reconhecimento de fala. Por favor, tente novamente mais tarde.")
        return

    talk('qual a nova descrição da tarefa?')
    time.sleep(1)
    print('Fale alguma coisa:')

    try:
        audio_nome = r.listen(fonte)
        nova_descricao = r.recognize_google(audio_nome, language="pt-BR")
        nova_descricao = remover_caracteres_especiais(nova_descricao)
        print(f'Nome da tarefa: {nova_descricao}')
    except sr.UnknownValueError:
        print("Não foi possível entender a descrição da tarefa.")
        talk("Não consegui entender o nome da tarefa. Por favor, tente novamente.")
        return
    except sr.RequestError as e:
        print(f"Erro na requisição ao serviço de reconhecimento de fala: {e}")
        talk("Houve um problema na requisição ao serviço de reconhecimento de fala. Por favor, tente novamente mais tarde.")
        return

    try:
        # Inicie o programa usando pexpect
        processo = pexpect.popen_spawn.PopenSpawn (caminho_programa)
        processo.sendline(f'3\n{indice_tarefa}\n{novo_nome}\n{nova_descricao}\n6\n')
        talk('tarefa atualizada com sucesso')
        print("Programa executado com sucesso!")
    except subprocess.CalledProcessError as e:
        mensagem_decodificada = e.output.decode (sys.getfilesystemencoding ())
        print(f"Erro ao executar o programa: {e.output.decode (sys.getfilesystemencoding ())}")


def generate_answer(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  ##
        # model="gpt-3.5-turbo-0301", ## ateh 1 junho 2023
        messages=messages,
        max_tokens=1000,
        temperature=0.5
    )
    return [response.choices[0].message.content, response.usage]


def talk(texto):
    # falando
    engine.say(texto)
    engine.runAndWait()
    engine.stop()


def save_file(dados):
    with open(path + filename, "wb") as f:
        f.write(dados)
        f.flush()


# reconhecer
r = sr.Recognizer()
mic = sr.Microphone()
model = whisper.load_model("base")

# falar
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('rate', 200)  # velocidade 120 = lento
for indice, vozes in enumerate(voices):  # listar vozes
    print(indice, vozes.name)
voz = 0  # "IVONA_2_Ricardo_OEM"
engine.setProperty('voice', voices[voz].id)

mensagens = [{"role": "system", "content": "Você é um assistente gente boa. E meu nome é Bob!"}]

path = os.getcwd()
filename = "audio.wav"

print("Speak to Text", escolher_stt)

ajustar_ambiente_noise = True

# Ajuste inicial do ambiente
with mic as fonte:
    r.adjust_for_ambient_noise(fonte)
    ajustar_ambiente_noise = False

while True:
    text = ""
    question = ""

    if entrada_por_texto:
        question = input("Perguntar pro ChatGPT (\"sair\"): ")
    else:
        # Ask a question
        with mic as fonte:
            print("Fale alguma coisa")
            audio = r.listen(fonte)
            print("Enviando para reconhecimento")

            if escolher_stt == "google":
                question = r.recognize_google(audio, language="pt-BR")
            elif escolher_stt == "whisper":
                save_file(audio.get_wav_data())

        if escolher_stt == "whisper":
            # Ajuste adicional do áudio se necessário
            model.transcribe(path + filename, language='pt', fp16=False)
            text = model.transcribe(path + filename, language='pt', fp16=False)
            question = text["text"]

    if ("desligar" in question and "assistente" in question) or question.startswith("sair"):
        print(question, "Saindo.")
        if falar:
            talk("Desligando")
        break
    elif question == "" and text == "":
        print("No sound")
        continue

    elif question.startswith('Maria'):
        talk('Olá matheus, em que posso te ajudar?:')
        time.sleep(1.5)
        with mic as fonte:
            print('Fale alguma coisa')
            audio = r.listen(fonte)
            print('enviando para reconhecimento')
            opcao = r.recognize_google(audio, language="pt-BR")
            if 'crie uma nova tarefa' in opcao:
                # Ajuste adicional do áudio se necessário
                r.adjust_for_ambient_noise(fonte)
                ajustar_ambiente_noise = False
                criar_tarefa_nova()
            elif 'atualize uma tarefa' in opcao:
                r.adjust_for_ambient_noise (fonte)
                ajustar_ambiente_noise = False
                atualizar_tarefa()
            elif 'marcar tarefa' in opcao:
                r.adjust_for_ambient_noise(fonte)
                ajustar_ambiente_noise = False
                marcar_tarefa()
            elif 'exclua uma tarefa' in opcao:
                r.adjust_for_ambient_noise(fonte)
                ajustar_ambiente_noise = False
                deletar_tarefa()
            elif 'quais são minhas tarefas?':
                r.adjust_for_ambient_noise(fonte)
                ajustar_ambiente_noise = False
                ler_tarefa()
            elif opcao == "":
                print('No mensagem')
                continue

    elif question.startswith("assistente GPT") or question.startswith("Maria GPT") or sem_palavra_ativadora:
        print("Me:", question)
        mensagens.append({"role": "user", "content": str(question)})

        answer = generate_answer(mensagens)

        print("ChatGPT:", answer[0])

        if debug_custo:
            print("Cost:\n", answer[1])

        mensagens.append({"role": "assistant", "content": answer[0]})

        if falar:
            talk(answer[0])
    else:
        print("No message")
        continue

    if debugar:
        print("Mensages", mensagens, type(mensagens))
print("Obrigado, até mais!!")