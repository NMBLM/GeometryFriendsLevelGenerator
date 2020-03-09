using System;
using System.Drawing;

namespace GeometryFriends.LevelGenerator
{
    //Playable Area: top left corner X=40 and Y=40  bottom right corner X=1240, Y=760
    //Max and Min Area: top left corner X=0 and Y=0  bottom right corner X=1280, Y=800
    
    
    public class PlatformGene :Gene
    {
        private int height, width;
        private Point position;
        private PlatformType platformType;

        //Random Constructor
        public PlatformGene(Random random)
        {
            type = GeneType.Platform;
            height = random.Next(1, 1000);
            width = random.Next(1, 1000);
            position = new Point(random.Next(40, 1240),random.Next(40, 1240));
            platformType = PlatformType.Common;
        }

        //Copy Constructor
        public PlatformGene(PlatformGene other)
        {
            type = GeneType.Platform;
            height = other.height;
            width = other.width;
            position = other.position;
            platformType = other.platformType;
        }
        
        //Specific Constructor
        public PlatformGene(int height, int width, Point position, PlatformType platformType = PlatformType.Common)
        {
            type = GeneType.Platform;
            this.height = height;
            this.width = width;
            this.position = position;
            this.platformType = platformType;
        }


        public override string Description()
        {
            return "<obstacle x=" + position.X + " y=" + position.Y + " width=" + width + " height=" + height+ ">\n";
        }

        public override void Mutate(Random random)
        {
            height = random.Next(1, 1000);
            width = random.Next(1, 1000);
            position = new Point(random.Next(40, 1240),random.Next(40, 1240));
        }
    }
}