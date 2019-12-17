from .Constants import *
from .Population import Population

# 
# By using this file, you are agreeing to this product's EULA
#
# This product can be obtained in https://github.com/jespb/Python-GSGP
#
# Copyright ©2019 J. E. Batista
#

class GSGP:
	population = None

	def __init__(self):
		self.population = Population()
		self.population.train()
		
	def getCurrentGeneration(self):
		return self.population.getCurrentGeneration()

	def getTrainingAccuracy(self):
		return self.population.bestIndividual.getTrainingAccuracy() if self.output == "Classification" else 0

	def getTestAccuracy(self):
		return self.population.bestIndividual.getTestAccuracy() if self.output == "Classification" else 0
	
	def getTrainingRMSE(self):
		return self.population.bestIndividual.getTrainingRMSE()
	
	def getTestRMSE(self):
		return self.population.bestIndividual.getTestRMSE()

	def getAccuracyOverTime(self):
		return [self.population.trainingAccuracyOverTime, self.population.testAccuracyOverTime]

	def getRmseOverTime(self):
		return [self.population.trainingRmseOverTime, self.population.testRmseOverTime]

	def getSizeOverTime(self):
		return self.population.sizeOverTime 

	def getBestIndividual(self):
		return self.population.bestIndividual

	def getFormatedModel(self):
		return self.population.getFormatedModel()