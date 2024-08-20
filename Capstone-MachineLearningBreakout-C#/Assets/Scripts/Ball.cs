using System;
using System.Collections;
using System.Collections.Generic;
using System.Numerics;
using Unity.VisualScripting;
using UnityEngine;
using UnityEngine.Serialization;
using Vector2 = UnityEngine.Vector2;
using Vector3 = UnityEngine.Vector3;

public class Ball : MonoBehaviour
{
    //import BreakoutInstance
    public BreakoutInstance bi;
    public Rigidbody2D ballRb;
    private float ballBaseSpeed = 4.2f;
    private float ballSpeedBoost = 1.45f;
    private int ballSpeedTier = 1; // 1 base, 5 is highest
    private GameObject _paddleAI;
    private bool _agentGame;
    private bool transmitToAgent = true; // For updating AI on landing characteristics.
    private float horizontalOverride = .5f;
    
    private Vector3 _velocityBackup = new Vector3(0,0,0);
    
    //Testing Parameters
    public bool testing;
    public float testingAngle;
    public int test = 0;
    
    //Cache components
    private PlayGameAgent _cachePlayGameAgentScript;

    // public void OnEnable()
    // {
    //     GameManager.FreezeBreakouts += freeze;
    //     GameManager.ThawBreakouts += unfreeze; 
    // }
    //
    // public void OnDisable()
    // {
    //     GameManager.FreezeBreakouts -= freeze;
    //     GameManager.ThawBreakouts -= freeze;
    // }

    public void Awake()
    {
        bi = transform.parent.gameObject.GetComponent<BreakoutInstance>();
        _agentGame = bi.get_agentGame();
        if (_agentGame) 
        { 
            _paddleAI = bi.GetPaddle(); 
            _cachePlayGameAgentScript = _paddleAI.GetComponent<PlayGameAgent>(); 
            }
        ballRb = GetComponent<Rigidbody2D>();
        ballRb.collisionDetectionMode = CollisionDetectionMode2D.Continuous;

    }

    public void Start()
    {
        ballRb.mass = 0;
        ballRb.drag = 0;
        ballRb.angularDrag = 0;
        SpawnBall();
        ballRb = GetComponent<Rigidbody2D>();
    }

    public void FixedUpdate()
    {
        PreventParallelVelocity();
        if (_agentGame)
        {
            ForecastLanding();
        }
        
    }

    // Updates AI with landing prediction so AI can select target.
    private void ForecastLanding()
    {
        // Ping AI when ball headed for failure boundary.
        RaycastHit2D DirectionCast = GetDirectionRaycast();
        if (DirectionCast.collider &&
            DirectionCast.collider.name == "FailureBoundary" &&
            _cachePlayGameAgentScript.TargetBricks.Count > 0 && transmitToAgent)
        {
            _cachePlayGameAgentScript.LandingForecastUpdate();
            transmitToAgent = false; //Transmit once
        }
        
        // Reset transmit switch
        if (ballRb.velocity.y > 0)
        {
            transmitToAgent = true;
        }
    }

    // Create raycast from ball in direction of movement.
    private RaycastHit2D GetDirectionRaycast()
    {
        // Start just slightly outside of body to avoid colliding with self.
        Vector2 origin = new Vector2(transform.position.x, transform.position.y) + (GetComponent<Rigidbody2D>().velocity * .05f);
        Vector2 direction = GetComponent<Rigidbody2D>().velocity.normalized;
        RaycastHit2D DirectionCast = Physics2D.Raycast(origin, direction, 100f);
        Debug.DrawRay(origin, direction * 10f, Color.red);
        return DirectionCast;
    }

