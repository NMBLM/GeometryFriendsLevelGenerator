using System;
using System.Collections.Generic;
using System.Linq;
using GeneticSharp.Domain.Chromosomes;
using GeneticSharp.Domain.Populations;
using GeneticSharp.Domain.Randomizations;
using GeneticSharp.Domain.Selections;

namespace GeometryFriends.WithGS
{
    public class UniqueStochasticSelection : SelectionBase
    {
        public UniqueStochasticSelection() : base(2)
        {
            
        }
        
        
        protected static IList<IChromosome> SelectFromWheel(int number, IList<IChromosome> chromosomes, IList<double> rouletteWheel, Func<double> getPointer)
        {
            var selected = new List<IChromosome>();
            var indexes = new List<int>();
            var uniqueSelected = new Dictionary<int,IChromosome>();
            for (int i = 0; i < number; i++)
            {
                var pointer = getPointer();

                var chromosome = rouletteWheel
                                        .Select((value, index) => new { Value = value, Index = index })
                                        .FirstOrDefault(r => r.Value >= pointer);

                if (chromosome != null)
                {
                    uniqueSelected[chromosome.Index] = chromosomes[chromosome.Index];
                }
            }

            foreach (var c in uniqueSelected)
            {
                selected.Add(c.Value);
                indexes.Add(c.Key);
            }
            
            for (int i = 0; i < number - uniqueSelected.Count; i++)
            {
                selected.Add(chromosomes[0].CreateNew());
            }
            InstrumentationManager.instance.WriteToRandom(indexes);
            return selected;
        }

        /// <summary>
        /// Calculates the cumulative percent.
        /// </summary>
        /// <param name="chromosomes">The chromosomes.</param>
        /// <param name="rouletteWheel">The roulette wheel.</param>
        protected static void CalculateCumulativePercentFitness(IList<IChromosome> chromosomes, IList<double> rouletteWheel)
        {
            var sumFitness = chromosomes.Sum(c => c.Fitness.Value);

            var cumulativePercent = 0.0;

            for (int i = 0; i < chromosomes.Count; i++)
            {
                cumulativePercent += chromosomes[i].Fitness.Value / sumFitness;
                rouletteWheel.Add(cumulativePercent);
            }
        }

        /// <summary>
        /// Performs the selection of chromosomes from the generation specified.
        /// </summary>
        /// <param name="number">The number of chromosomes to select.</param>
        /// <param name="generation">The generation where the selection will be made.</param>
        /// <returns>The select chromosomes.</returns>
        protected override IList<IChromosome> PerformSelectChromosomes(int number, Generation generation)
        {
            var chromosomes = generation.Chromosomes;
            var rouleteWheel = new List<double>();
            double stepSize = 1.0 / number;

            CalculateCumulativePercentFitness(chromosomes, rouleteWheel);

            var pointer = RandomizationProvider.Current.GetDouble();

            return SelectFromWheel(
                number,
                chromosomes,
                rouleteWheel,
                () =>
                {
                    if (pointer > 1.0)
                    {
                        pointer -= 1.0;
                    }

                    var currentPointer = pointer;
                    pointer += stepSize;

                    return currentPointer;
                });
        }
    }
}