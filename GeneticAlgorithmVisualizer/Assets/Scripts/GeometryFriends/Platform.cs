namespace GeometryFriends
{
    public enum PlatformType : byte
    {
        Common,
        CirclePlatform,     //Is a platform that only blocks the Circle
        RectanglePlatform,  //Is a platform that only blocks the Rectangle
        CooperativeArea,
        CircleOnlyArea,
        RectangleOnlyArea,
    }
    
    
    public class Platform
    {
        private int height, width;
        private int x, y;
        private PlatformType type;

    }
}