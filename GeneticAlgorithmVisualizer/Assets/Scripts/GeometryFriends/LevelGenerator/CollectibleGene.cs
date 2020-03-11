using System;
using System.Drawing;

namespace GeometryFriends.LevelGenerator
{
    
    //Playable Area: top left corner X=40 and Y=40  bottom right corner X=1240, Y=760
    //Max and Min Area: top left corner X=0 and Y=0  bottom right corner X=1280, Y=800
    
    
    public class CollectibleGene : Gene
    {
        public Point position;
        
        //Random Constructor
        public CollectibleGene(Random random)
        {
            type = GeneType.Collectible;
            position = new Point(random.Next(40, 1240),random.Next(40, 760));
        }

        //Copy Constructor
        public CollectibleGene(CollectibleGene other)
        {
            type = GeneType.Collectible;
            position = other.position;

        }
        
        //Specific Constructor
        public CollectibleGene( Point position)
        {
            type = GeneType.Collectible;
            this.position = position;
            
        }
        
        public override string Description()
        {
            return "<collectible x= " + position.X + " y=" + position.Y+">\n";
        }

        public override void Mutate(Random random )
        {
            position = new Point(random.Next(40, 1240),random.Next(40, 1240));
        }
    }
}