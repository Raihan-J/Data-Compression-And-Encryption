!pip3 install ffmpeg
!pip3 install -U kora


from kora.drive import upload_public
from IPython.display import HTML
from IPython.display import Audio
from IPython.display import Image, display
from scipy.io import wavfile


import tensorflow as tf
tf.test.gpu_device_name()


#Sample Video - 1
!rm Fpv.mp4*
!wget https://res.cloudinary.com/dtwr5vm0s/video/upload/v1599135625/Colab/Fpv.mp4

#Sample Watermark
!rm MyPost.*
!wget https://res.cloudinary.com/dtwr5vm0s/image/upload/v1599630860/Colab/MyPost.png

#Sample Video - 2
#!rm Carfpv.*
#!wget https://res.cloudinary.com/dtwr5vm0s/video/upload/v1599639196/Colab/Carfpv.mp4


hhhhhhh
