using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using GeneticSharp.Domain.Chromosomes;
using GeometryFriends.WithGS;
using Random = System.Random;

namespace GeometryFriends.LevelGenerator
{
    public class LevelDNA
    {
        public List<PlatformGeneT> platforms; 
        public List<CollectibleGeneT> collectibles; 
        public SpawnGeneT rectangleSpawn, circleSpawn; //These are necessary for every level but can still be randomized
        public float fitness;
        
        private Random random;
        private Func<int, float> fitnessFunction;


        public LevelDNA(Random random, Func<int, float> fitnessFunction, bool init = true)
        {
            this.platforms = new List<PlatformGeneT>();
            this.collectibles = new List<CollectibleGeneT>();
            this.fitness = -1;
            this.random = random;
            this.fitnessFunction = fitnessFunction;
            if (init)
            {
                InitGenes();
            }
            else
            {
                rectangleSpawn = new SpawnGeneT(random);
                circleSpawn = new SpawnGeneT(random);
                this.collectibles.Add(new CollectibleGeneT(random));
            }
            
        }
        
        public LevelDNA(LevelDNA other)
        {
            this.fitness = other.fitness;
            this.random = other.random;
            this.fitnessFunction = other.fitnessFunction;
            this.platforms = other.platforms.ToList();
            this.collectibles = other.collectibles.ToList();
            this.rectangleSpawn = new SpawnGeneT(other.rectangleSpawn);
            this.circleSpawn = new SpawnGeneT(other.circleSpawn);
        }
        public LevelDNA(List<PlatformGeneT> plats,List<CollectibleGeneT> coll, Point recSpawn, Point circSpawn)
        {
            this.fitness = 0;
            this.random = null;
            this.fitnessFunction = null;
            this.platforms = plats;
            this.collectibles = coll;
            this.rectangleSpawn = new SpawnGeneT(recSpawn);
            this.circleSpawn = new SpawnGeneT(circSpawn);
        }

        public LevelDNA(int[] attrList)
        {
            this.rectangleSpawn = new SpawnGeneT(new Point(attrList[1],attrList[2]));
            this.circleSpawn = new SpawnGeneT(new Point(attrList[3],attrList[4]));
            this.platforms = new List<PlatformGeneT>();
            for (int i = 5; i < 45; i+=5)
            {
                if (attrList[i] % 2 == 1)
                {
                    this.platforms.Add(new PlatformGeneT(attrList[i+4],attrList[i+3],new Point(attrList[i+1],(int) (attrList[i+2] * 720 / 1280))));
                }
            }
            this.collectibles = new List<CollectibleGeneT>();
            this.fitness = -1;
        }
        
        private void InitGenes()
        {
            int num_plat = random.Next(1, 8);
            int num_collectible = random.Next(1, 3);
            
            
            for (int i = 0; i < num_plat; i++)
            {
                platforms.Add(new PlatformGeneT(random));
            }
            for (int i = 0; i < num_collectible; i++)
            {
                collectibles.Add(new CollectibleGeneT(random));
            }

            rectangleSpawn = new SpawnGeneT(random);
            circleSpawn = new SpawnGeneT(random);
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
            List<PlatformGeneT> largestPlatNum = (platforms.Count > otherParent.platforms.Count) ? platforms : otherParent.platforms;
            
            int minCollNum = (collectibles.Count < otherParent.collectibles.Count) ? collectibles.Count : otherParent.collectibles.Count;
            List<CollectibleGeneT> largestCollNum = (collectibles.Count > otherParent.collectibles.Count) ? collectibles : otherParent.collectibles;
            
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
            text += "rectangle spawn " + rectangleSpawn.Description();
            text += "circle spawn " + circleSpawn.Description();
            
            foreach (var g in collectibles)
            {
                text += g.Description();
            }
            foreach (var g in platforms)
            {
                text += g.Description();
            }
            
            

            return text;
        }

