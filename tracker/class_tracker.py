from utils.utils import validate_json
from utils.utils import read_box_json_file
from utils.config import load_config 
from utils.config import get_logger
from tqdm import tqdm
import numpy as np
import json
import cv2
import os



LOG   = get_logger('tracking-player')
cf    = load_config("initial_config.yaml")


class MultiTracker():
  """
  Class which loads, validates, initialize, run and validates tracked objects

  Parameters
  ----------
  input_video_path: str, filepath for input mp4 and mkv format video
  input_boxes_json_path: str, filepath for input json file with bbox data
  output_video_path:  str, filepath for output annotated mp4 video
  """


  def __init__(self,
                input_video_path,
                output_video_path,
                input_boxes_json_path
                ):

    self.input_video_path = input_video_path
    self.output_video_path = output_video_path
    self.input_boxes_json_path = input_boxes_json_path

  def load_data(self):
    '''
     Load and validate video and json files
    '''
    LOG.info('Validation formats of inputs files.')  
    assert (self.input_video_path[-3:]=='mp4' or 
            self.input_video_path[-3:]=='mkv'), \
            'video should be .mp4 or .mkv format'

    assert self.input_boxes_json_path[-4:]=='json',\
           'file coordenate should be a.json file'      

    LOG.info('Start load video.')    
    self.video_in = cv2.VideoCapture(self.input_video_path)
    self.total_frame =int(self.video_in.get(cv2.CAP_PROP_FRAME_COUNT))
    
    LOG.info('Validate video file.')
    assert int(self.video_in.get(cv2.CAP_PROP_FRAME_COUNT))>0,\
            "Object's has no frame."

    LOG.info('Start load json file.') 
    bbox_json = read_box_json_file(self.input_boxes_json_path)

    LOG.info('Validate json file.')
    try:
      self.dicts_bbox = []    
      for box in bbox_json:
        self.dicts_bbox.append(validate_json(box))  
    except Exception as e:
      LOG.error(e)

    LOG.info('Read and Validate completed!!')    

  def initialize_multitracker(self):
    '''
    Initializes multitracker and define CSRT algorithm.
    '''
    LOG.info('Initialize Algorithm CSRT')
    self.trackers = cv2.MultiTracker_create()
    _, init_frame = self.video_in.read()

    for bb in tuple(self.dicts_bbox):
      self.trackers.add( cv2.TrackerCSRT_create(),init_frame,tuple(bb['coordinates']))

    LOG.info(f'There are { len(self.dicts_bbox)} objects to track.')

  def _get_dimensions_video(self):
    '''
    Gets the the dimensions of input video.
    Returns
    -------
    Tuple of integers (width and height)
    '''
    width = int(self.video_in.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(self.video_in.get(cv2.CAP_PROP_FRAME_HEIGHT))

    return width, height

  def create_videowriter_for_tracked(self):
    '''
    Creates VideoWriter for tracked video.
    '''
    cap_fps = self.video_in.get(cv2.CAP_PROP_FPS)
    frame_width, frame_height = self._get_dimensions_video()

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    self.video_out = cv2.VideoWriter(
      self.output_video_path,fourcc, cap_fps,  (frame_width, frame_height)
      )
          
  def run_multitracker(self):
    '''
    Runs the algorithm for all frames and objects
    '''   
    LOG.info('Start to track objects ...')
    pbar = tqdm(total=self.total_frame , desc ="Processing each Frame")

    i = 0
    self.correct_frame_tracking = 0
    while True:

      ret, frame = self.video_in.read()
      if ret == True:

          timer = cv2.getTickCount()
          ok, boxes = self.trackers.update(frame)
          fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
          
          if ok:
              self.correct_frame_tracking +=1
              for bbox in boxes:
                  
                  p1 = (int(bbox[0]), int(bbox[1]))
                  p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                  cv2.rectangle(frame, p1, p2, tuple(cf['color_box']), 2, 1)

          else :

            cv2.putText(frame, "Tracking failure detected", tuple(cf['org_failure']),
            cv2.FONT_HERSHEY_SIMPLEX, cf['fontScale'],tuple(cf['color_failure']),cf['thickness']
            )

          cv2.putText(frame, "CSRT Tracker", tuple(cf['org_tracker']),
           cv2.FONT_HERSHEY_SIMPLEX, cf['fontScale'],  tuple(cf['color_tracker']),cf['thickness']
           )
          cv2.putText(frame, "FPS : " + str(int(fps)), tuple(cf['org_fps']),
           cv2.FONT_HERSHEY_SIMPLEX,cf['fontScale'], tuple(cf['color_fps']), cf['thickness']
           )

          self.video_out.write(frame)
          pbar.update(1)
          i=i+1
          
      else:
       break  
    
    self.video_in.release()
    self.video_out.release()

  def validate_video_tracked(self):
    '''
    It is validad how many frames weres successfully tracked.
    '''
    percentage_frame = round(self.correct_frame_tracking/self.total_frame*100,2) 
    LOG.info(f'{percentage_frame}% frames were successfully processed.')