#-*-coding: utf-8 -*- 

import tensorflow as tf


def train_input_fn(train_X, train_Y, const_shuffle, batch_size):
    
    dataset = tf.data.Dataset.from_tensor_slices((dict(train_X), train_Y))

    dataset = dataset.shuffle(const_shuffle).repeat().batch(batch_size)

    return dataset.make_one_shot_iterator().get_next()

def eval_input_fn(train_X, train_Y, batch_size):
    """An input function for evaluation or prediction"""

    train_X=dict(train_X)
     
    if train_Y is None:
        # No train_Y, use only train_X.
        inputs = train_X
    else:
        inputs = (train_X, train_Y)
     
 
    # Convert the inputs to a Dataset.
    # dataset = tf.data.Dataset.from_tensor_slices(inputs)
    # dataset = tf.data.Dataset.from_tensor_slices((dict(train_X), train_Y))
    dataset = tf.data.Dataset.from_tensor_slices(inputs)
 
    # Batch the examples
    assert batch_size is not None, "batch_size must not be None"
    dataset = dataset.batch(batch_size)
    
    return dataset.make_one_shot_iterator().get_next()