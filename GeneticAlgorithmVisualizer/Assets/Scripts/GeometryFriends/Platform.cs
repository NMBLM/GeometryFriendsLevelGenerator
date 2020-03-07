namespace GeometryFriends
{
    public enum PlatformType : byte
    {
        Common,
        RectangleOnly,
        CircleOnly
    }
    
    
    public class Platform
    {
        private int height, width;
        private int x, y;
        private PlatformType type;

    }
}