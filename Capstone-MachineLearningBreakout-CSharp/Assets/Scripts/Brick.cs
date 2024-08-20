using System;
using System.Collections;
using System.Collections.Generic;
using FMODUnity;
using Unity.VisualScripting;
using UnityEngine;
using Random = System.Random;

public class Brick: MonoBehaviour
{
    public BreakoutInstance bi;
    private SpriteRenderer _spriteRenderer;
    private Color _color;
    private int _myRow;
    private int _myCol;
    private int _myGameRound;
    private Vector2 _myPosition;
    private string _myString;
    
    private void Awake()
    {
        bi = transform.parent.parent.gameObject.GetComponent<BreakoutInstance>();
    }
    private void Start()
    { 
        _spriteRenderer = GetComponent<SpriteRenderer>();
        _spriteRenderer.color = this._color;
    }

    public float rng1() { return UnityEngine.Random.Range(.5f, 1f); }
    public float rng2() { return UnityEngine.Random.Range(.1f, .8f); }
    public float rng3() { return UnityEngine.Random.Range(0f, .5f); }
    
    public void Set_Color(string rowColor)
    /*Cannot determine how to case "String" as a getter string from bi*/
    {
        Set_String(rowColor);
        switch (rowColor)
        // new Color(0f, .5f, 1f
        // new Color(1f, .5f, 1f);
        // new Color(.8f, 0f, .8f);
        // new Color(0f, .8f, .5f);
        { 
            case "BrickRed":
                this._color = _myGameRound < 2 ? new Color(.7f, .2f, .2f) : new Color(1f, rng2(), rng2());
                break;
            case "BrickOrange":
                this._color = _myGameRound < 2 ? new Color(.8f, .5f, 0) : new Color(rng2(), 1f, rng2());
                break;
            case "BrickGreen":
                this._color = _myGameRound < 2 ? new Color(0f, .5f, 0f) : new Color(rng3(), rng2(), 1f);
                break;
            case "BrickYellow":
                this._color = _myGameRound < 2 ? new Color(.7f, .7f, 0) : new Color(rng1(), rng3(), rng1());
                break;
        }
    }
    
    public void Set_String(string colorString)
        /*writes to brick object its position relative to other bricks vertically 0-7*/
    { this._myString = colorString; }
    
    public void Set_Row(int row)
    /*writes to brick object its position relative to other bricks vertically 0-7*/
    { this._myRow = row; }
    
    public void Set_GameRound(int gameRound)
        /*writes to brick object its position relative to other bricks vertically 0-7*/
    { this._myGameRound = gameRound; }

    public void Set_Column(int col)
    /*writes to brick object its position relative to other bricks horizontally 0-13*/
    { this._myCol = col; }

    public void OnCollisionEnter2D(Collision2D collision)
    {
        //AudioManager.instance.PlayBrickSound();
        if (collision.gameObject.GetComponent<Ball>())
        {
            int myRowtemp = _myRow;
            int myColtemp = _myCol;
            Destroy(gameObject);
            bi.BrickCollision(_myString, myRowtemp, myColtemp);
        }
    }
}
