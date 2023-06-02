#cd fastText-finetuned
#wget https://datainnovation.cardiff.ac.uk/is/wecy/files/FastText_WNLT_SkipGram.zip 
#unzip  FastText_WNLT_SkipGram.zip  

import gensim
from gensim.models.callbacks import CallbackAny2Vec
class EpochLogger(CallbackAny2Vec):
    """
    Callback to log information about training

    ** THIS MUST BE DEFINED BEFORE BEING ABLE TO LOAD IN MODELS **
    """
    def __init__(self):
        self.epoch = 0

    def on_epoch_begin(self, model):
        print("Epoch #{} start".format(self.epoch))

    def on_epoch_end(self, model):
        print("Epoch #{} end".format(self.epoch))
        self.epoch += 1
model_sg = gensim.models.FastText.load('/Users/katiana/Documents/Thesawrws-website/website/FastText_WNLT_SkipGram/skipgram_subword_model.model')
print(model_sg.wv.most_similar('glaw', topn=10))