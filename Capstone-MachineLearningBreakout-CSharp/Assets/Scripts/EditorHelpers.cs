using System.Collections.Generic;
using TMPro;
using Unity.VisualScripting;
using UnityEngine;

//[ExecuteInEditMode]
public class EditorHelpers : MonoBehaviour
{
    private List<GameObject> canvases;
    private List<GameObject> breakoutInstances;
    private List<GameObject> boundaries;

    private void Awake()
    {
        if (breakoutInstances == null)
        {
            breakoutInstances = new List<GameObject>(GameObject.FindGameObjectsWithTag($"BreakoutInstance"));
            boundaries = new List<GameObject>();
            foreach (var instance in breakoutInstances)
            {
                boundaries.Add(instance.transform.Find("GameBoundaries/UpperBoundaries").GameObject());
            }
        }
        
        AttachUIs();
        
    }

    private void Update()
    {
        RenderLinesOnBreakoutBoundaries();
    }

    void RenderLinesOnBreakoutBoundaries()
    {
        foreach (var boundary in boundaries)
        {
            EdgeCollider2D edgeCollider = boundary.GetComponent<EdgeCollider2D>();
            LineRenderer lr = boundary.GetComponent<LineRenderer>();
            List<Vector2> points = new List<Vector2>(edgeCollider.points);
            points.Add(points[0] + new Vector2(0.128f,0f)); //Needed to make a full square
            lr.positionCount = points.Count;
            Vector3[] linePositions = new Vector3[points.Count];

            for (int i = 0; i < points.Count; i++)
            {
                linePositions[i] = new Vector3(points[i].x, points[i].y, 0f);
            }

            lr.SetPositions(linePositions);

        }
    }

    void AttachUIs()
    {
        if (!NeedsCanvases())
        {
            return;
        }

        foreach (var breakoutInstance in breakoutInstances)
        {
            GameObject newObj = new GameObject();
            newObj.transform.parent = breakoutInstance.transform; 

            newObj.name = "BreakoutCanvas";
            newObj.tag = "BreakoutCanvas";
            newObj.AddComponent<Canvas>();
            newObj.AddComponent<UIManager>();
            newObj.AddComponent<RectTransform>();
            newObj.GetComponent<RectTransform>().position = breakoutInstance.transform.position;
            newObj.GetComponent<RectTransform>().sizeDelta = new Vector2(15, 20);
            
            //Instantiate the text prefabs and attach them to the UIManager script:
            UIManager uim = newObj.GetComponent<UIManager>();
            //var lives = Instantiate(Resources.Load("livesText"), newObj.transform, false) as GameObject;
            //var score = Instantiate(Resources.Load("scoreText"), newObj.transform, false) as GameObject;
            //var timer = Instantiate(Resources.Load("timerText"), newObj.transform, false) as GameObject;

            //if (lives != null) uim.livesText = lives.GetComponent<TextMeshProUGUI>();
            //if (score != null) uim.scoreText = score.GetComponent<TextMeshProUGUI>();
            //if (timer != null) uim.timerText = timer.GetComponent<TextMeshProUGUI>();
            
        }
    } 
    

    bool NeedsCanvases()
    {
        canvases = new List<GameObject>(GameObject.FindGameObjectsWithTag($"BreakoutCanvas"));
        return canvases.Count < breakoutInstances.Count;
    }
}