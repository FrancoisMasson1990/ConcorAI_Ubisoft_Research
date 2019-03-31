using UnityEngine;
using System.Collections;
using System.IO;

public class UPyPlotExampleSender : MonoBehaviour {

    [UPyPlot.UPyPlotController.UPyProbe] // Add probe so this value will be plotted.
    private float rotationX;

    [UPyPlot.UPyPlotController.UPyProbe] // Add probe so this value will be plotted.
    private float rotationY;

    [UPyPlot.UPyPlotController.UPyProbe] // Add probe so this value will be plotted.
    private float rotationZ;

    //[UPyPlot.UPyPlotController.UPyProbe] // Add probe so this value will be plotted.
    //private float rotationW;

    [UPyPlot.UPyPlotController.UPyProbe] // Add probe so this value will be plotted.
    private float timestamp;

    void Update () { // Some example code that makes the values change in the plot.


        Vector3 position = transform.position;
        Quaternion rotation = transform.rotation;

        Vector3 angles = rotation.eulerAngles;
        rotationX = angles.x;
        rotationY = angles.y;
        rotationZ = angles.z;

        //rotationX = rotation.x;
        //rotationY = rotation.y;
        //rotationZ = rotation.z;
        //rotationW = rotation.w;
        
        timestamp = Time.time; // Time ellapsed since the animation starts (in sec)
    }
}
