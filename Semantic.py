import time

import pandas
import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re
import seaborn as sns
from tensorflow.python.client import session

start_timeModule = time.time()
module_url = "https://tfhub.dev/google/universal-sentence-encoder/2" #@param ["https://tfhub.dev/google/universal-sentence-encoder/2", "https://tfhub.dev/google/universal-sentence-encoder-large/3"]
# Import the Universal Sentence Encoder's TF Hub module
embed = hub.Module(module_url)
print("--- %s seconds in loading module ---" % (time.time() - start_timeModule))
start_time = time.time()



def tf_sim(text1, text2):
    # Reduce logging output.
    tf.logging.set_verbosity(tf.logging.ERROR)

    sim_input1 = tf.placeholder(tf.string, shape=(None), name="sim_input1")
    sim_input2 = tf.placeholder(tf.string, shape=(None), name="sim_input2")

    embedding1 = embed([sim_input1])
    embedding2 = embed([sim_input2])

    encode1 = tf.nn.l2_normalize(embedding1, axis=1)
    encode2 = tf.nn.l2_normalize(embedding2, axis=1)
    sim_scores = 1.0 - tf.acos(tf.reduce_sum(tf.multiply(encode1, encode2), axis=1))

    init_vars = tf.global_variables_initializer()
    init_tables = tf.tables_initializer()

    with tf.Session() as sess:
        sess.run([init_vars, init_tables])
        evaluatedSimSimalirity = sess.run(sim_scores, feed_dict={sim_input1: text1, sim_input2: text2})
        print (evaluatedSimSimalirity)
tf_sim('Glad to find a walk in clinic conveniently located in the PATH right by work. Its a large walk in clinic and friends have said that they havent had to wait very long. I arrived right before lunch hour and waited for around an hour which wasnt too bad. The place is clean the staff was efficient and the doctor was friendly. So glad to have found this place so close to work.',
       'So rumour has it they make $10000 a day - can anyone please confirm this? After all the hype i HAD to try it out. I planned a whole lunch hour to get myself there and stand in line did thorough research on what to try - i dont work too close so i needed to get this right. The long line up can be discouraging however they have a car assembly line like production line making those sweet lunch boxes so fear not youll make it to browsing the internet at your desk back on time! (a) Lima box - my favourite! loved the vinaigrette and all the toppings - had it with quinoa. (b) Sparta box - with brown rice. I wasnt too crazy about it however i am the only one i know who did not like it as much. Its a GReek salad with rice or quinoa - your choice. Cherry tomatoes get cucumber and dressing. Wh')

print("--- %s seconds ---" % (time.time() - start_time))
