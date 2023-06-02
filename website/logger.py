import gensim
from gensim.models.callbacks import CallbackAny2Vec


class EpochLogger(CallbackAny2Vec):
    def __init__(self):
        self.epoch = 0
    def on_epoch_begin(self, model):
        print("Epoch #{} start".format(self.epoch))
    def on_epoch_end(self, model):
        print("Epoch #{} end".format(self.epoch))
        self.epoch += 1
    @staticmethod
    def mm():
        model_sg = gensim.models.FastText.load('/Users/katiana/Documents/Thesawrws-website/website/FastText_WNLT_SkipGram/skipgram_subword_model.model')
        return model_sg