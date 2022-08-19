import matplotlib
matplotlib.use("TkAgg")

import sklearn.linear_model as lm
from sklearn.svm import SVR
import numpy as np
import matplotlib.pyplot as plt

m=10**4
(a,b)=(1,1)
X=np.linspace(0,12,m).reshape(m,1)
y=a*np.exp(np.sin(b*X))
plt.plot(X,y,c='g')

X2=np.linspace(0,3,m//2).reshape(m//2,1)


model=SVR()
model.fit(X,y)
print(model.score(X,y))
prediction= model.predict(X2)
plt.plot(X2,prediction,c="r")

plt.show()