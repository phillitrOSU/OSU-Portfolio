using System;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using Unity.VisualScripting;
using UnityEngine.Serialization;
using Debug = UnityEngine.Debug;
using UnityEngine.Windows;

public class BreakoutInstance : MonoBehaviour
{
    public int level = 1;
    public int playerID;
    
    //Event Delegates
    public static Action<bool, bool, int, int, int, int, int, int, int, int> OnGameCompleted;
    public static Action<int, int> OnGameOver;
       
    // initialize objects
    public UIManager ui;
    public GameObject ballPrefab;
    private GameObject _ball;
    public GameObject PaddlePrefab;
    private GameObject _paddle;
    private GameObject _brickPrefab;
    private static string _nn1GameName = "NN1breakoutInstance";
    private static string _nn2GameName = "NN2breakoutInstance";
    private static string _nn3GameName = "NN3breakoutInstance";
    private static string _2PGameName = "2PbreakoutInstance";
    
    // initalize game states
    private float _startingTime = 999f;
    public float _currentTime;
    private float _ceilingTime;
    private float _round2Time;
    private int _score;
    private int _lives;
    private bool _gameOver;
    //private bool _gameCompleted;
    private int _gameRound;
    private bool _agentGame;
    private bool _2PGame;
  
    //brick variables
    public GameObject row;
    public List<GameObject> brickTypes;
    private List<List<GameObject>> _inPlayBricks;
    private int _inPlayBricksCounter;
    private static int _rowCount = 8;
    private static int _colCount = 14;    
    private static int _distinctColors = 4;
    private float _startingHeight = 3.5f;
    
    // init ball speed tiers
    private int _hit4SpeedBoost = 2;
    private int _hit12SpeedBoost = 12;
    private int _boostCounter;
    private bool _outerSpeedBoost;
    private bool _interSpeedBoost;
    private int _lowBrickCount = 20;

    // init combo / counters
    private int _comboState;
    private int _comboBrickCount;
    private int _comboPaddleCount;
    private int _lifeRed;
    private int _lifeOrange;
    private int _lifeGreen;
    private int _lifeYellow;
    private int _bounceRoofState;
    private int _comboRoofCount;
    private int _paddleBounce;
    private int _bricksDestroyed;
    private bool _rupturedCeiling;
    
    //init string handlers - from Resources folder
    //private string _mainMenuString = "MainMenu";
    private static string _rowString = "Row";
    private static string _ballString = "Ball";
    private static string _NN1PaddleString = "NN-1";
    private static string _NN2PaddleString = "NN-2";
    private static string _NN3PaddleString = "NN-3";
    private static string _playerPaddleString = "PlayerPaddle";
    private static string _brickString = "Brick";
    private List<string> _brickBuildList;
    private static string _redString = "BrickRed";
    private static string _orangeString = "BrickOrange";
    private static string _greenString = "BrickGreen";
    private static string _yellowString = "BrickYellow";
    private List<string> _brickOrder = new (_distinctColors) 
        { _yellowString, _greenString, _orangeString, _redString};

    // init brick points
    private static int _redPoint = 7;
    private static int _orangePoint = 5;
    private static int _greenPoint = 3;
    private static int _yellowPoint = 1;

    private void OnEnable()
    {
        GameManager.FreezeBreakouts += Freeze;
        GameManager.ThawBreakouts += UnFreeze;
    }

    private void OnDisable()
    {
        GameManager.FreezeBreakouts -= Freeze;
        GameManager.ThawBreakouts -= UnFreeze;
    }

