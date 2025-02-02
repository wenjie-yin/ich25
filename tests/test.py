import llm_agent

llm_agent = llm_agent.Agent()

print(llm_agent.update_certainty("The sky is fake", 0.5, ["The sky is blue", "The sky is green", "The sky is red"]))

for i in range(10):
    certainty = i* 0.1
    print(certainty, llm_agent.write_post("The earth is flat", certainty))

print('')