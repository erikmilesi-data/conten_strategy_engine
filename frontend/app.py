import json
import requests
import streamlit as st
import pandas as pd
import altair as alt

# ----------------------------
# ESTADO GLOBAL (SESSION STATE)
# ----------------------------
if "analysis_data" not in st.session_state:
    st.session_state["analysis_data"] = None

if "auth_token" not in st.session_state:
    st.session_state["auth_token"] = None

API_URL = "http://127.0.0.1:8000/api/content/strategy"

# ----------------------------
# CONFIGURAÇÃO GERAL DA PÁGINA
# ----------------------------
st.set_page_config(
    page_title="Content Strategy Engine",
    page_icon="📊",
    layout="wide",
)

# ----------------------------
# LOGIN
# ----------------------------
st.title("🔐 Content Strategy Engine - Login")

if st.session_state["auth_token"] is None:
    with st.form("login_form"):
        username = st.text_input("Usuário", value="admin")
        password = st.text_input("Senha", type="password")
        submitted = st.form_submit_button("Entrar")

    if submitted:
        try:
            resp = requests.post(
                "http://127.0.0.1:8000/api/auth/login",
                json={"username": username, "password": password},
                timeout=10,
            )
            if resp.status_code == 200:
                data_login = resp.json()
                st.session_state["auth_token"] = data_login["access_token"]
                st.success(f"Bem-vindo, {data_login['username']}!")
                st.rerun()  # após isso, o script reinicia e já entra logado
            else:
                st.error("Usuário ou senha inválidos.")
        except Exception as e:
            st.error(f"Erro ao tentar autenticar: {e}")

    st.stop()

