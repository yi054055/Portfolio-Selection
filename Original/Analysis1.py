# Compute asset allocation and the resulting risk versus return based on Markowitz 1952
# Take closing price of 10 stocks
# This code uses a randomized approach to assign the portfolio weights

import numpy
import random

# Analysis 2022-05-05
inputFileName = "StockHistory-10-2022-05-05.txt"
outputFileName = "PortfolioAnalysis-10-2022-05-05.txt"

# Symbols:
# ZSP.TO, IVOO, VIOO, ZCN.TO, VEE.TO, VIU.TO, ZAG.TO, VBG.TO, VBU.TO, HEP.TO
StockIndex = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
StockDividend = [0.0130, 0.0107, 0.0088, 0.0281, 0.0165, 0.0228, 0.0303,
                 0.0067, 0.0204, 0.0682]

# Load data into vectors
data = numpy.loadtxt(inputFileName)
nDataset = len(data)
nYears = 6
nStocks = 10
nSample = 500000

# For monthly return analysis consider this value for number of days in a month
returnFrequencyDays = int(nDataset / (nYears * 12))
daysInYear = int(nDataset / nYears)

# Define price matrix to be filled later
StockPrice = numpy.zeros((nDataset, nStocks))
for i in range(0, nStocks):
    for j in range(0, nDataset):
        StockPrice[j][i] = data[j, StockIndex[i]]

# First calculate the stock price return, i.e. share gain, through price history
StockShareGain = numpy.zeros((nDataset - returnFrequencyDays, nStocks))
StockReturn = numpy.zeros((nDataset - returnFrequencyDays, nStocks))

x = [i for i in range(0, returnFrequencyDays)]
for i in range(0, nStocks):
    # Find the returns in each of the time periods
    for j in range(0, nDataset - returnFrequencyDays):
        StockShareGain[j][i] = (StockPrice[j + returnFrequencyDays, i] - StockPrice[j, i]) / StockPrice[j][i]
        StockReturn[j][i] = StockShareGain[j][i] + StockDividend[i] * returnFrequencyDays / daysInYear

MeanStockReturn = numpy.zeros((nStocks))
CovStockReturn = numpy.zeros((nStocks, nStocks))

# Set vectors y and z
Vectory = numpy.zeros((nDataset - returnFrequencyDays))
Vectorz = numpy.zeros((nDataset - returnFrequencyDays))

# print the return of the selected stocks
for i in range(0, nStocks):
    MeanStockReturn[i] = numpy.mean(StockReturn[:, i])
    print('Stock Index, Average Monthly Return [Percent]:', i, numpy.round(100 * MeanStockReturn[i], 2))

for y in range(0, nStocks):
    for z in range(0, nStocks):
        for x in range(0, nDataset - returnFrequencyDays):
            Vectory[x] = StockReturn[x][y]
            Vectorz[x] = StockReturn[x][z]
        Covariance = numpy.cov(Vectory, Vectorz)
        CovStockReturn[y][z] = Covariance[0][1]
        print('Stock Index y, z, Covariance of Return [Percent Squared]:',
              y, z, numpy.round(10000 * CovStockReturn[y][z], 1))

# Now we should sample random portfolios for weights X0, X1, ... , X9 >= 0 subject to sum Xi = 1
X = numpy.zeros((nSample, nStocks))
Return = numpy.zeros((nSample))
Risk = numpy.zeros((nSample))

# Find random combinations of X0, X1, ..., X9 assuming Delta X = 0.1, subject to Sum Xi = 1
for a in range(0, nSample):
    # Random selection of stock
    for b in range(0, nStocks):
        RandStock = random.randint(0, nStocks - 1)
        X[a][RandStock] = X[a][RandStock] + 1 / nStocks

    # Calculate the sum of X0 to X9 and warn user if not close to 1
    SumX = numpy.sum(X[a][:])
    if SumX > 1.001 or SumX < 0.999:
        print('Warning, Sum of X[a][:] is not close to 1, it is:', SumX)

    Return[a] = sum(X[a][i] * MeanStockReturn[i] for i in range(nStocks))

    # To calculate risk, all the variances and covariances must be considered
    for y in range(0, nStocks):
        for z in range(0, nStocks):
            Risk[a] = Risk[a] + X[a][y] * X[a][z] * CovStockReturn[y][z]

# Write data to file
outputFile = open(outputFileName, "w")
outputFile.write("#Sample \t Risk \t Return \t "
                 "X0 \t X1 \t X2 \t X3 \t X4 \t "
                 "X5 \t X6 \t X7 \t X8 \t X9 \n")

# Now loop through data points and write to file
for a in range(0, nSample):
    outputFile.write("%i \t %f \t %f \t "
                     "%f \t %f \t %f \t %f \t %f \t "
                     "%f \t %f \t %f \t %f \t %f \n" %
                     (a, Risk[a], Return[a],
                      X[a][0], X[a][1], X[a][2], X[a][3], X[a][4],
                      X[a][5], X[a][6], X[a][7], X[a][8], X[a][9]))

# Close file
outputFile.close()
