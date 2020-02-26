using System;
using System.Collections.Generic;


#if (XNA)
using Microsoft.Xna.Framework; 
#endif


namespace FarseerGames.FarseerPhysics.Dynamics {
    public class AngleSpring : Controller {
        protected Body body1;
        protected Body body2;

        private float springConstant;
        private float dampningConstant;
        private float targetAngle;
        private float breakpoint = float.MaxValue;
        private float maxTorque = float.MaxValue;

        private float springError;

        public AngleSpring() {}

        public AngleSpring(Body body1, Body body2, float springConstant, float dampningConstant) {
            this.body1 = body1;
            this.body2 = body2;
            this.springConstant = springConstant;
            this.dampningConstant = dampningConstant;
            this.targetAngle = this.body2.TotalRotation - this.body1.TotalRotation;
        }

        public override Controller Clone(Dictionary<int, Body> oldToNewBodyMappings)
        {
            AngleSpring clone = new AngleSpring(
                oldToNewBodyMappings[body1.Id],
                oldToNewBodyMappings[body2.Id],
                springConstant,
                dampningConstant);

            clone.breakpoint = this.breakpoint;
            clone.maxTorque = this.maxTorque;
            clone.springError = this.springError;

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
                    System.Diagnostics.Debug.WriteLine("Cloning angle spring with non value-type tag. Not cloning the tag property.");
                }
            }
            clone.isEnabled = this.isEnabled;
            
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

        public float SpringConstant {
            get { return springConstant; }
            set { springConstant = value; }
        }

        public float DampningConstant {
            get { return dampningConstant; }
            set { dampningConstant = value; }
        }	

        //TODO: magic numbers
        public float TargetAngle {
            get { return targetAngle; }
            set {
                targetAngle = value;
                if (targetAngle > 5.5) { targetAngle = 5.5f; }
                if (targetAngle < -5.5f) { targetAngle = -5.5f; }
            }
        }

        public float Breakpoint {
            get { return breakpoint; }
            set { breakpoint = value; }
        }

        public float MaxTorque {
            get { return maxTorque; }
            set { maxTorque = value; }
        }

        public float SpringError {
            get { return springError; }
        }

        public override void Validate() {
            //if either of the springs connected bodies are disposed then dispose the joint.
            if (body1.IsDisposed || body2.IsDisposed) {
                Dispose();
            }
        }

        public override void Update(float dt) {
            if (Math.Abs(springError) > breakpoint) { Dispose(); } //check if joint is broken
            if (isDisposed) { return; }
            //calculate and apply spring force
            float angle = body2.totalRotation - body1.totalRotation;
            float angleDifference = body2.totalRotation - (body1.totalRotation + targetAngle);
            float springTorque = springConstant * angleDifference;
            springError = angleDifference; //keep track of 'springError' for breaking joint

            //apply torque at anchor
            if (!body1.IsStatic) {
                float torque1 = springTorque - dampningConstant * body1.angularVelocity;
                torque1 = Math.Min(Math.Abs(torque1), maxTorque) * Math.Sign(torque1);
                body1.ApplyTorque(torque1);
            }

            if (!body2.IsStatic) {
                float torque2 = -springTorque - dampningConstant * body2.angularVelocity;
                torque2 = Math.Min(Math.Abs(torque2), maxTorque) * Math.Sign(torque2);
                body2.ApplyTorque(torque2);
            }
        }
    }
}
