import shutil
from tempfile import mkdtemp
from unittest import TestCase

from sklearn.metrics import f1_score

from languageflow.data import CategorizedCorpus, Sentence
from languageflow.data_fetcher import DataFetcher, NLPData
from languageflow.models.text_classifier import TextClassifier, TEXT_CLASSIFIER_ESTIMATOR
from languageflow.trainers.model_trainer import ModelTrainer


class TestSVC(TestCase):
    def test(self):
        corpus: CategorizedCorpus = DataFetcher.load_corpus(NLPData.AIVIVN2019_SA_SAMPLE)
        # corpus: CategorizedCorpus = DataFetcher.load_corpus(NLPData.AIVIVN2019_SA)

        classifier = TextClassifier(estimator=TEXT_CLASSIFIER_ESTIMATOR.SVC)
        model_trainer = ModelTrainer(classifier, corpus)
        tmp_model_folder = mkdtemp()

        def negative_f1_score(y_true, y_pred):
            score_class_0, score_class_1 = f1_score(y_true, y_pred, average=None)
            return score_class_1

        def macro_f1_score(y_true, y_pred):
            return f1_score(y_true, y_pred, average='macro')

        model_trainer.train(tmp_model_folder, scoring=macro_f1_score)

        classifier = TextClassifier.load(tmp_model_folder)
        sentence = Sentence('tuyệt vời')
        classifier.predict(sentence)
        shutil.rmtree(tmp_model_folder)
        print(sentence)
