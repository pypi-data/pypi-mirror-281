import uuid

class Generator:
    @staticmethod
    def generate():
        return str(uuid.uuid4())
