using UnityEngine;
using System;
using System.Collections;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

public class SocketClient : MonoBehaviour {

	// Use this for initialization

	public GameObject hero;
	private float xPos = 10.0f;
	private float yPos = 10.0f;
	private float zPos = 10.0f;

	Thread receiveThread;
	UdpClient client;
	public int port;

    //info

    public string lastReceivedUDPPacket = "";
	public string allReceivedUDPPackets = "";

	void Start () {
		init();
	}

	void OnGUI(){
		Rect  rectObj=new Rect (40,10,200,400);
		
		GUIStyle  style  = new GUIStyle ();
		
		style .alignment  = TextAnchor.UpperLeft;
		
		GUI .Box (rectObj,"# UDPReceive\n127.0.0.1 "+port +" #\n"
		          
		          //+ "shell> nc -u 127.0.0.1 : "+port +" \n"
		          
		          + "\nLast Packet: \n"+ lastReceivedUDPPacket
		          
		          //+ "\n\nAll Messages: \n"+allReceivedUDPPackets
		          
		          ,style );

	}

	private void init(){
		print ("UPDSend.init()");

		port = 5065;

		print ("Sending to 127.0.0.1 : " + port);

		receiveThread = new Thread (new ThreadStart(ReceiveData));
		receiveThread.IsBackground = true;
		receiveThread.Start ();

	}

	private void ReceiveData(){
		client = new UdpClient (port);
		while (true) {
			try{
				IPEndPoint anyIP = new IPEndPoint(IPAddress.Parse("127.0.0.1"), port);
				byte[] data = client.Receive(ref anyIP);
				print (data);
				string text = Encoding.UTF8.GetString(data);
				string [] multitext = text.Split(new Char [] {','});
				print (">> " + text);
				lastReceivedUDPPacket=text;
				//lastReceivedUDPPacket=text;
				allReceivedUDPPackets=allReceivedUDPPackets+text;
				xPos = float.Parse(multitext[0]);
				xPos *= 0.021818f;
				yPos = float.Parse(multitext[1]);
				yPos *= 0.021818f;
				zPos = float.Parse(multitext[2]);
				zPos *= 0.021818f;
			}catch(Exception e){
				print (e.ToString());
			}
		}
	}

	public string getLatestUDPPacket(){
		allReceivedUDPPackets = "";
		return lastReceivedUDPPacket;
	}
	
	// Update is called once per frame
	void Update () {
		hero.transform.position = new Vector3(xPos-6.0f,-3,0);
		//hero.transform.position = new Vector3(xPos-6.0f,yPos-6.0f,zPos-6.0f);
		//hero.transform.position = new Vector3(10,-3,0);

	}

	void OnApplicationQuit(){
		if (receiveThread != null) {
			receiveThread.Abort();
			Debug.Log(receiveThread.IsAlive); //must be false
		}
	}
}
