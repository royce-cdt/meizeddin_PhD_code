import numpy as np

#using exponential kernel

#posterior mean calculation for gaussian conditional
x = np.array([1, 3])
y = np.array([1, 0.5])
xstar = np.array([2])
Kff = np.exp(-np.abs(x[:, None] - x[None, :])/4)
Kstarf = np.exp(-np.abs(xstar - x[None, :])/4)
posteriorMean = Kstarf@np.linalg.inv(Kff)@y
print(posteriorMean)


#posterior variance calculation 
x = np.array([1, 3])
y = np.array([1, 0.5])
xstar = np.array([2])
Kss = np.exp(-np.abs(xstar - xstar)/4)
Kff = np.exp(-np.abs(x[:, None] - x[None, :])/4)
Kstarf = np.exp(-np.abs(xstar - x[None, :])/4)
Kfstar = np.exp(-np.abs(x[:, None] - xstar)/4)

posteriorVar = Kss - Kstarf@np.linalg.inv(Kff)@Kfstar
print(posteriorVar)

#using exponential quadratic kernel

#posterior mean calculation for gaussian conditional
x = np.array([1, 3])
y = np.array([1, 0.5])
xstar = np.array([2])
Kff = np.exp(-np.square(x[:, None] - x[None, :])/32)
Kstarf = np.exp(-np.square(xstar - x[None, :])/32)
posteriorMean = Kstarf@np.linalg.inv(Kff)@y
print(posteriorMean)


#posterior variance calculation 
x = np.array([1, 3])
y = np.array([1, 0.5])
xstar = np.array([2])
Kss = np.exp(-np.square(xstar - xstar)/32)
Kff = np.exp(-np.square(x[:, None] - x[None, :])/32)
Kstarf = np.exp(-np.square(xstar - x[None, :])/32)
Kfstar = np.exp(-np.square(x[:, None] - xstar)/32)

posteriorVar = Kss - Kstarf@np.linalg.inv(Kff)@Kfstar
print(posteriorVar)