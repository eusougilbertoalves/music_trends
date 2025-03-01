# Music Trends Analyzer

Um sistema de análise de tendências da indústria musical que utiliza IA para gerar insights estratégicos baseados em dados atuais do mercado.

## Características

- Coleta automatizada de tendências musicais de múltiplas fontes
- Análise usando modelos de linguagem avançados
- Geração de relatórios em formato Markdown e PDF
- Categorização inteligente de tendências
- Foco em diferentes aspectos do mercado musical (TikTok, gêneros emergentes, tecnologia, etc.)

## Requisitos

- Python 3.8+
- Groq API Key
- Serper API Key

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/eusougilbertoalves/music_trends.git
cd music_trends
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas chaves de API
```

## Uso

Execute o script principal:
```bash
python main.py
```

O sistema irá:
1. Coletar dados de tendências atuais
2. Analisar as tendências usando IA
3. Gerar relatórios detalhados em formato Markdown e PDF

## Estrutura do Projeto

```
music_trends/
├── config/
│   └── prompts.yaml       # Configurações de prompts e queries
├── utils/
│   ├── llm_connector.py   # Conexão com LLM
│   ├── serper_dev_tool.py # Ferramenta de busca
│   └── report.py         # Geração de relatórios
├── main.py               # Script principal
├── requirements.txt      # Dependências
└── README.md            # Este arquivo
```

## Configuração

O arquivo `config/prompts.yaml` contém:
- Queries de busca para diferentes aspectos do mercado musical
- Configurações do prompt de análise
- Parâmetros do modelo de IA
- Estrutura do relatório

## Contribuindo

1. Fork o projeto
2. Crie sua Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Contato

Gilberto Alves - [@eusougilbertoalves](https://github.com/eusougilbertoalves)

Link do Projeto: [https://github.com/eusougilbertoalves/music_trends](https://github.com/eusougilbertoalves/music_trends)