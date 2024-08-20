using System.Collections.Generic;
using UnityEngine;
using FMODUnity;

namespace ScreenBoundaries
{
    public class UpperBoundariesCollider : MonoBehaviour
    {
        public BreakoutInstance bi;
        private EdgeCollider2D _edgeCollider;
        private LineRenderer _lineRenderer;
        private float _gameRoof;

        void Awake()
        {
            _edgeCollider = GetComponent<EdgeCollider2D>();
            _lineRenderer = GetComponent<LineRenderer>();
            SyncronizeEdgeColliderToLine();
        }

        void Start()
        {
            bi = transform.parent.parent.gameObject.GetComponent<BreakoutInstance>();
            _gameRoof = 8.8f;
        }

        private void SyncronizeEdgeColliderToLine()
        {
            Vector3[] positions = new Vector3[_lineRenderer.positionCount];
            _lineRenderer.GetPositions(positions);
            var positions2D = new List<Vector2>();
            for (var i = 0; i < positions.Length; i++)
            {
                positions2D.Add((Vector2) positions[i]);
            }
            _edgeCollider.SetPoints(positions2D);
        }
        
        private void OnCollisionEnter2D(Collision2D other)
            /*ball bounces off roof*/
        {
            if (other.gameObject.GetComponent<Ball>())
            { 
                //AudioManager.instance.PlayWallSound();
            }
            
            Ball ball = other.gameObject.GetComponent<Ball>();
            if (ball != null && ball.transform.position.y >= _gameRoof)
            {
                //does not know bi
                bi.set_roofBounceState(1);
            }
        }
    }
}
