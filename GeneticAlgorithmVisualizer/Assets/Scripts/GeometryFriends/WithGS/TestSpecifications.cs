using System.Drawing;

namespace GeometryFriends.WithGS
{
    public class TestSpecifications
    {
        //This is a Specification to try and
        //generate the Level one in the GeneticAlgorithmTest World in Geometry Friends
        public static LevelSpecifications LevelOne()
        {
            var levelOne = new LevelSpecifications();
            
            levelOne.AddArea(360,500,new Point(740,360), AreaType.CircleOnly);
            levelOne.AddArea(180,500,new Point(80,540), AreaType.RectangleOnly);
            
            return levelOne;
        }
        
        public static LevelSpecifications LevelTwo()
        {
            var levelOne = new LevelSpecifications();
            
            levelOne.AddArea(240,1100,new Point(100,80), AreaType.Cooperative);
            levelOne.AddArea(180,340,new Point(430,560), AreaType.RectangleOnly);
            
            return levelOne;
        }
    }
}