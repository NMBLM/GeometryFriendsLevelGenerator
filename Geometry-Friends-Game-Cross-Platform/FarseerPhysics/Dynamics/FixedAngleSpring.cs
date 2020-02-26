using System;
using System.Collections.Generic;


#if (XNA)
using Microsoft.Xna.Framework; 
#endif


namespace FarseerGames.FarseerPhysics.Dynamics {
    public class FixedAngleSpring : Controller {
        protected Body body;

        private float springConstant;
        private float dampningConstant;
        private float targetAngle;
        private float breakpoint = float.MaxValue;
        private float maxTorque = float.MaxValue;

        private float springError;

        public FixedAngleSpring() { }

        public FixedAngleSpring(Body body, float springConstant, float dampningConstant) {
            this.body = body;
            this.springConstant = springConstant;
            this.dampningConstant = dampningConstant;
            this.targetAngle = body.TotalRotation;
        }

        public override Controller Clone(Dictionary<int, Body> oldToNewBodyMappings)
        {
            FixedAngleSpring clone = new FixedAngleSpring(
                oldToNewBodyMappings[body.Id],
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
                    System.Diagnostics.Debug.WriteLine("Cloning fixed angle spring with non value-type tag. Not cloning the tag property.");
                }
            }
            clone.isEnabled = this.isEnabled;

            return clone;
        }

        public Body Body {
            get { return body; }
            set { body = value; }
        }

        public float SpringConstant {
            get { return springConstant; }
            set { springConstant = value; }
        }

        public float DampningConstant {
            get { return dampningConstant; }
            set { dampningConstant = value; }
        }	

        public float TargetAngle {
            get { return targetAngle; }
            set {targetAngle = value; }
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
            //if body is disposed then dispose the joint.
            if (body.IsDisposed) {
                Dispose();
            }
        }

        public override void Update(float dt) {
            if (Math.Abs(springError) > breakpoint) { Dispose(); } //check if joint is broken
            if (isDisposed) { return; }
            //calculate and apply spring force
            float angleDifference = targetAngle-body.totalRotation ;
            float springTorque = springConstant * angleDifference;
            springError = angleDifference;

            //apply torque at anchor
            if (!body.IsStatic) {
                float torque1 = springTorque - dampningConstant * body.angularVelocity;
                torque1 = Math.Min(Math.Abs(torque1), maxTorque) * Math.Sign(torque1);
                body.ApplyTorque(torque1);
            }
        }
    }
}
