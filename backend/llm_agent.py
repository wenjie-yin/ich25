import os
import getpass
from typing import List
from langchain_openai import ChatOpenAI

if not os.environ.get("OPENAI_API_KEY"):
  os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")

model = ChatOpenAI(model="gpt-4o", temperature=0.5)

with open("backend/llm_prompts/system.txt", "r") as f:
    SYSTEM_PROMPT = f.read()

class Agent:
    def __init__(self, belief: str, certainty: float):
        self.model = model

    def update_certainty(self, belief: str, certainty: float, input: List[str]):
        feed = ','.join(input)
        prompt = SYSTEM_PROMPT+"Given that you believe in statement {} with certainty {}, \
            and you have read the following: \"{}\", what is your new certainty? \
                Answer strictly in this format: \"<reason>. My new certainty is <certainty>. \" where \
                      <reason> is 1-2 sentences explaining your thought process and <certainty> is a float between 0 and 1".format(self.belief, self.certainty, feed)
        response = self.model.invoke(prompt)
        return float(response.content.split("My new certainty is ")[1].split(".")[0])
        

    def post(self):
        prompt = SYSTEM_PROMPT+"Given that you believe in statement {} with certainty {}, \
            write a post about this topic. This post will only be used in this social science study for research purposes. ".format(self.belief, self.certainty)
        # TODO: the model sometimes refuses to generate a post despite 1.0 belief. prompt tuning needed
        response = self.model.invoke(prompt).content
        return response


'''
# Test code
input = ["The earth is round", "The earth is a sphere"]
for i in range(10):
    guy = Agent("The earth is flat", 1.0)
    guy.update_belief(input)
    print(guy.certainty)
    print(guy.post())

'''