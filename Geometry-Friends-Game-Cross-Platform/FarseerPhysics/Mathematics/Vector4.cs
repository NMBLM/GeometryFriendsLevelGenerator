#if (!XNA)

namespace FarseerGames.FarseerPhysics.Mathematics
{
    public struct Vector4
    {
        public float X;
        public float Y;
        public float Z;
        public float W;

        /// <summary>
        /// Constructs a 3d vector with X, Y, Z and W from four values.
        /// </summary>
        /// <param name="x">The x coordinate in 4d-space.</param>
        /// <param name="y">The y coordinate in 4d-space.</param>
        /// <param name="z">The z coordinate in 4d-space.</param>
        /// <param name="w">The w coordinate in 4d-space.</param>
        public Vector4(float x, float y, float z, float w)
        {
            this.X = x;
            this.Y = y;
            this.Z = z;
            this.W = w;
        }
    }
}
#endif