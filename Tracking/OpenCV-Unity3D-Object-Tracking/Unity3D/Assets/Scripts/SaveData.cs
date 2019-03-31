using System;
using System.Collections.Generic;
using UnityEngine;

[Serializable]
public class SaveData
{
    public string name;
    public int armour;
    public List<string> items;

    public Vector3 position;
    public Quaternion rotation;
}
