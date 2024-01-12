import os
import time
import datetime
import subprocess
import zipfile
import requests

# Obtém o diretório atual onde o script Python está localizado
diretorio_atual = os.path.dirname(os.path.abspath(__file__))

# Define o caminho completo para a pasta steam.cmd
caminho_steamcmd = os.path.join(diretorio_atual, 'steamcmd')

# Verifica se a pasta steam.cmd não existe e a cria
if not os.path.exists(caminho_steamcmd):
    os.makedirs(caminho_steamcmd)

# Define o caminho completo para o executável steamcmd.exe
caminho_executavel = os.path.join(caminho_steamcmd, 'steamcmd.exe')

# Define a URL do arquivo compactado
url_arquivo_zip = 'https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip'

# Define o caminho para o arquivo compactado baixado
caminho_arquivo_zip = os.path.join(caminho_steamcmd, 'arquivo.zip')

# Baixa o arquivo compactado
response = requests.get(url_arquivo_zip)
with open(caminho_arquivo_zip, 'wb') as zip_file:
    zip_file.write(response.content)

# Extrai o conteúdo do arquivo compactado
with zipfile.ZipFile(caminho_arquivo_zip, 'r') as zip_ref:
    zip_ref.extractall(caminho_steamcmd)

# Remove o arquivo compactado após a extração
os.remove(caminho_arquivo_zip)

# Comando SteamCMD
steamcmd_command_download_serve = f'"{caminho_executavel}" +force_install_dir "{diretorio_atual}" +login anonymous +app_update 258550 +quit'

# Comando SteamCMD
steamcmd_command_validate_serve = f'"{caminho_executavel}" +force_install_dir "{diretorio_atual}" +login anonymous +app_update 258550 validate +quit'

# Função para executar comandos SteamCMD
def executar_comando_steamcmd(comando):
    try:
        subprocess.run(comando, shell=True, check=True)
        print("Comando SteamCMD executado com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando SteamCMD: {e}")

# Função para iniciar o servidor Rust
def iniciar_servidor():
    # Define o caminho completo para o RustDedicated.exe na mesma pasta do script
    rust_executable_path = os.path.join(diretorio_atual, 'RustDedicated.exe')

    # Verifica se o arquivo executável do servidor existe
    if not os.path.exists(rust_executable_path):
        # Validar os arquivos
        print("Arquivo executável do servidor não encontrado. Validando arquivos...")
        try:
            executar_comando_steamcmd(steamcmd_command_validate_serve)
        except subprocess.CalledProcessError:
            print("Arquivos do servidor corrompidos. Realizando download...")
            # Download dos arquivos
            executar_comando_steamcmd(steamcmd_command_download_serve)

    # Define o caminho completo para o arquivo server.cfg
    nome_servidor = "MEUPRIMEIRO"
    pasta_servidor = os.path.join(diretorio_atual, 'server', nome_servidor)
    pasta_oxide = os.path.join(pasta_servidor, 'oxide')
    pasta_cfg = os.path.join(pasta_servidor, 'cfg')

    os.makedirs(pasta_servidor, exist_ok=True)
    os.makedirs(pasta_oxide, exist_ok=True)
    os.makedirs(pasta_cfg, exist_ok=True)

    caminho_server_cfg = os.path.join(pasta_cfg, 'server.cfg')

    # Cria o arquivo server.cfg se não existir
    if not os.path.exists(caminho_server_cfg):
        with open(caminho_server_cfg, 'w', encoding='utf-8') as cfg_file:
            cfg_file.write("""server.headerimage "https://i.imgur.com/wexkpGV.png"
server.logoimage "https://i.imgur.com/YnYVl7j.png"
server.tags "SA,monthly,battlefield,vanilla"
server.url "https://discord.gg/7FZwy2mX2k"
server.description "-Servidor Brasileiro \\n-América do Sul \\n-Ping Extremamente baixo \\n-Nosso discord oficial: discord.gg/7FZwy2mX2k""")

    # Comandos que são usados junto com o RustDedicated.exe do servidor
    rust_command = [
        '-batchmode',
        '-nographics',
        '+oxide.directory', f'server/{nome_servidor}/oxide',
        '+server.hostname', '[BR] Meu-Servidor',
        '+server.ip', '0.0.0.0',
        '+server.port', '28015',
        '+server.maxplayers', '100',
        '+rcon.ip', '0.0.0.0',
        '+app.port', '89480',
        '+rcon.port', '82454',
        '+rcon.password', 'sdjksdg',
        f'+server.identity {nome_servidor}',
        '+server.level', 'Procedural Map',
        '+server.seed', '2234',
        '+server.worldsize', '4000',
        '+server.radiation', 'True',
        '+bradley.enabled', 'True',
        '+bradley.respawndelayminutes', '60',
        '+bradley.respawndelayvariance', '1',
        '+heli.lifetimeminutes', '15',
        '+server.stability', 'True',
        '+decay.upkeep', 'True',
        '+decay.upkeep_heal_scale', '1',
        '+decay.upkeep_inside_decay_scale', '0.1',
        '+decay.upkeep_period_minutes', '1440',
        '+rcon.web', 'True',
        '-LogFile', f'{pasta_servidor}/serverlog.log'
    ]
    # Configuração do ambiente para incluir o diretório atual
    env = os.environ.copy()
    env['PATH'] = f"{diretorio_atual};{env['PATH']}"
    # Comando para iniciar o RustDedicated.exe
    comando = [rust_executable_path] + rust_command

    try:
        subprocess.run(comando, cwd=diretorio_atual, env=env, check=True)
    except subprocess.CalledProcessError as e:
        # Log de erro com a data e hora atual
        data_hora = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_path = os.path.join(diretorio_atual, 'logs', f'error_log_{data_hora}.txt')
        with open(log_path, 'w') as log_file:
            log_file.write(f"Erro ao iniciar o servidor Rust em {data_hora}:\n{e}\n")

# Loop para executar o servidor continuamente
while True:
    # Iniciar o servidor e esperar 5 segundos antes de tentar reiniciar
    iniciar_servidor()
    print("Esperando 5 segundos antes de reiniciar o servidor...")
    time.sleep(5)
