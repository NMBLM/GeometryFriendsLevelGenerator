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
            
            levelOne.AddArea(500,360,new Point(700,360), AreaType.RectangleOnly);
            levelOne.AddArea(500,360,new Point(40,360), AreaType.CircleOnly);
            
            return levelOne;
        }
    }
}