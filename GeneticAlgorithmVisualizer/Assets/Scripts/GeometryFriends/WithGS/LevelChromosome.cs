


using GeneticSharp.Domain.Chromosomes;

namespace GeometryFriends.WithGS
{
    public class LevelChromosome : BinaryChromosomeBase
    {
        public const int MAXCOLLECTIBLES = 5;
        public const int MAXPLATFORMS = 8;

        public const int NUMBEROFBITS = 8 * (2 + MAXCOLLECTIBLES + MAXPLATFORMS * 2) +
                                        8 * (2 + MAXCOLLECTIBLES + MAXPLATFORMS * 2) + (MAXCOLLECTIBLES + MAXPLATFORMS);
        // [ RectangleSpawn | CircleSpawn | CollectibleArray | PlatformArray ]
        // [ Pos            | Pos         | Collectible x5   | Platform x8   ]
        // Pos = [ x | y ]
        // Collectible =[ On/Off | Pos ] => [ bit | x | y ]
        // Platform = [ On/Off | Pos | Pos ] => [ bit | x | y | x | y ]
        // First Pos is the position second is Width and Height
        // x and y are ushort because max value will be 1280 which a byte is not enough to represent and int are too big.
        // [ x | y | x | y |
        //   1 | x | y | 1 | x | y | 1 | x | y | 1 | x | y | 1 | x | y |
        //   1 | x | y | x | y | 1 | x | y | x | y | 1 | x | y | x | y | 1 | x | y | x | y | 1 | x | y | x | y |
        //   1 | x | y | x | y | 1 | x | y | x | y | 1 | x | y | x | y ]
        //   x * (2 + 5 + 8*2) + y * (2 + 5 + 8*2) + 1 * (5 + 8)
        //   8 * (2 + 5 + 8*2) + 8 * (2 + 5 + 8*2) + (5 + 8) = 381 bits
        
        
        public LevelChromosome() : base(NUMBEROFBITS)
        {
            CreateGenes();
        }

        public override IChromosome CreateNew()
        {
            return new LevelChromosome();
        }
    }
}