using System;
using System.Collections.Generic;


#if (XNA)
using Microsoft.Xna.Framework; 
#endif


namespace FarseerGames.FarseerPhysics.Dynamics {
    public class AngleJoint : Joint {
        protected Body body1;
        protected Body body2;

        private float biasFactor = .2f;
        private float targetAngle = 0f;
        private float softness = 0f;
        private float maxImpulse = float.MaxValue;
        private float breakpoint = float.MaxValue;

        private float massFactor;
        private float jointError;
        private float velocityBias;

        public AngleJoint() {}

        public AngleJoint(Body body1, Body body2) {
            this.body1 = body1;
            this.body2 = body2;
        }
        
        public AngleJoint(Body body1, Body body2, float targetAngle) {
            this.body1 = body1;
            this.body2 = body2;
            this.targetAngle = targetAngle;
        }

        public override Joint Clone(Dictionary<int, Body> oldToNewBodyMappings)
        {
            AngleJoint clone = new AngleJoint(
                oldToNewBodyMappings[body1.Id],
                oldToNewBodyMappings[body2.Id],
                targetAngle);

            clone.biasFactor = this.biasFactor;            
            clone.softness = this.softness;
            clone.maxImpulse = this.maxImpulse;
            clone.breakpoint = this.breakpoint;

            clone.massFactor = this.massFactor;
            clone.jointError = this.jointError;
            clone.velocityBias = this.velocityBias;

            //TODO: implement generic clone? -> for geometry friends purposes only value types are required
            if (this.Tag != null)
            {
                if (this.Tag.GetType() == typeof(String))
                {
                    //clone value also
                    clone.Tag = this.Tag;
                }
                else
                {
                    System.Diagnostics.Debug.WriteLine("Cloning angle joint with non value-type tag. Not cloning the tag property.");
                }
            }
            return clone;
        }

        public Body Body1 {
            get { return body1; }
            set { body1 = value; }
        }

        public Body Body2 {
            get { return body2; }
            set { body2 = value; }
        }

        public float BiasFactor {
            get { return biasFactor; }
            set { biasFactor = value; }
        }	

        public float TargetAngle {
            get { return targetAngle; }
            set { targetAngle = value; }
        }

        public float Softness {
            get { return softness; }
            set { softness = value; }
        }	

        public float MaxImpulse {
            get { return maxImpulse; }
            set { maxImpulse = value; }
        }

        public float  Breakpoint {
            get { return breakpoint; }
            set { breakpoint = value; }
        }

        public float JointError {
            get { return jointError; }
        }

        public override void Validate() {
            if (this.body1.IsDisposed || this.body2.IsDisposed) {
                Dispose();
            }
        }

        public override void PreStep(float inverseDt) {
            if (Math.Abs(jointError) > breakpoint) { Dispose(); } //check if joint is broken
            if (isDisposed) { return; }
            jointError = (body2.totalRotation - body1.totalRotation) - targetAngle;

            velocityBias = -biasFactor * inverseDt * jointError;

            massFactor = (1 - softness) / (body1.inverseMomentOfInertia + body2.inverseMomentOfInertia);
        }

        public override void Update() {
            if (isDisposed) { return; }
            float angularImpulse;
            angularImpulse = (velocityBias - body2.angularVelocity + body1.angularVelocity) * massFactor;

            body1.angularVelocity -= body1.inverseMomentOfInertia * Math.Sign(angularImpulse) * Math.Min(Math.Abs(angularImpulse), maxImpulse);
            body2.angularVelocity += body2.inverseMomentOfInertia * Math.Sign(angularImpulse) * Math.Min(Math.Abs(angularImpulse), maxImpulse);
        }
    }
}
