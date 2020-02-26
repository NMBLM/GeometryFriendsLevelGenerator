#if (!XNA)

namespace FarseerGames.FarseerPhysics.Mathematics
{
    public struct Vector3
    {
        public float X;
        public float Y;
        public float Z;

                /// <summary>
        /// Constructs a 3d vector with X, Y and Z from four values.
        /// </summary>
        /// <param name="x">The x coordinate in 4d-space.</param>
        /// <param name="y">The y coordinate in 4d-space.</param>
        /// <param name="z">The z coordinate in 4d-space.</param>
        public Vector3(float x, float y, float z)
        {
            this.X = x;
            this.Y = y;
            this.Z = z;
        }
    }
}
#endif