import gensim

class ModelLoader:
    model_sg = None

    @classmethod
    def load_model(cls):
        if cls.model_sg is None:
            cls.model_sg = gensim.models.FastText.load('/Users/katiana/Documents/Thesawrws-website/website/FastText_WNLT_SkipGram/skipgram_subword_model.model')
        return cls.model_sg