        public LevelChromosome DNAToChromosome()
        {
            void InsertPosition(Gene[] genes, int index, Point position)
            {
                var x = 0;
                var y = 0;
                var xBinary = Convert.ToString(x, 2);
                var yBinary = Convert.ToString(y, 2);
                //Rectangle Spawn
                x = position.X;
                y = position.Y;
                xBinary = Convert.ToString(x, 2);
                yBinary = Convert.ToString(y, 2);
                for (int i = 0; i < 16 - xBinary.Length ; i++)
                {
                    genes[index] = new Gene(0);
                    index++;
                }
                for (int i = 0; i < xBinary.Length; i++)
                {
                    genes[index] = new Gene( xBinary[i]);
                    index++;
                }
                for (int i = 0; i < 16 - yBinary.Length ; i++)
                {
                    genes[index] = new Gene(0);
                    index++;
                }
                for (int i = 0; i < yBinary.Length; i++)
                {
                    genes[index] = new Gene(yBinary[i]);
                    index++;
                }
            }
            Gene[] genesToReplace = new Gene[749];
            LevelChromosome lvl = new LevelChromosome();
            var currentGene = 0;
            //Rectangle Spawn
            InsertPosition(genesToReplace, currentGene, rectangleSpawn.position);
            currentGene += 16*2;
            //Circle Spawn
            InsertPosition(genesToReplace, currentGene, circleSpawn.position);
            currentGene += 16*2;
            //Collectibles
            var colNum = 0;
            foreach (var col in collectibles)
            {
                if (colNum >= 5) break; //max 5 collectibles
                genesToReplace[currentGene] = new Gene(1);
                currentGene++;
                InsertPosition(genesToReplace, currentGene, col.position);
                currentGene += 16*2;
                colNum++;
            }

            for (; colNum < 5; colNum++)
            {
                genesToReplace[currentGene] = new Gene(0);
                currentGene++;
                InsertPosition(genesToReplace, currentGene, Point.Empty);
                currentGene += 16*2;
            }
            //Platforms
            var platNum = 0;
            foreach (var plat in platforms)
            {
                if (platNum >= 8) break; //max 8 collectibles
                genesToReplace[currentGene] = new Gene(1);
                currentGene++;
                InsertPosition(genesToReplace, currentGene, plat.position);
                currentGene += 16*2;
                InsertPosition(genesToReplace, currentGene, new Point(plat.height,plat.width));
                currentGene += 16*2;
                platNum++;
            }

            for (; platNum < 8; platNum++)
            {
                genesToReplace[currentGene] = new Gene(0);
                currentGene++;
                InsertPosition(genesToReplace, currentGene, Point.Empty);
                currentGene += 16*2;
                InsertPosition(genesToReplace, currentGene, Point.Empty);
                currentGene += 16*2;
            }
            lvl.ReplaceGenes(0, genesToReplace);
            return lvl;
        }
        public SmallerLevelChromosome DNAToSmallChromosome()
        {
            void InsertPosition(Gene[] genes, int index, Point position)
            {
                var x = 0;
                var y = 0;
                var xBinary = Convert.ToString(x, 2);
                var yBinary = Convert.ToString(y, 2);
                //Rectangle Spawn
                x = position.X;
                y = position.Y;
                xBinary = Convert.ToString(x, 2);
                yBinary = Convert.ToString(y, 2);
                for (int i = 0; i < 16 - xBinary.Length ; i++)
                {
                    genes[index] = new Gene(0);
                    index++;
                }
                for (int i = 0; i < xBinary.Length; i++)
                {
                    genes[index] = new Gene( xBinary[i]);
                    index++;
                }
                for (int i = 0; i < 16 - yBinary.Length ; i++)
                {
                    genes[index] = new Gene(0);
                    index++;
                }
                for (int i = 0; i < yBinary.Length; i++)
                {
                    genes[index] = new Gene(yBinary[i]);
                    index++;
                }
            }
            Gene[] genesToReplace = new Gene[584];
            SmallerLevelChromosome lvl = new SmallerLevelChromosome();
            var currentGene = 0;
            //Rectangle Spawn
            InsertPosition(genesToReplace, currentGene, rectangleSpawn.position);
            currentGene += 16*2;
            //Circle Spawn
            InsertPosition(genesToReplace, currentGene, circleSpawn.position);
            currentGene += 16*2;
            //Platforms
            var platNum = 0;
            foreach (var plat in platforms)
            {
                if (platNum >= 8) break; //max 8 collectibles
                genesToReplace[currentGene] = new Gene(1);
                currentGene++;
                InsertPosition(genesToReplace, currentGene, plat.position);
                currentGene += 16*2;
                InsertPosition(genesToReplace, currentGene, new Point(plat.height,plat.width));
                currentGene += 16*2;
                platNum++;
            }

            for (; platNum < 8; platNum++)
            {
                genesToReplace[currentGene] = new Gene(0);
                currentGene++;
                InsertPosition(genesToReplace, currentGene, Point.Empty);
                currentGene += 16*2;
                InsertPosition(genesToReplace, currentGene, Point.Empty);
                currentGene += 16*2;
            }
            lvl.ReplaceGenes(0, genesToReplace);
            return lvl;
        }
    }
}