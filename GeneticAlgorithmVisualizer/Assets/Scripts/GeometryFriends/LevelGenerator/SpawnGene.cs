using System.Drawing;
using UnityEngine;
using Random = System.Random;

namespace GeometryFriends.LevelGenerator
{
    //Playable Area: top left corner X=40 and Y=40  bottom right corner X=1240, Y=760
    //Max and Min Area: top left corner X=0 and Y=0  bottom right corner X=1280, Y=800
    public class SpawnGene : Gene
    {
        public Point position;
        
        //Random Constructor
        public SpawnGene(Random random)
        {
            type = GeneType.Spawn;
            this.position = new Point(random.Next(40, 1140),random.Next(40, 660));
        }

        //Copy Constructor
        public SpawnGene(SpawnGene other)
        {
            type = GeneType.Spawn;
            this.position = other.position;

        }
        
        //Specific Constructor
        public SpawnGene(Point position)
        {
            type = GeneType.Spawn;
            this.position = position;
            
        }

        public override string Description()
        {
            return "x= " + position.X + " y=" + position.Y+"\n";
        }

        public override void Mutate(Random random)
        {
            this.position = new Point(random.Next(40, 1240),random.Next(40, 1240));
        }
    }
}