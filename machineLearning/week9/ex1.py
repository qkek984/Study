import tensorflow as tf
import random
# import matplotlib.pyplot as plt
from tensorflow.examples.tutorials.mnist import input_data

tf.set_random_seed(777)  # reproducibility

mnist = input_data.read_data_sets("MNIST_date", one_hot=True)

learning_rate = 0.01
training_epochs=15
batch_size = 100

X= tf.placeholder(tf.float32,[None, 784])
X_img = tf.reshape(X,[-1,28,28,1])#알아서 계산해 n개(==-1) , 28x26, 1색깔 이미지
Y = tf.placeholder(tf.float32,[None,10])
#in 28x28
W1 = tf.Variable(tf.random_normal([3,3,1,32],stddev=0.01))#3x3필터, 1개색, 32개의 필터사용
L1 = tf.nn.conv2d(X_img, W1, strides=[1,1,1,1], padding='SAME')#stride 2x2로 , 입출력 사이즈가 같아지도록 Zero padding을 넣어줌
L1 = tf.nn.relu(L1)
L1 = tf.nn.max_pool(L1, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME')#커널 2 2, stride 2 2기때문에 out은 14x14

#in 14x14
W2 = tf.Variable(tf.random_normal([3,3,32,64],stddev=0.01))
L2 = tf.nn.conv2d(L1, W2, strides=[1,1,1,1], padding='SAME')
L2 = tf.nn.relu(L2)
L2 = tf.nn.max_pool(L2, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME')
#out 7x7
L2_flat = tf.reshape(L2,[-1,7*7*64])#n개를 7*7*64개의 값으로 reshape
#out 7*7*64=3136

W3 = tf.get_variable("W3", shape=[7*7*64,10],initializer=tf.contrib.layers.xavier_initializer())#out 10
b= tf.Variable(tf.random_normal([10]))#equlas out value
logits = tf.matmul(L2_flat,W3)+b

cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=logits,labels=Y))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

sess = tf.Session()
sess.run(tf.global_variables_initializer())

print('Learning started. It takes sometime.')

for epoch in range(training_epochs):
    avg_cost = 0
    total_batch= int(mnist.train.num_examples / batch_size)

    for i in range(total_batch):
        batch_xs, batch_ys = mnist.train.next_batch(batch_size)
        feed_dict = {X:batch_xs, Y: batch_ys}
        c,_ = sess.run([cost,optimizer], feed_dict=feed_dict)
        avg_cost += c / total_batch
    print('Epoch:', '%04d' % (epoch + 1), 'cost =', '{:.9f}'.format(avg_cost))

print('Learning Finished!')
# Test model and check accuracy
correct_prediction = tf.equal(tf.argmax(logits, 1), tf.argmax(Y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
print('Accuracy:', sess.run(accuracy, feed_dict={
      X: mnist.test.images, Y: mnist.test.labels}))

# Get one and predict
r = random.randint(0, mnist.test.num_examples - 1)
print("Label: ", sess.run(tf.argmax(mnist.test.labels[r:r + 1], 1)))
print("Prediction: ", sess.run(
    tf.argmax(logits, 1), feed_dict={X: mnist.test.images[r:r + 1]}))
