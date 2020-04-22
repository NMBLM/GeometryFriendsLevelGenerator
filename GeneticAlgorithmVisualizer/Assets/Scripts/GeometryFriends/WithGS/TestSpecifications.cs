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
            
            levelOne.AddArea(500,360,new Point(740,360), AreaType.CircleOnly);
            levelOne.AddArea(500,360,new Point(80,360), AreaType.RectangleOnly);
            
            return levelOne;
        }
    }
}