using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using TMPro;
using Unity.VisualScripting;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;

public class GameManager : MonoBehaviour
{
    public static Action FreezeBreakouts;
    public static Action ThawBreakouts;
    
    static public GameObject Instance;
    private GameObject _canvas;
    private GameObject _pauseMenu;
    private GameObject _completedMenu;

    private List<BreakoutInstance> _breakoutInstances;
    private bool _gameIsPaused = false;
   
    private void OnEnable()
    {
        BreakoutInstance.OnGameOver += CheckAllGameOver;
        BreakoutInstance.OnGameCompleted += GameCompleted;
    }

    private void OnDisable()
    {
        BreakoutInstance.OnGameOver -= CheckAllGameOver;
        BreakoutInstance.OnGameCompleted -= GameCompleted;
    }
    
    void Start()
    {
        _canvas = gameObject.transform.Find("Canvas").GameObject();
        _pauseMenu = gameObject.transform.Find("Canvas/PauseMenu").GameObject();
        _completedMenu = gameObject.transform.Find("Canvas/CompletedMenu").GameObject();
        _canvas.SetActive(true);
        _breakoutInstances = GetBreakoutInstances();
    }

    private void Update()
    {
        CheckForPause();
    }

    private void CheckForPause()
    {
        if (Input.GetKeyDown(KeyCode.Escape))
        {
            if (!_gameIsPaused)
            {
                FreezeBreakouts?.Invoke();
                Time.timeScale = 0;
                _pauseMenu.SetActive(true);
                _gameIsPaused = true;
            }
            else
            {
                ThawBreakouts?.Invoke();
                Time.timeScale = 1;
                _pauseMenu.SetActive(false);
                _gameIsPaused = false;
            }
        }
    }

    private void CheckAllGameOver(int score, int time)
    {
        if (_breakoutInstances.Any(i => !i.IsGameOver()))
        {
            return;
        }
        
        FreezeBreakouts?.Invoke();
        BreakoutInstance highestScorer = HighestScoringInstance();
        GameOver(highestScorer);

    }

    private BreakoutInstance HighestScoringInstance()
    {
        BreakoutInstance highestScorer = _breakoutInstances[0];
        foreach (var instance in _breakoutInstances)
        {
            if (instance.GetScore() > highestScorer.GetScore())
            {
                highestScorer = instance;
            }
        }

        return highestScorer;
    }
    
    private void GameOver(BreakoutInstance instance)
    {
        _completedMenu.SetActive(true);
        TextMeshProUGUI title = _completedMenu.transform.Find("Title").GetComponent<TextMeshProUGUI>();
        TextMeshProUGUI results = _completedMenu.transform.Find("Results").GetComponent<TextMeshProUGUI>();
        title.SetText("Game\nOver");
        string winnerAnnouncement = "";
        if (_breakoutInstances.Count > 1)
        {
             winnerAnnouncement = "Highest Score: Player " + instance.playerID + "!\n\n";
        }
        results.SetText(winnerAnnouncement + 
                        "Score: " + instance.GetScore() +
                        "\n\nTime: " + (1000 - instance._currentTime)); 
        Time.timeScale = 0;
    }

    private void GameCompleted(bool agentGame, bool MultiGame, int score, int fTime, int rTime, int cTime,
     int lives, int cRoof, int cBrick, int wPaddle)
    {
        _completedMenu.SetActive(true);
        TextMeshProUGUI title = _completedMenu.transform.Find("Title").GetComponent<TextMeshProUGUI>();
        TextMeshProUGUI results = _completedMenu.transform.Find("Results").GetComponent<TextMeshProUGUI>();
        if (agentGame){
            title.SetText("AI\nBreakout\nComplete!");
        }
        else{
            title.SetText("Player\nBreakout\nComplete");
        }

        if (MultiGame || agentGame){
            results.SetText("Score:       " + score +
                "\nLives:       " + lives +
                "\n\nFinish Time: " + fTime +
                "\nRound2 Time: " + rTime +
                "\nBrkOut Time: " + cTime +
                "\n\nRoof Combo:  " + cRoof +
                "\nBrick Combo: " + cBrick +
                "\nBrick Miss:  " + wPaddle +
                "\n\nPress ESC to" +
                "\nResume GamePlay");
        } else {
        results.SetText("\nScore:       " + score +
                        "\nLives:       " + lives +
                        "\n\nFinish Time: " + fTime +
                        "\nRound2 Time: " + rTime +
                        "\nBrkOut Time: " + cTime +
                        "\n\nRoof Combo:  " + cRoof +
                        "\nBrick Combo: " + cBrick +
                        "\nBrick Miss:  " + wPaddle);
        }
        Time.timeScale = 0;

        // results pos y = 130, font size 24
        // main menu -260

        //single player
        //pos y -60
        // font size 80

        //Results 
        // pos y 160
        // font size 36

        //Main menu pos y 180




    }

    /*
    private void GameCompleted(int score, int time, int lives)
    {
        _completedMenu.SetActive(true);
        TextMeshProUGUI title = _completedMenu.transform.Find("Title").GetComponent<TextMeshProUGUI>();
        TextMeshProUGUI results = _completedMenu.transform.Find("Results").GetComponent<TextMeshProUGUI>();
        
        title.SetText("BREAKOUT\nCOMPLETE");
        results.SetText("Score: " + score +
                        "\nTime:  " + time +
                        "\nLives: " + lives +
                        "\n\nPress ESC to Resume Play!");
        Time.timeScale = 0;
    }
    */



    private List<BreakoutInstance> GetBreakoutInstances()
    {
        var instances = FindObjectsOfType<BreakoutInstance>();
        System.Array.Sort<BreakoutInstance>(instances, (a, b) => a.playerID.CompareTo(b.playerID));
        return instances.ToList();
    }

     public void ReturntoMainMenu()
     {
        ThawBreakouts?.Invoke();
        Time.timeScale = 1;
        _pauseMenu.SetActive(false);
        _gameIsPaused = false;
         SceneManager.LoadScene("MainMenu");
     }
}
