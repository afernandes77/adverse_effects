import os
import gradio as gr
import ollama

def analisar_incidente_local(descricao_evento, fatores_paciente, fatores_equipa, fatores_ambiente):
    prompt_sistema = (
        "Atue como um analista da qualidade em uma empresa de saúde que presta atendimento domiciliar (home care).\n"
        "O seu objetivo é classificar o caso descrito identificando em qual categoria de evento adverso ele se encaixa melhor. Escolha somente uma das categorias listadas abaixo: \n"
        "CIRCUNSTÂNCIA DE RISCO OU CONDIÇÕES INSEGURAS \n"
        "NEAR MISS \n"
        "INCIDENTE SEM DANO \n"
        "INCIDENTE COM DANO LEVE \n"
        "INCIDENTE COM DANO MODERADO \n"
        "INCIDENTE COM DANO GRAVE \n"
        "INCIDENTE COM DANO ÓBITO \n"
        "Use o seguinte contexto para cada uma das categorias listadas acima:\n"
        "CIRCUNSTÂNCIA DE RISCO OU CONDIÇÕES INSEGURAS - Uma situação com um potencial significativo para o dano, porém não ocorreu o incidente \n"
        "NEAR MISS - Uma falha que não atingiu o paciente \n"
        "INCIDENTE SEM DANO - Paciente assintomático. Não houve dano, sem necessidade de tratamento adicional \n"
        "INCIDENTE COM DANO LEVE - Paciente sintomático, com perda de função ou dano mínimo, com intervenção mínima ou monitoramento de curto prazo \n"
        "INCIDENTE COM DANO MODERADO - Paciente sintomático, com dano ou perda de função temporária, requer intervenção adicional(cirurgia de médio ou pequeno porte, tratamento clínico específico devido ao incidente), aumento do tempo de internação, não necessita de intervenção para suporte ou manutenção da vida \n"
        "INCIDENTE COM DANO GRAVE - Paciente sintomático com dano grave, necessitamos de intervenção para suporte ou manutenção da vida, intervenção clínica ou cirúrgica de grande porte \n"
        "INCIDENTE COM DANO ÓBITO - Paciente que evolui a óbito inesperado não relacionado ao curso natural da doença. O incidente pode ter causado ou antecipado a morte do paciente \n"
        "Depois de classificar o evento em uma categoria, enquadre o mesmo em um dos tipos abaixo: \n"
        "Erro de administração de medicamentos e dietas \n"
        "Falhas relacionadas a medicamentos \n"
        "Falhas relacionadas a dietas \n"
        "Erros de prescrição \n"
        "Eventos relacionados a infecções \n"
        "Falhas relacionadas a dispositivos \n"
        "Falhas relacionadas a procedimentos \n"
        "Queda do paciente (com ou sem lesão) \n"
        "Queixa relacionada à parte técnica \n"
        "Furo de escala e absenteísmo de profissionais \n"
        "Outros \n"
        "Segue o contexto para classificar os tipos de eventos: \n"
        "Erro de administração de medicamentos e dietas: se a descrição do evento contiver menções a erros de admnistração de medicamentos, NPT ou dietas, administração de dosagem errada, erro na via de administração \n"
        "Falhas relacionadas a medicamentos: falhas relacionadas a medicamentos que não sejam erros de admnistração nem de prescrição, por exemplo: não envio do item, atraso na entrega, avarias \n"
        "Falhas relacionadas a dietas : falhas relacionadas a dietas ou NPT que não sejam erros de administração ou de prescrição, por exemplo: falta do item, atraso na entrega, avarias \n"
        "Erros de prescrição: se a descrição do evento mencionar erro na prescrição de medicamento, NPT ou dieta, medicamento ou dieta prescrito errado, princípio ativo errado, dosagem errada, horários errados, prescrição rasurada \n"
        "Eventos relacionados a infecções: se o evento mencionar surgimento de infecção ou necessidade de iniciar uso de antibióticos \n"
        "Falhas relacionadas a dispositivos: se o evento mencionar problemas com dispositivos tais como sondas, catéteres, cânulas, tqt, gtt, sne, svd, sonda nasoenteral, tais como tração, oclusão, obstrução, perfuração, furo, rolha, saque e exteriorização dos mesmos \n"
        "Falhas relacionadas a procedimentos: se o evento mencionar problemas com procedimentos, por exemplo, realização errada de um procedimento, uso incorreto do material do procedimento, desperdício de material \n"
        "Queda do paciente (com ou sem lesão): se o evento mencionar que o paciente caiu, sofreu queda, havendo lesão ou não \n"
        "Queixa relacionada à parte técnica: se o evento mencionar explicitamente falta de conhecimento técnico ou falta de experiência do profissional. Não suponha uma queixa caso ela não esteja relatada. Se for mencionado falhas de pais, mães, genitores ou familiares do paciente, não use este tipo pois pais, mães e genitores não são profissionais contratados pela empresa. \n"
        "Furo de escala: se o evento mencionar furo de escala, faltas ou absenteísmo de técnicos de enfermagem \n"
        "Outros: caso o evento não se enquadre em nenhum dos tipos acima \n"
        "Tanto para decidir por uma categoria quanto para os tipos de eventos, não faça suposições nem sugira hipóteses sem base nos fatos descritos, decida usando somente as evidências disponíveis."
    )
    
    conteudo_usuario = f"""
    --- DESCRIÇÃO DO INCIDENTE ---
    {descricao_evento}
    
    --- DETALHES ADICIONAIS ---
    - Fatores do Paciente: {fatores_paciente if fatores_paciente else 'Não informado'}
    - Fatores da Equipe: {fatores_equipa if fatores_equipa else 'Não informado'}
    - Fatores do Ambiente: {fatores_ambiente if fatores_ambiente else 'Não informado'}
    """
    
    try:
        resposta = ollama.chat(
            model='llama3.1',
            messages=[
                {'role': 'system', 'content': prompt_sistema},
                {'role': 'user', 'content': conteudo_usuario}
            ],
            options={'temperature': 0.2}
        )
        return resposta['message']['content']
    except Exception as e:
        return f"⚠️ **Erro ao comunicar com o Ollama local:** {str(e)}"

