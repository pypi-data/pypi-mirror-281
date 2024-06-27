from typing import Callable, Dict, List

FilterFunc = Callable[[str], str]

class Normalizer():
    def __init__(self):
        self._filters: Dict[str, FilterFunc] = {}
    
    def __call__(self, text:str):
        return self.normalize(text)

    def normalize(self, text:str) -> str:
        for func in self._filters.values():
            text = func(text)
        return text

    def set(self, filters: Dict[str, FilterFunc]):
        for name, func in filters.items():
            self._filters[name] = func

    def list(self) -> List[str]:
        return self._filters.keys()

