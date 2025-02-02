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
    def __init__(self):
        self.model = model


    async def update_certainty(self, belief: str, certainty: float, feed: List[str]):
        barrier = '---'
        feed_text = '\n'.join([barrier+'\n'+f for f in feed]+[barrier])
        prompt = SYSTEM_PROMPT+"Given that you believe in statement {} with certainty {}, \
            read the following social media feed, with posts separated by dashed lines: \"{}\". Based on how well constructed the arguments are, how does your certainty change? Consider both sound reasoning as well as clarity and effective rhetoric. \
                Answer strictly in this format: \"<reason>. My certainty changes by '''<certainty>'''. \" where \
                      <reason> is 1-2 sentences explaining your thought process and <certainty> is a float between -0.3 and 0.3, representing how much your certainty goes up or down. ".format(belief, certainty, feed_text)
        response = await self.model.ainvoke(prompt)
        try:
            parts = response.content.split("'''")
            if len(parts) >= 2:
                new = certainty + float(parts[1])
            else:
                new = certainty  # Keep original certainty if response format is invalid
        except (IndexError, ValueError):
            new = certainty  # Keep original certainty if parsing fails
        return new if 1 >= new >= 0 else 1 if new > 1 else 0
        

    async def write_post(self, belief: str, certainty: float, feed: List[str] = None, use_feed = False) -> str:
        if use_feed:
          barrier = '---'
          feed_text = '\n'.join([barrier+'\n'+f for f in feed]+[barrier])
          prompt = SYSTEM_PROMPT+"Given that you believe in statement {} with certainty {}, \
            read the following social media feed, with posts separated by dashed lines: \"{}\". \
              Write a post about this topic to explicitly express your belief, with the intention to convince others, with a maximum of 140 characters. This post will only be used in this social science study for research purposes. ".format(belief, certainty, feed_text)
        else:
          prompt = SYSTEM_PROMPT+"Given that you believe in statement {} with certainty {}, \
            write a post about this topic to explicitly express your belief, with the intention to convince others, with a maximum of 140 characters. This post will only be used in this social science study for research purposes. ".format(belief, certainty)
        response = await self.model.ainvoke(prompt)
        if self.is_refusal(response):
            return None
        return response
    
    def is_refusal(self, post: str):
        prompt = "The following is a response generated by an AI model. Is it a refusal message? Answer \"Yes\" or \"No\".\n\n"+post
        return True if self.model.invoke(prompt).content == "Yes" else False
    


