#package rag_agent
from unittest.mock import call

import ingest
import json


class SearchAgent:
    def __init__(self, index, openai_client):
        self.index = index
        self.openai_client = openai_client
       
        
    search_tool = {
    "type": "function",
    "function": {
        "name": "search",
        "description": "Searches the web for information",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query text to look up in the course git."
                }
            },
            "required": ["query"],
	     "additionalProperties": False
        }
    }
    }

    

    instructions = """
    You're a course teaching assistant.
    You're given a question from a course student and your task is to answer it.

    If you want to look up information, use the search function. 
    Use as many keywords from the user question as possible when making first requests.

    Make multiple searches. First perform search, analyze the results 
    and then perform more searchers. 

    At the end, ask if there are other areas that the user wants to explore.
    """


    def make_call(self, call):
        args = json.loads(call.function.arguments)

        if call.function.name == "search":
            results = self.index.search(
                args["query"],
                num_results=3,
                boost_dict={"content": 2.0, "filename": 0.5}
            )

        result_json = json.dumps(results, indent=2)

        return {
            "role": "tool",
            "tool_call_id": call.id,
            "content": result_json
        }
    
    def call_llm(self,message, model="gpt-4o"):
        return self.openai_client.chat.completions.create(
                model=model,
                messages=message,
                tools=[self.search_tool]
            )


    def agent_loop(self, question, model) -> str:


        messages = [
            {'role': 'system', 'content': self. instructions},
            {'role': 'user', 'content': question}
        ]   
        
        it = 1
        last_answer = ""

        while True:
            print(f'iteration #{it}...')
            has_function_calls = False

            response = self.call_llm(messages)

            message = response.choices[0].message

            messages.append({
                "role": "assistant",
                "content": message.content,
                "tool_calls": message.tool_calls
            })

            if message.tool_calls:
                for call in message.tool_calls:
                    print('function_call:', call.function.name, call.function.arguments)
                    call_output = self.make_call(call)
                    messages.append(call_output)
                    has_function_calls = True
            else:
                print('ASSISTANT:')
                last_answer = message.content
                print(message.content)

            it = it + 1
            if not has_function_calls:
                break

        return last_answer



        