# ----------------------------
# HEADER PREMIUM (HERO)
# ----------------------------
st.markdown(
    """
    <style>
    .hero {
        padding: 30px 20px 10px 20px;
        border-radius: 12px;
        background: linear-gradient(145deg, #ffffff 0%, #eef2f7 100%);
        box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 25px;
    }
    .hero-title {
        font-size: 2.4rem;
        font-weight: 800;
        color: #1f2937;
    }
    .hero-sub {
        font-size: 1.1rem;
        color: #4b5563;
        margin-top: -10px;
    }
    .kpi {
        background: #ffffff;
        padding: 18px;
        border-radius: 14px;
        text-align: left;
        box-shadow: 0px 1px 4px rgba(0,0,0,0.08);
        border: 1px solid #e5e7eb;
    }
    .kpi-title {
        font-size: 0.8rem;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 4px;
    }
    .kpi-value {
        font-size: 1.3rem;
        font-weight: 700;
        color: #111827;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">⚡ Content Strategy Engine</div>
        <div class="hero-sub">
            Ferramenta inteligente para análise de público, composição de estratégias e recomendações de conteúdo.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        """
        <div class="kpi">
            <div class="kpi-title">Estratégia</div>
            <div class="kpi-value">Tema + Público + Plataforma</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        """
        <div class="kpi">
            <div class="kpi-title">Horários Otimizados</div>
            <div class="kpi-value">Faixas Inteligentes</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        """
        <div class="kpi">
            <div class="kpi-title">Sugestões</div>
            <div class="kpi-value">Conteúdo acionável</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ----------------------------
# SIDEBAR
# ----------------------------
with st.sidebar:
    st.header("⚙️ Configurações")

    api_url = st.text_input("API URL", API_URL)

    topic = st.text_input("Tema do conteúdo", "marketing digital")

    platform = st.selectbox(
        "Plataforma",
        ["instagram", "tiktok", "linkedin"],
        index=0,
    )

    mode = st.selectbox(
        "Modo de sugestão",
        ["rich", "basic"],
        index=0,
        help="Rich = sugestão estruturada por formato/plataforma. Basic = lista simples.",
    )

    st.markdown("---")
    st.subheader("📂 Público-alvo")

    use_sample = st.checkbox(
        "Usar exemplo de público (demo)",
        value=True,
        help="Se marcado, usa um conjunto de usuários de exemplo.",
    )

    uploaded = st.file_uploader(
        "Ou envie um JSON com usuários",
        type=["json"],
        help='Formato esperado: {"users": [...]} ou lista simples de usuários.',
    )

    users_data = []

    if use_sample:
        users_data = [
            {"age": 25, "gender": "female", "region": "Sudeste"},
            {"age": 34, "gender": "male", "region": "Nordeste"},
            {"age": 19, "gender": "female", "region": "Sudeste"},
            {"age": 42, "gender": "male", "region": "Sul"},
            {"age": 29, "gender": "female", "region": "Sudeste"},
        ]
    elif uploaded:
        try:
            raw = json.load(uploaded)
            if isinstance(raw, dict) and "users" in raw:
                users_data = raw["users"]
            elif isinstance(raw, list):
                users_data = raw
            else:
                st.warning(
                    "Formato de JSON não reconhecido. Use lista ou {'users': [...]}."
                )
        except Exception as e:
            st.error(f"Erro ao ler JSON: {e}")

# ----------------------------
# AÇÃO PRINCIPAL (BOTÃO)
# ----------------------------
st.subheader("🧠 Gerar estratégia")

col_left, col_right = st.columns([2, 1])

with col_left:
    st.write(f"**Tema:** `{topic}`")
    st.write(f"**Plataforma:** `{platform}` · **Modo:** `{mode}`")
    st.write(f"**Total de usuários no público:** `{len(users_data)}`")

with col_right:
    st.markdown(
        """
        <style>
        .modern-button {
            background-color: #4361ee;
            color: white !important;
            padding: 14px 24px;
            font-size: 1.1rem;
            border-radius: 10px;
            border: none;
            cursor: pointer;
            text-align: center;
            font-weight: 600;
            width: 100%;
        }
        .modern-button:hover {
            background-color: #3451d1;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    generate = st.button(
        "🚀 Gerar Estratégia Agora",
        key="trigger",
        help="Clique para gerar a estratégia completa",
    )

# Se clicou no botão, chama a API e salva o resultado no session_state
if generate:
    payload = {
        "topic": topic,
        "platform": platform,
        "mode": mode,
        "users": users_data,
    }

    with st.spinner("Gerando estratégia..."):
        try:
            headers = {"Authorization": f"Bearer {st.session_state['auth_token']}"}
            resp = requests.post(api_url, json=payload, headers=headers, timeout=15)
        except Exception as e:
            st.error(f"Erro ao chamar a API: {e}")
            st.stop()

        if resp.status_code != 200:
            st.error(f"Erro da API ({resp.status_code}): {resp.text}")
            st.stop()

        st.session_state["analysis_data"] = resp.json()

# ----------------------------
# RENDERIZAÇÃO DOS RESULTADOS
# (BASEADA EM SESSION_STATE)
# ----------------------------
data = st.session_state["analysis_data"]

if data is not None:
    st.success("Estratégia gerada com sucesso ✅")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📊 Resultados da Análise")

    audience = data.get("audience", {})
    best_times = data.get("best_times", {})
    summary = audience.get("summary", {})
    profiles = audience.get("profiles", [])
    dominant = audience.get("dominant_profile", None)

    # JSON para download
    json_export = json.dumps(data, ensure_ascii=False, indent=2)

    # abas
    tab_hist, tab_aud, tab_sug, tab_time, tab_cal, tab_check, tab_raw = st.tabs(
        [
            "🗂 Histórico",
            "🎯 Público",
            "💡 Sugestões",
            "⏰ Horários",
            "📅 Calendário",
            "📋 Checklist (Tráfego Pago)",
            "📦 Resposta completa",
        ]
    )

    # ----------------------------
    # ABA 0 — HISTÓRICO
    # ----------------------------
    with tab_hist:
        st.markdown("### 🗂 Histórico de análises")

        try:
            headers = {"Authorization": f"Bearer {st.session_state['auth_token']}"}
            history_resp = requests.get(
                API_URL.replace("strategy", "history"),
                headers=headers,
                timeout=10,
            )
            history = history_resp.json().get("history", [])
        except Exception as e:
            st.error(f"Erro ao carregar histórico: {e}")
            history = []

        if history:
            df_hist = pd.DataFrame(history)
            st.dataframe(df_hist, use_container_width=True)

            selected = st.selectbox("Abrir análise ID:", [h["id"] for h in history])

            if st.button("📂 Carregar análise selecionada"):
                try:
                    headers = {
                        "Authorization": f"Bearer {st.session_state['auth_token']}"
                    }
                    entry_resp = requests.get(
                        API_URL.replace("strategy", f"history/{selected}"),
                        headers=headers,
                        timeout=10,
                    )
                    entry_json = entry_resp.json()
                    result = entry_json.get("result")
                    if result:
                        st.session_state["analysis_data"] = result
                        st.success(
                            f"Análise {selected} carregada com sucesso! Role para cima para ver as abas atualizadas."
                        )
                    else:
                        st.error("Não foi possível carregar os dados dessa análise.")
                except Exception as e:
                    st.error(f"Erro ao carregar análise: {e}")
        else:
            st.info("Nenhuma análise encontrada no histórico.")

    # ----------------------------
    # ABA 1 — PÚBLICO
    # ----------------------------
    with tab_aud:
        st.markdown("### 🎯 Análise de Público")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Resumo por gênero:**")
            st.json(summary.get("by_gender", {}))

            st.markdown("**Resumo por região:**")
            st.json(summary.get("by_region", {}))

        with col2:
            st.markdown("**Faixas etárias:**")
            st.json(summary.get("by_age_bucket", {}))

            st.markdown("**Perfis detectados:**")
            st.json(profiles)

        if dominant:
            st.markdown("**Perfil predominante:**")
            st.json(dominant)

        st.markdown("---")
        st.markdown("### 📈 Visualização gráfica")

        # Gráfico de pizza por gênero
        gender_data = summary.get("by_gender", {})
        if gender_data:
            df_gender = pd.DataFrame(
                [{"genero": k, "quantidade": v} for k, v in gender_data.items()]
            )

            st.markdown("**Distribuição por gênero:**")
            chart_gender = (
                alt.Chart(df_gender)
                .mark_arc(innerRadius=40)
                .encode(
                    theta=alt.Theta("quantidade:Q", title="Quantidade"),
                    color=alt.Color("genero:N", title="Gênero"),
                    tooltip=["genero", "quantidade"],
                )
                .properties(height=300)
            )
            st.altair_chart(chart_gender, use_container_width=True)
        else:
            st.info("Sem dados suficientes de gênero para gerar gráfico.")

        # Gráfico por faixa etária
        age_bucket = summary.get("by_age_bucket", {})
        if age_bucket:
            df_age = pd.DataFrame(
                [{"faixa_etaria": k, "quantidade": v} for k, v in age_bucket.items()]
            )

            st.markdown("**Distribuição por faixa etária:**")
            chart_age = (
                alt.Chart(df_age)
                .mark_bar()
                .encode(
                    x=alt.X("faixa_etaria:N", sort="-y", title="Faixa etária"),
                    y=alt.Y("quantidade:Q", title="Quantidade"),
                    tooltip=["faixa_etaria", "quantidade"],
                )
                .properties(height=300)
            )
            st.altair_chart(chart_age, use_container_width=True)
        else:
            st.info("Sem dados suficientes de faixa etária para gerar gráfico.")

        # Gráfico por região (barras horizontais)
        region_data = summary.get("by_region", {})
        if region_data:
            df_region = pd.DataFrame(
                [{"regiao": k, "quantidade": v} for k, v in region_data.items()]
            )

            st.markdown("**Distribuição por região:**")
            chart_region = (
                alt.Chart(df_region)
                .mark_bar()
                .encode(
                    y=alt.Y("regiao:N", sort="-x", title="Região"),
                    x=alt.X("quantidade:Q", title="Quantidade"),
                    tooltip=["regiao", "quantidade"],
                )
                .properties(height=300)
            )
            st.altair_chart(chart_region, use_container_width=True)
        else:
            st.info("Sem dados suficientes de região para gerar gráfico.")

    # ----------------------------
    # ABA 2 — SUGESTÕES
    # ----------------------------
    with tab_sug:
        st.markdown("### 💡 Sugestões de Conteúdo")
        suggestions = data.get("suggestions", {})

        if isinstance(suggestions, dict) and "suggestions" in suggestions:
            items = suggestions["suggestions"]
        else:
            items = suggestions

        if isinstance(items, list):
            for idx, item in enumerate(items, start=1):
                if isinstance(item, dict):
                    st.markdown(f"**{idx}. {item.get('format', 'formato')}**")
                    st.write(item.get("idea", ""))
                else:
                    st.markdown(f"**{idx}.** {item}")
        else:
            st.json(suggestions)

    # ----------------------------
    # ABA 3 — HORÁRIOS
    # ----------------------------
    with tab_time:
        st.markdown("### ⏰ Melhores Horários de Postagem")

        st.markdown("**Plataforma:** " + str(best_times.get("platform", platform)))
        st.markdown("**Janelas sugeridas:**")
        st.write(best_times.get("recommended_slots", []))

        st.markdown("**Notas:**")
        for note in best_times.get("notes", []):
            st.write(f"- {note}")

    # ----------------------------
    # ABA 4 — CALENDÁRIO
    # ----------------------------
    with tab_cal:
        st.markdown("### 📅 Calendário semanal sugerido")

        slots = best_times.get("recommended_slots", [])

        if not slots:
            st.info("Sem janelas sugeridas para montar o calendário.")
        else:
            st.markdown(
                "Com base nas janelas de horário recomendadas, sugerimos a seguinte "
                "distribuição ao longo da semana."
            )

            days = [
                "Segunda",
                "Terça",
                "Quarta",
                "Quinta",
                "Sexta",
                "Sábado",
                "Domingo",
            ]
            rows = []

            for day in days:
                for slot in slots:
                    prioridade = (
                        "Alta"
                        if day in ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
                        else "Moderada"
                    )
                    rows.append(
                        {
                            "dia": day,
                            "janela": slot,
                            "prioridade": prioridade,
                        }
                    )

            df_calendar = pd.DataFrame(rows)

            st.markdown("**Visão consolidada por dia:**")
            grouped = (
                df_calendar.groupby(["dia", "prioridade"])["janela"]
                .apply(lambda x: " · ".join(x))
                .reset_index()
            )

            st.dataframe(grouped, use_container_width=True)

            # Exportar calendário em CSV
            csv_calendar = df_calendar.to_csv(index=False).encode("utf-8")

            st.markdown("### 📥 Exportar calendário")
            st.download_button(
                label="📥 Baixar calendário semanal (CSV)",
                data=csv_calendar,
                file_name="content_calendar.csv",
                mime="text/csv",
            )

            st.markdown(
                """
                Use essa grade como base para:
                - Planejar posts fixos nos dias úteis com prioridade **Alta**
                - Testar conteúdos diferentes aos finais de semana (prioridade **Moderada**
                """
            )

    # ----------------------------
    # ABA 5 — CHECKLIST TRÁFEGO PAGO
    # ----------------------------
    with tab_check:
        st.markdown("### 📋 Checklist rápido de campanha (Data-Driven)")

        by_region = summary.get("by_region", {})
        by_age_bucket = summary.get("by_age_bucket", {})
        slots = best_times.get("recommended_slots", [])

        main_region = max(by_region, key=by_region.get) if by_region else "Indefinido"
        main_age = (
            max(by_age_bucket, key=by_age_bucket.get) if by_age_bucket else "Indefinido"
        )

        st.info(
            f"Checklist gerado com base no público detectado: **{main_age}**, região **{main_region}**, "
            f"plataforma **{platform}**, tema **{topic}**."
        )

        st.markdown("#### 1️⃣ Configurações essenciais")
        st.markdown(
            f"""
- Objetivo sugerido para `{platform}`: **Conversão ou Engajamento**, dependendo da oferta.
- Público base:
  - Faixa etária predominante: **{main_age}**
  - Região predominante: **{main_region}**
- Interesses: relacionados a **{topic}**
- Criativos devem falar diretamente com **{main_age}**.
            """
        )

        st.markdown("#### 2️⃣ Segmentação recomendada (base nos dados)")
        st.markdown(
            f"""
- Idade alvo: **{main_age}**
- Região prioritária: **{main_region}**
- Caso queira expandir, priorize:
  - Outras regiões com volume relevante
  - Faixas etárias logo abaixo da dominante
            """
        )

        st.markdown("#### 3️⃣ Horários recomendados")
        if slots:
            st.markdown("Ative a campanha em janelas de maior probabilidade de clique:")
            for s in slots:
                st.write(f"- **{s}**")
        else:
            st.info("Nenhuma janela específica — usar entrega contínua (24/7).")

        st.markdown("#### 4️⃣ Estrutura inicial da campanha")
        st.markdown(
            """
- 1 campanha → 2 conjuntos de anúncios:
  - Conjunto A: público principal (idade + região dominante)
  - Conjunto B: expansão leve (idade ou região adjacente)
- 2 a 3 criativos por conjunto (testes A/B simples)
- Orçamento: valor que permita rodar 7 dias sem dor de cabeça
            """
        )

        if "25" in main_age:
            persona_msg = "Conteúdos diretos, práticos e que mostrem ganho rápido."
        elif "18" in main_age:
            persona_msg = "Mensagem dinâmica, visual e com forte apelo emocional."
        elif "35" in main_age or "44" in main_age:
            persona_msg = "Foque em autoridade, segurança e clareza de benefício."
        elif "45" in main_age or "60" in main_age:
            persona_msg = "Conteúdo com mais detalhes, confiança e redução de risco."
        else:
            persona_msg = "Mensagem adaptada ao perfil detectado."

        st.markdown("#### 5️⃣ Mensagem baseada no público")
        st.markdown(
            f"""
- Linguagem recomendada para **{main_age}**:  
  👉 **{persona_msg}**
- Use o tema `{topic}` ligado a uma dor real desse público.
- CTA: obrigatório, direto e curto.
            """
        )

        st.markdown("#### 6️⃣ Monitoramento (modo preguiçoso)")
        st.markdown(
            f"""
- Primeiras 24h: verificar entrega (impressões + CPM estável).
- Entre 48–72h:
  - Pausar criativos com desempenho ruim.
  - Manter só o criativo campeão.
- Ao final de 7 dias:
  - Decidir entre escalar ou testar outra segmentação baseada em `{main_region}` ou `{main_age}`.
            """
        )

        st.markdown("---")
        st.success("Checklist finalizado. Baseado nos dados da análise do seu público.")

    # ----------------------------
    # ABA 6 — RAW + DOWNLOAD JSON
    # ----------------------------
    with tab_raw:
        st.markdown("### 📦 Resposta completa (debug)")
        st.json(data)

        st.markdown("---")
        st.markdown("### 📥 Exportar estratégia")

        st.download_button(
            label="📥 Baixar estratégia completa (JSON)",
            data=json_export,
            file_name="content_strategy.json",
            mime="application/json",
        )

else:
    st.info("Configure os parâmetros e clique em **🚀 Gerar Estratégia Agora**.")
