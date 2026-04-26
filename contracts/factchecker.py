# { "Depends": "py-genlayer:test" }
from genlayer import *
import json

class FactChecker(gl.Contract):
    result: bool

    def __init__(self):
        self.result = False

    @gl.public.write
    def check_fact(self, question: str) -> None:
        prompt = f"""
        You are a fact checker. Answer the following yes/no question.
        Question: {question}
        Respond ONLY with JSON in this exact format: {{"answer": true}} or {{"answer": false}}
        """
        def nondet():
            res = gl.nondet.exec_prompt(prompt, response_format="json")
            return json.dumps(res, sort_keys=True)
        
        output = gl.eq_principle.strict_eq(nondet)
        self.result = json.loads(output)["answer"]

    @gl.public.view
    def get_result(self) -> bool:
        return self.result