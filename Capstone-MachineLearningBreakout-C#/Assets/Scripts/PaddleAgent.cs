using System;
using System.Collections.Generic;
using System.Numerics;
using UnityEngine;
using Unity.MLAgents;
using Unity.MLAgents.Actuators;
using Unity.MLAgents.Sensors;
using UnityEngine.SceneManagement;
using Vector2 = UnityEngine.Vector2;

public class PlayGameAgent : Agent
{
    // Objects and representation lists.
    public bool deadBallUnlock;
    public GameObject paddle;
    public GameObject ball;
    public BreakoutInstance bi;
    public List<List<int>> BrickGraph = new List<List<int>>();
    
    // Target Tracking
    private List<(int, int)> HighestTargetsPerColumn = new List<(int, int)>();
    private List<(int, int)> HighestTargets = new List<(int, int)>();
    public List<GameObject> TargetBricks = new List<GameObject>();
    private List<int> BrokenColumns = new List<int>();
    private int highestTargetableRow = 0;
    private Vector2 TargetPosition;
    private GameObject TargetBrick;
    //private bool _brokenCeiling;
    private string neuralNet3 = "NN3breakoutInstance";
    private int _rowCount;
    private int _colCount;
    
    // Penalties
    private float _deadBallPenalty = -100.0f;
    private float _paddleComboPenalty = -5.0f;
    
    // Rewards
    private float _MaxTargetingReward = 100.0f;
    private float _brickComboReward = 10.0f;
    private float brickCollisionReward = 3.0f;
    private float _paddleBounceReward = 1.0f;
    private float _rewardRoofBounce = 20.0f;
    
    //Component Cache (performance)
    Rigidbody2D _cacheBallRB2D;
    
    private void Awake()
    {
        bi = transform.parent.gameObject.GetComponent<BreakoutInstance>();
        paddle = gameObject;
        _rowCount = bi.get_rowCount();
        _colCount = bi.get_colCount();
        
        // Build the representation graph and object graph.
        BuildBrickGraph(_rowCount, _colCount);
    }

    private void Start()
    {
        SetTargetPositionFromBrick(bi.getBrick_inPlayBricks(0, 7)); // Starting target is middle brick
    }

    public override void OnEpisodeBegin()
    {
        // this is called by the breakout instance
        //CacheBall();
    }
    
    // Relevant observations for mlagents to learn.
    public override void CollectObservations(VectorSensor sensor)
    {
        sensor.AddObservation(GetAngleBetween(paddle, ball)); // Angle between paddle and ball
        sensor.AddObservation(ball.transform.localPosition); // Ball position
        sensor.AddObservation(paddle.transform.localPosition); // Paddle position
        
        // observations unique to Neural Net 3
        if (bi.name == neuralNet3){
            sensor.AddObservation(GetTargetBrickAngle()); // Target Angle
            sensor.AddObservation(GetBallLaunchAngle()); // Ball launch Angle
            sensor.AddObservation(GetBallVelocity()); // Direction ball is moving
        }
    }

    // Control paddle movement
    public override void OnActionReceived(ActionBuffers actions)
    {
        int dir = actions.DiscreteActions[0];
        if(dir == 0)
        {
            // do nothing
        }
        else if(dir == 1)
        {
            paddle.GetComponent<Paddle>().PaddleMoveLeft();
        }
        else {
            paddle.GetComponent<Paddle>().PaddleMoveRight();
        }
    }

    private void Update()
    {
        // If game time expires, start a new scene.
        if (bi._currentTime <= 0)
        {
            EndEpisode();
            SceneManager.LoadScene("SingleGame");
        }
        
        //Optional: run visualizer lines each frame (need to toggle "gizmos" from editor).
        DebugVisualizer();
    }
    
    // Called by bi if ball dies, gives penalty.
    public void DeadBall()
    {
        AddReward(_deadBallPenalty);
    }
    
    public void CacheBall()
    /*ensures Agent is tracking the ball and maintains the cache of the ball's RB*/
    /*todo, consider better routing than bi -> agent -> bi.Function()*/
    { 
        ball = bi.GetBall();
        _cacheBallRB2D = ball.GetComponent<Rigidbody2D>();
    }

    // Update graph, targets and rewards whenever a brick is hit.
    public void BrickHitUpdate(int row, int column)
    {
        // Knock out brick from graph representation and run targeting algorithm;
        BrickGraph[row][column] = 0;
        if (bi.getCounter_inPlayBricks() > 0) { SetTargetBricks(); }
        else {ResetBrickGraph(_rowCount, _colCount); }
        
        // Optional Debugging: Print Graph
        // printGraph(BrickGraph);
    }
    
