import random
import numpy as np 


class Network (object) :

	#This is the constructor, it takes in the the dimensions of neural
	# network in form of the layer_sizes array and 
	#instantiates the weights and biases parameters accordingly.
	def __init__(self, layer_sizes) :
		
		self.layer_nos = len(layer_sizes)
		self.layer_sizes = layer_sizes
		self.nn_weights = [np.random.randn(r,c) for r,c in zip(layer_sizes[1:] , layer_sizes[:-1])]
		self.nn_bias = [np.random.randn(r,1) for r in layer_sizes[1:]]



	#This function takes in the test data runs it 
	#on to the model, returns the no of samples which 
	#passed the test.
	def evaluate(self, tester_data) :

		ans_array = [(np.argmax(self.feedforward(a)), b) for (a,b) in tester_data]
		return sum(int(p == q) for (p,q) in ans_array)



	#This the helper function used for testing the trained dataset
	#Works layer by layer takes in the entering data and produces the output data
	def feedforward (self, entering_data):

		for b,w in zip(self.nn_bias, self.nn_weights):
			entering_data = sigmoid(np.dot(w,entering_data) + b) 
		return entering_data




	#This function takes in mini_batch and learning rate and 
	#updates the current model with new weights and biases
	#Although the it has a helper function backprop doing the job of finding
	#change in biases and weights due to contribution of each sample 
	def operate_on_batch(self, batch, learning_rate) :

		differential_weight = [np.zeros(w.shape) for w in self.nn_weights]
		differential_bias = [np.zeros(b.shape) for b in self.nn_bias]

		for sample, result in batch:
			
			#Delta weight and Delta bias will have the same size as of nn_weights/differential_weight and nn_bias/ differential_bias repectively  
			delta_weight, delta_bias  = self.backprop(sample, result)

			differential_weight = [dw + dew for dw , dew in zip(differential_weight, delta_weight)]
			differential_bias = [db + deb for db, deb in zip (differential_bias, delta_bias)]

		self.nn_weights = [nw - (learning_rate/len(batch))*dnw for nw, dnw in zip (nn_weights , differential_weight)]
		self.nn_bias = [nb - (learning_rate/len(batch))*dnb for nb , dnb in zip(nn_bias, differential_bias)]


	#Main Helper Function in using Gradient Descent Algorithm
	def backprop(self, x, y) :
		
		nabla_w = [np.zeros(w.shape) for w in self.nn_weights]
		nabla_b = [np.zeros(b.shape) for b in self.nn_bias]

		#forward_pass storing the values of z and sigmoid(z) into
		#zs and activations respectively 

		activation = x
		activations = [x]
		zs = []
		for b,w in zip(self.nn_bias, self.nn_weights):

			z = np.dot(w,activation) + b
			zs.append(z)

			activation = sigmoid(z)
			activations.append(activation)

		#Making a backward pass 
		#for negative indices in python arrays please read documentation

		delta = (activations[-1] - y)*sigmoid_prime(zs[-1])
		nabla_b[-1]  = delta
		nabla_w[-1] = np.dot(delta, activations[-2].transpose())


		for l in xrange(2, self.layer_nos):
			
			z = zs[-l]
			sp = sigmoid_prime(z)
			delta = np.dot(self.nn_weights[-l+1].transpose(), delta) * sp
			nabla_b[-l] = delta
			nabla_w[-l] = np.dot(delta, activations[-l-1].transpose())

		return (nabla_b, nabla_w)



	#This the main function present inside the model that'll trigger the Schoastic Gradient Descent Algorithm and will train the model
	#This will also test the model after training if the testing data is provided 

	def stochastic_gradient_descent(self, trainer_data , epochs , batch_size , learning_rate , tester_data = None ) :

		if tester_data : tester_data_len  = len(tester_data)
		trainer_data_len = len(trainer_data)

		for epch in xrange(epochs):

			random.shuffle(trainer_data)
			batches = [trainer_data[i  : i + batch_size] for i in xrange(0, trainer_data_len, batch_size)]

		#This loop actually carries out the training part.
		for batch in batches :
			self.operate_on_batch(batch, learning_rate)


		if tester_data:
			print "Epoch {0} : {1} / {2}".format(j,self.evaluate(tester_data), tester_data_len)
		else:
			print "Epoch {0} complete".format(j)



#Derivative of the sigmoid function
def sigmoid_prime (z):
	return sigmoid(z)*(1-sigmoid(z))


#Just the sigmoid function 
def sigmoid(z) :
	return (1.0/(1.0 + np.exp(-z)))