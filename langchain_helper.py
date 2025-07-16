from secret_key import togetherapi_key
from langchain_community.llms import Together
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

import os
os.environ['TOGETHER_API_KEY'] = togetherapi_key # set together api key

# Load Mistral Model
llm = Together(
    model="mistralai/Mistral-7B-Instruct-v0.1",
    temperature=0.7,
    max_tokens=128
)

def generate_restaurant_name_and_items(cuisine):
    # sequential chain (output of one step will be input of another step,
    # Chain 1: Restuarant Name
    prompt_template_name = PromptTemplate(
        input_variables=['cuisine'],
        template="""### Instruction:
    Suggest only one fancy name (no description or explanation) for a restaurant that serves {cuisine} food. Just return the name only.
    ### Response:"""
    )

    name_chain = LLMChain(llm=llm, prompt=prompt_template_name, output_key='restaurant_name')

    # Chain 2: Menu Items
    prompt_template_items = PromptTemplate(
        input_variables=['cuisine', 'restaurant_name'],
        template="""### Instruction:
    Suggest a list of traditional and popular {cuisine} dishes served at a restaurant named "{restaurant_name}". 
    Only return the dish names in bullet-point format like this:

    - Dish 1
    - Dish 2
    - Dish 3
    ...

    No description or extra text. Just the list.
    ### Response:"""
    )

    food_items_chain = LLMChain(llm=llm, prompt=prompt_template_items, output_key = 'menu_items')

    # Sequential chain to combine both steps
    chain = SequentialChain(
        chains=[name_chain, food_items_chain],
        input_variables=['cuisine'],
        output_variables=['restaurant_name', 'menu_items']
    )
    # Run the chain and capture result
    result = chain({'cuisine':cuisine})
    
    return{
        "restaurant_name": result['restaurant_name'],
        "menu_items": result['menu_items']
    }
    

if __name__ == "__main__":
    output = generate_restaurant_name_and_items("Italian")
    print(f" Restaurant Name: {output['restaurant_name']}\n")
    print(" Menu:")
    print(output['menu_items'])