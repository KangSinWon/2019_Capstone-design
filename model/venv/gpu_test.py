import sys
import numpy as np
import tensorflow as tf
from datetime import datetime

shape = (int(10000), int(10000))
print(tf.__version__)
with tf.device("/gpu:0"):
    random_matrix = tf.random_uniform(shape=shape, minval=0, maxval=1)
    dot_operation = tf.matmul(random_matrix, tf.transpose(random_matrix))
    sum_operation = tf.reduce_sum(dot_operation)

startTime = datetime.now()
with tf.Session(config=tf.ConfigProto(log_device_placement=True)) as session:
    result = session.run(sum_operation)
    print(result)

print("\n" * 2)
print("Time taken:", datetime.now() - startTime)
print("\n" * 2)