# --- CUSTOMIZAÇÃO VISUAL (CSS) ---
# Aqui definimos a cor do botão principal (Verde Hospitalar Moderno) e ajustes de fontes
custom_css = """
.btn-analisar {
    background-color: #00875A !important;
    color: white !important;
    font-weight: bold !important;
    border-radius: 8px !important;
    transition: background-color 0.3s !important;
}
.btn-analisar:hover {
    background-color: #006644 !important;
}
.titulo-principal {
    text-align: center;
    color: #172B4D;
}
"""

# Configuração da Interface Gráfica
with gr.Blocks(theme=gr.themes.Soft(primary_hue="teal", secondary_hue="slate"), css=custom_css) as app:
    
    # Cabeçalho com Logótipo e Título Centralizado
    with gr.Row():
        gr.HTML("""
            <div class='titulo-sistema' style='padding: 15px 0;'>
                <h1 style='margin-top: 0px; margin-bottom: 0px;'>Sistema Avançado de Gestão de Risco Clínico</h1>
                <p style='color: #6B778C; margin-top: 5px;'>Plataforma Inteligente de Análise de Incidentes Adversos</p>
            </div>
        """)
            
    gr.Markdown("---")

    with gr.Column(scale=4):
            gr.HTML("""
                <div class='titulo-principal'>
                    <h1 style='margin-bottom: 0px;'>🏥 Portal de Gestão de Risco Clínico</h1>
                    <p style='color: #6B778C; margin-top: 5px;'>Análise de Eventos Adversoss</p>
                </div>
            """)
            
    gr.Markdown("---")
    
    # Organização do Layout lado a lado
    with gr.Row():
        # Coluna da Esquerda: Formulário de Entrada
        with gr.Column(scale=1):
            gr.Markdown("### 📝 Dados do Incidente")
            txt_evento = gr.Textbox(
                label="Descrição Geral do Evento Adverso", 
                lines=5, 
                placeholder="Descreva detalhadamente o que aconteceu durante o incidente..."
            )
            
            # Agrupamento sanfonado (Accordion) para fatores opcionais para limpar o visual
            with gr.Accordion("🔍 Fatores Contributivos Adicionais (Opcional)", open=False):
                txt_paciente = gr.Textbox(label="Fatores do Paciente", placeholder="Ex: Idade, barreiras linguísticas, complexidade clínica...")
                txt_equipa = gr.Textbox(label="Fatores da Equipe", placeholder="Ex: Falhas de comunicação na passagem de turno, liderança...")
                txt_ambiente = gr.Textbox(label="Fatores do Ambiente / Equipamentos", placeholder="Ex: Sobrecarga de trabalho, falta de consumíveis...")
            
            # Botão estilizado via classe CSS definida acima
            btn_analisar = gr.Button("🚀 Gerar Análise", elem_classes="btn_analisar")
            
        # Coluna da Direita: Relatório Final
        with gr.Column(scale=1):
                    gr.Markdown("### 📊 Classificação do Evento Adverso")
                    
                    # Usamos um Textbox estilizado como Markdown, com altura fixa garantida
                    txt_resultado = gr.TextArea(
                        value="Aguardando o envio dos dados para gerar a classificação...",
                        lines=18,          # Garante uma janela vertical grande e visível
                        max_lines=25,      # Limita o crescimento para não quebrar o layout
                        show_label=False,  # Remove o rótulo redundante
                        interactive=False, # Impede que o usuário apague o relatório gerado
                        container=True     # Mantém uma borda bonita e limpa ao redor
                    )
            
    # Ação do Botão
    btn_analisar.click(
    fn=analisar_incidente_local,
    inputs=[txt_evento, txt_paciente, txt_equipa, txt_ambiente],
    outputs=txt_resultado
    )

if __name__ == "__main__":
    # Inicia e gera o link público de 72h
    port = int(os.environ.get("PORT", 10000))
    demo.launch(server_name="0.0.0.0", server_port=port)