    // Update target based on ball landing characteristics.
    public void LandingForecastUpdate()
    {
        Vector2 ballVelocity = GetBallVelocity();
        
        // If ball incoming from right to left, aim for leftmost target.
        if (ballVelocity.x < 0)
        {
            GameObject leftmostTarget = TargetBricks[0];
            foreach (var brick in TargetBricks)
            {
                if (brick.transform.position.x < leftmostTarget.transform.position.x)
                {
                    leftmostTarget = brick;
                }
            }
            TargetBrick = leftmostTarget;
        }
    
        // If ball incoming from left to right, aim for rightmost target.
        if (ballVelocity.x > 0)
        {
            GameObject rightmostTarget = TargetBricks[0];
            foreach (var brick in TargetBricks)
            {
                if (brick.transform.position.x > rightmostTarget.transform.position.x)
                {
                    rightmostTarget = brick;
                }
            }
            TargetBrick = rightmostTarget;
        }
        
        if (TargetBrick)
        {
            SetTargetPositionFromBrick(TargetBrick);
        }

        else
        {
            TargetPosition.x = transform.parent.localPosition.x;
            TargetPosition.y = transform.parent.localPosition.y;
        }
    }
    
    // Add the highest targetable bricks per column to a list of coordinates
    public void SetHighestTargetsPerColumn(List<List<int>> currentGraph)
    {
        // Scan up each column until the first brick that exists.
        for (int column = 0; column < _colCount; column++)
        {
            for (int row = 0; row < _rowCount; row++)
            {
                if (BrickGraph[row][column] == 1)
                {
                    HighestTargetsPerColumn.Add((row, column));
                    if (row > highestTargetableRow)
                    {
                        highestTargetableRow = row;
                    }
                    break;
                }
                else // If column broken
                {
                    BrokenColumns.Add(column);
                }
            }
        }
    }
    
    // Set the highest targets as coordinates and add brick positions
    private void SetTargetCoordinates()
    {
        SetHighestTargetsPerColumn(BrickGraph);
        foreach (var brick in HighestTargetsPerColumn)
        {
            if (brick.Item1 == highestTargetableRow)
            {
                HighestTargets.Add((brick.Item1, brick.Item2));
            }
        }
    }
    
    // Analyze graph to set target brick objects.
    private void SetTargetBricks()
    {
        ClearTargets();
        SetTargetCoordinates();
        foreach (var coordinate in HighestTargets)
        {
            TargetBricks.Add(bi.getBrick_inPlayBricks(coordinate.Item1,coordinate.Item2));
        }
        //PrintTargets();
    }
    
    // Sets target position from brick object
    private void SetTargetPositionFromBrick(GameObject brick)
    {
        TargetPosition.x = brick.transform.position.x;
        TargetPosition.y = brick.transform.position.y;
    }

    // Clear all current targets
    private void ClearTargets()
    {
        TargetBricks.Clear();
        HighestTargets.Clear();
        HighestTargetsPerColumn.Clear();
        highestTargetableRow = 0;
    }

    // Debugging: List current targets
    private void PrintTargets()
    {
        Debug.Log(String.Join(" ", HighestTargets));
    }
    
    // Reward bouncing ball
    private void OnCollisionExit2D(Collision2D other)
    {
        if (other.gameObject.GetComponent<Ball>())
        {
            AddReward(_paddleBounceReward);
            
            // Check for how well bounce trajectory matches target trajectory.
            RewardTargetting();
            //Debug.Log("Bounced ball! Total reward: "+ GetCumulativeReward());
        }
    }
    
    // Get direction the ball is moving
    private Vector2 GetBallVelocity()
    {
        Vector2 movementDir;
        if (_cacheBallRB2D)
        {
            movementDir = _cacheBallRB2D.velocity; 
        }
        else
        {
            movementDir = new Vector2(0, 0);
        }
        
        return movementDir;
    }
    
    // Calculate angle of ball launch after paddle bounce (against vertical line).
    private float GetBallLaunchAngle()
    {
        Vector2 movementDir = GetBallVelocity();
        float launchAngle = Vector2.SignedAngle(Vector2.up, movementDir);
        return launchAngle;
    }
    
    // Calculate angle from paddle to target brick (against vertical line).
    private float GetTargetBrickAngle()
    {
        Vector2 paddlePos;
        paddlePos.x = transform.position.x;
        paddlePos.y = transform.position.y;
        Vector2 targetDir = TargetPosition - paddlePos;
        float targetAngle = Vector2.SignedAngle(Vector2.up, targetDir);
        return targetAngle;
    }
    
