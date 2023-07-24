# Face Recognition Lock
This is not a face recognition lock build from scratch. It is based on existing hardwares and softwares. It is only for a reference, unless you have the same environment. 
For lock, I am using **August Smart Wifi Lock (Gen 4)**, for software platform, I am using **home assistant** . It is a great home automation platform. The customizability is endless.  

## some notes before implementation detail
The face recognition part is actually the easy part of this project. By using exisiting model of opencv, and tons of available resources online. The hard part is actually setting up the communication between the lock and the porgram

## Implementation for Lock interaction
1. you need a computer/docker/server/raspberry pi running home assistant. 
2. you need to connect you august lock to home assistant
   - If you keep seeing undefined error during the 2 factor authentication process of august, remeber to disable the ipv6 of home assistant, that can be the reason
   - For some reason, even your device is found by home assistant, it can possibly have a offline status. It some how get fixed. But I don't know why
   - For home assistant **alternative**, it is possible use **seam api** to establish communication between progam and lock. But I still cannot figure out why the lock is offline when it is online. (This definitely need further investigation)
   - After checking the lock is operable (through seam api or home assistant), now it is possible to communicate with your lock through program
3. In home assistant, we need to create an automation to interact with the lock. 
4. choose webhook as a trigger, and door open as the action
5. Then by sending a post request to you home assistant server with the webhood id provided, we can trigger the lock to unlock. [Webhook Trigger implementation detail](https://www.home-assistant.io/docs/automation/trigger/)

## Implementation for face recognition
1. We need to get our face data and save them to a file. The dataset can be as large as you want
   - this is accomplished by the main.py
   - We cannot just take random selfies as dataset. Sometimes, Haar Cascade cannot detect your random selfie
2. In main.py, I use haar Cascade to detect faces. The minimum size of the faces is set to (120,120), it helps to eliminate some useless data
3. In each frame of the video, if a face has been detected, it will automatically saved to the faces directory as dataset, with name labeled. The amount of image stored can be configured
4. With image obtained, we can use the images to compare with real time video input. The comparison is done by **face_recognition** library. It is a easy to use version of **dlib**, which has the pre-trained model for face recognition and more.
5. Finally, we can send the unlock request to the door lock base on the comparison result
   - I set a 100s timeout for each person
     - if a person has been scanned within 100s, the door lock will not unlock twice
   - The door will not unlock unless it has successfully detect a user's face for 5 times

## some final note
- The face detection can be slow, there is two ways to speed it up (i have seen so far)
  - shrink the image size
  - only process for a half/quarter of the frame
- The request send to the home assistant webhook might not be secure
  - we can also send some encoded message by json to add a level of security
