# { "description": "A fact checker contract" }
from genlayer import *

@gl.contract
class FactChecker:
    result: bool

    def __init__(self):
        self.result = False

    @gl.public.write
    def check_fact(self, question: str) -> None:
        task = f"""
        Answer this yes/no question based on real world facts:
        {question}
        Respond with only 'true' or 'false'.
        """
        output = gl.exec_prompt(task)
        self.result = output.strip().lower() == "true"

    @gl.public.view
    def get_result(self) -> bool:
        return self.result