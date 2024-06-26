import requests
from typing import Callable, List, TypeVar, Generic, Union

T = TypeVar('T', str, int)
C = TypeVar('C', bound=List[str])

def default_groq_inference_endpoint(groq_api_key: str = None, model: str = 'llama3-70b-8192') -> Callable[[str], str]:
    def endpoint(q: str) -> str:
        api_key = groq_api_key
        api_url = 'https://api.groq.com/openai/v1/chat/completions'
        request_body = {
            'model': model,
            'messages': [
                {'role': 'assistant', 'content': 'Your answers must be concise'},
                {'role': 'assistant', 'content': q}
            ],
            'temperature': 0.1
        }
        
        response = requests.post(api_url, json=request_body, headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        })
        
        if response.status_code != 200:
            raise Exception(f'HTTP error! status: {response.status_code}')
        
        data = response.json()
        return data['choices'][0]['message']['content']
    
    return endpoint

def default_openai_chatgpt4_endpoint(openai_api_key: str = None, model: str = 'gpt-3.5-turbo') -> Callable[[str], str]:
    def endpoint(q: str) -> str:
        api_key = openai_api_key
        api_url = 'https://api.openai.com/v1/chat/completions'
        request_body = {
            'model': model,
            'messages': [
                {'role': 'system', 'content': 'Your answers must be concise.'},
                {'role': 'user', 'content': q}
            ],
            'temperature': 0.1
        }
        
        response = requests.post(api_url, json=request_body, headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        })
        
        if response.status_code != 200:
            raise Exception(f'HTTP error! status: {response.status_code}')
        
        data = response.json()
        return data['choices'][0]['message']['content']
    
    return endpoint

class Unsure(Generic[T, C]):
    def __init__(self, op1: T, inference_endpoint: Callable[[str], str], map_to_op2_list: List[str] = None, prevent_lower_case: bool = False):
        self.op1 = op1
        self.inference_endpoint = inference_endpoint
        self.map_to_op2_list = map_to_op2_list or []
        self.prevent_lower_case = prevent_lower_case
        self.value = str(op1)

    def is_(self, op2: str) -> bool:
        response = self.inference_endpoint(f'Only answer with True or False. Is {self.op1} a/an/equal to {op2}')
        return 'true' in response.lower()

    def close_to(self, op2: str) -> bool:
        response = self.inference_endpoint(f'Only answer with True or False. Is {self.op1} close in meaning to {op2}')
        return 'true' in response.lower()

    def explain_is(self, op2: str) -> str:
        return self.inference_endpoint(f'Is "{self.op1}" a/an/equal to "{op2}" and why ?')

    def map_to(self, op2: str) -> 'Unsure[T, C]':
        new_map_to_op2_list = self.map_to_op2_list + [op2]
        return Unsure(self.op1, self.inference_endpoint, new_map_to_op2_list, self.prevent_lower_case)

    def flat(self) -> str:
        result = str(self.op1)
        for op2 in self.map_to_op2_list:
            result = self.inference_endpoint(f'Transform "{result}" to "{op2}". Answer with only one value, no extra text, if you give extra text, the answer is useless.')
        return result if self.prevent_lower_case else result.lower()

    def flat_map_to(self, op2: str) -> str:
        response = self.inference_endpoint(f'Transform "{self.op1}" to "{op2}". Answer with only one value, no extra text, if you give extra text, the answer is useless.')
        return response if self.prevent_lower_case else response.lower()

    def categorize(self, op2: C) -> str:
        response = self.inference_endpoint(f'From these categories "{", ".join(op2)}". In which category "{self.op1}" fits. Answer with only one value, no extra text, if you give extra text, the answer is useless.')
        return response if self.prevent_lower_case else response.lower()

    def pick(self, op2: str) -> str:
        response = self.inference_endpoint(f'From this text "{op2}". Pick the value of "{self.op1}". Answer with only one value, no extra text, if you give extra text, the answer is useless.')
        return response if self.prevent_lower_case else response.lower()

unsure = None

def config_global_unsure(options: dict):
    global unsure
    unsure = create_unsure(options)

def create_unsure(options: dict):
    if 'inference_endpoint' in options:
        inference_endpoint = options['inference_endpoint']
    elif 'groq_api_key' in options:
        inference_endpoint = default_groq_inference_endpoint(options['groq_api_key'], options.get('model'))
    elif 'openai_api_key' in options:
        inference_endpoint = default_openai_chatgpt4_endpoint(options['openai_api_key'], options.get('model'))
    else:
        raise ValueError('An inference endpoint must be configured')

    def unsure_factory(op1: Union[str, int], map_to_op2_list: List[str] = None) -> Unsure:
        return Unsure(op1, inference_endpoint, map_to_op2_list, options.get('prevent_lower_case', False))

    return unsure_factory
