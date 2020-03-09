using System;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using Random = System.Random;

namespace GeometryFriends.LevelGenerator
{
    public class LevelDNA
    {
        public List<PlatformGene> platforms; 
        public List<CollectibleGene> collectibles; 
        public SpawnGene rectangleSpawn, circleSpawn; //These are necessary for every level but can still be randomized
        public float fitness;
        
        private Random random;
        private Func<int, float> fitnessFunction;


        public LevelDNA(Random random, Func<int, float> fitnessFunction, bool init = true)
        {
            this.platforms = new List<PlatformGene>();
            this.collectibles = new List<CollectibleGene>();
            this.fitness = -1;
            this.random = random;
            this.fitnessFunction = fitnessFunction;
            if(init) InitGenes();
            
        }

        public LevelDNA(LevelDNA other)
        {
            this.fitness = other.fitness;
            this.random = other.random;
            this.fitnessFunction = other.fitnessFunction;
            this.platforms = other.platforms.ToList();
            this.collectibles = other.collectibles.ToList();
            this.rectangleSpawn = new SpawnGene(other.rectangleSpawn);
            this.circleSpawn = new SpawnGene(other.circleSpawn);
            Debug.Log(this.rectangleSpawn.Description());
        }
        
        private void InitGenes()
        {
            int num_plat = random.Next(1, 8);
            int num_collectible = random.Next(1, 3);
            
            
            for (int i = 0; i < num_plat; i++)
            {
                platforms.Add(new PlatformGene(random));
            }
            for (int i = 0; i < num_collectible; i++)
            {
                collectibles.Add(new CollectibleGene(random));
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
            LevelDNA child = new LevelDNA(random,fitnessFunction,false);

            int minPlatNum = (platforms.Count < otherParent.platforms.Count) ? platforms.Count : otherParent.platforms.Count;
            List<PlatformGene> largestPlatNum = (platforms.Count > otherParent.platforms.Count) ? platforms : otherParent.platforms;
            
            int minCollNum = (collectibles.Count < otherParent.collectibles.Count) ? collectibles.Count : otherParent.collectibles.Count;
            List<CollectibleGene> largestCollNum = (collectibles.Count > otherParent.collectibles.Count) ? collectibles : otherParent.collectibles;
            
            for (int i = 0; i < minPlatNum; i++)
            {
                child.platforms.Add(random.NextDouble() < 0.5 ? platforms[i] : otherParent.platforms[i]);
            }

            for (int i = 0; i < minCollNum; i++)
            {
                child.collectibles.Add(random.NextDouble() < 0.5 ? collectibles[i] : otherParent.collectibles[i]);
            }

            if (random.NextDouble() < 0.5)
            {
                for (int i = minPlatNum; i < largestPlatNum.Count; i++)
                {
                    child.platforms.Add(largestPlatNum[i]);
                }
            }
            if (random.NextDouble() < 0.5)
            {
                for (int i = minCollNum; i < largestCollNum.Count; i++)
                {
                    child.collectibles.Add(largestCollNum[i]);
                }
            }

            if (random.NextDouble() < 0.5)
            {
                child.rectangleSpawn = this.rectangleSpawn;
                child.circleSpawn = this.circleSpawn;
            }
            else
            {
                child.rectangleSpawn = otherParent.rectangleSpawn;
                child.circleSpawn = otherParent.circleSpawn;
            }

            return child;
        }


        public void Mutation(float mutationRate)
        {

            foreach (var g in platforms)
            {
                if (random.NextDouble() < mutationRate)
                {
                    g.Mutate(random);
                }
                
            }
            foreach (var g in collectibles)
            {
                if (random.NextDouble() < mutationRate)
                {
                    g.Mutate(random);
                }
            }
            
        }


        public string Description()
        {
            string text = "";

            
            foreach (var g in platforms)
            {
                text += g.Description();
            }
            foreach (var g in collectibles)
            {
                text += g.Description();
            }
            text += "circle spawn " + circleSpawn.Description();
            text += "rectangle spawn " + rectangleSpawn.Description();

            return text;
        }
    }
}