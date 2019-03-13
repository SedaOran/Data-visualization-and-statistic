import sys
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
import random
import timeit

electionFile = sys.argv[1]
nomineeList = sys.argv[2].split(",")
nomineeColumnIndex = [0 for i in range(len(nomineeList))]
outputFile = "retrievedData.txt"
answerFile = "myAnswer.txt"

stateList = []
nomineesVotes = [[] for i in range(len(nomineeList))]
colorList = ['r','b','y','c','m']

meanArray = [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1]
numUSAGreater = 0
percUSAGreater = 0
pLevel = 0
electionDataSize = 0
randMSESize =  10000

def retrieveData(filename,nominees):
	global electionDataSize
	numLines = 0
	with open(filename) as f:
		firstline = 1
		for line in f:
			if 1 == firstline:
				lineArr = line.rstrip().split(",")
				for i in range(len(nominees)):
					nomineeColumnIndex[i] = lineArr.index(nominees[i])
			else:
				lineArr = line.split(",")
				stateList.append(lineArr[0])
				for i in range(len(nominees)):
					nomineesVotes[i].append(int(lineArr[nomineeColumnIndex[i]]))
				numLines = numLines + 1
			firstline = 0
	electionDataSize = numLines * len(nominees)
	outputList = []
	for i in range(len(nominees)):
		for vote in nomineesVotes[i]:
			outputList.append(vote)
	return outputList

voteList = retrieveData(electionFile,nomineeList)

with open(outputFile,"w") as output:
	output.write(str(voteList))

output.close()

def DispBarPlot():
	firstNom = 0
	secondNom = 0
	for i in range(len(nomineeList)):
		if sum(nomineesVotes[i]) > sum(nomineesVotes[firstNom]):
			firstNom = i
			secondNom = firstNom
		elif sum(nomineesVotes[i]) > sum(nomineesVotes[secondNom]):
			secondNom = i
		elif secondNom == firstNom:
			secondNom = i

	n_groups =  len(stateList)

	firstVotes = nomineesVotes[firstNom]

	secondVotes = nomineesVotes[secondNom]

	fig, ax = plt.subplots(figsize=(20,10))
	index = np.arange(n_groups)

	bar_width = 0.3
	opacity = 1
	error_config = {'ecolor': '0.3'}

	rects2 = plt.bar(index + 1, secondVotes, bar_width,
					 alpha=opacity,
					 color='r',
					 yerr=None,
					 error_kw=error_config,
					 label=nomineeList[secondNom])

	rects1 = plt.bar(index+1+bar_width, firstVotes, bar_width,
					 alpha=opacity,
					 color='b',
					 yerr=None,
					 error_kw=error_config,
					 label=nomineeList[firstNom])

	plt.xlabel('State')
	plt.ylabel('Votes')
	plt.title('Votes per State')
	plt.xticks(index + bar_width + 1, stateList,rotation =90)
	plt.legend()
	plt.tight_layout()
	plt.savefig("ComparativeVotes.pdf")

def calculatepersantages():
	persantageList=[0 for i in range(len(nomineeList))]
	totalVotes = [0 for i in range(len(nomineeList))]
	allTotal=0
	for i in range(len(nomineeList)):
		for vote in nomineesVotes[i]:
			totalVotes[i] = totalVotes[i] + vote
		allTotal = allTotal + totalVotes[i]

	for i in range(len(nomineeList)):
		persantageList[i] = (totalVotes[i] / allTotal) * 100
	return persantageList

def compareVoteonBar():
	percentages =calculatepersantages()
	n_groups = len(percentages)

	fig, ax = plt.subplots()

	index = np.arange(n_groups)
	bar_width = 0.7

	opacity = 1
	error_config = {'ecolor': '0.3'}

	rects = plt.bar(index,percentages, bar_width,
					 color = colorList[0],
					 alpha=opacity,
					 yerr=None,
					 error_kw=error_config,
					 label=nomineeList[0]
					 )

	for i in range(1,len(nomineeList)):
		plt.bar(0,0, bar_width,
		color = colorList[i%5],
		alpha=opacity,
		yerr=None,
		error_kw=error_config,
		label=nomineeList[i])

		rects[i].set_color(colorList[i])

	percentagesFormatted = []
	for percent in percentages:
		percentagesFormatted.append("{0:.3f}".format(percent))

	plt.xlabel('Nominees')
	plt.ylabel('vote percentages')
	plt.xticks(index + bar_width/2, percentagesFormatted)
	plt.legend()
	plt.tight_layout()
	plt.savefig("CompVotePercs.pdf")

