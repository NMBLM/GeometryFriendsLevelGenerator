using System;
using System.Drawing;

namespace GeometryFriends.LevelGenerator
{
    //Playable Area: top left corner X=40 and Y=40  bottom right corner X=1240, Y=760
    //Max and Min Area: top left corner X=0 and Y=0  bottom right corner X=1280, Y=800
    
    public enum PlatformType : byte
    {
        Common,
        CirclePlatform,     //Is a platform that only blocks the Circle
        RectanglePlatform,  //Is a platform that only blocks the Rectangle
        CooperativeArea,
        CircleOnlyArea,
        RectangleOnlyArea,
        NotPlatform,
    }
    public class PlatformGeneT :GeneT
    {
        public int height, width;
        public Point position;
        public PlatformType platformType;

        //Random Constructor
        public PlatformGeneT(Random random)
        {
            type = GeneType.Platform;
            width = random.Next(1, 500);
            height = random.Next(1, 300);
            position = new Point(random.Next(40, 1240),random.Next(40, 760));
            platformType = PlatformType.Common;
        }

        //Copy Constructor
        public PlatformGeneT(PlatformGeneT other)
        {
            type = GeneType.Platform;
            height = other.height;
            width = other.width;
            position = other.position;
            platformType = other.platformType;
        }
        
        //Specific Constructor
        public PlatformGeneT(int height, int width, Point position, PlatformType platformType = PlatformType.Common)
        {
            type = GeneType.Platform;
            this.height = height;
            this.width = width;
            this.position = position;
            this.platformType = platformType;
        }


        public override string Description()
        {
            return "<obstacle x=" + position.X + " y=" + position.Y  + " height=" + height + " width=" + width + ">\n";
        }

        public override void Mutate(Random random)
        {
            height = random.Next(1, 1000);
            width = random.Next(1, 1000);
            position = new Point(random.Next(40, 1240),random.Next(40, 1240));
        }
    }
}