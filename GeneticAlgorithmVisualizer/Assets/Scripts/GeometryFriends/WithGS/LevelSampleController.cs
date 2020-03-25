using GeneticSharp.Domain.Crossovers;
using GeneticSharp.Domain.Mutations;
using GeneticSharp.Domain.Populations;
using GeneticSharp.Domain.Selections;
using GeneticSharp.Domain.Terminations;
using GeneticSharp.Infrastructure.Framework.Threading;
using GeometryFriends.LevelGenerator;
using GeneticAlgorithm = GeneticSharp.Domain.GeneticAlgorithm;

namespace GeometryFriends.WithGS
{
    public class LevelSampleController 
    {
        private OldReachHeuristic m_fitness;
        private const int MaxGenerations = 100;
        
        protected GeneticAlgorithm CreateGA()
        {
            m_fitness = new OldReachHeuristic();
            var chromosome = new LevelChromosome();      
            var crossover = new UniformCrossover();
            var mutation = new FlipBitMutation();
            var selection = new EliteSelection();
            var population = new Population(10,10 , chromosome)
            {
                GenerationStrategy = new PerformanceGenerationStrategy()
            };

            var ga = new GeneticAlgorithm(population, m_fitness, selection, crossover, mutation);
            ga.Termination = new OrTermination(new GenerationNumberTermination(MaxGenerations), 
                new FitnessStagnationTermination(10));
            ga.TaskExecutor = new ParallelTaskExecutor
            {
                MinThreads = population.MinSize,
                MaxThreads = population.MaxSize * 2
            };
            ga.GenerationRan += delegate
            {
                
            };

            ga.MutationProbability = .1f;

            return ga;
        }
    }
}