def obtainHistogram(numbers):
	dataLen = len(numbers)
	histogramNums = []
	histogramPerc = []
	totalDigits = 0
	for i in range(0,10):
		histogramNums.append(0)
		histogramPerc.append(0)
	for num in numbers:
		digitOnes = int(num % 10)
		histogramNums[digitOnes] = histogramNums[digitOnes] + 1
		digitTens = int((num/10) % 10)
		histogramNums[digitTens] = histogramNums[digitTens] + 1
		totalDigits = totalDigits + 2
	for i in range(0,10):
		histogramPerc[i] = histogramNums[i] / totalDigits
	return histogramPerc

def plotHistogram(histData, plotColor, outputPdfFile):
	plt.clf()
	dashedLine = plt.plot(meanArray)
	plt.setp(dashedLine, color = 'g',label='Mean',linestyle="dashed")
	digitLine = plt.plot(histData)
	plt.setp(digitLine, color=plotColor,label='Digit Dist.')
	plt.title('Histogram of least sign. digits')
	plt.ylabel('Distribution')
	plt.xlabel('Digits')
	plt.legend()
	plt.savefig(outputPdfFile)

def plotHistogramWithSample():
	rand_10 = [];rand_50 = []; rand_100 = []; rand_1000 = []; rand_10000 = []
	for i in range(0,10):
		rand_10.append(random.choice(range(0,100)))
	for i in range(0,50):
		rand_50.append(random.choice(range(0,100)))
	for i in range(0,100):
		rand_100.append(random.choice(range(0,100)))
	for i in range(0,1000):
		rand_1000.append(random.choice(range(0,100)))
	for i in range(0,10000):
		rand_10000.append(random.choice(range(0,100)))

	hist_1 = obtainHistogram(rand_10)
	plotHistogram(hist_1,'r',"HistogramofSample1.pdf")

	hist_2 = obtainHistogram(rand_50)
	plotHistogram(hist_2,'b',"HistogramofSample2.pdf")

	hist_3 = obtainHistogram(rand_100)
	plotHistogram(hist_3,'y',"HistogramofSample3.pdf")

	hist_4 = obtainHistogram(rand_1000)
	plotHistogram(hist_4,'c',"HistogramofSample4.pdf")

	hist_5 = obtainHistogram(rand_10000)
	plotHistogram(hist_5,'m',"HistogramofSample5.pdf")

def calculateMSE(list1,list2) :
	calcualatedVal = 0
	for i in range(0,len(list1)):
		calcualatedVal =  calcualatedVal + (list2[i] - list1[i])**2
	return calcualatedVal

def compareMSEs(usaElectionMSE):
	global numUSAGreater
	global percUSAGreater
	global pLevel
	for i in range(randMSESize):
		rand_Election = []
		for i in range(0,electionDataSize):
			rand_Election.append(random.choice(range(0,100)))
		histPercentRand = obtainHistogram(rand_Election)
		mseRand = calculateMSE(histPercentRand, meanArray)
		if usaElectionMSE > mseRand:
			numUSAGreater = numUSAGreater + 1
	percUSAGreater = (numUSAGreater / randMSESize) * 100
	pLevel = numUSAGreater / randMSESize

DispBarPlot()
compareVoteonBar()

histPercent = obtainHistogram(voteList)
plotHistogram(histPercent, 'r', "Histogram.pdf")
plotHistogramWithSample()

usaMSE = calculateMSE(histPercent, meanArray)
compareMSEs(usaMSE)

print("MSE value of 2012 USA election is : " + str(usaMSE))
print("The number of MSE of random samples which are larger than or equal to USA election MSE is : " + str(randMSESize-numUSAGreater))
print("The number of MSE of random samples which are smaller than USA election MSE is : " + str(numUSAGreater))
print("2012 USA election rejection level p is : " + str(pLevel))
if percUSAGreater <= 95:
	print("Finding: We reject the null hypothesis at the p = " + str(pLevel) + " level")
else:
	print("Finding: There is no statistical evidence to reject null")

with open(answerFile,"w") as answer:
	answer.writelines("MSE value of 2012 USA election is : " + str(usaMSE) + "\n")
	answer.writelines("The number of MSE of random samples which are larger than or equal to USA election MSE is : " + str(randMSESize-numUSAGreater)+ "\n")
	answer.writelines("The number of MSE of random samples which are smaller than USA election MSE is : " + str(numUSAGreater)+ "\n")
	answer.writelines("2012 USA election rejection level p is : " + str(pLevel) + "\n")
	if percUSAGreater <= 95:
		answer.writelines("Finding: We reject the null hypothesis at the p = " + str(pLevel) + " level" + "\n")
	else:
		answer.writelines("Finding: There is no statistical evidence to reject null")
answer.close()
