using FarseerGames.FarseerPhysics.Mathematics;
using System;
using System.Drawing;

namespace GeometryFriends.AI.Debug
{
    public static class DebugInformationFactory
    {
        public static DebugInformation CreateCircleDebugInfo(PointF position, float radius, GeometryFriends.XNAStub.Color color)
        {
            return new DebugInformation(GeometryFriends.AI.Debug.DebugInformation.RepresentationType.CIRCLE, new Vector2(position.X, position.Y), radius, Size.Empty, "", Vector2.Zero, color);
        }

        public static DebugInformation CreateRectangleDebugInfo(PointF position, Size size, GeometryFriends.XNAStub.Color color)
        {
            return new DebugInformation(GeometryFriends.AI.Debug.DebugInformation.RepresentationType.RECTANGLE, new Vector2(position.X, position.Y), float.NaN, size, "", Vector2.Zero, color);
        }

        public static DebugInformation CreateLineDebugInfo(PointF startPoint, PointF endPoint, GeometryFriends.XNAStub.Color color)
        {
            return new DebugInformation(GeometryFriends.AI.Debug.DebugInformation.RepresentationType.LINE, new Vector2(startPoint.X, startPoint.Y), float.NaN, Size.Empty, "", new Vector2(endPoint.X, endPoint.Y), color);
        }

        public static DebugInformation CreateTextDebugInfo(PointF position, String text, GeometryFriends.XNAStub.Color color)
        {
            return new DebugInformation(GeometryFriends.AI.Debug.DebugInformation.RepresentationType.TEXT, new Vector2(position.X, position.Y), float.NaN, Size.Empty, text, Vector2.Zero, color);
        }

        public static DebugInformation CreateClearDebugInfo()
        {
            return new DebugInformation(GeometryFriends.AI.Debug.DebugInformation.RepresentationType.CLEAR, Vector2.Zero, float.NaN, Size.Empty, "", Vector2.Zero, GeometryFriends.XNAStub.Color.Transparent);
        }

    }
}
