import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from huggingface_hub import InferenceClient
import re
import os

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="AI Insight Engine",
    layout="wide",
    page_icon="✨"
)

# ---------------------------------------------------
# PREMIUM CSS
# ---------------------------------------------------
def inject_custom_css():
    st.markdown("""
        <style>

        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;700;800&family=Outfit:wght@400;700;800&display=swap');

        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        html, body {
            overflow-x: hidden !important;
            background-color: #050505;
        }

        * {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }

        .stApp {
            background:
            radial-gradient(circle at top left, #1a1a2e 0%, #0a0a12 50%, #16213e 100%);
            background-attachment: fixed;
            color: #f8fafc;
        }

        .block-container {
            max-width: 1450px !important;
            padding-top: 2rem !important;
            padding-bottom: 4rem !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }


        h1 {
            font-family: 'Outfit', sans-serif !important;
            font-size: 4.5rem !important;
            font-weight: 800 !important;
            text-align: center !important;
            margin-bottom: 0.5rem !important;
            background: linear-gradient(
                135deg,
                #ffffff 0%,
                #cbd5e1 40%,
                #818cf8 100%
            );
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        h2, h3 {
            color: white !important;
            font-family: 'Outfit', sans-serif !important;
        }

        p {
            color: #e2e8f0 !important;
        }

        [data-testid="stSidebar"] {
            background: rgba(10, 10, 18, 0.72) !important;
            backdrop-filter: blur(30px) saturate(180%) !important;
            border-right: 1px solid rgba(255,255,255,0.06) !important;
            padding-top: 1rem !important;
        }

        .stTextInput>div>div>input {
            background: rgba(255,255,255,0.04) !important;
            border: 1px solid rgba(255,255,255,0.08) !important;
            border-radius: 16px !important;
            color: white !important;
            padding: 15px !important;
        }

        .stTextInput>div>div>input:focus {
            border-color: #818cf8 !important;
            box-shadow: 0 0 20px rgba(99,102,241,0.4) !important;
        }

        .stButton > button {
            width: 100%;
            background: rgba(255,255,255,0.03) !important;
            border: 1px solid rgba(255,255,255,0.08) !important;
            border-radius: 12px !important;
            color: #cbd5e1 !important;
            font-weight: 500 !important;
            padding: 10px !important;
            transition: all 0.3s ease !important;
            font-size: 13px !important;
            text-align: left !important;
            white-space: normal !important;
            height: auto !important;
            line-height: 1.4 !important;
        }

        .stButton > button:hover {
            background: rgba(99,102,241,0.1) !important;
            border-color: rgba(99,102,241,0.3) !important;
            transform: translateX(5px);
            color: white !important;
        }

        /* Action Button Styling */
        div[data-testid="column"] .stButton > button {
             background: linear-gradient(135deg,#6366f1,#8b5cf6) !important;
             color: white !important;
             font-weight: 700 !important;
             text-align: center !important;
        }

        .metric-card {
            background: linear-gradient(
                145deg,
                rgba(255,255,255,0.05),
                rgba(255,255,255,0.02)
            );
            backdrop-filter: blur(18px);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 26px;
            padding: 35px 20px;
            text-align: center;
            transition: all 0.4s ease;
            box-shadow: 0 12px 35px rgba(0,0,0,0.35);
            min-height: 220px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        .metric-card:hover {
            transform: translateY(-8px);
            border-color: rgba(99,102,241,0.5);
        }

        .metric-value {
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(to bottom,#ffffff,#818cf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .metric-label {
            margin-top: 10px;
            letter-spacing: 2px;
            color: #94a3b8;
            text-transform: uppercase;
            font-size: 0.85rem;
            font-weight: 700;
        }

    

        [data-testid="stDataFrame"] {
            border-radius: 22px !important;
            overflow: hidden !important;
            border: 1px solid rgba(255,255,255,0.08) !important;
        }
        /* Remove expander header background text */
.streamlit-expanderHeader {
    background: transparent !important;
    border: none !important;
    color: transparent !important;
    padding: 0 !important;
}

/* Remove expander arrow */
.streamlit-expanderHeader svg {
    display: none !important;
}

/* Remove expander background */
[data-testid="stExpander"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

        .stPlotlyChart {
            background: rgba(255,255,255,0.03);
            border-radius: 24px;
            border: 1px solid rgba(255,255,255,0.06);
            padding: 15px;
        }

        ::-webkit-scrollbar {
            width: 10px;
        }

        ::-webkit-scrollbar-thumb {
            background: rgba(99,102,241,0.5);
            border-radius: 10px;
        }

        /* Hide default upload text */
[data-testid="stFileUploaderDropzoneInstructions"] {
    display: none !important;
}

/* Hide uploaded filename text area */
[data-testid="stFileUploaderFileName"] {
    display: none !important;
}

/* Upload Box Styling */
[data-testid="stFileUploaderDropzone"] {
    background: rgba(255,255,255,0.03) !important;
    border: 2px dashed rgba(99,102,241,0.4) !important;
    border-radius: 24px !important;
    min-height: 180px !important;

    display: flex !important;
    align-items: center !important;
    justify-content: center !important;

    transition: all 0.3s ease !important;
}

/* Hover Effect */
[data-testid="stFileUploaderDropzone"]:hover {
    border-color: #818cf8 !important;
    background: rgba(99,102,241,0.08) !important;
}

/* Upload Symbol */
[data-testid="stFileUploaderDropzone"]::before {
    content: "⭱";
    font-size: 50px;
    color: rgba(129,140,248,0.95);
    font-weight: bold;
}

/* Remove internal upload text */
[data-testid="stFileUploader"] button {
    color: transparent !important;
    background: transparent !important;
    border: none !important;
}

/* Remove any text inside uploader */
/* Hide only uploader text safely */
[data-testid="stFileUploaderDropzoneInstructions"] {
    display: none !important;
}

[data-testid="stFileUploader"] small {
    display: none !important;
}

/* Remove expander background */
.streamlit-expanderHeader {
    background: transparent !important;
    border: none !important;
    color: white !important;
    font-weight: 600 !important;
}

/* Remove expander content background */
.streamlit-expanderContent {
    background: transparent !important;
    border: none !important;
}

/* Remove schema box styling */
[data-testid="stExpander"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

/* Remove extra grey background */
[data-testid="stSidebar"] details {
    background: transparent !important;
}

/* Remove expander header background text */
.streamlit-expanderHeader {
    background: transparent !important;
    border: none !important;
    color: transparent !important;
    padding: 0 !important;
}

/* Remove expander arrow */
.streamlit-expanderHeader svg {
    display: none !important;
}

/* Remove expander background */
[data-testid="stExpander"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}


        </style>
    """, unsafe_allow_html=True)