    public void SpawnBall() 
        /*reset the position of the ball to a spawn point
         with a variable angle of release at constant speed*/
    {
        //Paddle will be next hit after SpawnBall
        bi.set_brickComboState(1);
        const float minAngle = .5f;
        const float maxAngle = 1f;
        //Add the BreakoutInstance (parent of ball) position so the ball spawns relative
        //to the instance's center position wherever it's located in world space
        Vector3 spawnLeft = new Vector3(-5,.5f, 0f) + transform.parent.position;
        Vector3 spawnRight = new Vector3(5,.5f, 0f) + transform.parent.position;
        Vector3 spawnMid = new Vector3(0,.5f, 0f) + transform.parent.position;
        Vector2 spawnPos = default;
        Vector2 initialDir = default;
        
        var spawnPoint = UnityEngine.Random.Range(0, 4);
        var angleRandom = UnityEngine.Random.Range(minAngle, maxAngle);
        if (testing) { angleRandom = testingAngle; } //Override angle if we're testing
        var complDown = 1 + maxAngle - angleRandom;
        switch (spawnPoint)
        { 
            case 0: //left spawn - move rightward
                spawnPos = spawnLeft;
                initialDir = Vector2.right; 
                break;
                
            case 1: //right spawn - move leftward
                spawnPos = spawnRight;
                initialDir = Vector2.left;
                break;
            
            case 2: //middle spawn - move leftward
                spawnPos = spawnMid;
                initialDir = Vector2.left;
                break;
                
            case 3: //middle spawn - move rightward
                spawnPos = spawnMid;
                initialDir = Vector2.right;
                break;
        }

        transform.position = spawnPos;
        
        //Lower music intensity
        //AudioManager.instance.ResetIntensity();
        StartCoroutine(LaunchDelay(complDown, initialDir, angleRandom));
    }

    
    IEnumerator LaunchDelay(float complDown, Vector2 initialDir, float angleRandom)
    {
        /*The process of updating the ball's position in spawnBall() appeared to cause a force to be applied to the
        object once it was visible. This freezes the ball, waits for one second, and then unfreezes the ball before
        applying the launch velocity. The ball appears to spawn and wait before moving.*/
        ballRb.constraints = RigidbodyConstraints2D.FreezePosition;
        yield return new WaitForSeconds(1f);
        ballRb.constraints = RigidbodyConstraints2D.None;
        ballRb.velocity = ((Vector2.down * (ballBaseSpeed * complDown)) + (initialDir * (ballBaseSpeed * angleRandom)));
        yield return null;
    }

    //Checks whether the current angle of movement is parallel to a normal vector on the x-axis. If it its, adjust the
    //ball's velocity slightly down to get it back into the game:
    //TODO: How sharp should the degree be?
    private void PreventParallelVelocity()
    {   
        //Debug.Log("Y velocity" + ballRB.velocity.y);
        if (-1 * horizontalOverride < ballRb.velocity.y && ballRb.velocity.y < horizontalOverride)
        {
            ballRb.velocity = new Vector2(transform.position.x, transform.position.y * .99f) * (float)Math.Pow((ballSpeedBoost/1.2f), ballSpeedTier);
        }
    }
    
    public int get_ballSpeedTier() 
        /* return 1-5 based on number of boosts applied to current ball*/
    { return ballSpeedTier; }
    
    public float get_ballSpeedBoost() 
        /* return 1-5 based on number of boosts applied to current ball*/
    { return ballSpeedBoost; }
    
    public float get_ballBaseSpeed() 
        /* return constant value of base ball speed*/
    { return ballBaseSpeed; }
    
    public void set_SpeedBoost()
        /* apply set modifier to ball speed*/
    {
        
        if (ballSpeedTier < 5)
        {
            ballRb.velocity *= ballSpeedBoost;
            ballSpeedTier += 1;
            //AudioManager.instance.AddIntensity(1);
        }
    }

    public void Freeze()
    {
        if (_velocityBackup == new Vector3(0, 0, 0))
        {
            _velocityBackup = ballRb.velocity; 
        }
        ballRb.constraints = RigidbodyConstraints2D.FreezeAll;
    }

    public void Unfreeze()
    {
        //AI clipping out of bounds
        if (ballRb.transform.position.y > 20 ||  ballRb.transform.position.y < -20 ||
        ballRb.transform.position.x > 20 || ballRb.transform.position.x < -20){
            SpawnBall();
        }
        ballRb.constraints = RigidbodyConstraints2D.None;
        ballRb.velocity = _velocityBackup;
        _velocityBackup = new Vector3(0, 0, 0);
    }
}
