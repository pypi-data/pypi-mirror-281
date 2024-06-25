import tensorflow as tf

def ctc_decode(predictions, max_length):
    input_length = tf.ones(len(predictions)) * predictions.shape[1]
    preds_decoded = tf.keras.backend.ctc_decode(
        predictions,
        input_length = input_length,
        greedy = True,
    )[0][0][:, :max_length]
    
    return tf.where(
        preds_decoded == tf.cast(1, tf.int64),
        tf.cast(-1, tf.int64), # Treat [UNK] token same as blank label
        preds_decoded
    )

def tokens2sparse(batch_tokens):
    idxs = tf.where(tf.logical_and(
        batch_tokens != 0, # For [PAD] token
        batch_tokens != -1 # For blank label if use_ctc_decode 
    ))
    return tf.SparseTensor(
        tf.cast(idxs, tf.int64),
        tf.gather_nd(batch_tokens, idxs),
        tf.cast(tf.shape(batch_tokens), tf.int64)
    )

def sparse2dense(tensor, shape):
    tensor = tf.sparse.reset_shape(tensor, shape)
    tensor = tf.sparse.to_dense(tensor, default_value=-1)
    tensor = tf.cast(tensor, tf.float32)
    return tensor