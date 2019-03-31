using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;

public class JsonCharacterSaver : MonoBehaviour
{
    public GameObject characterData;
    string dataPath;

    void Start()
    {
        dataPath = Path.Combine(Application.persistentDataPath, "CharacterData.txt");
    }

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.S))
            SaveCharacter(characterData, dataPath);

        if (Input.GetKeyDown(KeyCode.L))
            characterData = LoadCharacter(dataPath);
    }

    static void SaveCharacter(GameObject data, string path)
    {
        string jsonString = JsonUtility.ToJson(data);

        using (StreamWriter streamWriter = File.CreateText(path))
        {
            streamWriter.Write(jsonString);
        }
    }

    static GameObject LoadCharacter(string path)
    {
        using (StreamReader streamReader = File.OpenText(path))
        {
            string jsonString = streamReader.ReadToEnd();
            return JsonUtility.FromJson<GameObject>(jsonString);
        }
    }
}