    public void Awake()
    {
		//Load Prefabs and Dependency Scripts
        ui = GetComponentInChildren<UIManager>();
        row = Resources.Load<GameObject>(_rowString);
        ballPrefab = Resources.Load<GameObject>(_ballString);
        
        //private static string _nn1GameName = "NN1breakoutInstance";
        //private static string _nn2GameName = "NN2breakoutInstance";
        //private static string _nn3GameName = "NN3breakoutInstance";
        //private static string _2PGameName = "2PbreakoutInstance";

        //Switch statement not accepting variable names
        switch (name)
        {

            case "NN1breakoutInstance":
                PaddlePrefab = Resources.Load<GameObject>(_NN1PaddleString);
                break;
            case "NN2breakoutInstance":
                PaddlePrefab = Resources.Load<GameObject>(_NN2PaddleString);
                break;
            case "NN3breakoutInstance":
                PaddlePrefab = Resources.Load<GameObject>(_NN3PaddleString);
                break;
            default:
                PaddlePrefab = Resources.Load<GameObject>(_playerPaddleString);
                break;

        }
        _brickPrefab = Resources.Load<GameObject>(_brickString);
        _brickBuildList = new List<string>();
        for (var i = 0; i < (_rowCount/_distinctColors); i++){_brickBuildList.Add(_brickOrder[0]);}
        for (var i = 0; i < (_rowCount/_distinctColors); i++){_brickBuildList.Add(_brickOrder[1]);}
        for (var i = 0; i < (_rowCount/_distinctColors); i++){_brickBuildList.Add(_brickOrder[2]);}
        for (var i = 0; i < (_rowCount/_distinctColors); i++){_brickBuildList.Add(_brickOrder[3]);}
        
        //Do not allow scene to play if player_id variables on any breakoutInstance have not been set
        if (playerID < 1)
        {
            throw new UnityException("player_id has not been set on one or more breakoutInstance objects. Please " +
                                     "assign every instance an id greater than 1.");
        }
    }
    
    public void Start()
    {
        NewGame();
    }
    
    public void NewGame()
    {
        SpawnGameTimer();
        InitGameVariables();
        SpawnPaddle();
        //ClearBrickField();
        SpawnBrickField(_startingHeight);
        InstantiateBall();
        UnFreeze();
    }
    
    public void SpawnGameTimer()
    {
        _currentTime = _startingTime;
        ui.UpdateTimerUI(_currentTime);
    }

    public void Update()
    // Called every frame, potentially more efficient way to handle this?
    {
        if (!_gameOver)
        {
            _currentTime -= 1 * Time.deltaTime;
            ui.UpdateTimerUI(_currentTime); 
        }
    }

    public void InstantiateBall()
    {
        //Debug.Log(_lives);
        if (_ball != null) { Destroy(_ball); }
        _ball = Instantiate(ballPrefab, gameObject.transform); 

        //update the Agent's reference to the ball object
        if (_agentGame) 
        {
            _paddle.GetComponent<PlayGameAgent>().CacheBall();
        }
    }
    
    public void SpawnPaddle()
    {
        _paddle = Instantiate(PaddlePrefab, gameObject.transform);
    }
    
    public void SpawnBrickField(float startHeight)
    {
        //set global bricks list and counter
        _inPlayBricks = Create_inPlayBricks(_rowCount, _colCount);
        _inPlayBricksCounter = _rowCount * _colCount;
        
        // Set brick field visuals (spawn height of field must be set in BrickManager.cs)
        // xSpacing argument is float (0 - 1). 0 = no space and all brick, 1 = all space and no brick.
        float brickHeight = .24f;
        float xSpacing = .1f; 
        float ySpacing = .1f;
        
        // Spawn brick field
        row.GetComponent<RowConstructor>().SetStartingPosition(startHeight);
        for (var i = 0; i < _rowCount; i++)
        {
            var currRow = Instantiate(row, gameObject.transform);
            currRow.transform.localPosition = new Vector3(0, 0, 0);
            RowConstructor currRowConstructorScript = currRow.GetComponent<RowConstructor>();
            currRowConstructorScript.constructRow(_brickPrefab, _colCount, brickHeight, xSpacing, ySpacing, i);
        }
        row.GetComponent<RowConstructor>().ClearStartingPosition();
    }
    
    private void ClearBrickField(){
        var foundBricksInField = FindObjectsOfType<Brick>();
        foreach(Brick brick in foundBricksInField) {
            Destroy(brick.gameObject);
        }
    }

