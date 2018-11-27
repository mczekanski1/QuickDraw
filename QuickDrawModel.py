"""
A slightly modified VGG Network
"""
from AuxiliaryCNN import csv_generator, text_to_labels, get_batch
import numpy as np
import tensorflow as tf
from subprocess import check_output

# constants
DIRPATH = "/data/scratch/epeake/Google-Doodles/"
MODELPATH = "~/ML-Final-Code/qd_model/"
BATCH_SIZE = 40
HEIGHT = 256
WIDTH = 256
N_EPOCHS = 7


label_to_class = text_to_labels(DIRPATH)
class_eye = np.eye(len(label_to_class))
n_outputs = len(label_to_class)
csv_len = int(check_output('wc -l ' + DIRPATH + 'train.csv | grep -o "[0-9]\+"', shell=True))


def conv_layer_vgg(input, chanels_in, chanels_out, scope_name):
    """
    Convolutional layer for VGGNet16

    :param input: input layer
    :param chanels_in: (int)
    :param chanels_out: (int)
    :return: activation layer
    """
    with tf.name_scope(scope_name):
        W = tf.get_variable([3, 3, chanels_in, chanels_out], initializer=tf.contrib.layers.xavier_initializer(), name="W")
        b = tf.Variable(tf.constant(0.1, shape=[chanels_out]), name="B")
        conv = tf.nn.conv2d(input, W, strides=[1, 1, 1, 1], padding="SAME")
        active = tf.nn.relu(conv + b)
        return active


def conv_layer(input, filter_size, chanels_in, chanels_out, stride, pad, scope_name):
    """
    Convolutional layer for VGGNet16

    :param input: input layer
    :param chanels_in: (int)
    :param chanels_out: (int)
    :return: activation layer
    """
    with tf.name_scope(scope_name):
        W = tf.get_variable([filter_size, filter_size, chanels_in, chanels_out], initializer=tf.contrib.layers.xavier_initializer(), name="W")
        b = tf.Variable(tf.constant(0.1, shape=[chanels_out]), name="B")
        conv = tf.nn.conv2d(input, W, strides=[1, stride, stride, 1], padding=pad)
        active = tf.nn.relu(conv + b)
        return active


