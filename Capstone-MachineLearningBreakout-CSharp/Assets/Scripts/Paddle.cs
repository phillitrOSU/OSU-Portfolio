using System;
using Unity.VisualScripting;
using UnityEngine;
using FMODUnity;
using UnityEngine.InputSystem;
using Quaternion = UnityEngine.Quaternion;
using Vector2 = UnityEngine.Vector2;
using Vector3 = UnityEngine.Vector3;

public class Paddle : MonoBehaviour
{
    public BreakoutInstance bi;
    public Rigidbody2D paddleRb;
    public BoxCollider2D paddle2Dc;
    private InputAction _paddleRightAction;
    private InputAction _paddleLeftAction;
    private InputAction _paddleSlowRight;
    private InputAction _paddleSlowLeft;
    public InputActionAsset playerControls;
    private SpriteRenderer _paddleSpriteRenderer;
    private Transform _paddleTransformations;
    private bool _hardMode;
    private bool _frozen = false;
    [SerializeField] private EventReference _paddleSound;
    
    private bool _agentGame;
    private bool _2PGame;
    
    // strength of movement of paddle
    private float _moveStrength;
    private float _slowStrength;
    
    //deactivate paddle movement in out of bounds direction if out of bounds
    private float _leftBarrier;
    private float _rightBarrier;

    //force ball to bounce vertically within 0 to 45 degree angle
    private float _maxBounceAngle = 45f;

    public void Awake()
    {
        bi = transform.parent.gameObject.GetComponent<BreakoutInstance>();
        _agentGame = bi.get_agentGame();
        
        //Set Paddle Physics & Characteristics
        //Rb = Rigid Body
        paddleRb = GetComponent<Rigidbody2D>();
        paddleRb.isKinematic = false;
        paddleRb.mass = 200;
        paddleRb.drag = 0;
        paddleRb.collisionDetectionMode = CollisionDetectionMode2D.Continuous;
        paddleRb.angularDrag = 0;
        
        //Collider and Size
        //Vertical collisions set to combat ball clipping at high speeds
        paddle2Dc = GetComponent<BoxCollider2D>();
        paddle2Dc.size = new Vector2(1,3);
        paddle2Dc.offset = new Vector2(0,-1.5f);
        
        //disable paddle clipping through boundaries with frame taps
        _2PGame = bi.get_2PGame();
        switch (_2PGame)
        {
            case true: _leftBarrier = -18.35f; _rightBarrier =-5.80f; break;
            case false: _leftBarrier = -6.25f; _rightBarrier = 6.25f; break;
        }
        
        //Cosmetics
        update_HardMode(false);
        
        //Set Control Scheme
        _moveStrength = 35;
        _slowStrength = 15;

        _paddleRightAction = playerControls.FindActionMap("Player", true).FindAction("PaddleRight");
        _paddleLeftAction = playerControls.FindActionMap("Player", true).FindAction("PaddleLeft");
        _paddleRightAction.Enable();
        _paddleLeftAction.Enable();
        if (!(_agentGame)){
            _paddleSlowRight = playerControls.FindActionMap("Player", true).FindAction("SlowRight");
            _paddleSlowLeft = playerControls.FindActionMap("Player", true).FindAction("SlowLeft");
            _paddleSlowRight.Enable();
            _paddleSlowLeft.Enable();
        }
    }
    
    private void Update()
    {
        // Move Paddle Right - // NEED MOVEMENT LOCK
        if (_paddleRightAction.IsPressed() && (paddleRb.position.x < _rightBarrier))
        {
            PaddleMoveRight();
        } 
        // Move Paddle Left // NEED MOVEMENT LOCK
        if (_paddleLeftAction.IsPressed() && (paddleRb.position.x > _leftBarrier))
        {
            PaddleMoveLeft();
        }

        if (!(_agentGame)){
            if (_paddleSlowRight.IsPressed() && (paddleRb.position.x < _rightBarrier))
            {
                PaddleMoveSlowRight();
            } 
            // Move Paddle Left // NEED MOVEMENT LOCK
            if (_paddleSlowLeft.IsPressed() && (paddleRb.position.x > _leftBarrier))
            {
                PaddleMoveSlowLeft();
            }
        }
    }

