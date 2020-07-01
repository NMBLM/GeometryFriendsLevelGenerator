


using System;
using System.Collections;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using GeneticSharp.Domain.Chromosomes;
using GeometryFriends.LevelGenerator;

namespace GeometryFriends.WithGS
{
    public class LevelChromosome : BinaryChromosomeBase
    {
        public const int MAXCOLLECTIBLES = 5;
        public const int MAXPLATFORMS = 8;
        public const int SIZEOFSHORT = 16;
        public const int NUMBEROFBITS = SIZEOFSHORT * (2 + MAXCOLLECTIBLES + MAXPLATFORMS * 2) +
                                        SIZEOFSHORT * (2 + MAXCOLLECTIBLES + MAXPLATFORMS * 2) + (MAXCOLLECTIBLES + MAXPLATFORMS);

        public const int XMax = 1280;

        public const int YMax = 760;
        public const int XYMin = 40;
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
        //   16 * (2 + 5 + 8*2) + 16 * (2 + 5 + 8*2) + (5 + 8) = 749 bits
        
        
        public LevelChromosome() : base(NUMBEROFBITS)
        {
            CreateGenes();
            this.Fitness = null;
        }

        public LevelChromosome(String s) : base(NUMBEROFBITS)
        {
            CreateGenes();
            Gene[] genesToReplace = new Gene[NUMBEROFBITS];
            for (int i = 0; i < NUMBEROFBITS; i++)
            {
                if (i >= s.Length)
                {
                    genesToReplace[i] = new Gene(0);
                }
                if (s[i] == '0')
                {
                    genesToReplace[i] = new Gene(0);
                }

                if (s[i] == '1')
                {
                    genesToReplace[i] = new Gene(1);
                }
            }
            ReplaceGenes(0,genesToReplace);
            this.Fitness = null;
        }
        public override IChromosome CreateNew()
        {
            return new LevelChromosome();
        }

        private bool isTrue(string v)
        {
            return v == "1";
        }
        public LevelDNA GetLevelDNA()
        {
            var plats = new List<PlatformGeneT>();
            var coll = new List<CollectibleGeneT>();
            Point recSpawn;
            Point circSpawn;
            var genes = GetGenes().Select(g => isTrue(g.ToString())).ToArray();
            var bitArray = new BitArray(genes);
            
            recSpawn = new Point( ToShort(0,bitArray,XMax,XYMin),
                ToShort(SIZEOFSHORT,bitArray,YMax,XYMin));
            circSpawn = new Point( ToShort(SIZEOFSHORT*2,bitArray,XMax),
                ToShort(SIZEOFSHORT*3,bitArray,YMax));

            int collectiblesStart = SIZEOFSHORT * 4;
            int sizeOfCollectible = 1 + 2 * SIZEOFSHORT;
            for (int i = 0; i < MAXCOLLECTIBLES; i++)
            {
                int currentCollectibleStart = collectiblesStart + i * sizeOfCollectible;
                if (genes[currentCollectibleStart])
                {
                    int collX = ToShort(currentCollectibleStart + 1,bitArray,XMax,XYMin);
                    int collY = ToShort(currentCollectibleStart + 1 + SIZEOFSHORT ,bitArray,YMax,XYMin);
                    coll.Add(new CollectibleGeneT( new Point(collX,collY)));
                }
            }
            int platformsStart = SIZEOFSHORT * 4 + sizeOfCollectible * 5;
            int sizeOfPlatform = 1 + 4 * SIZEOFSHORT;
            for (int i = 0; i < MAXPLATFORMS; i++)
            {
                int currentPlatformStart = platformsStart + i * sizeOfPlatform;
                if (genes[currentPlatformStart])
                {
                    int platX = ToShort(currentPlatformStart + 1,bitArray,XMax,XYMin);
                    int platY = ToShort(currentPlatformStart + 1 + SIZEOFSHORT ,bitArray,YMax,XYMin);
                    int platW = ToShort(currentPlatformStart + 1 + SIZEOFSHORT * 2,bitArray,XMax);
                    int platH = ToShort(currentPlatformStart + 1 + SIZEOFSHORT * 3,bitArray,YMax);
                    plats.Add(new PlatformGeneT(platW, platH, new Point(platX,platY)));
                }
            }
            return new LevelDNA(plats, coll, recSpawn, circSpawn);
        }

        private ushort ToShort(int startIndex, BitArray bitArray, int max, int min = 0)
        {
            var array = new int[1];
            BitArray bits = new BitArray(SIZEOFSHORT);
            int j = SIZEOFSHORT-1;
            for (int i = startIndex; i < startIndex + SIZEOFSHORT; i++,j--)
            {
                bits[j] = bitArray[i];
            }
            bits.CopyTo(array, 0);
            int value = 0;
            Math.DivRem(array[0], max, out value);
            if (value < min)
            {
                return (ushort) min;
            }
            return (ushort) value;
        }
    }
}