    public void BrickCollision(string color, int rowBrick, int colBrick){
        /* Event Handler when for Brick Collision*/
            _bricksDestroyed += 1;
            BrickRewardHandler(color);
            BallSpeedBoost(color);
            BrickAlterGameState();
            BrickComboManager(1);
            RoofComboManager();
            if (_rupturedCeiling == false && rowBrick == _rowCount - 1){
                RupturedCeiling(rowBrick);}
            ExtraLifeHandler(color);

            // Update Agent of brick collision and destruction
            if (_agentGame) { _paddle.GetComponent<PlayGameAgent>().BrickHitUpdate(rowBrick, colBrick); }
    }

    public void RupturedCeiling(int rowBrick)
    /*Highest brick has been broken into*/
    {
        _rupturedCeiling = true;
        _ceilingTime = _currentTime;
        if (_agentGame) { _paddle.GetComponent<PlayGameAgent>().TopBrickReward(150 - (_startingTime - _ceilingTime)); }
    }

    public void BrickComboManager(int comboUpdate)
    {
        /*Reward/Punishment Manager for consecutive ball / paddle hits
        _comboState = previous hit: Brick = True; Paddle = False
        comboUpdate = current hit: Brick = True; Paddle = False*/

        // combo paddle hit (paddle, then paddle)
        if (comboUpdate == 0 && _comboState == 0)
        {
            _comboPaddleCount += 1;
            if (_agentGame)
            {
                _paddle.GetComponent<PlayGameAgent>().set_paddleComboPenalty();
            }
        }

        // combo brick hit (brick, then brick)
        if (comboUpdate == 1 && _comboState == 1)
        {
            _comboBrickCount += 1;
            if (_agentGame)
            {
                _paddle.GetComponent<PlayGameAgent>().set_brickComboReward();
            }
        }
        set_brickComboState(comboUpdate);
    }
    
    public void RoofComboManager(){
        /* combo roof hit (roof, then brick)*/ 
        if (_bounceRoofState == 1)
        {
            _comboRoofCount += 1;
            _bounceRoofState = 0;
            if (_agentGame) { _paddle.GetComponent<PlayGameAgent>().RoofReward(); }
        }
    }
    
    private void BrickAlterGameState()
    {
        _inPlayBricksCounter -= 1;
        //Debug.Log("IN PLAY COUNTER " + this + " " + _inPlayBricksCounter);
        if (_inPlayBricksCounter <= 0) //0
        {
            _gameRound += 1;
            if (_gameRound == 2) //==2
            {
                //need a time delay?
                //ScoreCard();
                _paddle.GetComponent<Paddle>().update_HardMode(true);
                _round2Time = _currentTime;
                _score += 104; //for an even 1000
                ui.UpdateScoreUI(_score);
                SpawnBrickField(_startingHeight);
            }
            if (_gameRound > 2) //> 2
            {
                //Game Over, tally scores
                //ScoreCard();
                //_gameOver = _gameCompleted = true;
                Freeze();
                // Call score to Game Complete Menu
                OnGameCompleted?.Invoke(_agentGame, _2PGame, _score, (int)_currentTime, (int)_round2Time,
                (int)_ceilingTime, _lives,_comboRoofCount, _comboBrickCount, _comboPaddleCount);
                /*OnGameCompleted?.Invoke(_score, (int)_currentTime, _lives);*/
            }
        }
    }

    private void BrickRewardHandler(string color)
        /* Increment Points based on Brick Collision
        Rewards Agent on Brick Collision
        Updates UI on score change*/
    {
        if (color == _redString) { _score += _redPoint;
            if (_agentGame) { _paddle.GetComponent<PlayGameAgent>().set_brickCollisionReward(_redPoint);}
        } 
        else if (color == _orangeString) { _score += _orangePoint; 
            if (_agentGame) {_paddle.GetComponent<PlayGameAgent>().set_brickCollisionReward(_orangePoint);}
        } 
        else if (color == _greenString) { _score += _greenPoint; 
            if (_agentGame) {_paddle.GetComponent<PlayGameAgent>().set_brickCollisionReward(_greenPoint);}
        } 
        else if (color == _yellowString) { _score += _yellowPoint; 
            if (_agentGame) {_paddle.GetComponent<PlayGameAgent>().set_brickCollisionReward(_yellowPoint);}
        } 
        ui.UpdateScoreUI(_score);
    }

