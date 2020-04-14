using System.Collections.Generic;
using System.Drawing;

namespace GeometryFriends.WithGS
{
    public enum AreaType
    {
        Cooperative,
        Common,
        CircleOnly,
        RectangleOnly
    }
    public class LevelSpecifications
    {
        public struct SpecificArea
        {
            public Point position;
            public int width;
            public int height;
            public AreaType type;
        }
        
        
        public LevelSpecifications(List<SpecificArea> areas)
        {
            this.areas = areas;
        }
        
        public LevelSpecifications()
        {
            this.areas = new List<SpecificArea>();
        }
        
        public void AddArea(SpecificArea area)
        {
            this.areas.Add(area);
        }

        public void AddArea(int width, int height, Point position, AreaType type)
        {
            var area = new SpecificArea();
            area.width = width;
            area.height = height;
            area.position = area.position;
            area.type = type;
            this.areas.Add(area);
        }
        public List<SpecificArea> areas;
        
    }
}