using System.Collections.Generic;
using System.Drawing;
using GeometryFriends.LevelGenerator;

namespace GeometryFriends
{
    public class GATestWorld
    {
        //This is the LevelDNA for the level one in
        //the GeneticAlgorithmTest World in Geometry Friends
        public static LevelDNA LevelOne()
        {
            List<PlatformGene> plats = new List<PlatformGene>();
            List<CollectibleGene> coll = new List<CollectibleGene>();
            
            Point recSpawn = new Point(120,680);
            Point circSpawn= new Point(744,664);
            
            plats.Add(new PlatformGene(720,48,new Point(616,40)));
            
            coll.Add(new CollectibleGene(new Point(1160,664)));
            coll.Add(new CollectibleGene(new Point(552,680)));
            
            return new LevelDNA(plats,coll,recSpawn,circSpawn);
        }
        
        public static LevelDNA LevelTwo()
        {
            List<PlatformGene> plats = new List<PlatformGene>();
            List<CollectibleGene> coll = new List<CollectibleGene>();
            
            Point recSpawn = new Point(1128,680);
            Point circSpawn= new Point(120,664);
            
            plats.Add(new PlatformGene(352,160,new Point(264,344)));
            plats.Add(new PlatformGene(352,160,new Point(776,344)));
            plats.Add(new PlatformGene(32,384,new Point(408,312)));
            
            coll.Add(new CollectibleGene(new Point(584,584)));
            coll.Add(new CollectibleGene(new Point(456,152)));
            coll.Add(new CollectibleGene(new Point(744,152)));
            
            return new LevelDNA(plats,coll,recSpawn,circSpawn);
        }

        public static LevelDNA LevelTest()
        {
            List<PlatformGene> plats = new List<PlatformGene>();
            List<CollectibleGene> coll = new List<CollectibleGene>();
            
            Point recSpawn = new Point(120,680);
            Point circSpawn= new Point(744,664);
            
            plats.Add(new PlatformGene(360,500,new Point(700,360)));
            plats.Add(new PlatformGene(360,500,new Point(40,360)));
            
            coll.Add(new CollectibleGene(new Point(1160,664)));
            coll.Add(new CollectibleGene(new Point(552,680)));
            
            return new LevelDNA(plats,coll,recSpawn,circSpawn);
        }
    }
}