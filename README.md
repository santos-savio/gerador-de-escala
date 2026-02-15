# Gerador de Escala

Sistema web para criação automática de escalas de voluntários para a Igreja Adventista do Sétimo Dia de Boa Vista.

## 🚀 Como Executar

### Pré-requisitos
- Python 3.7 ou superior
- Pip (gerenciador de pacotes Python)

### Instalação
1. Instale as dependências:
```bash
pip install -r requirements.txt
```

### Execução
1. Inicie o servidor Flask:
```bash
python app.py
```

2. Acesse a aplicação no navegador:
```
http://localhost:5000
```

## 📁 Estrutura do Projeto

```
gerador-de-escala/
├── app.py              # Servidor Flask
├── requirements.txt    # Dependências Python
├── templates/
│   └── index.html     # Página principal da aplicação
├── IMG/               # Imagens temáticas dos departamentos
│   ├── mesa-som.png
│   ├── sabatina.png
│   ├── pregacao.jpg
│   ├── louvor.png
│   ├── recepcao.jpg
│   ├── diacono.jpg
│   ├── limpeza.jpeg
│   └── infantil.jpg
└── README.md          # Este arquivo
```

## 🎯 Funcionalidades

- **Gestão de Departamentos**: Suporte para múltiplos departamentos da igreja
- **Cadastro de Voluntários**: Sistema de disponibilidade semanal
- **Geração Automática**: Algoritmo balanceado para criação de escalas
- **Exportação**: Geração de imagens PNG das escalas
- **Persistência**: Dados salvos localmente no navegador
- **Interface Moderna**: Design responsivo com modo dark/light

## 🔧 Configuração

O servidor Flask está configurado para:
- Rodar na porta 5000
- Aceitar conexões externas (host: 0.0.0.0)
- Servir arquivos estáticos da pasta IMG
- Debug mode ativado para desenvolvimento

## 📝 Uso

1. Selecione o departamento e período desejado
2. Cadastre os voluntários com suas disponibilidades
3. Configure a frequência necessária por dia
4. Gere a escala automaticamente
5. Exporte como imagem para compartilhamento

## 🌐 Tecnologias

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript Vanilla
- **Exportação**: html2canvas
- **Armazenamento**: LocalStorage (navegador)

## 👨‍💻 Créditos

**Criador:** [MrKronox](https://github.com/MrKronox)

**Repositório Original:** https://github.com/MrKronox/escala-boa-vista.git

Desenvolvido para a comunidade da Igreja Adventista do Sétimo Dia de Boa Vista.
