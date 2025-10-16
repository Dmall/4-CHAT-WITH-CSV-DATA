import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from pandasai.llm.openai import OpenAi
from pandasai import SmartDataframe


load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    st.error("⚠️ OpenAI API key missing. Please check your .env file.")
    st.stop()

def chat_with_csv(df, prompt):
    llm = OpenAi(api_token = openai_api_key)
    pandas_ai = SmartDataframe(df, config = {"llm": llm})
    result = pandas_ai.chat(prompt)

    if isinstance(result, pd.DataFrame): # ensures correct data type before returning {Layer: Backend / Processing, Purpose: Normalize/convert raw model output into consistent Python types}
        return result
    
    elif isinstance(result, list) or isinstance(result, dict): # elif isinstance(result, (list, dict)):
        try:

            result_df = pd.DataFrame(result)

            return result_df

        except Exception as e:
            print("Could Not Convert Result To DataFrame")

    # print(result)
    return result


st.set_page_config(layout="wide")

st.title("📊 Chat With CSV Using LLm Model")

input_csv = st.file_uploader("Upload Your CSV File", type=["csv"])

if input_csv is not None:
    col1, col2 = st.columns([1,1])

    with col1:
        st.info("✅ CSV File Uploaded Successfully")
        data = pd.read_csv(input_csv)
        st.dataframe(data, use_container_width= True)

    with col2:
        st.info("Chat Below With Your Dataset")

        input_text = st.text_area("Enter Your Query...")

        if input_text is not None:
            if st.button("Chat With CSV"):
                st.info("🔎 Your Query: " + input_text)
                result = chat_with_csv(data, input_text)

                if isinstance(result, pd.DataFrame): #ensures correct way to display result {Layer: Frontend / Display, Purpose: Decide how to show the processed result}
                    st.dataframe(result, use_container_width=True)
                st.success(result)










# Excellent question 👍 — you’re asking **why we check `isinstance(result, pd.DataFrame)` and try converting it** *inside* the `chat_with_csv()` function,
# when we’re already checking again **outside**, in the second Streamlit column (`if isinstance(result, pd.DataFrame): ... else: ...`).

# Let’s unpack that carefully 👇

# ---

# ## 🧩 The key idea

# You are right — at first glance it looks like **duplicate logic**, but each check serves a **different purpose** in a **different layer** of your app.

# Let’s separate them conceptually:

# ---

# ### 🧠 1️⃣ Inside `chat_with_csv()`

# This is **data processing logic** — the *back-end* function.

# ```python
# if isinstance(result, pd.DataFrame):
#     return result
# elif isinstance(result, (list, dict)):
#     try:
#         return pd.DataFrame(result)
#     except Exception as e:
#         return f"Could not convert to DataFrame: {e}"
# return result
# ```

# 👉 Purpose:

# * This ensures that whatever the LLM (`pandas_ai.chat`) returns — whether it’s a list, dict, or raw text —
#   you **normalize it into a predictable format** (ideally a DataFrame).
# * It’s a **data cleanup / type normalization** step.
# * The function’s *job* is to make sure it returns something Streamlit can display safely.

# ---

# ### 💬 2️⃣ Outside, in the Streamlit UI

# This is **display logic** — the *front-end* part:

# ```python
# if isinstance(result, pd.DataFrame):
#     st.dataframe(result, use_container_width=True)
# else:
#     st.success(result)
# ```

# 👉 Purpose:

# * Streamlit needs to **decide how to render** the result —
#   if it’s a DataFrame, show a table;
#   if it’s text (string), show it as a message.
# * This check is purely **for presentation**, not data conversion.

# ---

# ### ⚙️ Think of it like layers:

# | Layer                    | Where                                      | Purpose                                                         |
# | ------------------------ | ------------------------------------------ | --------------------------------------------------------------- |
# | **Backend / Processing** | `chat_with_csv()`                          | Normalize/convert raw model output into consistent Python types |
# | **Frontend / Display**   | Streamlit (`st.dataframe` or `st.success`) | Decide how to show the processed result                         |

# ---

# ### 💡 Why both are needed

# If you remove the `isinstance()` check inside `chat_with_csv()`,
# you might get raw output from the LLM like:

# ```python
# [{'col1': 10, 'col2': 20}]
# ```

# Then your front-end check sees it’s not a DataFrame,
# and `st.success(result)` just prints that list — not a nice table.

# By keeping the conversion inside `chat_with_csv()`,
# you **guarantee** the result is either:

# * a DataFrame, or
# * a human-readable string (error message or text)

# so the Streamlit layer doesn’t have to worry about “fixing” bad data types.

# ---

# ### ✅ In short:

# * `isinstance()` inside → ensures **correct data type before returning**
# * `isinstance()` outside → ensures **correct way to display result**

# They look similar but handle **different stages** of the workflow.

# ---

# Would you like me to show you a diagram (flowchart) of how data flows between these layers? It would make this relationship very clear visually.





# Flowchart


    #             ┌────────────────────────┐
    #             │  User uploads CSV file │
    #             └────────────┬───────────┘
    #                          │
    #                          ▼
    #            ┌───────────────────────────┐
    #            │   User enters text query  │
    #            └────────────┬──────────────┘
    #                          │
    #                          ▼
    #              ┌──────────────────────┐
    #              │  chat_with_csv(df,   │
    #              │       prompt)        │
    #              └──────────┬───────────┘
    #                         │
    #                         ▼
    #        ┌────────────────────────────────────┐
    #        │  LLM runs: pandas_ai.chat(prompt)  │
    #        └────────────────────────────────────┘
    #                         │
    #                         ▼
    #        ┌────────────────────────────────────┐
    #        │   Inside chat_with_csv():           │
    #        │   if isinstance(result, DataFrame): │
    #        │       return result                 │
    #        │   elif isinstance(result, (list,    │
    #        │         dict)): convert to DF       │
    #        │   else: return raw text             │
    #        └────────────────────────────────────┘
    #                         │
    #                         ▼
    #      ┌────────────────────────────────────┐
    #      │   Result returned to Streamlit app │
    #      └────────────────────────────────────┘
    #                         │
    #                         ▼
    #  ┌────────────────────────────────────────────┐
    #  │  Outside (in Streamlit UI):                │
    #  │  if isinstance(result, DataFrame):         │
    #  │       st.dataframe(result)  ← table view   │
    #  │  else: st.success(result)   ← text output  │
    #  └────────────────────────────────────────────┘


# 🧩 Summary

# ✅ Inside chat_with_csv() → ensures data type normalization (convert to DataFrame if possible).

# ✅ Outside in Streamlit → ensures correct rendering (decides how to display it).
