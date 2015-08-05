#!/usr/bin/env python3
import random

class GA(object):
	"""docstring for GA"""
	def __init__(self, population, fitness, randomSelection, reproduce, mutationProb, mutate):
		self.population = population
		self.fitness = fitness
		self.randomSelection = randomSelection
		self.reproduce = reproduce
		self.mutationProb = mutationProb
		self.mutate = mutate
	def run(self, generations):
		for g in range(generations):
			newPopulation = []
			for i in range(len(self.population)):
				x = self.randomSelection(self.population, self.fitness)
				y = self.randomSelection(self.population, self.fitness)
				child = self.reproduce(x, y)
				if random.random() < self.mutationProb:
					child = self.mutate(child)
				newPopulation.append(child)
			self.population = newPopulation
	def generator(self, stepsize=1):
		while True:
			self.run(stepsize)
			yield self.population