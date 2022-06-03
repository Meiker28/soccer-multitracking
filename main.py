# -*- coding: utf-8 -*-
""" main.py """

from tracker.class_tracker import MultiTracker
from utils.config import get_logger
import argparse




def main():

  parser = argparse.ArgumentParser(description='tracking-player')

  parser.add_argument('-input_path', action='store',
                    type=str, help='Input video path')
  parser.add_argument('-input_bbox_path', action='store',
                    type=str, help='Input bbox json path')
  parser.add_argument('-output_path', action='store',
                    type=str, help='Output video path')

  parser.set_defaults(feature=True)
  args = parser.parse_args()


  object_tracker = MultiTracker(
    args.input_path,
    args.output_path,
    args.input_bbox_path)

  object_tracker.load_data() 
  object_tracker.initialize_multitracker() 
  object_tracker.create_videowriter_for_tracked()
  object_tracker.run_multitracker()
  object_tracker.validate_video_tracked()

if __name__ == '__main__':
  main()