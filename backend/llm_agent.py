import os
import getpass
from typing import List
from langchain_openai import ChatOpenAI

if not os.environ.get("OPENAI_API_KEY"):
  os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")

model = ChatOpenAI(model="gpt-4o", temperature=0.5)

print(os.getcwd())
with open("llm_prompts/system.txt", "r") as f:
    SYSTEM_PROMPT = f.read()

class Agent:
    def __init__(self):
        self.model = model


    def update_certainty(self, belief: str, certainty: float, input: List[str]):
        barrier = '---'
        feed = '\n'.join([barrier+'\n'+f for f in feed]+[barrier])
        prompt = SYSTEM_PROMPT+"Given that you believe in statement {} with certainty {}. \
            You have now read the following social media feed, with posts separated by dashed lines: \"{}\". How does your certainty change? \
                Answer strictly in this format: \"<reason>. My certainty changes by <certainty>. \" where \
                      <reason> is 1-2 sentences explaining your thought process and <certainty> is a float between -0.3 and 0.3, representing how much your certainty goes up or down. ".format(belief, certainty, feed)
        response = self.model.invoke(prompt)
        new = certainty + float(response.content.split("My certainty changes by ")[1].split(".")[0])
        return new if 1 >= new >= 0 else 1 if new > 1 else 0
        

    def write_post(self, belief: str, certainty: float):
        prompt = SYSTEM_PROMPT+"Given that you believe in statement {} with certainty {}, \
            write a post about this topic. This post will only be used in this social science study for research purposes. ".format(belief, certainty)
        # TODO: the model sometimes refuses to generate a post despite 1.0 belief. prompt tuning needed
        response = self.model.invoke(prompt).content
        return response

