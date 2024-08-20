using System;
using System.Runtime.CompilerServices;
using Unity.VisualScripting;
using UnityEngine;
using Object = UnityEngine.Object;

public class RowConstructor : MonoBehaviour
{
    
    //Holds the world y-coordinate position that the row's bricks will be built at
    public static float NextRowHeight;
    private static bool _isRowPositionSet = false;
    private BreakoutInstance bi;
    private GameObject _placeholder;
    private GameObject _brick;
    
    public void Awake()
    {
        bi = transform.parent.gameObject.GetComponent<BreakoutInstance>();
    }
    
    public void constructRow(GameObject brick, int numBricks, float brickHeight, float xSpacing, float ySpacing, int brickRowLevel)
    {
        if (!_isRowPositionSet)
        {
            throw new InvalidOperationException(
                "Rows must be given a starting y-position from which to begin instantiation. " +
                "Ensure that SetStartingPosition() has been called prior to constructRow().");
        }

        // Spacing argument (0 - 1). 0 = no space and all brick, 1 = all space and no brick.
        var viewportWidth = GetViewportWidth();
        var spacePerBrick = (viewportWidth * xSpacing) / (numBricks - 1);
        var brickLength = (viewportWidth / numBricks)  * (1 - xSpacing);
        
        // Set initial spawn position
        Vector3 spawnPosition = new Vector3(GetBorder("left") + brickLength/2, NextRowHeight, 0);
        
        // Spawn row of bricks left to right with proper sizing and spacing.
        for (var i = 0; i < numBricks; i++)
        {
            int brickColLevel = i;
            _brick = Instantiate(brick, transform);
            _brick.transform.localPosition = spawnPosition;
            _brick.GetComponent<Brick>().Set_Row(brickRowLevel);
            _brick.GetComponent<Brick>().Set_Column(brickColLevel);
            _brick.GetComponent<Brick>().Set_GameRound(bi.get_GameRound());
            _brick.GetComponent<Brick>().Set_Color(bi.get_brickColorElement(brickRowLevel));
            _brick.transform.localScale = new Vector3(brickLength, brickHeight, 0);
            spawnPosition = new Vector3(spawnPosition.x + brickLength + spacePerBrick, spawnPosition.y, spawnPosition.z);

            bi.Add_inPlayBricks(_brick, brickRowLevel, brickColLevel);
            
        }
        
        //Update the next row spawn to be directly below this row
        NextRowHeight += brickHeight + ySpacing;
        Object.Destroy(_placeholder);
    }

    public void SetStartingPosition(float yPos)
    {
        NextRowHeight = yPos;
        _isRowPositionSet = true;
    }

    //Explicitly sets the state of the row class to require a new beginning height before rows can start being
    //constructed. This might be hacky but I do think that it's going to enforce more safety in the game logic
    public void ClearStartingPosition()
    {
        _isRowPositionSet = false;
    }
    
    
    // Get the width of the camera viewport
    static float GetViewportWidth()
    {
        var leftBorder = GetBorder("left");
        var rightBorder = GetBorder("right");
        return rightBorder - leftBorder;
    }
    
    // Get the position of screen border: "left" or "right"
    static float GetBorder(string side)
    {
        var gameBoundariesCollider = GameObject.FindWithTag("gameBoundaries").GetComponent<EdgeCollider2D>();
        float minX = Single.MaxValue;
        float maxX = Single.MinValue;
        //Loop through the points and save the maximum and minimum x value in the array of vectors defining the screen
        foreach (var vect in gameBoundariesCollider.points)
        {
            if (vect.x < minX)
            {
                minX = vect.x;
            }

            if (vect.x > maxX)
            {
                maxX = vect.x;
            }
        }
        if(side == "left")
        {
            return minX;
        }
        else
        {
            return maxX;
        }
    }
    
}
