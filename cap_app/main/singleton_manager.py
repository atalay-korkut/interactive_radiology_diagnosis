from main.AIhelper import load_model, load_validator


class SingletonManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.transformer = None
            cls._instance.tokenizer = None
            cls._instance.cxr_validator_model = None
        return cls._instance

    def load_objects(self):
        if self.transformer is None and self.tokenizer is None:
            try:
                self.transformer, self.tokenizer = load_model()
            except Exception as e:
                print(f"Error loading transformer and tokenizer: {e}")
        if self.cxr_validator_model is None:
            try:
                self.cxr_validator_model = load_validator()
            except Exception as e:
                print(f"Error loading cxr_validator_model: {e}")

    def get_transformer(self):
        if self.transformer is None:
            self.load_objects()
        return self.transformer

    def get_tokenizer(self):
        if self.tokenizer is None:
            self.load_objects()
        return self.tokenizer

    def get_cxr_validator_model(self):
        if self.cxr_validator_model is None:
            self.load_objects()
        return self.cxr_validator_model


singleton_manager = SingletonManager()
