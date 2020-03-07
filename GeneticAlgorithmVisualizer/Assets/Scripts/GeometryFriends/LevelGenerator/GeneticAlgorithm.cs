using System;
using System.Collections.Generic;

namespace GeometryFriends.LevelGenerator
{
    public class GeneticAlgorithm
    {
        public List<LevelDNA> population { get; private set; }
        public int generationNumber { get; private set; }
        public float bestFitness { get; private set; }

        public LevelDNA bestLevel;


		public float mutationRate;
		
		private List<LevelDNA> newPopulation;
		private Random random;
		private float fitnessSum;
		private Func<Gene> getRandomGene;
		private Func<int, float> fitnessFunction;
		
		
		public GeneticAlgorithm(int populationSize, Random random, Func<Gene> getRandomGene, Func<int, float> fitnessFunction, float mutationRate = 0.01f)
		{
			generationNumber = 1;
			this.mutationRate = mutationRate;
			population = new List<LevelDNA>(populationSize);
			newPopulation = new List<LevelDNA>(populationSize);
			this.random = random;
			this.getRandomGene = getRandomGene;
			this.fitnessFunction = fitnessFunction;
		
		
			for (int i = 0; i < populationSize; i++)
			{
				population.Add(new LevelDNA(random, getRandomGene, fitnessFunction, init: true));
			}
		}
		
		public void NewGeneration(int numNewDNA = 0)
		{		
			if (population.Count <= 0) {
				return;
			}
		
			if (population.Count > 0) {
				CalculateFitness();
				population.Sort(CompareDNA);
			}
			
			newPopulation.Clear();
		
			for (int i = 0; i < population.Count; i++)
			{
				if (i < population.Count)
				{
					LevelDNA parent1 = ChooseParent();
					LevelDNA parent2 = ChooseParent();
		
					LevelDNA child = parent1.Crossover(parent2);
		
					child.Mutation(mutationRate);
		
					newPopulation.Add(child);
				}
			}
		
			List<LevelDNA> tmpList = population;
			population = newPopulation;
			newPopulation = tmpList;
		
			generationNumber++;
		}
		
		private int CompareDNA(LevelDNA a, LevelDNA b)
		{
			if (a.fitness > b.fitness) {
				return -1;
			} else if (a.fitness < b.fitness) {
				return 1;
			} else {
				return 0;
			}
		}
		
		private void CalculateFitness()
		{
			fitnessSum = 0;
			LevelDNA best = population[0];
		
			for (int i = 0; i < population.Count; i++)
			{
				fitnessSum += population[i].CalculateFitness(i);
		
				if (population[i].fitness > best.fitness)
				{
					best = population[i];
				}
			}
		
			bestFitness = best.fitness;
			bestLevel = new LevelDNA(best);
		}
		
		private LevelDNA ChooseParent()
		{
			double randomNumber = random.NextDouble() * fitnessSum;
		
			for (int i = 0; i < population.Count; i++)
			{
				if (randomNumber < population[i].fitness)
				{
					return population[i];
				}
		
				randomNumber -= population[i].fitness;
			}
		
			return null;
		}

    }
}