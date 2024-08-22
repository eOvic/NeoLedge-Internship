from langchain import LLMChain
from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
import os
os.environ['OLLAMA_API_KEY'] = "/usr/share/ollama/.ollama/id_ed25519.pub"

# Define the Ollama LLM
llm = Ollama(model="llama3.1")

# Define the prompt template for correcting text
prompt_template = PromptTemplate(
    input_variables=["text"],
    template="Fix typos and remove unnecessary whitespaces from the following text: {text}",
)

# Create the LangChain LLMChain
chain = LLMChain(llm=llm, prompt=prompt_template)

# Example extracted text
extracted_text = "Thiss is    an exmaple of textt withh typos  and  extra  spaces."

# Use the chain to correct the text
corrected_text = chain.run(text=extracted_text)

print("Corrected Text:\n", corrected_text)
