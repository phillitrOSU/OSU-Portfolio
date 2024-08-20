using UnityEngine;
using UnityEngine.SceneManagement;

public class MainMenu : MonoBehaviour
{

     //SpeedTutor (2021, Jul 8). MAIN MENU in Unity Best Main Menu Tutorial 2024. YouTube.
     //https://www.youtube.com/watch?v=Cq_Nnw_LwnI
     private string SingleGame = "SingleGame";
     private string VsGameNN1 = "VsGameNN1";
    private string VsGameNN2 = "VsGameNN2";
    private string VsGameNN3 = "VsGameNN3";
    private string AgentFarm = "AgentFarm";
     public void SingleGameExec()
     {
         SceneManager.LoadScene(SingleGame);
     }
     
     public void NN1Exec()
     {
         SceneManager.LoadScene(VsGameNN1);
     }

     public void NN2Exec()
     {
         SceneManager.LoadScene(VsGameNN2);
     }


     public void NN3Exec()
     {
         SceneManager.LoadScene(VsGameNN3);
     }

    public void AgentFarmExec()
     {
         SceneManager.LoadScene(AgentFarm);
     }


     public void ExitButton()
     {
         Application.Quit();
     }
}
