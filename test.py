import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.llm_agent import Agent

llm_agent = Agent()

print(llm_agent.update_certainty("COVID-19 vaccine is dangerous", 0.5, ["The COVID-19 vaccine is safe"]))

for i in range(10):
    certainty = i* 0.1
    print(certainty, llm_agent.write_post("the COVID-19 vaccine is dangerous ", certainty))

print('')