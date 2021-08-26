import collections
import operator 
import numpy as np

Class = collections.namedtuple('Class', ['id', 'score'])

def input_details(interpreter, key):
    """Returns input details by specified key."""
    return interpreter.get_input_details()[0][key]

def input_size(interpreter):
    """Returns input image size as (width, height) tuple."""
    _, height, width, _ = input_details(interpreter, 'shape')
    return width, height

def input_tensor(interpreter):
    """Returns input tensor view as numpy array of shape (height, width, 3)."""
    tensor_index = input_details(interpreter, 'index')
    return interpreter.tensor(tensor_index)()[0]

def output_tensor(interpreter, dequantize=True):

    output_details = interpreter.get_output_details()[0]
    output_data = np.squeeze(interpreter.tensor(output_details['index'])())

    if dequantize and np.issubdtype(output_details['dtype'], np.integer):
        scale, zero_point = output_details['quantization']
        return scale * (output_data - zero_point)

    return output_data


def set_input(interpreter, data):
    input_tensor(interpreter)[:,:] = data

def get_output(interpreter, top_k=1, score_threshold=0.0):
  """Returns no more than top_k classes with score >= score_threshold."""
  scores = output_tensor(interpreter)
  classes = [
      Class(i, scores[i])
      for i in np.argpartition(scores, -top_k)[-top_k:]
      if scores[i] >= score_threshold
  ]
  return sorted(classes, key=operator.itemgetter(1), reverse=True)