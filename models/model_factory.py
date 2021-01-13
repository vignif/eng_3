#!/usr/bin/env python3
import os

from tensorflow.keras.models import load_model
from tensorflow.keras.models import model_from_json

import tensorflow as tf
from tensorflow.keras.optimizers import Adam, SGD, RMSprop
from tensorflow.keras.losses import categorical_crossentropy

def load_json_model(model_name, folder_path = None, weights_format = None, compile = 'default'):
   """Method to load model from architecture + weights file (json + h5 or hdf5)."""
   if folder_path: # Verify model path exists.
      if folder_path == 'models': # Convenience option, to load from model directory instead of savedmodels.
         folder_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'model')
      assert os.path.exists(folder_path), f"The model path {folder_path} does not exist."
   else: # Otherwise, load from default savedmodels directory.
      folder_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'savedmodels')

   # Verify and load model architecture from JSON file.
   json_path = os.path.join(folder_path, f'{model_name}.json')
   if not os.path.exists(json_path):
      raise FileNotFoundError(f"JSON file containing model architecture at {json_path} not found.")
   try:
      model = model_from_json(json_path)
   except Exception as e:
      raise e
   finally:
      del json_path

   # Verify and load model weights from h5 or hdf5 file.
   if weights_format: # If weight format is provided, then directly use it.
      if weights_format not in ['h5', 'hdf5']:
         raise ValueError("Weights format should be either h5 or hdf5.")
      weights_path = os.path.join(folder_path)
      if not os.path.exists(weights_path):
         raise FileNotFoundError(f"Weights file at {weights_path} not found.")
      try:
         model.load_weights(weights_path)
      except Exception as e:
         raise e
      finally:
         del weights_path
   else:
      h5_path = os.path.join(folder_path, f'{model_name}.h5')
      hdf5_path = os.path.join(folder_path, f'{model_name}.hdf5')
      if not os.path.exists(h5_path) and not os.path.exists(hdf5_path):
         raise FileNotFoundError(f"Neither an h5 ({h5_path}) or hdf5 ({hdf5_path}) weights path was found.")
      elif os.path.exists(h5_path) and os.path.exists(hdf5_path):
         raise FileExistsError(f"Both the h5 ({h5_path}) and hdf5 ({hdf5_path}) paths exist, choose one with the format option.")
      weights_path = h5_path if os.path.exists(h5_path) else hdf5_path
      try:
         model.load_weights(weights_path)
      except Exception as e:
         raise e
      finally:
         del weights_path

   # Compile model if `compile` is set to a certain setting or an optimizer.
   if compile:
      if compile == 'default': # Loss is categorical_crossentropy by default.
         model.compile(
            optimizer = Adam(),
            loss = categorical_crossentropy,
            metrics = ['accuracy']
         )
      if isinstance(compile, tf.keras.optimizers.Optimizer):
         try:
            model.compile(
               optimizer = compile,
               loss = categorical_crossentropy,
               metrics = ['accuracy']
            )
         except Exception as e:
            raise e
      else:
         raise ValueError("You have provided an invalid value for compilation, should be either 'default' or an optimizer.")

   return model