# ---------------------------------------------------
# DATABASE CONNECTION
# ---------------------------------------------------
@st.cache_resource
def get_db_connection():
    db_path = 'user_data.db' if os.path.exists('user_data.db') else 'sample.db'
    conn = sqlite3.connect(db_path, check_same_thread=False)
    return conn

@st.cache_data
def get_database_schema(_conn):
    try:
        cursor = _conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        schema = {}

        for table_name in tables:
            table_name = table_name[0]

            if table_name == 'sqlite_sequence':
                continue

            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()

            schema[table_name] = [col[1] for col in columns]

        return schema

    except Exception:
        return {}

# ---------------------------------------------------
# FORMAT SCHEMA
# ---------------------------------------------------
def format_schema_for_prompt(schema):

    schema_str = "Database Schema:\n"

    for table, columns in schema.items():
        schema_str += f"- Table '{table}' with columns: {', '.join(columns)}\n"

    return schema_str

# ---------------------------------------------------
# GENERATE SQL
# ---------------------------------------------------
def generate_sql(api_key, schema_str, user_query):

    try:
        client = InferenceClient(api_key=api_key)

        system_prompt = f"""
You are an expert SQL assistant.

{schema_str}

Rules:
1. Return ONLY SQL query.
2. Never use markdown.
3. Only SELECT queries allowed.
4. Use SQLite syntax.
5. Use LIKE for text searches.
"""

        response = client.chat_completion(
            model="meta-llama/Meta-Llama-3-8B-Instruct",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ],
            max_tokens=250,
            temperature=0.1
        )

        sql = response.choices[0].message.content.strip()

        sql = re.sub(r'^```sql', '', sql)
        sql = re.sub(r'^```', '', sql)
        sql = re.sub(r'```$', '', sql)

        return sql.strip()

    except Exception as e:
        return f"ERROR: {str(e)}"

