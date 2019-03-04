import os
import tensorflow as tf
from collections import Counter
from typing import List, Tuple, Any


data_filepath = 'dummy'
labels = []
label_balanced_param = []


def __set_label_info(beta: float) -> None:
    """
    :param beta: hypter parameter of class-balanced softmax (ref: https://arxiv.org/abs/1901.05555)
    """
    with tf.gfile.Open(os.path.join(data_filepath), "r") as f:
        label_counter = Counter(line.split('\t')[0] for line in f.read().split('\n'))
    labels = sorted(list(filter(lambda x: x, label_counter)))
    for label in labels:
        label_balanced_param.append(10 * (1 - beta) / (1 - pow(beta, label_counter[label])))


def get_output(self, input_tensor: tf.keras.layers.Layer, label_ids: List[List[int]]) -> Tuple[Any, Any, Any]:
    log_probs = tf.nn.log_softmax(input_tensor, axis=-1)
    labels = tf.reshape(label_ids, [-1])

    # multuply label_sample_nums for cross-balanced loss
    one_hot_labels = tf.one_hot(labels, depth=len(labels), dtype=tf.float32) * label_balanced_param

    per_exampe_loss = -tf.reduce_sum(one_hot_labels * log_probs, axis=-1)
    loss = tf.reduce_mean(per_exampe_loss)
    return loss, per_exampe_loss, log_probs
