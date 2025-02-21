from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import Ollama


# Step 1: Load examples from a file and cache them in memory
def load_examples(file_path):
    """Read examples from the examples.txt file and cache them in memory."""
    with open(file_path, "r") as file:
        examples = file.read()
    return examples


# Load the examples only once into memory
examples_cache = load_examples("./data/examples.txt")

# Step 2: Define the Prompt Template, reusing the cached examples
multi_shot_prompt = PromptTemplate(
    input_variables=["message"],
    template=f"""
    You are an assistant that helps classify Slack messages based on priority. Here are some examples:

    {examples_cache}

    Now, classify the following message:
    Message: {{message}}
    Classification:
    """,
)

# Step 3: Load the LLM (using Ollama 70b-instruct-q8_0 model)
llm = Ollama(model="llama3.1:8b-instruct-q8_0")

# Step 4: Create a LangChain chain for classification
classification_chain = LLMChain(llm=llm, prompt=multi_shot_prompt)


# Step 5: Function to classify a message
def classify_message(message):
    """Classify a new Slack message using cached examples."""
    return classification_chain.run({"message": message})


# Example usage
if __name__ == "__main__":
    # Example Slack message to classify
    slack_message = "Our production environment is experiencing latency issues."

    # Get classification
    classification = classify_message(slack_message)

    # Output the classification result
    print(f"Classification: {classification}")