# ---------------------------------------------------
# STYLE PLOTLY
# ---------------------------------------------------
def style_fig(fig):

    fig.update_layout(
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        height=500,
        title_x=0.02,
        margin=dict(l=40, r=40, t=60, b=40),
        font=dict(color='#0f172a')
    )

    fig.update_xaxes(gridcolor='#e2e8f0')
    fig.update_yaxes(gridcolor='#e2e8f0')

    return fig

# ---------------------------------------------------
# CHART GENERATION
# ---------------------------------------------------
def suggest_and_render_chart(df):

    if df.empty or len(df.columns) < 2:
        st.info("Not enough data for charts.")
        return

    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    categorical_cols = df.select_dtypes(exclude='number').columns.tolist()

    try:

        if len(categorical_cols) >= 1 and len(numeric_cols) >= 1:

            fig = px.bar(
                df.head(20),
                x=categorical_cols[0],
                y=numeric_cols[0],
                color=numeric_cols[0],
                title=f"{numeric_cols[0]} by {categorical_cols[0]}"
            )

            style_fig(fig)

            st.plotly_chart(fig, use_container_width=True)

        elif len(numeric_cols) >= 2:

            fig = px.scatter(
                df,
                x=numeric_cols[0],
                y=numeric_cols[1],
                title=f"{numeric_cols[1]} vs {numeric_cols[0]}"
            )

            style_fig(fig)

            st.plotly_chart(fig, use_container_width=True)

    except Exception:
        st.info("Unable to generate chart.")

