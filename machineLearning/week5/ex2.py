import tensorflow as tf
import numpy as np

tf.set_random_seed(777)

xy = np.loadtxt('data-04-zoo.csv', delimiter=',', dtype=np.float32)

x_data= xy[:, 0:-1]
y_data= xy[:, [-1]]
print(x_data.shape, y_data.shape)

nb_classes = 7 #0~6

X=tf.placeholder(tf.float32, [None, 16])
Y=tf.placeholder(tf.int32, [None, 1])
Y_one_hot = tf.one_hot(Y, nb_classes) # one_hot
print("one_hot",Y_one_hot)
Y_one_hot = tf.reshape(Y_one_hot, [-1,nb_classes])
print("reshape", Y_one_hot)

W= tf.Variable(tf.random_normal([16, nb_classes]),name='weight')
b= tf.Variable(tf.random_normal([nb_classes]), name='bias')

#hypothesis = tf.nn.softmax(tf.matmul(X, W) + b)#softmax
logits= tf.matmul(X,W)+b
hypothesis = tf.nn.softmax(logits)#softmax

#----cross entropy cost/Loss----
#cost = tf.reduce_mean(-tf.reduce_sum(Y* tf.log(hypothesis), axis=1))
cost_i= tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=Y_one_hot)
cost = tf.reduce_mean(cost_i)

optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.1).minimize(cost)

prediction = tf.argmax(hypothesis, 1)
correct_prediction = tf.equal(prediction, tf.argmax(Y_one_hot, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

with tf.Session() as sess:
	sess.run(tf.global_variables_initializer())
	for step in range(2000):
		sess.run(optimizer, feed_dict={X: x_data,Y: y_data})		
		if step % 100 ==0:
			loss, acc = sess.run([cost,accuracy], feed_dict={X: x_data,Y: y_data})			
			print("step: {:5}\tLoss: {:.3f}\tAcc: {:2%}".format(step, loss, acc))
	pred = sess.run(prediction, feed_dict={X: x_data})
	for p,y in zip(pred,y_data.flatten()):
		print("[{}] Prediction : {} True Y: {}".format(p==int(y), p, int(y)))

