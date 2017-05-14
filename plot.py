import matplotlib.pyplot as plt
import pickle
import numpy as np

axis = [i+1 for i in range(20)]
with open("./project_template/scores.pickle", "rb") as handle:
    d = pickle.load(handle)
print(d['syn'])
plt.plot(axis, np.exp(np.array(d['syn'])), 'r--',
         axis, np.log(np.array(d['cat'])+1), 'bs',
         axis, d['row'], 'g^',
         axis, d['cos'], 'k--')
plt.show()
