from sklearn.ensemble import GradientBoostingClassifier
import pandas
from sklearn.preprocessing import LabelEncoder
from collections import defaultdict
import pickle


class InfectionPredictor:
    def __init__(self):
        self.encoder = defaultdict(LabelEncoder)
        self.NeededFields = ['gender','district','infection']
        self.data = pandas.read_csv('infection_dataset.csv')
        self.data.dropna(inplace=True)
        self.data.drop(['name'], inplace=True,axis=1)
        self.data = self.data.apply(lambda x:  self.encoder[x.name].fit_transform(x) if x.name in self.NeededFields else x)
        self.data = self.data.loc[:, ~self.data.columns.str.contains('^Unnamed')]

        try:
            self.model = pickle.load(open('infection_model', 'rb'))
            print("Model loaded successfully!!")
        except Exception as e:
            print("Model not found, training data..")
            self.train_model()

    def train_model(self):
        X = self.data[self.data.columns[:-1]]
        Y = self.data['infection']
        print(X.columns)
        self.model = GradientBoostingClassifier()
        self.model = self.model.fit(X, Y)
        print("Training completed, saving model...")
        pickle.dump(self.model, open('infection_model', 'wb'))

    def predict_infection(self, inputdata):
        inputdata = pandas.DataFrame(inputdata).apply(
            lambda x: self.encoder[x.name].transform(x) if x.name in self.NeededFields else x)
        return self.encoder["infection"].inverse_transform(self.model.predict(inputdata))[0]

    def test_model_user_input(self):
        print("Enter data for predection (for string data be careful to add only already present data!!)")
        inputdata = {}
        for x in self.data.columns[:-1]:
            inputdata[x] = [input("Enter " + x + ": ")]
        inputdata = pandas.DataFrame(inputdata).apply(
            lambda x: self.encoder[x.name].transform(x) if x.name in self.NeededFields else x)
        print("Infected: ", self.model.predict(inputdata)[0])
