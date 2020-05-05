using System;
using System.Linq;
using System.Threading;
using GeneticSharp.Domain;
using GeneticSharp.Domain.Chromosomes;
using GeneticSharp.Domain.Crossovers;
using GeneticSharp.Domain.Fitnesses;
using GeneticSharp.Domain.Mutations;
using GeneticSharp.Domain.Populations;
using GeneticSharp.Domain.Selections;
using GeneticSharp.Domain.Terminations;
using GeneticSharp.Infrastructure.Framework.Texts;
using GeneticSharp.Infrastructure.Framework.Threading;
using UnityEngine;

namespace GeometryFriends.WithGS
{
    public class GAController
    {
        private IFitness m_fitness;
        private const int MaxGenerations = 500;
        private const int MinPopulation = 20;
        private const int MaxPopulation = 20;
        
        private Thread m_gaThread;
        private double m_previousBestFitness;
        private double m_previousAverageFitness;
        private bool previewed = false;
        protected GeneticAlgorithm GA { get; private set; }
        protected bool ChromosomesCleanupEnabled { get; set; }

        private ReachabilityViewer _viewer;
        private System.Nullable<Double> previousbestfitness = 0;
        private FitnessStagnationTermination fs = new FitnessStagnationTermination(50);

        private int numberGenerations = 1;
        private int currentGenerations = 0;
        protected GeneticAlgorithm CreateGA()
        {
            //m_fitness = new OldReachHeuristic();
            m_fitness = new AreaHeuristic(TestSpecifications.LevelOne());
            var chromosome = new LevelChromosome();

            CrossoverBase crossover;
            //crossover = new OnePointCrossover();
            //crossover = new TwoPointCrossover();
            //crossover = new UniformCrossover();
            crossover = new ThreeParentCrossover();

            /** / // Crossover for ordered lists
            crossover = new AlternatingPositionCrossover();
            crossover = new CutAndSpliceCrossover() //Changes children lenght so NO!
            crossover = new CycleCrossover();
            crossover = new OrderBasedCrossover();
            crossover = new OrderedCrossover();
            crossover = new PartiallyMappedCrossover();
            crossover = new PositionBasedCrossover();
            crossover = new VotingRecombinationCrossover();
            /**/


            MutationBase mutation;
            //mutation = new DisplacementMutation();
            mutation = new FlipBitMutation();
            //mutation = new InsertionMutation();
            //mutation = new PartialShuffleMutation();
            //mutation = new ReverseSequenceMutation();
            //mutation = new TworsMutation();
            //mutation = new UniformMutation();

            
            SelectionBase selection;
            selection = new EliteSelection();
            //selection = new StochasticUniversalSamplingSelection();
            //selection = new TournamentSelection(4);
            //selection = new RouletteWheelSelection();
            
            
            var population = new Population(MinPopulation,MaxPopulation , chromosome)
            {
                GenerationStrategy = new PerformanceGenerationStrategy()
            };

            var ga = new GeneticAlgorithm(population, m_fitness, selection, crossover, mutation);
            ga.Termination = new OrTermination(new GenerationNumberTermination(MaxGenerations), 
                fs);
            
            ga.TaskExecutor = new ParallelTaskExecutor
            {
                MinThreads = population.MinSize,
                MaxThreads = population.MaxSize * 2
            };

            ga.MutationProbability = .3f;
            
            
            return ga;
        }

        public GAController()
        {
            Start();
        }
        
        private void Start()
        {
            var v = GameObject.Find("Visualizer");
            if (v != null)
            {
               _viewer = v.GetComponent<ReachabilityViewer>();
                
            }

            GA = CreateGA();
            GA.GenerationRan += delegate {
                m_previousBestFitness = GA.BestChromosome.Fitness.Value;
                m_previousAverageFitness = GA.Population.CurrentGeneration.Chromosomes.Average(c => c.Fitness.Value);
                Debug.Log($"Generation: {GA.GenerationsNumber} - Best: ${m_previousBestFitness} - Average: ${m_previousAverageFitness} - Time: ${GA.TimeEvolving}");
                if (ChromosomesCleanupEnabled)
                {
                    foreach (var c in GA.Population.CurrentGeneration.Chromosomes)
                    {
                        c.Fitness = null;
                    }
                }

                currentGenerations += 1;
                if (numberGenerations <= currentGenerations)
                {
                    GA.Stop();
                }

            };
            /**/
            m_gaThread = new Thread(() =>
            {
                try
                {
                    Thread.Sleep(1000);
                    GA.Start();
                }
                catch(Exception ex)
                {
                    Debug.LogError($"GA thread error: {ex.Message}");
                }
            });
            m_gaThread.Start();
            /**/
            //GA.Start();

        }


        public bool ShowNPopulation(int n)
        {
            var chromosomes = GA.Population.CurrentGeneration.Chromosomes;
            if (n >= 0 && n < chromosomes.Count)
            {
                var levelC = chromosomes[n] as LevelChromosome;
                _viewer.ViewBest( levelC);
                return true;
            }

            return false;
        }

        public void NextGen(int genNum = 1)
        {
            //GA.Termination = new OrTermination(new GenerationNumberTermination(GA.GenerationsNumber + 1),fs);
            numberGenerations = genNum;
            currentGenerations = 0;
            GA.Resume();
        }

    }
}