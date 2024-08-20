using UnityEngine;

namespace ScreenBoundaries
{
    public class FailureBoundaryCollider: MonoBehaviour
    {
        public BreakoutInstance bi;

        //Only this edgeCollider object needs to handle events on collision, as it's the out of bounds boundary
        private void OnCollisionEnter2D(Collision2D other)
        {
            Ball ball = other.gameObject.GetComponent<Ball>();
            if (ball != null)
            {
                bi.EndLife();
            }
        }
    
    }
}