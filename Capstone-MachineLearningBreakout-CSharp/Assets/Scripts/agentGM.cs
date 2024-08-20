using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using TMPro;
using Unity.VisualScripting;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;

public class AgentParty : MonoBehaviour
{
    public static Action FreezeBreakouts;
    public static Action ThawBreakouts;
    static public GameObject Instance;
    
     public void ReturntoMainMenu_Party()
     {
         SceneManager.LoadScene("MainMenu");
     }

}