    // Calculate angle of difference between ball direction and target direction
    private float GetTargettingMismatch()
    {
        float launchAngle = GetBallLaunchAngle();
        float TargetAngle = GetTargetBrickAngle();
        float AngleMismatch = Math.Abs(launchAngle - TargetAngle);
        return AngleMismatch;
    }
    
    // Reward if targetting is accurate
    private void RewardTargetting()
    {
        float TargettingMismatch = GetTargettingMismatch();
        float reward = (float)(_MaxTargetingReward / (1 + 0.5f * Math.Pow(TargettingMismatch, 2)));
        AddReward(reward);
    }
    
    // Get angle between two objects, referenced from 0,0 origin.
    private float GetAngleBetween(GameObject object1, GameObject object2)
    {
        if (object1 == null || object2 == null)
        {
            return 0.0f;
        }

        float obj1angle = GetAngle(object1);
        float obj2angle = GetAngle(object2);

        // Calculate difference in angle.
        float angleBetween = Math.Abs(obj1angle - obj2angle);
        
        return angleBetween;
    }
    
    private Vector2 Get2DPosition(GameObject object1)
    {
        return new Vector2(object1.transform.position.x, object1.transform.position.y);
    }
    
    // Get angle referenced from vertical line.
    private float GetAngle(GameObject object1)
    {
        Vector2 pos = Get2DPosition(object1);
        Vector2 parentOrigin = new Vector2(transform.parent.position.x, transform.parent.position.y);
        Vector2 line = parentOrigin - pos;
        float angle = Vector2.SignedAngle(Vector2.up, line);
        return angle;
    }
    
    // Builds a nested list of 1s in BrickGraph, representing starting state of bricks.
    private void BuildBrickGraph(int rows, int columns)
    {
        for (int i = 0; i < rows; i++)
        {
            List<int> sublist = new List<int>();
            BrickGraph.Add(sublist);
            for (int j = 0; j < columns; j++)
            {
                sublist.Add(1);
            }
        }
    }
    
    private void ResetBrickGraph(int rows, int columns)
    {
        for (int i = 0; i < rows; i++)
        {
            for (int j = 0; j < columns; j++)
            {
                BrickGraph[rows][columns] = 1;
            }
        }
    }
    
    //For Debugging: Prints the nested list in reverse to visually align with game state.
    public void printGraph(List<List<int>> myNestedList)
    {
        string str = "";
        for(int i=myNestedList.Count - 1;i>=0;i--)
        {
            for (int j = 0; j < myNestedList[i].Count; j++)
            {
                str += myNestedList[i][j] + "   ";
            }
            str += "\n";
        }
        Debug.Log(str);
    }
    
    
    // Optional line drawing functions to visualize learning process.
    private void DebugVisualizer()
    {
        // Vertical line against which target and ball launch angle are referenced
        // Debug.DrawLine(Vector2.zero, Vector2.up * 20, Color.white);
        // Debug.DrawLine(Vector2.zero, Vector2.down * 20, Color.white);
        
        // Visualize movement direction of ball
        //Debug.DrawLine(ball.transform.position, new Vector2(ball.transform.position.x, ball.transform.position.y) + GetBallVelocity(), Color.green);
        
        // Visualize line from paddle to target brick
        Debug.DrawLine(transform.position, TargetPosition, Color.yellow);
        
        //Visualize paddle-ball angle referenced from origin
        Debug.DrawLine(transform.parent.localPosition, ball.transform.position, Color.blue);
        Debug.DrawLine(transform.parent.localPosition, transform.position, Color.magenta);
    }
    
    public void TopBrickReward(float reward)
        /*Reward Agent for first rupture into highest layer of bricks*/
    {
        if (reward > 0) { AddReward(reward); } 
        //_brokenCeiling = true;
    }
    
    public void RoofReward()
        /*Reward Agent for first rupture into highest layer of bricks*/
    { AddReward(_rewardRoofBounce); }
    
    public void set_paddleComboPenalty(){
        // paddle, paddle collision without brick receive penalty
        AddReward(_paddleComboPenalty);
    }
    
    public void set_brickComboReward(){
        // brick, brick collision without paddle receive penalty
        AddReward(_brickComboReward); }
    
    public void set_brickCollisionReward(float point){
        // Rewards based on brick destroyed: 7 - 1
        // AddReward(point);
        // or
        // Rewards static amount for each brick1
        AddReward(brickCollisionReward);
    }
}