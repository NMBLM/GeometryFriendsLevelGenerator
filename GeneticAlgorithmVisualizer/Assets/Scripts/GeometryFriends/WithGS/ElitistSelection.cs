using System.Collections.Generic;
using System.Linq;
using GeneticSharp.Domain.Chromosomes;
using GeneticSharp.Domain.Populations;
using GeneticSharp.Domain.Selections;

namespace GeometryFriends.WithGS
{
    public class ElitistSelection : SelectionBase
    {
        private int amountToKeep;
        
        #region Constructors
        /// <summary>
        /// Initializes a new instance of the <see cref="GeneticSharp.Domain.Selections.EliteSelection"/> class.
        /// </summary>
        public ElitistSelection(int number) : base(2)
        {
            amountToKeep = number;
        }
        #endregion

        #region ISelection implementation
        /// <summary>
        /// Performs the selection of chromosomes from the generation specified.
        /// </summary>
        /// <param name="number">The number of chromosomes to select.</param>
        /// <param name="generation">The generation where the selection will be made.</param>
        /// <returns>The select chromosomes.</returns>
        protected override IList<IChromosome> PerformSelectChromosomes(int number, Generation generation)
        {                
            var ordered = generation.Chromosomes.OrderByDescending(c => c.Fitness);
            if (amountToKeep <= number)
            {
                return ordered.Take(amountToKeep).ToList(); 
            }
            return ordered.Take(number).ToList();
        }

        #endregion
    }
}