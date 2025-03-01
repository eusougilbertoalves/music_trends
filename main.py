import os
import logging
import yaml
from dotenv import load_dotenv
from utils.llm_connector import LLMConnector
from utils.report import generate_markdown_report, save_markdown_report, convert_markdown_to_pdf
from utils.serper_dev_tool import SerperDevTool

# Configuração do logging
log_dir = 'log'
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_dir, 'app.log'),
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_prompt_config(config_path: str = 'config/prompts.yaml') -> dict:
    """
    Carrega a configuração de prompts do arquivo YAML.
    
    Args:
        config_path (str): Caminho para o arquivo de configuração.
    
    Returns:
        dict: Configuração carregada.
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        logging.info("Configuração de prompts carregada com sucesso.")
        return config
    except Exception as e:
        logging.error(f"Erro ao carregar configuração: {e}")
        raise

def get_enhanced_trends(serper_tool: SerperDevTool, config: dict) -> list:
    """
    Coleta dados de tendências de múltiplas fontes usando o SerperDevTool.
    
    Args:
        serper_tool (SerperDevTool): Instância do SerperDevTool.
        config (dict): Configuração de prompts.
    
    Returns:
        list: Lista combinada de tendências e insights.
    """
    all_trends = []
    max_results = config['analysis_prompt']['max_results_per_query']
    
    for query_config in config['queries']:
        query = query_config['query']
        weight = query_config.get('weight', 1.0)
        
        logging.info(f"Buscando tendências para: {query}")
        results = serper_tool.search(query)
        
        if results and isinstance(results, dict):
            organic_results = results.get('organic', [])
            trends = [{
                'title': item.get('title', ''),
                'snippet': item.get('snippet', ''),
                'link': item.get('link', ''),
                'position': item.get('position', 0),
                'query': query,
                'category': query_config['name'],
                'weight': weight
            } for item in organic_results[:max_results]]
            all_trends.extend(trends)
    
    return all_trends

def analyze_trends(trends: list, llm_connector: LLMConnector, config: dict) -> str:
    """
    Utiliza o LLMConnector para analisar os dados de tendências coletados.

    Args:
        trends (list): Lista de tendências.
        llm_connector (LLMConnector): Instância do LLMConnector.
        config (dict): Configuração de prompts.

    Returns:
        str: Insights gerados pelo LLM.
    """
    if not trends:
        logging.warning("Nenhuma tendência encontrada para análise.")
        return "Nenhuma tendência encontrada para análise."

    # Organizando as tendências por categoria
    categorized_trends = {}
    for trend in trends:
        category = trend['category']
        if category not in categorized_trends:
            categorized_trends[category] = []
        categorized_trends[category].append(trend)

    # Construindo o prompt baseado na configuração
    prompt_config = config['analysis_prompt']
    prompt = f"{prompt_config['system_context']}\n{prompt_config['main_instruction']}\n\n"

    # Adicionando tendências categorizadas ao prompt
    for category, trend_list in categorized_trends.items():
        prompt += f"\n## Categoria: {category}\n"
        for trend in trend_list:
            prompt += f"\nFonte: {trend['link']}\n"
            prompt += f"- {trend['title']}\n"
            prompt += f"  {trend['snippet']}\n"

    # Adicionando tópicos e requisitos
    prompt += "\n## Tópicos para Análise:\n"
    for topic in prompt_config['topics']:
        prompt += f"- {topic['name']}\n"

    prompt += "\n## Requisitos da Análise:\n"
    for req in prompt_config['requirements']:
        prompt += f"- {req}\n"

    logging.info("Enviando prompt para o LLM.")
    response = llm_connector.complete(
        prompt,
        temperature=prompt_config['temperature'],
        max_tokens=prompt_config['max_tokens']
    )
    logging.info("Recebida resposta do LLM.")
    return response

def main():
    # Carregar variáveis de ambiente e configurações
    load_dotenv()
    config = load_prompt_config()
    
    # Criar diretório de relatórios, se não existir
    reports_dir = 'reports'
    os.makedirs(reports_dir, exist_ok=True)
    
    # Inicializar SerperDevTool
    logging.info("Inicializando SerperDevTool.")
    serper_tool = SerperDevTool()
    
    # Coletar dados de tendências usando SerperDevTool
    logging.info("Coletando dados de tendências.")
    trends = get_enhanced_trends(serper_tool, config)
    
    # Inicializar o conector LLM
    logging.info("Inicializando o LLMConnector.")
    llm_connector = LLMConnector(provider="groq", model="groq/llama-3.3-70b-versatile")
    
    # Analisar as tendências coletadas
    logging.info("Analisando tendências.")
    insights = analyze_trends(trends, llm_connector, config)
    
    # Gerar relatório em Markdown
    logging.info("Gerando relatório em Markdown.")
    markdown_report = generate_markdown_report(insights)
    markdown_path = os.path.join(reports_dir, 'trends_report.md')
    save_markdown_report(markdown_report, markdown_path)
    
    # Converter relatório para PDF
    logging.info("Convertendo relatório para PDF.")
    pdf_path = os.path.join(reports_dir, 'trends_report.pdf')
    convert_markdown_to_pdf(markdown_path, pdf_path)
    
    logging.info(f"Relatórios gerados: {markdown_path} e {pdf_path}")
    print(f"Relatórios gerados: {markdown_path} e {pdf_path}")

if __name__ == "__main__":
    main()