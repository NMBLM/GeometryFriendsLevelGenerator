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
    }
}