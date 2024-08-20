using System.Collections;
using System.Collections.Generic;
using FMOD.Studio;
using UnityEngine;
using FMODUnity;

public class AudioManager : MonoBehaviour
{
    public static AudioManager instance;
    public BreakoutInstance bi;
    public static StudioEventEmitter speaker;

    [SerializeField] private EventReference _paddleSound;
    [SerializeField] private EventReference _wallSound;
    [SerializeField] private EventReference _brickSound;
    
    private int intensity = 0;
    
    // Start is called before the first frame update
    void Awake()
    {
       //bi = transform.parent.gameObject.GetComponent<BreakoutInstance>();
    }
    
    void Start()
    {
        StartCoroutine(wait());
        if (instance != null)
        {
            Debug.Log("Missing audio manager");
        }

        instance = this;
        speaker = this.GetComponent<StudioEventEmitter>();
        AddIntensity(1);
    }

    IEnumerator wait()
    {
        yield return new WaitForSeconds(1);
    }
    

    public void AddIntensity(int amount)
    {
        intensity = intensity + amount;
        speaker.SetParameter("Intensity", intensity);
    }
    
    public void ResetIntensity()
    {
        intensity = 1;
        speaker.SetParameter("Intensity", intensity);
    }

    public void PlayWallSound()
    {
        PlayOneShot(_wallSound);
    }

    public void PlayBrickSound()
    {
        PlayOneShot(_brickSound);
    }
    
    public void PlayPaddleSound()
    {
        PlayOneShot(_paddleSound);
    }
    
    public void PlayOneShot(EventReference sound)
    {
        RuntimeManager.PlayOneShot(sound);
    }
}