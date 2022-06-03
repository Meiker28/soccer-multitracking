# soccer-multitracking

## Overview

Football is the most followed sports across the world, in recent years there has been as increasing interest in sport analytics side of this sport. In this project my goal is to develop a system using computer vision techniques that allows tracking of specific players in a video.

## Project Organization

```.
├─────── configs
│              └──────── logging_config.yaml         <--- Project Log Settings     
├─────── data
│            ├────────initial_conditions2.json       <--- Inputs for system, video and json files
│            ├────────initial_conditions.json
│            ├────────input2.mp4
│            └────────input.mkv
├───────docker-compose.yml                           <--- docker-compose file
├───────dockerfile                                   <--- docker image file
├─────── main.py                                     <--- Script to run the tracker 
├───────notebook
│           └ experiments_multiple_algorithms.ipynb  <--- Testing algorithms
├─────── requirements.txt                            <--- The requirements file for reproducing analysis
├───────tracker
│           ├──────── algorithm_tracker.py           <--- Script to setup tracker 
│           ├──────── class_tracker.py               <--- 
│           ├──────── multi_object_tracker.py        <---
└─────── utils
            ├────────colors.py                       <---
            ├────────config.py                       <--- Functions for log and 
            └────────utils.py                        <--- useful functions

```

## Approach
### Algorithms for Tracking

These four algorithms found within Opencv were compared:

- CSRT
- KCF
- MedianFlow
- Mosse
for more information see

[]https://broutonlab.com/blog/opencv-object-tracking

## Experiment

### Example video 1

After using the four algorithms these are the results:

Algorithm: CSRT

![output_CSRT](https://user-images.githubusercontent.com/33854300/171506937-0de43180-d5fb-4f52-8f9a-c03554ee20af.gif)

Algorithm: KCF

![output_KCF](https://user-images.githubusercontent.com/33854300/171512221-8b729864-2dd2-484a-ac56-a5ff69991958.gif)

Algorithm: MEDIANFLOW

![output_MEDIANFLOW](https://user-images.githubusercontent.com/33854300/171512288-8318ee3f-c065-4553-892b-f30efdab3930.gif)

Algorithm: MOSSE

![output_MOSSE](https://user-images.githubusercontent.com/33854300/171512327-473ac09a-d031-432b-ba5c-bbcad3b451d1.gif)

As you can see the Medianflow and Mosse algorithms have a
considerable FPS but they cannot detect the players correctly, on the other hand KCF manages to perform much better although in the last frames it is lost, finally we have CSRT that does manage to track all the frames of the video. 

### Example video 2


Now we are going to test these last two algorithms in another video to see how robust they are.

Algorithm: CSRT

![output2_CSRT (1)(1)](https://user-images.githubusercontent.com/33854300/171512376-eafe2c99-b093-404d-8cfa-2a7a8232543d.gif)

Algorithm: KFC

![output2_KCF (1)](https://user-images.githubusercontent.com/33854300/171512384-15dbafe2-6f4b-439d-8002-72fefea5501c.gif)

In this video we have to track two players from the same team and as a result the KCF algorithm gives worse results than the previous example while the CSRT algorithm manages to track correctly at the cost of very low Fps.

Now we are going to implement the CSRT algorithm with docker for use in any environment.

## Usage

After cloning the repo just build the docker image

```
docker-compose build tracker
```


```
docker-compose run tracker \
        -input_path <input video filepath> \
        -input_bbox_path <input bbox json filepath> \
        -output_path <output video filepath> \
```





For example 

```
docker run -v "$PWD":/app tracker:latest \
        -input_path /app/data/input.mkv \
        -input_bbox_path /app/data/initial_conditions.json \
        -output_path /app/output_tracked.mp4
```