    private void BallSpeedBoost(string color)
        /*Determine ball boost logic*/
    {

        //first brick hit on top row, round 1?
        if (_outerSpeedBoost is false && color == _redString && _gameRound < 2)
        {
            _outerSpeedBoost = true;
            _ball.GetComponent<Ball>().set_SpeedBoost();
        }

        //first brick hit on middle-top row, round 1?
        else if (_interSpeedBoost is false && color == _orangeString && _gameRound < 2)
        {
            _interSpeedBoost = true;
            _ball.GetComponent<Ball>().set_SpeedBoost();
        }

        //first brick hit on middle-bottom row, round 2?
        else if (_interSpeedBoost is false && color == _greenString && _gameRound >= 2)
        {
            _interSpeedBoost = true;
            _ball.GetComponent<Ball>().set_SpeedBoost();
        }

        //first brick hit on bottom row, round 2?
        else if (_outerSpeedBoost is false && color == _yellowString && _gameRound >= 2)
        {
            _outerSpeedBoost = true;
            _ball.GetComponent<Ball>().set_SpeedBoost();
        }

        if (_boostCounter < _hit12SpeedBoost)
        {
            _boostCounter += 1;
            if (_boostCounter == _hit4SpeedBoost || _boostCounter == _hit12SpeedBoost)
            {
                _ball.GetComponent<Ball>().set_SpeedBoost();
            }
        }
    }

    public int PaddleBallBoost(){
        int boolBoost =_inPlayBricksCounter < _lowBrickCount ? 1 : 0;
        return boolBoost;
    }

    private void ResetLifeBools()
    { _lifeRed = _lifeOrange = _lifeYellow = _lifeGreen = 0; }
    
    public void EndLife(){
        // notify Agent dead ball
        if (_agentGame) {_paddle.GetComponent<PlayGameAgent>().DeadBall();}

        // update lives
        _lives -= 1;
        ui.UpdateLivesUI(_lives);
        
        // update boosts and combo states
        _outerSpeedBoost = false;
        _interSpeedBoost = false;
        _boostCounter = 0;
        InstantiateBall();
        /*
        if (_lives == 0){
            _gameOver = true;
            _gameCompleted = false;
            Freeze();
            SetWaitingNotice();
            OnGameOver?.Invoke(this._score, (int)this._currentTime);
        }
        else {
            InstantiateBall();
        }
        */
    }

    public void ScoreCard()
    {
        Debug.Log("*** GAME OVER: " + name + " *** ");
        Debug.Log("TIME: " + _currentTime);
        Debug.Log("SCORE: " + _score);
        Debug.Log("LIVES: " + _lives);
        Debug.Log("CEILING TIME " + _ceilingTime);
        //Debug.Log("ROUND 2 TIME " + _round2Time);
        Debug.Log("BRICK HIT " + _bricksDestroyed);
        Debug.Log("ROOF COMBO " + _comboRoofCount);
        Debug.Log("BRICK COMBO: " + _comboBrickCount);
        Debug.Log("PADDLE HIT" + _paddleBounce);
        Debug.Log("PADDLE COMBO: " + _comboPaddleCount);
        Debug.Log("*** END REPORT *** ");
    }

    public List<List<GameObject>> Create_inPlayBricks(int rowC, int colC)
    {
        List<List<GameObject>>nestedNullList = new List<List<GameObject>>();
        for (var r = 0; r < rowC; r++) { nestedNullList.Add(new List<GameObject>(new GameObject[colC])); }
        return nestedNullList;
    }
    
