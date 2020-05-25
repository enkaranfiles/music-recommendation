from keras.models import load_model
import numpy as np
from analyze import x_test,y_test

model = load_model('model/song_classify.h5')

from sklearn.metrics import accuracy_score

def unsplit(values):
    chunks = np.split(values, 100)
    return np.array([np.argmax(chunk) % 10 for chunk in chunks])

pred_values = model.predict(x_test)
predictions = unsplit(pred_values)
truth = unsplit(y_test)
print("actual accuracy shown here")
print(accuracy_score(predictions, truth))