# ---------------------------------------------------
# MAIN APP
# ---------------------------------------------------
def main():

    inject_custom_css()

    # 1. INITIALIZE STATE
    if "query_history" not in st.session_state:
        st.session_state.query_history = []

    st.markdown(
        "<h1>✧ AI Insight Engine</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center;font-size:18px;color:#cbd5e1;'>Next Generation AI SQL Analytics Dashboard</p>",
        unsafe_allow_html=True
    )

    # 2. HANDLE INPUTS FIRST (for instant sidebar sync)
    chat_input_query = st.chat_input("Ask anything about your data...")
    
    # Priority: Clicked history query > Chat input query
    query = None
    if st.session_state.get("active_query"):
        query = st.session_state.active_query
        del st.session_state.active_query
    elif chat_input_query:
        query = chat_input_query
        # Add new query to history immediately
        st.session_state.query_history.append(query)

    # 3. SIDEBAR
    with st.sidebar:
        st.header("⚡ Settings")
        hf_api_key = st.text_input("Hugging Face API Token", type="password")

        st.divider()
        st.header("📂 Upload CSV")
        uploaded_file = st.file_uploader("", type=["csv"], label_visibility="collapsed")

        if uploaded_file is not None:
            try:
                df_upload = pd.read_csv(uploaded_file)
                df_upload = df_upload.dropna(how='all')
                df_upload.columns = (
                    df_upload.columns
                    .str.strip()
                    .str.lower()
                    .str.replace(r'[^a-z0-9_]', '_', regex=True)
                )
                table_name = os.path.splitext(uploaded_file.name)[0]
                table_name = re.sub(r'[^a-z0-9_]', '_', table_name.lower())
                conn_upload = sqlite3.connect('user_data.db', check_same_thread=False)
                df_upload.to_sql(table_name, conn_upload, if_exists='replace', index=False)
                conn_upload.close()
                st.success(f"Uploaded as table: {table_name}")
                st.cache_resource.clear()
                st.cache_data.clear()
            except Exception as e:
                st.error(f"Upload Error: {e}")

        st.divider()
        
        # Query History Section
        st.header("⏳ History")
        if "query_history" not in st.session_state:
            st.session_state.query_history = []
        
        def display_history():
            if st.session_state.query_history:
                for i, h_query in enumerate(reversed(st.session_state.query_history[-10:])):
                    if st.button(h_query, key=f"hist_{i}"):
                        st.session_state.active_query = h_query
                        st.rerun()
            else:
                st.info("No queries yet.")
        
        display_history()

    # Fetch schema for AI (not displayed anymore)
    conn = get_db_connection()
    schema = get_database_schema(conn)

    if query:
        # We already added to history above if it was a new query
        st.markdown(f'''
<div style="
background: rgba(99,102,241,0.15);
padding: 16px;
border-radius: 18px;
margin-bottom: 15px;
border: 1px solid rgba(99,102,241,0.25);
color: white;
font-size: 16px;
">
🧑 {query}
</div>
''', unsafe_allow_html=True)

        if not hf_api_key:
            st.error("Please enter Hugging Face API token.")
            return

        if not schema:
            st.error("No database schema available.")
            return

        with st.container():

            with st.spinner("Generating SQL Query..."):

                schema_str = format_schema_for_prompt(schema)

                sql_query = generate_sql(
                    hf_api_key,
                    schema_str,
                    query
                )

            if sql_query.startswith("ERROR"):
                st.error(sql_query)
                return

            st.success("SQL Query Generated")

            # WHITE SQL QUERY BOX
            st.markdown(f'''
            <div style="
                background: rgba(255,255,255,0.04);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 18px;
                padding: 18px;
                margin-top: 10px;
                margin-bottom: 15px;
                overflow-x:auto;
            ">
            <pre style="
                color: white;
                font-size: 15px;
                font-family: monospace;
                margin: 0;
                white-space: pre-wrap;
            ">{sql_query}</pre>
            </div>
            ''', unsafe_allow_html=True)

            try:

                if not sql_query.upper().startswith(("SELECT", "WITH")):
                    st.error("Only SELECT queries are allowed.")
                    return

                df = pd.read_sql_query(sql_query, conn)

                if df.empty:
                    st.warning("No rows returned.")
                    return

                # METRICS
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown(f'''
                    <div class="metric-card">
                        <div class="metric-value">{len(df)}</div>
                        <div class="metric-label">Rows</div>
                    </div>
                    ''', unsafe_allow_html=True)

                with col2:
                    st.markdown(f'''
                    <div class="metric-card">
                        <div class="metric-value">{len(df.columns)}</div>
                        <div class="metric-label">Columns</div>
                    </div>
                    ''', unsafe_allow_html=True)

                with col3:

                    numeric_cols = df.select_dtypes(include='number').columns.tolist()

                    if numeric_cols:
                        total = round(df[numeric_cols[0]].sum(), 2)
                    else:
                        total = "-"

                    st.markdown(f'''
                    <div class="metric-card">
                        <div class="metric-value">{total}</div>
                        <div class="metric-label">Total</div>
                    </div>
                    ''', unsafe_allow_html=True)

                st.write("")

                st.subheader("📊 Query Results")

                st.dataframe(df, use_container_width=True)

                st.write("")

                st.subheader("✨ AI Visual Intelligence")

                suggest_and_render_chart(df)

            except Exception as e:
                st.error(f"SQL Execution Error: {e}")

# ---------------------------------------------------
# RUN APP
# ---------------------------------------------------
if __name__ == "__main__":
    main()