    public void Add_inPlayBricks(GameObject brick, int brickRow, int brickCol)
    { _inPlayBricks[brickRow][brickCol] = brick; }

    public GameObject getBrick_inPlayBricks(int brickRow, int brickCol) 
    { return _inPlayBricks[brickRow][brickCol]; }

    public int getCounter_inPlayBricks()
    { return _inPlayBricksCounter; }

    public GameObject GetBall()
    { return _ball; }
    
    public GameObject GetPaddle()
    { return _paddle; }

    public int GetScore()
    { return _score; }
    
    public int get_colCount()
    { return _colCount; }
    
    public string get_biname()
    { return name; }

    public int get_rowCount()
    { return _rowCount; }
    
    public string get_brickColorElement(int index)
    { return _brickBuildList[index]; }

    public bool get_agentGame()
    { return _agentGame; }
    
    public int get_GameRound()
    { return _gameRound; }
    
    public bool get_2PGame()
    { return _2PGame; }

    public bool IsGameOver()
    { return _gameOver; }
    
    public void set_roofBounceState(int roofBounce)
        /*roofBounce = 1, collision from upperboundary == roof elevation
        roofBounce = 0, collision from brick or paddle*/
        { _bounceRoofState = roofBounce; }
    
    public void set_brickComboState(int comboUpdate)
        /*update consecutive ball/paddle hit bool status
        set to True at ball spawn: as next hit always paddle*/
        { _comboState = comboUpdate; } 
        
    public void increment_PaddleBounce()
    { _paddleBounce += 1; }
    

    private void InitGameVariables() {
        _agentGame = (name == _nn1GameName) || (name == _nn2GameName) || (name == _nn3GameName);
        _2PGame = name == _2PGameName;
        _lives = 99;
        ui.UpdateLivesUI(_lives);
        _score = 0;
        ui.UpdateScoreUI(_score);
        _gameRound = 1;
        _gameOver = false;
        _boostCounter = 0;
        _outerSpeedBoost = false;
        _interSpeedBoost = false;
        _comboState = 0;
        _rupturedCeiling = false;
        _comboPaddleCount = 0;
        _comboBrickCount = 0;
        _bounceRoofState = 0;
        _comboRoofCount = 0;
        _paddleBounce = 0;
        _bricksDestroyed = 0;
    }
    
    private void ExtraLifeHandler(string colorCollision)
        /*Four consecutive hits of distinct brick class (color) awards extra life*/
    {
        switch (colorCollision)
        {
            case "BrickRed":
                if (_lifeRed == 0) { _lifeRed = 1; }
                else { ResetLifeBools();}
                break;
            case "BrickOrange":
                if (_lifeOrange == 0) { _lifeOrange = 1; }
                else { ResetLifeBools();}
                break;
            case "BrickGreen":
                if (_lifeGreen == 0) { _lifeGreen = 1; }
                else { ResetLifeBools();}
                break;
            case "BrickYellow":
                if (_lifeYellow == 0) { _lifeYellow = 1; }
                else { ResetLifeBools();}
                break;
        }

        if (_lifeRed + _lifeOrange + _lifeYellow + _lifeGreen == _distinctColors)
        {
            _lives += 100;
            ui.UpdateLivesUI(_lives);
        }
    }

    public void Freeze()
    {
        _paddle.GetComponent<Paddle>().Freeze();
        _ball.GetComponent<Ball>().Freeze();
    }

    public void UnFreeze()
    {
        _paddle.GetComponent<Paddle>().Unfreeze();
        // if quit game when ball is destroyed
        if (_ball != null){
            _ball.GetComponent<Ball>().Unfreeze();
        }

    }

    private void SetWaitingNotice()
    {
        var test = transform.Find("BreakoutCanvas/WaitingNotice").GameObject();
        test.SetActive(true);
    }

    private void ClearWaitingNotice()
    {
        gameObject.transform.Find("BreakoutCanvas/WaitingNotice").GameObject().SetActive(false);
    }
    
}
