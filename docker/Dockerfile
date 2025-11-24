# Define nossa imagem base
FROM jenkins/jenkins:lts

# Define nosso usuario dentro do container
USER root

# Atualiza os pacotes do sistema
RUN apt-get update

# Instala Python e pip
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-venv

#instalando o npm
RUN apt-get install -y nodejs npm

# Instala Docker CLI
RUN apt-get install -y docker.io

# Adiciona jenkins ao grupo docker
RUN usermod -aG docker jenkins

# Da permissão para o usuário jenkins
RUN chown -R jenkins:jenkins /usr/local

# Limpa arquivos baixados com apt-get
RUN apt-get clean

USER jenkins