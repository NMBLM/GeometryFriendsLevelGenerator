using System;
using System.Collections.Generic;
using System.Linq;

namespace GeometryFriends.LevelGenerator
{
    public class LevelDNA
    {
        public List<Gene> genes;
        public SpawnGene rectangleSpawn, circleSpawn; //These are necessary for every level but can still be randomized
        public float fitness;
        
        private Random random;
        private Func<Gene> getRandomGene;
        private Func<int, float> fitnessFunction;


        public LevelDNA(Random random, Func<Gene> randomGene, Func<int, float> fitnessFunction, bool init = true)
        {
            this.fitness = -1;
            this.random = random;
            this.getRandomGene = randomGene;
            this.fitnessFunction = fitnessFunction;
            if(init) InitGenes();
        }

        public LevelDNA(LevelDNA other)
        {
            this.fitness = other.fitness;
            this.random = other.random;
            this.getRandomGene = other.getRandomGene;
            this.fitnessFunction = other.fitnessFunction;
            this.genes = other.genes.ToList();
        }
        
        private void InitGenes()
        {
            int num_plat = random.Next(1, 8);
            int num_collectible = random.Next(1, 3);
            
            /*
            for (int i = 0; i < num_plat; i++)
            {
                genes.Add(new PlatformGene(random));
            }
            for (int i = 0; i < num_collectible; i++)
            {
                genes.Add(new CollectibleGene(random));
            }
            */
            
            // So that the order in which the genes are positioned is random
            while (num_plat + num_collectible > 0)
            {
                if (random.NextDouble() < 0.5)
                {
                    if (num_plat > 0)
                    {
                        num_plat -= 1;
                        genes.Add(new PlatformGene(random));
                        continue;
                    }
                }
                
                if (num_collectible > 0)
                {
                    num_collectible -= 1;
                    genes.Add(new CollectibleGene(random));
                }
                
            }
            
            
            rectangleSpawn = new SpawnGene(random);
            circleSpawn = new SpawnGene(random);
        }

        public float CalculateFitness(int index)
        {
            fitness = fitnessFunction(index);
            return fitness;
        }


        public LevelDNA Crossover(LevelDNA otherParent)
        {
            LevelDNA child = new LevelDNA(random,getRandomGene,fitnessFunction,false);

            int len = (genes.Count < otherParent.genes.Count) ? genes.Count : otherParent.genes.Count;
            List<Gene> biggestlen = (genes.Count > otherParent.genes.Count) ? genes : otherParent.genes;
            for (int i = 0; i < len; i++)
            {
                child.genes.Add(random.NextDouble() < 0.5 ? genes[i] : otherParent.genes[i]);
            }

            if (random.NextDouble() < 0.5)
            {
                for (int i = len; i < biggestlen.Count; i++)
                {
                    child.genes.Add(biggestlen[i]);
                }
            }
            
            return child;
        }


        public void Mutation(float mutationRate)
        {
        
            for (int i = 0; i < genes.Count; i++)
            {
                if (random.NextDouble() < mutationRate)
                {
                    genes[i] = getRandomGene();
                }
            }
            
        }
    }
}