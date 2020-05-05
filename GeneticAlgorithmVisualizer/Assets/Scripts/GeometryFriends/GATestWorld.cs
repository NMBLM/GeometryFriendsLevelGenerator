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
            List<PlatformGeneT> plats = new List<PlatformGeneT>();
            List<CollectibleGeneT> coll = new List<CollectibleGeneT>();
            
            Point recSpawn = new Point(120,680);
            Point circSpawn= new Point(744,664);
            
            plats.Add(new PlatformGeneT(720,48,new Point(616,40)));
            
            coll.Add(new CollectibleGeneT(new Point(1160,664)));
            coll.Add(new CollectibleGeneT(new Point(552,680)));
            
            return new LevelDNA(plats,coll,recSpawn,circSpawn);
        }
        
        public static LevelDNA LevelTwo()
        {
            List<PlatformGeneT> plats = new List<PlatformGeneT>();
            List<CollectibleGeneT> coll = new List<CollectibleGeneT>();
            
            Point recSpawn = new Point(1128,680);
            Point circSpawn= new Point(120,664);
            
            plats.Add(new PlatformGeneT(352,160,new Point(264,344)));
            plats.Add(new PlatformGeneT(352,160,new Point(776,344)));
            plats.Add(new PlatformGeneT(32,384,new Point(408,312)));
            
            coll.Add(new CollectibleGeneT(new Point(584,584)));
            coll.Add(new CollectibleGeneT(new Point(456,152)));
            coll.Add(new CollectibleGeneT(new Point(744,152)));
            
            return new LevelDNA(plats,coll,recSpawn,circSpawn);
        }

        public static LevelDNA LevelSpecificationOneTest()
        {
            List<PlatformGeneT> plats = new List<PlatformGeneT>();
            List<CollectibleGeneT> coll = new List<CollectibleGeneT>();
            
            Point recSpawn = new Point(120,680);
            Point circSpawn= new Point(744,664);
            
            plats.Add(new PlatformGeneT(360,500,new Point(740,360)));
            plats.Add(new PlatformGeneT(180,500,new Point(80,540)));
            
            coll.Add(new CollectibleGeneT(new Point(1160,664)));
            coll.Add(new CollectibleGeneT(new Point(552,680)));
            
            return new LevelDNA(plats,coll,recSpawn,circSpawn);
        }
        
        public static LevelDNA LevelTest()
        {
            List<PlatformGeneT> plats = new List<PlatformGeneT>();
            List<CollectibleGeneT> coll = new List<CollectibleGeneT>();
            
            Point recSpawn = new Point(465,410);
            Point circSpawn= new Point(720,244);
            
            plats.Add(new PlatformGeneT(724,288,new Point(963,737)));
            plats.Add(new PlatformGeneT(438,142,new Point(451,728)));
            plats.Add(new PlatformGeneT(303,661,new Point(689,40)));
            plats.Add(new PlatformGeneT(554,47,new Point(617,681)));
            plats.Add(new PlatformGeneT(667,696,new Point(1187,284)));
            
            coll.Add(new CollectibleGeneT(new Point(765,209)));
            
            return new LevelDNA(plats,coll,recSpawn,circSpawn);
        }
        
    }
}