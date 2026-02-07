# Portfolio selection to maximize return for a given level of risk
# A portfolio of 20 stocks

# Import libraries
import numpy
import matplotlib.pyplot as plt

# Stocks: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
inputFileName = "PortfolioAnalysis-10-2022-05-05.txt"
InvAmount = 10000
minRisk = 0.0010
maxRisk = 0.0030
nSimulations = 70
minRiskDesired = 0.0012
maxRiskDesired = 0.0015

dRisk = (maxRisk - minRisk) / nSimulations
nAverage = 0.0
bestRiskSum = 0.0
bestReturnSum = 0.0
X0Sum = 0.0
X1Sum = 0.0
X2Sum = 0.0
X3Sum = 0.0
X4Sum = 0.0
X5Sum = 0.0
X6Sum = 0.0
X7Sum = 0.0
X8Sum = 0.0
X9Sum = 0.0

# Load data into vectors
data = numpy.loadtxt(inputFileName)
Risk = data[:, 1]
Return = data[:, 2]
X0 = data[:, 3]
X1 = data[:, 4]
X2 = data[:, 5]
X3 = data[:, 6]
X4 = data[:, 7]
X5 = data[:, 8]
X6 = data[:, 9]
X7 = data[:, 10]
X8 = data[:, 11]
X9 = data[:, 12]
nDataset = len(data)

# Plot risk versus return
plt.rc('xtick', labelsize=16)
plt.rc('ytick', labelsize=16)
plt.figure(figsize=(12, 7))
plt.title('Scatter Plot of Risk versus Return', fontsize=20)
plt.plot(10000 * Risk, 100 * Return, 'co')
plt.xlim([0, 40])
plt.ylim([0, 2])
plt.xlabel('Risk [Percent Squared]', fontsize=20)
plt.ylabel('Monthly Return [Percent]', fontsize=20)
plt.savefig('RiskVersusReturn.png', dpi=300)
plt.show()

print('Best portfolio: Risk, Return, \n'
      'X0, X1, X2, X3, X4, X5, X6, X7, X8, X9 \n')

for j in range(0, nSimulations):
    bestReturn = -100
    for i in range(0, nDataset):
        if (Risk[i] > minRisk + j * dRisk) \
                and (Risk[i] < minRisk + (j + 1) * dRisk) \
                and (Return[i] > bestReturn):
            bestRisk = Risk[i]
            bestReturn = Return[i]
            X0Best = X0[i]
            X1Best = X1[i]
            X2Best = X2[i]
            X3Best = X3[i]
            X4Best = X4[i]
            X5Best = X5[i]
            X6Best = X6[i]
            X7Best = X7[i]
            X8Best = X8[i]
            X9Best = X9[i]
    if (bestRisk >= minRiskDesired) and (bestRisk <= maxRiskDesired):
        nAverage += 1
        bestRiskSum += bestRisk
        bestReturnSum += bestReturn
        X0Sum += X0Best
        X1Sum += X1Best
        X2Sum += X2Best
        X3Sum += X3Best
        X4Sum += X4Best
        X5Sum += X5Best
        X6Sum += X6Best
        X7Sum += X7Best
        X8Sum += X8Best
        X9Sum += X9Best

    print('Simulation, Best Risk [Percent Squared], Best Monthly Return [Percent]: ',
          j, numpy.round(10000 * bestRisk, 1), numpy.round(100 * bestReturn, 2))
    print('X0 to X9: ', X0Best, X1Best, X2Best, X3Best, X4Best,
          X5Best, X6Best, X7Best, X8Best, X9Best)

print('AvgRisk [Percent Squared], Monthly AvgReturn [Percent]: ')
print('%0.4f %0.4f' % (10000 * bestRiskSum / nAverage, 100 * bestReturnSum / nAverage))
print('X0Avg X1Avg X2Avg X3Avg X4Avg X5Avg X6Avg X7Avg X8Avg X9Avg: ')
print('%0.3f %0.3f %0.3f %0.3f %0.3f %0.3f %0.3f %0.3f %0.3f %0.3f' %
      (X0Sum / nAverage, X1Sum / nAverage, X2Sum / nAverage, X3Sum / nAverage, X4Sum / nAverage,
       X5Sum / nAverage, X6Sum / nAverage, X7Sum / nAverage, X8Sum / nAverage, X9Sum / nAverage))
print('Inv0 Inv1 Inv2 Inv3 Inv4 Inv5 Inv6 Inv7 Inv8 Inv9: ')
print('%5.0f %5.0f %5.0f %5.0f %5.0f %5.0f %5.0f %5.0f %5.0f %5.0f'
      % (X0Sum / nAverage * InvAmount, X1Sum / nAverage * InvAmount,
         X2Sum / nAverage * InvAmount, X3Sum / nAverage * InvAmount, X4Sum / nAverage * InvAmount,
         X5Sum / nAverage * InvAmount, X6Sum / nAverage * InvAmount, X7Sum / nAverage * InvAmount,
         X8Sum / nAverage * InvAmount, X9Sum / nAverage * InvAmount))
