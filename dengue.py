from sklearn.ensemble import GradientBoostingClassifier
import pandas
from sklearn.preprocessing import LabelEncoder
from collections import defaultdict
import pickle


class DenguePredictor:
    def __init__(self):
        self.encoder = defaultdict(LabelEncoder)
        self.NeededFields = ['gender']
        self.data = pandas.read_csv('dengue_dataset.csv')
        self.data.dropna(inplace=True)
        self.data.drop(['timestamp', 'name(first name only):','email', 'district'], inplace=True,axis=1)

        self.data['bp'] = self.data['bp'].apply(self.convert_bp_to_map)
        self.data = self.data.apply(lambda x:  self.encoder[x.name].fit_transform(x) if x.name in self.NeededFields else x)
        
        try:
            self.model = pickle.load(open('dengue_model', 'rb'))
            print("Model loaded successfully!!")
        except Exception as e:
            print("Model not found, training data..")
            self.train_model()

    def convert_bp_to_map(self, bp):
        val = bp.split("/")
        dbp = int(val[0])
        sbp = int(val[1])
        return ((2 * dbp) + sbp)/3

    def train_model(self):
        X = self.data[self.data.columns[:-1]]
        Y = self.data['dengue']
        print(X.columns)
        self.model = GradientBoostingClassifier()
        self.model = self.model.fit(X, Y)
        print("Training completed, saving model...")
        pickle.dump(self.model, open('dengue_model', 'wb'))

    def predict_infection(self, inputdata):
        inputdata = pandas.DataFrame(inputdata).apply(
            lambda x: self.encoder[x.name].transform(x) if x.name in self.NeededFields else x)
        return self.model.predict(inputdata)[0]

    def test_model_user_input(self):
        print("Enter data for predection (for string data be careful to add only already present data!!)")
        inputdata = {}
        for x in self.data.columns[:-1]:
            inputdata[x] = [input("Enter " + x + ": ")]
        inputdata = pandas.DataFrame(inputdata).apply(
            lambda x: self.encoder[x.name].transform(x) if x.name in self.NeededFields else x)
        print("Infected: ", self.model.predict(inputdata)[0])
