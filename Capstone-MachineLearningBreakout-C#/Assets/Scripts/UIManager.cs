using TMPro;
using UnityEngine;

public class UIManager : MonoBehaviour
{
    // initialize objects
    public TextMeshProUGUI scoreText;
    public TextMeshProUGUI livesText;
    public TextMeshProUGUI timerText;

    public void UpdateLivesUI(int lives)
    {
        switch (lives)
        { 
            case < 0:
                livesText.text = "RIP";
                break;
            case < 10:
                livesText.text = "00" + lives.ToString();
                break;
            case < 100:
                livesText.text = "0" + lives.ToString();
                break; 
            default:
                livesText.text = lives.ToString();
                break;
        }
    }
    
    public void UpdateScoreUI(int score)
    {
        //update UI
        
        switch (score)
        { 
            case < 10:
                scoreText.text = "000" +  score.ToString();
                break;
            case < 100:
                scoreText.text = "00" +  score.ToString();
                break;
            case < 1000:
                scoreText.text = "0" +  score.ToString();
                break;
            default:
                scoreText.text = score.ToString();
                break;
        }
    }
    
    public void UpdateTimerUI(float countdown)
    {
        //update UI
        if (countdown > 0f)
        {
            timerText.text = countdown.ToString("000");      
        }
        else
        {
            timerText.text = "000";
        }
    }
}
    