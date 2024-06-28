import requests
from urllib.parse import quote

__all__ = ["api"]


class HorridAPI:
    
    def __init__(self)->None:
        """        
        """
        pass

    
    
    @staticmethod
    def llama(query: str):        
        prompt = quote(query)
        api = f'https://horrid-api.onrender.com/llama?query={prompt}'
        res = requests.get(api).json()
        k = res['response']
        return k


api=HorridAPI()
