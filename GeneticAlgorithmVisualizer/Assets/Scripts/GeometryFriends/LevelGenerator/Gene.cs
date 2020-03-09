using System;

namespace GeometryFriends.LevelGenerator
{
    public enum GeneType : byte
    {
        Platform,
        Spawn,
        Collectible
    }
    public abstract class Gene
    {
        protected GeneType type;


        public abstract string Description();
        
        public abstract void Mutate(Random random);

    }
    
    
    
}