    // Separating these functions from update and making them public allows access to MlAgents.
    public void PaddleMoveLeft()
    {
        if (!_frozen)
        {
            paddleRb.transform.position += Vector3.left * _moveStrength * Time.deltaTime;
        }
    }

    public void PaddleMoveRight()
    {
        if (!_frozen)
        { 
            paddleRb.transform.position += Vector3.right * _moveStrength * Time.deltaTime; 
        }
    }

    public void PaddleMoveSlowLeft()
    {
        if (!_frozen)
        {
            paddleRb.transform.position += Vector3.left * _slowStrength * Time.deltaTime;
        }
    }

    public void PaddleMoveSlowRight()
    {
        if (!_frozen)
        { 
            paddleRb.transform.position += Vector3.right * _slowStrength * Time.deltaTime; 
        }
    }


    private void OnCollisionEnter2D(Collision2D collision)
    {
        Ball ball = collision.gameObject.GetComponent<Ball>();
        if (ball != null)
        {          
            //AudioManager.instance.PlayPaddleSound();
            // increase ball speed if few bricks remain in play
            if (bi.PaddleBallBoost() == 1){
                ball.set_SpeedBoost();
            }

            bi.increment_PaddleBounce();

            //Code to control ball bounce angle: https://www.youtube.com/watch?v=RYG8UExRkhA (time: 45:57)
            Vector3 paddlePosition = transform.position;
            Vector2 contactPoint = collision.GetContact(0).point;

            float offset = paddlePosition.x - contactPoint.x;
            float width = collision.otherCollider.bounds.size.x / 2;

            // calculate angle - 0 angle = 0 x.velocity
            float currentAngle = Vector2.SignedAngle(Vector2.up, ball.GetComponent<Rigidbody2D>().velocity);
            float bounceAngle = (offset / width) * _maxBounceAngle;
            float newAngle = Math.Clamp((currentAngle + bounceAngle), -_maxBounceAngle, _maxBounceAngle);

            Quaternion rotation = Quaternion.AngleAxis(newAngle, Vector3.forward);
            int ballSpeedTier = ball.get_ballSpeedTier();
            float ballSpeedBoost = ball.get_ballSpeedBoost();
            float ballBaseSpeed = ball.get_ballBaseSpeed();
            
            // new angle of ball based on landing position from paddle
            ball.transform.Translate(Vector3.forward * 0 * Time.deltaTime);
            
            // reset speed with each paddle collision to the base speed * speed boost modifiers
            ball.GetComponent<Rigidbody2D>().velocity = rotation * Vector2.up * ballBaseSpeed * (float)Math.Pow(ballSpeedBoost, ballSpeedTier);
            bi.BrickComboManager(0);
            bi.set_roofBounceState(0);
        }
    }
    public void update_HardMode(bool mode)
    {
        //Round 2 Hard Mode settings when first round of bricks cleared.
        _paddleTransformations = GetComponent<Transform>();
        _paddleSpriteRenderer = GetComponent<SpriteRenderer>();
        _hardMode = mode;
        _paddleTransformations.localScale = new Vector3(2.15f, .175f, 1f);

        switch (bi.name)
        {

            case "NN1breakoutInstance":
                _paddleSpriteRenderer.color = _hardMode ? new Color(.8f, .8f, 0) : new Color(.7f, .7f, 0);
                break;
            case "NN2breakoutInstance":
                _paddleSpriteRenderer.color = _hardMode ? new Color(.9f, .6f, 0) : new Color(.8f, .5f, 0);
                break;
            case "NN3breakoutInstance":
                _paddleSpriteRenderer.color = _hardMode ? new Color(.8f, .3f, .3f) : new Color(.7f, .2f, .2f);
                break;
            default:
                _paddleSpriteRenderer.color = _hardMode ? Color.magenta : Color.cyan;
                break;
        }
    }

    public void Freeze()
    {
        _frozen = true;
    }

    public void Unfreeze()
    {
        _frozen = false;
    }
}

