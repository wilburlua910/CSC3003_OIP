
import time


#Added tflite dependencies
from Inference import classify 
import tflite_runtime.interpreter as tflite
import platform 

#Added libraries
import time
import os
import io
import picamera 
from PIL import Image

#Regex 
import re

#For the states
from enum import Enum

#Custom import 
import gpiocontrol

EDGETPU_SHARED_LIB = {
  'Linux': 'libedgetpu.so.1',
  'Darwin': 'libedgetpu.1.dylib',
  'Windows': 'edgetpu.dll'
}[platform.system()]


#Enum class to represent the 3 states
class State(Enum):
    STATE_IN_PROGRESS = 0
    STATE_ALL_CLEAN = 1
    STATE_UNCLEAN = 2


class Camera:
    #Interpreter and Label files
    interpreter = None
    labels = None
    size = None
    image_input = None

    #File paths
    labels_file = "Inference/syringe_labels.txt"
    path_to_labels = os.path.join(os.getcwd(),  labels_file)
    path_to_model = "Inference/model_edgetpu.tflite"

    def __init__(self):

       # self.interpreter = self.
       self.labels = self.load_labels(self.path_to_labels)
       self.interpreter = self.make_interpreter(self.path_to_model)
       self.interpreter.allocate_tensors()

       #Get the input size of the model from the interpreter 
       self.size = classify.input_size(self.interpreter)

    def take_photo(size):
        stream_buffer = io.BytesIO()

        with picamera.PiCamera() as camera:
            camera.capture(stream_buffer, format='jpeg')
        
        stream_buffer.seek(0)
        image = Image.open(stream_buffer)
        width, height = image.size

        #Local variables
        left = width/4
        top = height/4
        right = 3 * width/4
        bottom = 3 * height/4

        image_cropped = image.crop((left, top, right, bottom))
        image_cropped.save("Image_cropped.jpg")

        #Have to resize to fit the 
        image_cropped_resized = image_cropped.resize(size)
        return image_cropped_resized

    def run_inference(self, interpreter, size, labels):

        gpiocontrol.turn_on_ringlight()

        while (gpiocontrol.goto_next_grid()):
            image_ = Camera.take_photo(size)
            classify.set_input(interpreter= interpreter, data=image_)

            #Inferencing
            print('----- INFERENCE TIME------')

            no_of_inferences = 5
            for _ in range(no_of_inferences):
                start = time.perf_counter()
                interpreter.invoke()
                infererence_time = time.perf_counter() - start

                #args top k - 1
                #args threshold 
                classes = classify.get_output(interpreter, 1, 0.0)
                print('%.1fms' % (infererence_time * 1000))
                
                print('-------RESULTS--------')
                for klass in classes:
                    output = labels.get(klass.id, klass.id), klass.score
                    print('%s: %.5f' % (labels.get(klass.id, klass.id), klass.score))

                    if re.search("dirty_wet", output[0]):
                        #Change the state

                        gpiocontrol.turn_off_ringlight
                        gpiocontrol.return_to_rest()
                        
                        return State.STATE_UNCLEAN

        gpiocontrol.turn_off_ringlight()
        gpiocontrol.return_to_rest()
        return State.STATE_ALL_CLEAN

    def load_labels(self, path):
        with open(path, 'r', encoding= 'utf-8') as f:
            lines = f.readlines()
            if not lines:
                return {}
            if lines[0].split(' ', maxsplit=1)[0].isdigit():
                pairs = [line.split(' ', maxsplit=1) for line in lines]
                return {int(index): label.strip() for index, label in pairs}
            else:
                return {index: line.strip() for index, line in enumerate(lines)}

    def make_interpreter(self, model_file):
        model_file, *device = model_file.split('@')
        return tflite.Interpreter(
            model_path=model_file,
            experimental_delegates=[
                tflite.load_delegate(EDGETPU_SHARED_LIB,
                {'device': device[0]} if device else {})
      ])

    # cam = Camera()
    # size, interpreter, labels = cam.size, cam.interpreter, cam.labels
    # output = cam.run_inference(interpreter = interpreter, size=size, labels=labels)
    # print(output)

def main():

    cam = Camera()
    time.sleep(0.5)
    size, interpreter, labels = cam.size, cam.interpreter, cam.labels
    output = cam.run_inference(interpreter = interpreter, size=size, labels=labels)
    print(output[0], output[1])

    #if output is dirty_wet => State ?
    #if output is clean_dry => State ?

if __name__ == '__main__':
    main()






