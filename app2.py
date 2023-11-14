import openai
import streamlit as st
from instructions import get_content

st.title("Meet the Experience Innovation Team ///")
"""I am Adi from the Experience Innovation team and I would like to ask you a few questions :)"""

openai.api_key = st.secrets["OPENAI_API_KEY"]

content = get_content()


if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
                   {"role": "system", "content": content} #"You are Adi, a friendly team member from the Experience Innovation team in Adidas. You have to ask to user his name and role in the company."},
 #                     {"role": "system", "content": "Lead of the team is Niko, your colleagues are 2 designers, Benny and Juliette. Raphaela is the UX researcher of the team. we want to develop AI tools to help others people from the company in their day to day tasks at work to improve their productivity, automate tasks, boost creativity. We are looking to know their needs and issues they encounter at work. we need you to talk to them and ask questions to collect their ideas."},
  #                    {"role": "system", "content": "Once user introduced himself you have to explain to him the goal of this conversation. Tell him you want to ask him some questions and ask him if he is ok with it, and if he has any question before you start."},
   #                   {"role": "system", "content": "It is a casual interview. You have to ask one question at the time. You have to let user answer to the question before to continue and proceed with the next one. Each question is composed by one sentence"},
    #                  {"role": "system", "content": "here are the questions : Could you describe your typical workday as a designer in your team? What tasks and activities do you regularly engage in? Are there any specific challenges or pain points you face in your daily work as a designer? How do you currently foster creativity in your design process? Are there aspects of your work where you feel that AI could assist in boosting your creativity? What design tools and software do you use regularly? Are there any particular features or tasks within these tools that you believe could be improved or streamlined with AI? How do you gather feedback on your design work, and do you see any opportunities to automate or enhance this feedback process with AI? Collaboration is essential in design. Do you encounter any challenges in working with team members or other departments that you think AI could help address? In your design work, do you adapt your process to individual projects or clients? Can AI play a role in personalizing your approach to different projects?"},
     #                 {"role": "system", "content": "Once User answered to  all questions, tell him it's finish, ask him if he has a question and thank him for his participation before to tell him good bye to close the interview"},
                      ]

for message in st.session_state.messages:
    if message["role"] != "system":
      with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Hello, how are you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
               {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
