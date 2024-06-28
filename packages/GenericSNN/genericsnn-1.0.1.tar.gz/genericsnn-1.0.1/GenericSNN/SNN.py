import os

from GenericSNN.SNN_template import SNNTemplate
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import nengo
import nengo_dl
import pickle
import numpy as np
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt


class SpikingNeuralNetworkModel(SNNTemplate):
    """ This class can be used as a template to define and build a spiking neural network (SNN) using nengo_dl framework, as well as fit it and make predictions.
    """

    def __init__(self,
                 layers,
                 optimizer,
                 lr,
                 input_size,
                 loss_train=tf.losses.SparseCategoricalCrossentropy(from_logits=True),
                 loss_predict=None,
                 callbacks=[EarlyStopping(monitor='loss', min_delta=0.00001, patience=25)],
                 minibatch_size=200,
                 epochs=5,
                 dt=0.001,
                 neuron_type='LIF',
                 max_rate=100,
                 amp=None,
                 tau_rc=0.2,
                 tau_ref=0.002,
                 min_voltage=0,
                 synapse=None,
                 synapse_post_trainig=0.005,
                 synapse_probe=0.01,
                 radius=1.5,
                 problem_type='regression',
                 verbose=True,
                 seed_=1234
                 ):
        """Class constructor

        Args:
            layers (list): list of dicts in which each element must of the list be a dictionary which key must be the kind of population (node, ensemble) and which must contain a dictionary containing the population paramets.
            optimizer (str): Indicates the optimizer that will be used in the training.
            lr (float): Learning rate to be used during training. 
            input_size (int): size of the input of the SNN.
            loss_train (callable, optional): loss function to use in the training. Defaults to tf.losses.SparseCategoricalCrossentropy(from_logits=True).
            loss_predict (callable, optional): loss funciton to use in the prediction. Defaults to None.
            callbacks (list, optional): contains the callbacks that should be applied during the training. Defaults to [EarlyStopping(monitor='loss', min_delta=0.00001, patience=25)].
            minibatch_size (int, optional): Indicates the mini-batch size to be used during training/prediction. Defaults to 200.
            epochs (int, optional): Number of epochs to train the model. Defaults to 5.
            dt (float, optional): Indicates the simulation timestep. Defaults to 0.001.
            neuron_type (str, optional): indicates the neuron type used along the neural network.  Defaults to 'LIF'.
            max_rate (int, optional): indicates the neuron firing rates. Defaults to 100
            amp (float, optional): neuron spike amplitude (scaled so that the overall output is ~1). Defaults to None.
            tau_rc (float, optional): indicates the membrane RC time constant. Affects how quickly the membrane voltage decays to zero in the absence of input. Defaults to 0.2.
            tau_ref (float, optional): indicates the absolute refractory period. This is how long the membrane voltage is held at zero after a spike. Defaults to 0.002.
            min_voltage (int, optional): indicates minimum value for the membrane voltage. Defaults to 0.
            synapse (float, optional): ndicates the synapse to use for filtering while training. Defaults to None.
            synapse_post_trainig (float, optional): indicates the synapse to be set for filtering after training. Defaults to 0.005.
            synapse_probe (float, optional): indicates the synapse to use for filtering output probe. Defaults to 0.01.
            radius (float, optional): indicates the representational radius of the ensemble. Defaults to 1.5.
            problem_type (str, optional): indicates if the problem is classification ('classification-binary','classification-multiclass') or regression ('regression'). Defaults to 'regression'.
            verbose (bool, optional): Indicates if the verbose of the SNN training/prediction should be shown. Defaults to True.
            seed_ (int, optional): The seed to be fixed to ensure reproducibility. Defaults to 1234.

        """

        self.possible_optimizers = ['adam', 'rmsprop', 'sgd', 'adadelta', 'adagrad', 'adamax', 'nadam']
        self.possible_neuron_types = ['LIF', 'SoftLIF', 'Sigmoid']
        # --- Set params --- #
        # NN related params
        self.layers = layers
        self.optimizer = optimizer  # .lower()
        self.lr = lr
        self.input_size = input_size
        self.callbacks = callbacks
        self.loss_train = loss_train
        self.loss_predict = loss_predict

        self.minibatch_size = minibatch_size
        self.epochs = epochs

        # Time related params
        self.dt = dt

        # Spiking Neurons related params
        self.neuron_type = neuron_type
        self.max_rate = max_rate
        if amp:
            self.amp = amp
        else:
            self.amp = 1 / self.max_rate
        self.tau_rc = tau_rc
        self.tau_ref = tau_ref
        self.min_voltage = min_voltage
        self.synapse = synapse
        self.synapse_post_trainig = synapse_post_trainig
        self.synapse_probe = synapse_probe
        self.radius = radius
        self.probes = {
            'output_no_syn': {'probe': [], 'data': []},
            'output_syn': {'probe': [], 'data': []},
            'output_spikes': {'probe': [], 'data': []},
            'output_voltage': {'probe': [], 'data': []},
            'output_refractory_time': {'probe': [], 'data': []}
        }

        self.problem_type = problem_type
        self.verbose = verbose
        self.seed_ = seed_

        if loss_predict == None:
            self._set_default_loss_function()
        # Check params
        self._check_params()
        # Set seed
        # self._set_seed()
        self.reset_seeds()
        # Build SNN model
        self.build_model()

    def reset_seeds(self, reset_graph_with_backend=True):
        """Reset random seeds.

        Args:
            reset_graph_with_backend (bool, optional): Indicates if the graph should be restarted too. Defaults to True.
        """
        if reset_graph_with_backend != None:
            tf.compat.v1.reset_default_graph()
            print("KERAS AND TENSORFLOW GRAPHS RESET")  # optional

        tf.compat.v1.set_random_seed(self.seed_)
        self._set_seed()
        print("RANDOM SEEDS RESET")

    def set_params(self, **parameters):
        """Set class parameters

        Args:
            parameters (dict): Indicates all the parameters to be set. Structur must be: {parameter_name: parameter_vale}

        Returns:
            SpikingNengoNeuralNetworkModel: current object of the class .
        """
        for parameter, value in parameters.items():
            setattr(self, parameter, value)
        if not self.amp:
            self.amp = 1 / self.max_rate
        self.optimizer = self.optimizer.lower()
        self._check_params()
        self._set_seed()
        self.build_model()
        return self

    def get_params(self, deep=False):
        """Get class parameters

        Args:
            deep (bool, optional): Indicates if the model should be included in the output parameters dictionary. Defaults to False.

        Returns:
            dict: Current parameters of the class.{parameter_name:paramter_vale,...}
        """
        output = dict(
            layers=self.layers,
            optimizer=self.optimizer,
            lr=self.lr,
            input_size=self.input_size,
            loss_train=self.loss_train,
            loss_predict=self.loss_predict,
            callbacks=self.callbacks,

            minibatch_size=self.minibatch_size,
            epochs=self.epochs,

            dt=self.dt,
            neuron_type=self.neuron_type,
            max_rate=self.max_rate,
            amp=self.amp,
            tau_rc=self.tau_rc,
            tau_ref=self.tau_ref,
            min_voltage=self.min_voltage,
            synapse=self.synapse,
            synapse_post_trainig=self.synapse_post_trainig,
            synapse_probe=self.synapse_probe,
            radius=self.radius,
            problem_type=self.problem_type,
            seed_=self.seed_,
            verbose=self.verbose
        )
        if deep:
            output['net'] = self.net

        return output

    def _create_layer(self, act_layer, prev_layer, output_layer=False):
        """Create a Nengo_dl layer

        Args:
            act_layer (dict): Dictionary containing needed information to create Nengo_dl.layer objet. The structure of that dictionary should be: {layer_name: {feature_name: feature_vale,...}}
            prev_layer (nengo_dl.layer): Previous layer to be concatenated.
            output_layer (bool, optional): Indicates if it is the output layer or no. Defaults to False.

        Returns:
            nengo_dl.layer : Nengo_dl Layer object.
        """
        keys = list(act_layer.keys())
        if 'conv' in keys:
            new_layer = nengo_dl.Layer(tf.keras.layers.Conv2D(
                **act_layer['conv']))(prev_layer, shape_in=act_layer['shape_in'])
        elif 'dense' in keys:
            new_layer = nengo_dl.Layer(tf.keras.layers.Dense(**act_layer['dense']))(prev_layer)
        elif 'maxpool' in keys:
            new_layer = nengo_dl.Layer(tf.keras.layers.MaxPooling2D(**act_layer['maxpool']))(prev_layer)
        else:
            print('ERROR. Layer not defined. Options: dense, conv')
        if not output_layer:
            neuron = self.neuron if not 'neuron_type' in act_layer.keys() else act_layer['neuron_type']
            new_layer = nengo_dl.Layer(neuron)(new_layer)
        return new_layer

    def build_model(self):
        """ Build spiking neural network model 
        """
        self.net = nengo.Network(seed=self.seed_)
        with self.net:
            # set up the default parameters for ensembles/connections
            # nengo_loihi.add_params(net)
            # max_rate == neuron response magnitud when its value = max_value
            self.net.config[nengo.Ensemble].max_rates = nengo.dists.Choice([self.max_rate])
            # Intercepts == input value in which a neuron is going to start responding
            self.net.config[nengo.Ensemble].intercepts = nengo.dists.Choice([0])
            # Synapse low-pass filter
            self.net.config[nengo.Connection].synapse = self.synapse
            # expected magnitude of the inputs to that ensemble
            self.net.config[nengo.Ensemble].radius = self.radius

            # Set neuron type used along the neural network
            if self.neuron_type == 'LIF':
                self.neuron = nengo.LIF(tau_rc=self.tau_rc, tau_ref=self.tau_ref,
                                        min_voltage=self.min_voltage, amplitude=self.amp)
            elif self.neuron_type == 'SoftLIF':
                self.neuron = nengo_dl.SoftLIFRate(sigma=1.0, tau_rc=self.tau_rc,
                                                   tau_ref=self.tau_ref, amplitude=self.amp)
            else:
                self.neuron = nengo.Sigmoid(tau_ref=self.tau_ref)

            # the input node that will be used to feed in input images
            prev_layer = nengo.Node(np.zeros(self.input_size))

            self.probes['layer0_output'] = dict()
            self.probes['layer0_output']['probe'] = nengo.Probe(prev_layer,
                                                                attr='output', label='layer0_output', seed=self.seed_)
            c = 1
            for layer in self.layers[:-1]:
                prev_layer = self._create_layer(layer, prev_layer)

                self.probes['layer' + str(c) + '_ref'] = dict()
                self.probes['layer' + str(c) + '_vol'] = dict()
                self.probes['layer' + str(c) + '_output'] = dict()
                self.probes['layer' + str(c) + '_output']['probe'] = nengo.Probe(prev_layer,
                                                                                 attr='output', label='layer' + str(c) + "_output", seed=self.seed_)
                self.probes['layer' + str(c) + '_ref']['probe'] = nengo.Probe(prev_layer,
                                                                              attr='refractory_time', label='layer' + str(c) + "_ref", seed=self.seed_)
                self.probes['layer' + str(c) + '_vol']['probe'] = nengo.Probe(prev_layer,
                                                                              attr='voltage', label='layer' + str(c) + "_vol", seed=self.seed_)
                c += 1
            prev_layer = self._create_layer(self.layers[-1], prev_layer, output_layer=True)
            output_neuron = self.neuron if not 'neuron_type' in self.layers[-1].keys(
            ) else self.layers[-1]['neuron_type']
            output_l = nengo_dl.Layer(output_neuron)(prev_layer)
            # --- PROBES --- #
            # nengo.Probe -> objects that collect data from the simulation

            self.probes['output_no_syn']['probe'] = nengo.Probe(
                prev_layer, attr='output', label="output_p_nosyn", seed=self.seed_)
            if self.synapse_probe:
                self.probes['output_syn']['probe'] = nengo.Probe(
                    prev_layer, attr='output', synapse=nengo.Alpha(self.synapse_probe), label="output_p", seed=self.seed_)

            if not isinstance(output_neuron, nengo.Sigmoid) and not isinstance(output_neuron, nengo_dl.SoftLIFRate):
                self.probes['output_spikes']['probe'] = nengo.Probe(
                    output_l, attr='output', label="output_p", seed=self.seed_)
                self.probes['output_voltage']['probe'] = nengo.Probe(
                    output_l, attr='voltage', label="output_voltage", seed=self.seed_)
                self.probes['output_refractory_time']['probe'] = nengo.Probe(
                    output_l, attr='refractory_time', label="output_refractory_time", seed=self.seed_)
            else:
                if 'output_spikes' in self.probes.keys():
                    del self.probes['output_spikes']
                    del self.probes['output_voltage']
                    del self.probes['output_refractory_time']

    def fit(self, x_train, y_train):
        """Fit neural network model 

        Args:
            x_train (numpy.array): matrix with the data to train the SNN. Shape must be (samples,time,values)
            y_train (numpy.array): matrix with the labels to train the SNN. Shape must be (samples,time,values)

        Returns:
            SpikingNeuralNetworkModel: current object of the class
        """
        with nengo_dl.Simulator(self.net, minibatch_size=self.minibatch_size, seed=self.seed_) as sim:
            sim.compile(
                optimizer=self._create_optimizer(),
                loss={self.probes['output_no_syn']['probe']: self.loss_train},
            )
            # sim.fit(x_train, y_train, epochs=self.epochs, callbacks=self.callbacks, verbose=self.verbose)
            sim.fit(x_train, {self.probes['output_no_syn']['probe']: y_train},
                    epochs=self.epochs, callbacks=self.callbacks, verbose=self.verbose)
            # sim.compile(loss={self.probes['output_syn']: self.loss_function})
            sim.freeze_params(self.net)

        self.set_synapse_post_training()

        return self

    def set_synapse_post_training(self, synapse_post_trainig=None):
        """Set synapse after training (will be used for predictions)

        Args:
            synapse_post_trainig (float, optional): Synapse to be set for filtering after training. Defaults to None.
        """
        if synapse_post_trainig != None:
            self.synapse_post_trainig = synapse_post_trainig
        if self.synapse_post_trainig:
            for conn in self.net.all_connections:
                conn.synapse = self.synapse_post_trainig

    def predict(self, x_test):
        """Get the score obtained in a set of data

        Args:
            x_test (numpy.array): dataset to predict

        Returns:
            numpy.array: prediction
        """
        self.x_test = x_test

        with nengo_dl.Simulator(self.net, dt=self.dt, minibatch_size=self.minibatch_size, seed=self.seed_) as sim:
            sim.compile(loss={self.probes['output_syn']['probe']: self.loss_function})

        return self.do_prediction(x_test)

    def do_prediction(self, x_test):
        """Makes a prediction (model already compiled)

        Args:
            x_test (numpy.array): dataset to predict

        Returns:
            numpy.array: prediction
        """
        with nengo_dl.Simulator(self.net, dt=self.dt, minibatch_size=self.minibatch_size, seed=self.seed_) as sim:
            y_pred = sim.predict(x_test)
        self._save_probes(y_pred)
        return y_pred[self.probes['output_syn']['probe']]

    def score(self, x_test, y_test):
        """Get the score obtained in a set of data

        Args:
            x_test (numpy.array): dataset to predict
            y_test (numpy.array): labels to predict

        Returns:
            float: score obtained in the prediction
        """
        self.x_test = x_test
        # When fit is called from predict or score function
        if self.synapse_post_trainig:
            for conn in self.net.all_connections:
                conn.synapse = self.synapse_post_trainig
        with nengo_dl.Simulator(self.net, dt=self.dt, minibatch_size=self.minibatch_size, seed=self.seed_) as sim:
            sim.compile(loss={self.probes['output_syn']['probe']: self.loss_function})
            output = sim.evaluate(x_test, {self.probes['output_syn']['probe']: y_test}, verbose=self.verbose)
            if self.problem_type == 'regression':
                return - output['output_p_loss']  # MSE must me minimized
            else:
                return output['output_p_loss']

    def save_params(self, filename, print_weights_shape=False):
        """Save spiking neural network weights in a file.

        Args:
            filename (str): filename where the parameters should be saved. 
            print_weights_shape (bool, optional): Indicates if the weights of the SNN should be printed. Defaults to False.
        """
        if not os.path.exists(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        sim = nengo_dl.Simulator(self.net, dt=self.dt, minibatch_size=self.minibatch_size, seed=self.seed_)
        # sim.save_params(filename,include_state=True)

        np.save(filename, np.array(sim.keras_model.get_weights(), dtype=object))
        if print_weights_shape:
            new_weights = sim.keras_model.get_weights()
            for i in range(len(new_weights)):
                print(new_weights[i].shape)

    def save_network(self, filename):
        """Save SNN.

        Args:
            filename (str): path where the SNN should be saved. 
        """
        if not os.path.exists(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        pickle.dump(self.net, open(filename, 'wb'))

    def load_params(self, filename):
        """Load neural network weights from filename.

        Args:
            filename (str): filename from which the parameters should be loaded.
        """
        sim = nengo_dl.Simulator(self.net, dt=self.dt, minibatch_size=self.minibatch_size, seed=self.seed_)
        # Load parameters from file
        ################
        '''
        act_weights = sim.keras_model.get_weights()
        prev = act_weights
        new_weights = np.load(filename,allow_pickle=True)
        for i in range(len(act_weights)): act_weights[i] = new_weights[i]
        sim.keras_model.set_weights(act_weights)

        # Check
        aux = sim.keras_model.get_weights()
        for i in range(len(aux)): print((aux[i] == prev[i]).all())
        print('--')
        for i in range(len(aux)): print((aux[i] == new_weights[i]).all())
        '''
        #################
        sim.keras_model.set_weights(np.load(filename, allow_pickle=True))
        # sim.load_params(filename,include_state=False)

        # Freeze this parameters in class network
        sim.freeze_params(self.net)
