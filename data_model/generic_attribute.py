class GenericAttribute:
    def __init__(self,id:str='') -> None:
        self.id = id
    
    def get_id(self) -> str:
        return self.id