using System;
using System.Linq;
using GeneticSharp.Domain.Crossovers;
using GeneticSharp.Domain.Mutations;
using GeneticSharp.Domain.Populations;
using GeneticSharp.Domain.Selections;
using GeneticSharp.Domain.Terminations;
using GeneticSharp.Infrastructure.Framework.Threading;
using GeometryFriends.LevelGenerator;
using UnityEngine;
using System.Threading;
using GeneticSharp.Domain;
using GeneticSharp.Domain.Fitnesses;
using GeneticAlgorithm = GeneticSharp.Domain.GeneticAlgorithm;

namespace GeometryFriends.WithGS
{
    public class SmallerLevelSampleController : MonoBehaviour
    {

        public IFitness m_fitness;
        private const int MaxGenerations = 1000;
        private const int MinPopulation = 100;
        private const int MaxPopulation = MinPopulation;
        
        private Thread m_gaThread;
        private double m_previousBestFitness;
        private double m_previousAverageFitness;
        private bool previewed = false;
        public GeneticAlgorithm GA { get; private set; }
        protected bool ChromosomesCleanupEnabled { get; set; }

        private ReachabilityViewer _viewer;
        private System.Nullable<Double> previousbestfitness = 0;
        private bool WriteToFile = true;
        
        protected GeneticAlgorithm CreateGA()
        {
            //m_fitness = new OldReachHeuristic();
            m_fitness = new AreaHeuristic(TestSpecifications.LevelTwo());
            var chromosome = new SmallerLevelChromosome();

            CrossoverBase crossover;
            crossover = new OnePointCrossover();
            //crossover = new TwoPointCrossover();
            //crossover = new UniformCrossover();
            //crossover = new ThreeParentCrossover();

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
            ////mutation = new DisplacementMutation();
            mutation = new FlipBitMutation();
            //mutation = new InsertionMutation();
            //mutation = new PartialShuffleMutation();
            //mutation = new ReverseSequenceMutation();
            //mutation = new TworsMutation();
            //mutation = new UniformMutation();

            
            SelectionBase selection;
            //selection = new EliteSelection();
            //selection = new StochasticUniversalSamplingSelection();
            selection = new UniqueStochasticSelection();
            //selection = new TournamentSelection(6);
            //selection = new RouletteWheelSelection();
            
            
            var population = new Population(MinPopulation,MaxPopulation , chromosome)
            {
                GenerationStrategy = new PerformanceGenerationStrategy()
            };

            var ga = new GeneticAlgorithm(population, m_fitness, selection, crossover, mutation);
            ga.Termination = new OrTermination(new GenerationNumberTermination(MaxGenerations), 
                new FitnessStagnationTermination(200));
            //ga.Termination = new GenerationNumberTermination(MaxGenerations);
            ga.TaskExecutor = new ParallelTaskExecutor
            {
                MinThreads = population.MinSize,
                MaxThreads = population.MaxSize * 2
            };

            ga.MutationProbability = .3f;
            //ga.CrossoverProbability = 1;
            
            ga.OperatorsStrategy = new TplOperatorsStrategy();
            if (WriteToFile)
            {
                InstrumentationManager.instance.WriteDescription(MaxPopulation,chromosome, crossover, mutation, selection, ga.Termination, m_fitness);
            }
            
            return ga;
        }
        
        private void Start()
        {
            Application.runInBackground = true;
            var v = GameObject.Find("Visualizer");
            if (v != null)
            {
               _viewer = v.GetComponent<ReachabilityViewer>();
                
            }

            GA = CreateGA();
            GA.GenerationRan += delegate {
                m_previousBestFitness = GA.BestChromosome.Fitness.Value;
                m_previousAverageFitness = GA.Population.CurrentGeneration.Chromosomes.Average(c => c.Fitness.Value);
                Debug.Log($"Generation: {GA.GenerationsNumber} - Best: ${m_previousBestFitness} - Average: ${m_previousAverageFitness} - Time: ${GA.TimeEvolving} - PopSize: ${GA.Population.CurrentGeneration.Chromosomes.Count}");
                if (true)
                {
                    foreach (var c in GA.Population.CurrentGeneration.Chromosomes)
                    {
                        c.Fitness = m_fitness.Evaluate(c);
                    }
                    //m_previousAverageFitness = GA.Population.CurrentGeneration.Chromosomes.Average(c => c.Fitness.Value);
                    //Debug.Log($"RecalculatedAverage: ${m_previousAverageFitness}");
                }

                if (WriteToFile)
                {
                    InstrumentationManager.instance.WriteGenData(GA.GenerationsNumber,GA.Population.CurrentGeneration.Chromosomes);
                }
            };
            
            
            /**/
            GA.TerminationReached += delegate
            {
                var best = GA.BestChromosome as SmallerLevelChromosome;
                m_previousBestFitness = GA.BestChromosome.Fitness.Value;
                m_previousAverageFitness = GA.Population.CurrentGeneration.Chromosomes.Average(c => c.Fitness.Value);
                Debug.Log($"Last Generation: {GA.GenerationsNumber} - Best: ${m_previousBestFitness} - Average: ${m_previousAverageFitness} - Time: ${GA.TimeEvolving} - PopSize: ${GA.Population.CurrentGeneration.Chromosomes.Count}");

            };
            /**/
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
            /** /
            GA.Start();
            /**/

        }
    
        void Update()
        {
            /**/
            if (GA.State == GeneticAlgorithmState.TerminationReached && !previewed)
            {
                previewed = true;
                var best = GA.BestChromosome as SmallerLevelChromosome;
                Debug.Log("Best Level: " + best.ToString() +"\n" + best.GetLevelDNA().Description());

                var v = GameObject.Find("Visualizer");
                if (v != null)
                {
                    var viewer = v.GetComponent<ReachabilityViewer>();
                    
                    viewer.ViewBest(best);
                }
                Debug.Log("Best fitness: " + best.Fitness);
            }
            /**/
            /** /
            if (GA.GenerationsNumber > 2 && GA.IsRunning && (previousbestfitness < GA.BestChromosome.Fitness))
            {
                previousbestfitness = GA.BestChromosome.Fitness;
                if (_viewer != null)
                {
                    _viewer.ViewBest(GA.BestChromosome as LevelChromosome);
                }
            }
            /**/
        }
    
        public bool ShowNPopulation(int n)
        {
            var chromosomes = GA.Population.CurrentGeneration.Chromosomes;
            if (n >= 0 && n < chromosomes.Count)
            {
                var levelC = chromosomes[n] as SmallerLevelChromosome;
                _viewer.ViewBest( levelC);
                return true;
            }

            return false;
        }
        
        private void OnDestroy()
        {
            GA.Stop();
            m_gaThread.Abort();
    
        }

        
    }
}