def cnn_model(model_type, l_r):
    learning_rate = l_r

    with tf.device("/gpu:1"):
        if model_type == "VGG":
            X = tf.placeholder("float", [None, HEIGHT, WIDTH, 1])
            Y = tf.placeholder("float", [None, n_outputs])

            conv_1_1 = conv_layer_vgg(X, 1, 64, "conv_1_1")
            conv_1_2 = conv_layer_vgg(conv_1_1, 64, 64, "conv_1_2")
            pool1 = tf.nn.max_pool(conv_1_2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME', name="pool1")

            conv_2_1 = conv_layer_vgg(pool1, 64, 128, "conv_2_1")
            conv_2_2 = conv_layer_vgg(conv_2_1, 128, 128, "conv_2_2")
            pool2 = tf.nn.max_pool(conv_2_2, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1], padding='SAME', name="pool2")

            conv_3_1 = conv_layer_vgg(pool2, 128, 256, "conv_3_1")
            conv_3_2 = conv_layer_vgg(conv_3_1, 256, 256, "conv_3_2")
            conv_3_3 = conv_layer_vgg(conv_3_2, 256, 256, "conv_3_3")
            pool3 = tf.nn.max_pool(conv_3_3, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1], padding='SAME', name="pool3")

            conv_4_1 = conv_layer_vgg(pool3, 256, 512, "conv_4_1")
            conv_4_2 = conv_layer_vgg(conv_4_1, 512, 512, "conv_4_2")
            conv_4_3 = conv_layer_vgg(conv_4_2, 512, 512, "conv_4_3")
            pool4 = tf.nn.max_pool(conv_4_3, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1], padding='SAME', name="pool4")

            conv_5_1 = conv_layer_vgg(pool4, 512, 512, "conv_5_1")
            conv_5_2 = conv_layer_vgg(conv_5_1, 512, 512, "conv_5_2")
            conv_5_3 = conv_layer_vgg(conv_5_2, 512, 512, "conv_5_3")
            pool5 = tf.nn.max_pool(conv_5_3, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1], padding='SAME', name="pool5")

            pre_fully_connected = tf.contrib.layers.flatten(pool5, scope="flattened")

            fully_connected_1 = tf.layers.dense(pre_fully_connected, 410,
                                                kernel_initializer=tf.contrib.layers.xavier_initializer(),
                                                activation=tf.nn.relu, name="fc1")

            fully_connected_2 = tf.layers.dense(fully_connected_1, 410,
                                                kernel_initializer=tf.contrib.layers.xavier_initializer(),
                                                activation=tf.nn.relu, name="fc2")

            logits = tf.layers.dense(fully_connected_2, n_outputs, activation=tf.nn.relu, name="logits")

        elif model_type == "Alex":
            X = tf.placeholder("float", [None, HEIGHT, WIDTH, 1])
            Y = tf.placeholder("float", [None, n_outputs])

            conv_1_1 = conv_layer(X, 11, 1, 96, 4, "VALID", "conv_1_1")
            pool1 = tf.nn.max_pool(conv_1_1, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1], padding='SAME', name="pool1")

            conv_2_1 = conv_layer(pool1, 5, 96, 256, 1, "SAME", "conv_2_1")
            pool2 = tf.nn.max_pool(conv_2_1, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1], padding='Same', name="pool2")

            conv_3_1 = conv_layer(pool2, 3, 256, 348, 1, "SAME", "conv_3_1")
            conv_3_2 = conv_layer(conv_3_1, 3, 348, 348, 1, "SAME", "conv_3_2")
            conv_3_3 = conv_layer(conv_3_2, 3, 96, 256, 1, "SAME", "conv_3_3")
            pool3 = tf.nn.max_pool(conv_3_3, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1], padding='SAME', name="pool3")

            pre_fully_connected = tf.contrib.layers.flatten(pool3, scope="flattened")

            fully_connected_1 = tf.layers.dense(pre_fully_connected, 410,
                                                kernel_initializer=tf.contrib.layers.xavier_initializer(),
                                                activation=tf.nn.relu, name="fc1")

            fully_connected_2 = tf.layers.dense(fully_connected_1, 410,
                                                kernel_initializer=tf.contrib.layers.xavier_initializer(),
                                                activation=tf.nn.relu, name="fc2")

            logits = tf.layers.dense(fully_connected_2, n_outputs, activation=tf.nn.relu, name="logits")

        else:
            raise ValueError("Unsupported model_type")

        with tf.name_scope("xent"):
            xent = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=logits, labels=Y, name="softmax"))
            tf.summary.scalar("Cross Entropy", xent)

        with tf.name_scope("train"):
            train_step = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(xent)

        with tf.name_scope("accuracy"):
            correct_prediction = tf.equal(tf.argmax(logits, 1), tf.argmax(Y, 1))
            accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
            tf.summary.scalar("Accuracy", accuracy)

        var_summary = tf.summary.merge_all()

    config = tf.ConfigProto()
    config.allow_soft_placement = True
    with tf.Session(config=config) as sess:
        tf.reset_default_graph()
        sess.run(tf.global_variables_initializer())
        saver = tf.train.Saver()
        writer = tf.summary.FileWriter(MODELPATH + "lr-" + str(l_r) + "-mt-" + model_type + "/", filename_suffix="board")
        writer.add_graph(sess.graph)
        batch_number = 1
        total_correct = 0
        for epoch in range(N_EPOCHS):
            csv_gen = csv_generator(DIRPATH, BATCH_SIZE)
            while True:
                try:
                    X_batch, Y_batch = get_batch(csv_gen, label_to_class, class_eye)
                except StopIteration:
                    break

                sess.run(train_step, feed_dict={X: X_batch, Y: Y_batch})
                if batch_number % 500 == 0:
                    [train_accuracy, summ] = sess.run([accuracy, var_summary], feed_dict={X: X_batch, Y: Y_batch})
                    writer.add_summary(summ, batch_number)
                    print("Epoch:", epoch + 1, "Total Batch Number:", batch_number, "Train accuracy:", train_accuracy)

                if batch_number % 5000 == 0:
                    saver.save(sess, MODELPATH + "lr-" + str(l_r) + "-mt-" + model_type + "/", batch_number)

                batch_number += 1

        print("Total accuracy: ", total_correct / (csv_len * N_EPOCHS))


def main():
    for l_r in [0.0003, 0.00003]:
        for m_type in ["VGG", "Alex"]:
            print("Starting", m_type, "with learning rate", str(l_r))
            cnn_model(m_type, l_r)


if __name__ == "__main__":
    main()
