class Dataset:
    def __init__(self, dataset_name, data):
        self.name = dataset_name
        self.data = data
    
    def to_json(self):
        return {
            "name": self.name,
            "data": self.data
        }