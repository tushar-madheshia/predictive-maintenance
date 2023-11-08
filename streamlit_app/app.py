import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
st.set_page_config(page_title="RAG chatbot",layout="wide")

with st.sidebar:
    from PIL import Image
    image = Image.open('assets/images/ref.png')
    st.image(image, use_column_width=True)
    with st.expander("Application Details",expanded=True):
        st.write("Streamlit app built on Refract by Fosfor and deployed on Snowpark Container Services from one click deployment feature of Refract. This is a chat app being powered by a llama2 model deployed on SCS, find more about the model in Model Details")
        
    with st.expander("Model Details",expanded=True):
        st.write("Llama 2 is a collection of pretrained and fine-tuned generative text models ranging in scale from 7 billion to 70 billion parameters. Llama-2-Chat, are optimized for dialogue use cases. The model used in this use-case is finetuned on instruction dataset on Snowpark Container Services")
        st.info("Model : Llama-2-7b-chat-hf")
        st.info("Model Size : 6.74B params")
        st.info("Fine-tuned using : Refract on SCS - GPU_3 compute")

str_ctx = None
    
@st.cache
def load_model():
    import torch
    from peft import AutoPeftModelForCausalLM
    from transformers import AutoTokenizer
    model_name = "NousResearch/Llama-2-7b-chat-hf"

    model = AutoPeftModelForCausalLM.from_pretrained("/data/fine-tuned-model-qna-full-save-pretrained/", device_map="auto",torch_dtype=torch.float16)
    model = model.merge_and_unload()
    model.to("cuda")
    
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    return model, tokenizer

# bot_col, context_col = st.columns([6,3])
# with context_col:
    # st.header('Supporting Docs')

#     uploaded_file = st.file_uploader("Select an article")
#     if uploaded_file:
#         bytes_data = uploaded_file.getvalue()
#         # To convert to a string based IO:
#         stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
#         # To read file as string:
#         str_ctx = stringio.read()
#         from streamlit.components.v1 import html
#         #encoded_ctx = encode_text(str_ctx)
#         cntxt = ("<p align='justify' style='background-color:#d3d3d3;padding:10px'>" + str_ctx + "</p>")

#         html(cntxt, height=600, scrolling=True)

    
# with bot_col:
st.header('Chat Bot Assitant')

## generated stores AI generated responses
if 'generated' not in st.session_state:
    st.session_state['generated'] = ["Hello, I am a chat bot running on top of finetuned llama2-7b model on instruction data. I will answer your questions. Type your first question!"]
## past stores User's questions
if 'past' not in st.session_state:
    st.session_state['past'] = ['Hi!']
# Layout of input/response containers
input_container = st.container()
colored_header(label='', description='', color_name='blue-30')
response_container = st.container()


# User input
## Function for taking user provided prompt as input
def get_text():
    with st.form("my_form"):
        # col1,col2 =  st.columns([10,2])
        # with col1:
        input_text = st.text_input("User: ", "", key="input")
        # with col2:
        submitted = st.form_submit_button("Ask me!")
        if submitted:
            return input_text
with input_container:
    user_input = get_text()
# Response output
## Function for taking user prompt as input followed by producing AI generated responses
def generate_response(prompt):
    model, tokenizer = load_model()
    _inputs = tokenizer.encode(f"### Human: {prompt} ### Assistant: ", return_tensors="pt")
    outputs = model.generate(input_ids=_inputs.to('cuda'), max_length= 200, pad_token_id=tokenizer.eos_token_id)
    output = tokenizer.decode(outputs[0])
    start_index = output.find("### Assistant:")
    second_start_index = output.find("### Assistant:", start_index + 1)
    num_human_occurrences = 0
    end_index = -1
    while num_human_occurrences < 2:
        end_index = output.find("### Human:", end_index + 1)
        if end_index == -1:
            break
        num_human_occurrences += 1
    if end_index == -1:
        end_index = len(output)
    substring = output[start_index + len("### Assistant:"):end_index]

    return substring
## Conditional display of AI generated responses as a function of user provided prompts
with response_container:
    if user_input:
        print(user_input)
        response = generate_response(user_input)
        print(response)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(response)
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state['past'][i], is_user=True,avatar_style="thumbs", key=str(i) + '_user')
            message(st.session_state["generated"][i],avatar_style="shapes", key=str(i))