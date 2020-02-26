using System;
using System.Collections.Generic;


#if (XNA)
using Microsoft.Xna.Framework; 
#endif


namespace FarseerGames.FarseerPhysics.Dynamics {
    public class FixedAngleJoint : Joint {
        protected Body body;

        private float biasFactor = .2f;
        private float targetAngle = 0;
        private float softness = 0f;
        private float maxImpulse = float.MaxValue;
        private float breakpoint = float.MaxValue;
  
        private float massFactor;
        private float jointError;
        private float velocityBias;

        public FixedAngleJoint() { }

        public FixedAngleJoint(Body body) {
            this.body = body;
        }

        public FixedAngleJoint(Body body, float targetAngle) {
            this.body = body;
            this.targetAngle = targetAngle;
        }

        public override Joint Clone(Dictionary<int, Body> oldToNewBodyMappings)
        {
            FixedAngleJoint clone = new FixedAngleJoint(
                oldToNewBodyMappings[body.Id],
                targetAngle);

            clone.biasFactor = this.biasFactor;
            clone.targetAngle = this.targetAngle;
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
                    System.Diagnostics.Debug.WriteLine("Cloning fixed angle joint with non value-type tag. Not cloning the tag property.");
                }
            }
            return clone;
        }

        public Body Body {
            get { return body; }
            set { body = value; }
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

        public float Breakpoint {
            get { return breakpoint; }
            set { breakpoint = value; }
        }

        public float JointError {
            get { return jointError; }
        }

        public override void Validate() {
            if (this.body.IsDisposed) {
                Dispose();
            }
        }

        public override void PreStep(float inverseDt) {
            if (Math.Abs(jointError) > breakpoint) { Dispose(); } //check if joint is broken
            if (isDisposed) { return; }
            jointError = body.totalRotation - targetAngle;

            velocityBias = -biasFactor * inverseDt * jointError;
            massFactor = (1 - softness) / (body.inverseMomentOfInertia);
        }

        public override void Update() {
            if (isDisposed) { return; }
            float angularImpulse;
            angularImpulse = (velocityBias - body.angularVelocity) * massFactor;
            body.angularVelocity += body.inverseMomentOfInertia * Math.Sign(angularImpulse) * Math.Min(Math.Abs(angularImpulse),maxImpulse);
        }
    }
}
