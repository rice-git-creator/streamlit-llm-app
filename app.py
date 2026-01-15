# OpenAI APIキーが自動で参照されるようにする
from dotenv import load_dotenv

load_dotenv()

# パッケージのインポート
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


def get_llm_response(user_input, expert_type):
    """
    入力テキストと専門家の種類を受け取り、LLMからの回答を返す関数 [7, 8]
    """

    # ラジオボタンの選択値に応じてシステムメッセージを切り替える
    if expert_type == "デザイナー":
        system_message = "あなたは優秀なグラフィックデザイナーです。ユーザーの質問に対して、専門的かつ丁寧に回答してください。"
    elif expert_type == "コピーライター":
        system_message = "あなたは優秀なコピーライターです。クライアントの質問に対して、専門的かつ丁寧に回答してください。"
    
    # LLMのインスタンス化
    llm = ChatOpenAI(
        model_name="gpt-4o-mini",
        temperature=0.7, # 多様な回答を得るために数値を上げる
        max_tokens=500 # 回答を長くするために上限を引き上げる
    )

    # プロンプトテンプレートの作成
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("user", "{user_input}")
    ])

    # LangChainのChainを作成・実行
    chain = prompt | llm
    response = chain.invoke({"user_input": user_input})
    return response.content

# Streamlitアプリの設定
st.set_page_config(page_title="専門家アシスタント", page_icon="🤖")
st.title("専門家アシスタント 🤖")

# Webアプリの概要や操作方法の明示
st.write("デザイナーまたはコピーライターとして質問に答えます。")
st.write("""
        ### アプリ概要
        このアプリでは、相談したい「専門家の種類」を選択して質問を送信すると、LLMがその分野のプロとして回答します。
        ### 操作方法
        1. 相談したい専門家の種類を選択します。
        2. 質問内容を入力します。
        3. 「送信」ボタンをクリックして回答を取得します。
        """)

st.divider()

# ラジオボタンで専門家の種類を選択
expert_type = st.radio(
    "相談したい専門家の種類を選択してください。",
    ("デザイナー", "コピーライター")
)

# テキストエリアでユーザー入力を受け取る
user_input = st.text_area("質問内容を入力してください。", height=150)

# 実行ボタン
if st.button("送信"):
    if user_input.strip() == "":
        st.warning("質問内容を入力してください。")
    else:
        # 入力内容が空欄でない場合、LLMからの回答を取得して表示
        with st.spinner("回答を生成中..."):
            response = get_llm_response(user_input, expert_type)
        st.subheader("回答:")
        st.write(response)