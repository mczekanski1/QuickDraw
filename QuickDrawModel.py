"""
Module allows users to run several CNN architectures in a loop to compare multiple models in a tf loop
"""
from AuxiliaryCNN import csv_generator, text_to_labels, get_batch
import numpy as np
import tensorflow as tf
import time


# constants
DIR_PATH = "/data/scratch/epeake/Google-Doodles/"
MODEL_PATH = "./qd_model/"
BATCH_SIZE = 40
HEIGHT = 256
WIDTH = 256
N_EPOCHS = 2
START_TIME = time.time()


label_to_index = text_to_labels(DIR_PATH)
class_eye = np.eye(len(label_to_index))
n_outputs = len(label_to_index)


def cnn_model(model_type, l_r):
    learning_rate = l_r

    with tf.device("/gpu:1"):
        if model_type == "VGG":
            X = tf.placeholder("float", [None, HEIGHT, WIDTH, 1], name="X")
            Y = tf.placeholder("float", [None, n_outputs], name="Y")

            conv_1_1 = tf.layers.conv2d(X, filters=64, kernel_size=3,
                                        kernel_initializer=tf.contrib.layers.xavier_initializer(), padding="SAME",
                                        activation=tf.nn.relu, name="conv_1_1")
            conv_1_2 = tf.layers.conv2d(conv_1_1, filters=64, kernel_size=3,
                                        kernel_initializer=tf.contrib.layers.xavier_initializer(), padding="SAME",
                                        activation=tf.nn.relu, name="conv_1_2")
            pool1 = tf.nn.max_pool(conv_1_2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME', name="pool1")

            conv_2_1 = tf.layers.conv2d(pool1, filters=128, kernel_size=3,
                                        kernel_initializer=tf.contrib.layers.xavier_initializer(), padding="SAME",
                                        activation=tf.nn.relu, name="conv_2_1")
            conv_2_2 = tf.layers.conv2d(conv_2_1, filters=128, kernel_size=3,
                                        kernel_initializer=tf.contrib.layers.xavier_initializer(), padding="SAME",
                                        activation=tf.nn.relu, name="conv_2_2")
            pool2 = tf.nn.max_pool(conv_2_2, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1], padding='SAME', name="pool2")

            conv_3_1 = tf.layers.conv2d(pool2, filters=256, kernel_size=3,
                                        kernel_initializer=tf.contrib.layers.xavier_initializer(), padding="SAME",
                                        activation=tf.nn.relu, name="conv_3_1")
            conv_3_2 = tf.layers.conv2d(conv_3_1, filters=256, kernel_size=3,
                                        kernel_initializer=tf.contrib.layers.xavier_initializer(), padding="SAME",
                                        activation=tf.nn.relu, name="conv_3_2")
            conv_3_3 = tf.layers.conv2d(conv_3_2, filters=256, kernel_size=3,
                                        kernel_initializer=tf.contrib.layers.xavier_initializer(), padding="SAME",
                                        activation=tf.nn.relu, name="conv_3_3")
            pool3 = tf.nn.max_pool(conv_3_3, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1], padding='SAME', name="pool3")

            conv_4_1 = tf.layers.conv2d(pool3, filters=512, kernel_size=3,
                                        kernel_initializer=tf.contrib.layers.xavier_initializer(), padding="SAME",
                                        activation=tf.nn.relu, name="conv_4_1")
            conv_4_2 = tf.layers.conv2d(conv_4_1, filters=512, kernel_size=3,
                                        kernel_initializer=tf.contrib.layers.xavier_initializer(), padding="SAME",
                                        activation=tf.nn.relu, name="conv_4_2")
            conv_4_3 = tf.layers.conv2d(conv_4_2, filters=512, kernel_size=3,
                                        kernel_initializer=tf.contrib.layers.xavier_initializer(), padding="SAME",
                                        activation=tf.nn.relu, name="conv_4_3")
            pool4 = tf.nn.max_pool(conv_4_3, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1], padding='SAME', name="pool4")

            conv_5_1 = tf.layers.conv2d(pool4, filters=512, kernel_size=3,
                                        kernel_initializer=tf.contrib.layers.xavier_initializer(), padding="SAME",
                                        activation=tf.nn.relu, name="conv_5_1")
            conv_5_2 = tf.layers.conv2d(conv_5_1, filters=512, kernel_size=3,
                                        kernel_initializer=tf.contrib.layers.xavier_initializer(), padding="SAME",
                                        activation=tf.nn.relu, name="conv_5_2")
            conv_5_3 = tf.layers.conv2d(conv_5_2, filters=512, kernel_size=3,
                                        kernel_initializer=tf.contrib.layers.xavier_initializer(), padding="SAME",
                                        activation=tf.nn.relu, name="conv_5_3")
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
            X = tf.placeholder("float", [None, HEIGHT, WIDTH, 1], name="X")
            Y = tf.placeholder("float", [None, n_outputs], name="Y")

            conv_1_1 = tf.layers.conv2d(X, filters=96, kernel_size=11, strides=(4, 4),
                                        kernel_initializer=tf.contrib.layers.xavier_initializer(), padding="VALID",
                                        activation=tf.nn.relu, name="conv_1_1")
            pool1 = tf.nn.max_pool(conv_1_1, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1], padding='SAME', name="pool1")

            conv_2_1 = tf.layers.conv2d(pool1, filters=256, kernel_size=5, strides=(1, 1),
                                        kernel_initializer=tf.contrib.layers.xavier_initializer(), padding="VALID",
                                        activation=tf.nn.relu, name="conv_2_1")
            pool2 = tf.nn.max_pool(conv_2_1, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1], padding='SAME', name="pool2")

            conv_3_1 = tf.layers.conv2d(pool2, filters=348, kernel_size=3, strides=(1, 1),
                                        kernel_initializer=tf.contrib.layers.xavier_initializer(), padding="SAME",
                                        activation=tf.nn.relu, name="conv_3_1")
            conv_3_2 = tf.layers.conv2d(conv_3_1, filters=348, kernel_size=3, strides=(1, 1),
                                        kernel_initializer=tf.contrib.layers.xavier_initializer(), padding="SAME",
                                        activation=tf.nn.relu, name="conv_3_2")
            conv_3_3 = tf.layers.conv2d(conv_3_2, filters=256, kernel_size=3, strides=(1, 1),
                                        kernel_initializer=tf.contrib.layers.xavier_initializer(), padding="SAME",
                                        activation=tf.nn.relu, name="conv_3_3")
            pool3 = tf.nn.max_pool(conv_3_3, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1], padding='SAME', name="pool3")

            pre_fully_connected = tf.contrib.layers.flatten(pool3, scope="flattened")

            fully_connected_1 = tf.layers.dense(pre_fully_connected, 410,
                                                kernel_initializer=tf.contrib.layers.xavier_initializer(),
                                                activation=tf.nn.relu, name="fc1")

            fully_connected_2 = tf.layers.dense(fully_connected_1, 410,
                                                kernel_initializer=tf.contrib.layers.xavier_initializer(),
                                                activation=tf.nn.relu, name="fc2")

            logits = tf.layers.dense(fully_connected_2, n_outputs, activation=tf.nn.relu, name="logits")

        elif model_type == "AlexDeep":
            X = tf.placeholder("float", [None, HEIGHT, WIDTH, 1], name="X")
            Y = tf.placeholder("float", [None, n_outputs], name="Y")

            conv_1_1 = tf.layers.conv2d(X, filters=96, kernel_size=11, strides=(4, 4),
                                        kernel_initializer=tf.contrib.layers.xavier_initializer(), padding="VALID",
                                        activation=tf.nn.relu, name="conv_1_1")
            pool1 = tf.nn.max_pool(conv_1_1, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1], padding='SAME', name="pool1")

            conv_2_1 = tf.layers.conv2d(pool1, filters=256, kernel_size=5, strides=(1, 1),
                                        kernel_initializer=tf.contrib.layers.xavier_initializer(), padding="VALID",
                                        activation=tf.nn.relu, name="conv_2_1")
            pool2 = tf.nn.max_pool(conv_2_1, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1], padding='SAME', name="pool2")

            conv_3_1 = tf.layers.conv2d(pool2, filters=348, kernel_size=3, strides=(1, 1),
                                        kernel_initializer=tf.contrib.layers.xavier_initializer(), padding="SAME",
                                        activation=tf.nn.relu, name="conv_3_1")
            conv_3_2 = tf.layers.conv2d(conv_3_1, filters=348, kernel_size=3, strides=(1, 1),
                                        kernel_initializer=tf.contrib.layers.xavier_initializer(), padding="SAME",
                                        activation=tf.nn.relu, name="conv_3_2")
            conv_3_3 = tf.layers.conv2d(conv_3_2, filters=256, kernel_size=3, strides=(1, 1),
                                        kernel_initializer=tf.contrib.layers.xavier_initializer(), padding="SAME",
                                        activation=tf.nn.relu, name="conv_3_3")
            pool3 = tf.nn.max_pool(conv_3_3, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1], padding='SAME', name="pool3")

            pre_fully_connected = tf.contrib.layers.flatten(pool3, scope="flattened")

            fully_connected_1 = tf.layers.dense(pre_fully_connected, 4010,
                                                kernel_initializer=tf.contrib.layers.xavier_initializer(),
                                                activation=tf.nn.relu, name="fc1")

            fully_connected_2 = tf.layers.dense(fully_connected_1, 4010,
                                                kernel_initializer=tf.contrib.layers.xavier_initializer(),
                                                activation=tf.nn.relu, name="fc2")

            logits = tf.layers.dense(fully_connected_2, n_outputs, activation=tf.nn.relu, name="logits")

        elif model_type == "AlexDeep2":
            X = tf.placeholder("float", [None, HEIGHT, WIDTH, 1], name="X")
            Y = tf.placeholder("float", [None, n_outputs], name="Y")

            conv_1_1 = tf.layers.conv2d(X, filters=96, kernel_size=11, strides=(4, 4),
                                        kernel_initializer=tf.contrib.layers.xavier_initializer(), padding="VALID",
                                        activation=tf.nn.relu, name="conv_1_1")
            pool1 = tf.nn.max_pool(conv_1_1, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1], padding='SAME', name="pool1")

            conv_2_1 = tf.layers.conv2d(pool1, filters=256, kernel_size=5, strides=(1, 1),
                                        kernel_initializer=tf.contrib.layers.xavier_initializer(), padding="VALID",
                                        activation=tf.nn.relu, name="conv_2_1")
            pool2 = tf.nn.max_pool(conv_2_1, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1], padding='SAME', name="pool2")

            conv_3_1 = tf.layers.conv2d(pool2, filters=348, kernel_size=3, strides=(1, 1),
                                        kernel_initializer=tf.contrib.layers.xavier_initializer(), padding="SAME",
                                        activation=tf.nn.relu, name="conv_3_1")
            conv_3_2 = tf.layers.conv2d(conv_3_1, filters=348, kernel_size=3, strides=(1, 1),
                                        kernel_initializer=tf.contrib.layers.xavier_initializer(), padding="SAME",
                                        activation=tf.nn.relu, name="conv_3_2")
            conv_3_3 = tf.layers.conv2d(conv_3_2, filters=256, kernel_size=3, strides=(1, 1),
                                        kernel_initializer=tf.contrib.layers.xavier_initializer(), padding="SAME",
                                        activation=tf.nn.relu, name="conv_3_3")
            pool3 = tf.nn.max_pool(conv_3_3, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1], padding='SAME', name="pool3")

            pre_fully_connected = tf.contrib.layers.flatten(pool3, scope="flattened")

            fully_connected_1 = tf.layers.dense(pre_fully_connected, 4010,
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
            accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"), name="accuracy")
            tf.summary.scalar("Accuracy", accuracy)

        var_summary = tf.summary.merge_all()

    config = tf.ConfigProto()
    config.allow_soft_placement = True
    with tf.Session(config=config) as sess:
        sess.run(tf.global_variables_initializer())
        saver = tf.train.Saver()
        writer = tf.summary.FileWriter(MODEL_PATH + "tboard", filename_suffix="lr-" + str(l_r) + "-mt-" + model_type)
        writer.add_graph(sess.graph)
        batch_number = 1
        for epoch in range(N_EPOCHS):
            csv_gen = csv_generator(DIR_PATH, BATCH_SIZE)
            while True:
                try:
                    X_batch, Y_batch = get_batch(csv_gen, label_to_index, class_eye)
                except StopIteration:
                    break

                sess.run(train_step, feed_dict={X: X_batch, Y: Y_batch})
                if batch_number % 100 == 0:
                    [train_accuracy, summ] = sess.run([accuracy, var_summary], feed_dict={X: X_batch, Y: Y_batch})
                    writer.add_summary(summ, batch_number)
                    print("Epoch:", epoch + 1, "Total Batch Number:", batch_number, "Train accuracy:", train_accuracy)

                if batch_number % 2500 == 0:
                    saver.save(sess, MODEL_PATH + "lr-" + str(l_r) + "-mt-" + model_type + "/cnnmodel", batch_number)

                batch_number += 1

            print("Epoch time:", (time.time() - START_TIME) // 3600, "hr", ((time.time() - START_TIME) % 3600) / 60, "min")

        # final reports
        summ = sess.run(var_summary, feed_dict={X: X_batch, Y: Y_batch})
        writer.add_summary(summ, batch_number)
        saver.save(sess, MODEL_PATH + "lr-" + str(l_r) + "-mt-" + model_type + "/cnnmodel", batch_number)


def main():
    for l_r in [0.0003]:
        for m_type in ["Alex", "AlexDeep", "AlexDeep2"]:
            tf.reset_default_graph()
            print("Starting", m_type, "with learning rate", str(l_r))
            cnn_model(m_type, l_r)


if __name__ == "__main__":
    main()
