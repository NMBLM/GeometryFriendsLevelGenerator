using FarseerGames.FarseerPhysics.Mathematics;
using System;
using System.Drawing;

namespace GeometryFriends.AI.Debug
{
    public struct DebugInformation
    {
        //shared
        /// <summary>
        /// The type of representation for the associated debug information.
        /// </summary>
        public RepresentationType Representation { get; set; }
        /// <summary>
        /// The position for visually depicting the associated debug information.
        /// </summary>
        public Vector2 Position { get; private set; }
        /// <summary>
        /// The color of the visual representation of the element.
        /// </summary>
        public GeometryFriends.XNAStub.Color Color { get; set; }

        //circle specific
        /// <summary>
        /// The radius for a circle debug information.
        /// </summary>
        public float Radius { get; private set; }

        //rectangle specific
        /// <summary>
        /// The dimensions for a rectangle debug information.
        /// </summary>
        public Size Size { get; private set; }

        //string specific
        /// <summary>
        /// The text to be drawn for a text debug information.
        /// </summary>
        public String Text { get; private set; }

        //line specific
        /// <summary>
        /// The end point of the line debug information.
        /// </summary>
        public Vector2 EndPoint { get; private set; }
        /// <summary>
        /// The start point of the line debug information.
        /// </summary>
        public Vector2 StartPoint { 
            get {
                return Position;
            } 
        }

        /// <summary>
        /// The possible types of debug information.
        /// </summary>
        public enum RepresentationType
        {
            CIRCLE,
            LINE,
            RECTANGLE,
            TEXT,
            CLEAR
        }

        /// <summary>
        /// Constructor for a a debug information representation.
        /// </summary>
        /// <param name="representation">The type of debug information to be represented.</param>
        /// <param name="position">The position of the debug information to be represented.</param>
        /// <param name="radius">The radius of a circle debug information type.</param>
        /// <param name="size">The width and height of a rectangle debug information type.</param>
        /// <param name="text">The text of a text debug information type.</param>
        /// <param name="endPoint">The end point of a line debug information type.</param>
        /// <param name="color">The color of the visual representation of this element.</param>
        internal DebugInformation(RepresentationType representation, Vector2 position, float radius, Size size, String text, Vector2 endPoint, GeometryFriends.XNAStub.Color color) : this()
        {
            this.Representation = representation;
            this.Position = position;
            this.Radius = radius;
            this.Size = size;
            this.Text = text;
            this.EndPoint = endPoint;
            this.Color = color;
        }
    }
}
