import collections
import nengo
import nengo_dl
import numpy as np
import random
import tensorflow as tf
from GenericSNN.SNN_template import SNNTemplate
from tensorflow.keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt


class SpikingNengoNeuralNetworkModel(SNNTemplate):
    """This class can be used as a template to define and build a spiking neural network (SNN) using Nengo framework, as well as fit it and make predictions.
    """

    def __init__(self,
                 layers,
                 connections,
                 optimizer,  # String with the optimizer that will be used in the training
                 lr,         # Learning rate
                 input_size,  # Input size for the NN
                 loss_train=tf.losses.SparseCategoricalCrossentropy(
                     from_logits=True),  # Loss function to use in the training
                 loss_predict=None,
                 callbacks=[EarlyStopping(monitor='loss', min_delta=0.00001, patience=15)],

                 minibatch_size=200,   # Mini-batch size
                 epochs=5,               # Epochs

                 presentation_time=0.2,  # input presentation time
                 dt=0.001,               # simulation timestep
                 neuron_type='LIF',    # Neuron type used along the neural network
                 max_rate=100,         # neuron firing rates
                 amp=None,             # neuron spike amplitude (scaled so that the overall output is ~1)
                 tau_rc=0.2,             # Membrane RC time constant. Affects how quickly the membrane voltage decays to zero in the absence of input
                 tau_ref=0.002,          # Absolute refractory period. This is how long the membrane voltage is held at zero after a spike
                 min_voltage=0,          # Minimum value for the membrane voltage

                 synapse=None,           # Synapse to use for filtering while training
                 synapse_post_trainig=0.005,  # Synapse to be set for filtering after training
                 synapse_probe=0.01,   # Synapse to use for filtering output probe
                 radius=1.5,           # The representational radius of the ensemble.
                 spike_func_mode='random',  # String with spike function mode (random, noise) or callable
                 problem_type='regression',  # String indicating the kind of problem (regression,classification)
                 seed_=1234            # Seed for reproducible results
                 ):
        """Class constructor.

        Args:
            layers (list): list of dicts in which each element must of the list be a dictionary which key must be the kind of population (node, ensemble) and which must contain a dictionary containing the population paramets.
            connections (list):  list of dicts in which each element must be a dictionary which key must be the kind of connection (conv,conn)
            optimizer (str): Indicates the optimizer that will be used in the training.
            lr (float): learning rate to use during training. 
            input_size (tuple): size of the input of the SNN.
            loss_train (callable): loss function to be use in the training. Default tf.losses.SparseCategoricalCrossentropy(from_logits=True).
            loss_predict (callable). loss function to be used in the prediction. Default None. 
            callbacks (list, optional): contains the callbacks that should be applied during the training. Defaults to [EarlyStopping(monitor='loss', min_delta=0.00001, patience=15)].
            minibatch_size (int, optional): Indicates the mini-batch size to use in the training/prediction. Defaults to 200.
            epochs (int). Indicates the number of epochs to train the SNN. Default 5.
            presentation_time (float). Indicates the input presentation time. Default 0.2.
            df (float). Indicate the simulation timestep. Default 0.001.
            neuron_type (str). Indicates the neuron type used along the neural network. Default 'LIF'.
            max_rate (int). Indicates the neuron firing rates. Default 100.
            amp (float). Indicates neuron spike amplitude (scaled so that the overall output is ~1). Default None.
            tau_rc (float). Indicates the membrane RC time constant. Affects how quickly the membrane voltage decays to zero in the absence of input. Default 0.2
            tau_ref (float). Indicates the absolute refractory period. This is how long the membrane voltage is held at zero after a spike. Default 0.002.
            min_voltage (float). Indicates minimum value for the membrane voltage. Default 0.
            synapse (float). Indicates the synapse to use for filtering while training. Default None.
            synapse_post_trainig (float). Indicates the synapse to be set for filtering after training. Default 0.005.
            synapse_probe (float). Indicates the synapse to use for filtering output probe. Default 0.01.
            radius (float). Indicates the representational radius of the ensemble. Default 1.5.
            spike_func_mode (str). Indicates the spike function mode (random, noise) or callable. Default 'random'.
            problem_type (str). Indicates if the problem is classification ('classification-binary','classification-multiclass') or regression ('regression'). Default 'classif'.
            seed_ (int). The seed to be fixed to ensure reproducibility. Default 12345.
        """

        self.possible_optimizers = ['adam', 'rmsprop', 'sgd', 'adadelta', 'adagrad', 'adamax', 'nadam']
        self.possible_spike_func_modes = ['random', 'noise']
        self.possible_neuron_types = ['LIF', 'SoftLIF', 'Sigmoid']
        # --- Set params --- #
        # NN related params
        self.layers = layers
        self.connections = connections
        self.optimizer = optimizer  # .lower()
        self.lr = lr
        self.input_size = input_size
        self.loss_train = loss_train
        self.callbacks = callbacks

        self.minibatch_size = minibatch_size
        self.epochs = epochs

        # Time related params
        self.presentation_time = presentation_time
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
        self.spike_func_mode = spike_func_mode
        self.probes = {'output_no_syn': {'probe': [], 'data': []}, 'output_syn': {'probe': [], 'data': []},
                       'output_spikes': {'probe': [], 'data': []}}  # ,'input_spikes':{'probe':[],'data':[]}}

        self.problem_type = problem_type
        self.seed_ = seed_

        self.loss_predict = loss_predict
        if loss_predict == None:
            self._set_default_loss_function()

        # Check params
        self._check_params()
        # Set seed
        self._set_seed()
        # Build SNN model
        self.build_model()

    def _check_params(self):
        """ Check if the set parameters are compatibles between them.
        """
        super()._check_params()
        if self.presentation_time < self.dt:
            raise ValueError('Presentation time must be greater than dt.')
        if not isinstance(self.spike_func_mode, collections.Callable) and self.spike_func_mode not in self.possible_spike_func_modes:
            raise ValueError(
                'Spike function mode not define. It must be callable or one of the following strings: `random`,`no')
        if len(self.layers) != len(self.connections) + 1:
            raise ValueError('The number of connections must be one less than number of layers.')

    def get_params(self, deep=False):
        """Get class parameters

        Args:
            deep (bool, optional): Indicates if the model should be included in the output parameters dictionary. Defaults to False.

        Returns:
            dict: Current parameters of the class.{parameter_name:paramter_vale,...}
        """
        output = dict(
            layers=self.layers,
            connections=self.connections,
            optimizer=self.optimizer,
            lr=self.lr,
            input_size=self.input_size,
            loss_train=self.loss_train,
            loss_predict=self.loss_predict,
            callbacks=self.callbacks,

            minibatch_size=self.minibatch_size,
            epochs=self.epochs,

            presentation_time=self.presentation_time,
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
            spike_func_mode=self.spike_func_mode,
            problem_type=self.problem_type,
            seed_=self.seed_
        )
        if deep:
            output['net'] = self.net

        return output

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

    def noise_spike_input(self, data, thershold, max_noise=0.5, min_noise=0.1):
        """Function to transform the data into spikes by generate a 1 for each value higher than 0, and 0 otherwise. Moreover, some random pixels will changed by adding random noise. 

        Args:
            data (numpy.arary): Input dataset to transform into spikes.
            thershold (float): Number in [0,1] from which a spike can be randomly changed. 
            max_noise (float, optional): Maximum proportion of the dataset that can be randomly changed. Defaults to 0.5.
            min_noise (float, optional): Minum proportion of the dataset that can be randomly changed. Defaults to 0.1.

        Returns:
            numpy.array: Dataset transformed into spikes. 
        """
        r = [random.random() for _ in range(len(data))]
        output = np.array([1 if d > 0 else 0 for d in data])
        noise = np.where(r > thershold)[0]
        if len(noise) > len(data) * max_noise:
            noise = noise[[random.randint(0, len(noise) - 1) for _ in range(int(len(data) * max_noise))]]
        elif len(noise) < len(data) * min_noise:
            for _ in range(int(len(data) * min_noise - len(noise))):
                noise = np.append(noise, random.randint(0, len(data) - 1))
        output[noise] = [1 if d == 0 else 0 for d in output[noise]]
        return np.array(output)

    # Function for spikes input for the neural network.
    def spike_func(self, t):
        """Function to transform the test dataset into spikes. 
        *** THIS FUNCTION SHOULD BE CHECKED / TESTED *** 

        Args:
            t (int): Indicates the timing index 

        Returns:
            numpy.array: Dataset transformed into spikes. 
        """
        ts = np.arange(self.dt, self.x_test.shape[0] * self.presentation_time + self.dt, self.dt)
        ts = [round(t, 3) for t in ts]
        n_img = int(round(t / self.presentation_time, 3))

        act_data = self.x_test[n_img, int(n_img * self.presentation_time / self.dt - ts.index(round(t, 3))), :]  # / 255

        if isinstance(self.spike_func_mode, collections.Callable):
            return self.spike_func_mode(act_data, t)
        if self.spike_func_mode == 'random':
            output = [1 if random.random() < d else 0 for d in act_data]
        elif self.spike_func_mode == 'noise':
            # The image will be noisy at the begining and, while the time pass, it becomes clearler
            probs = np.arange(0, 1, 1 / (self.presentation_time / self.dt))
            times = np.arange(0, self.presentation_time, self.dt)
            times = np.array([round(t_i, 3) for t_i in times])
            thershold = probs[np.where(times == round(t - n_img / 255 * self.presentation_time, 3))[0]][0]
            output = self.noise_spike_input(act_data, thershold)
        return output

    def spike_func_full_set(self, data, mode='random'):
        """Transform the full dataset into spikes

        Args:
            data (numpy.array): Dataset to transform 
            mode (str, optional): Indicates the method to use, options: 'random','noise'. Defaults to 'random'.

        Returns:
            numpy.array: Dataset transformed into spikes. 
        """
        n_steps = int(self.presentation_time / self.dt)
        output = []
        for img in range(data.shape[0]):
            for t in np.arange(0, 1, 1 / (self.presentation_time / self.dt)):
                if mode == 'random':
                    output.append([1 if random.random() < d / 255 else 0 for d in data[img, :]])
                elif mode == 'noise':
                    output.append(self.noise_spike_input(data[img, :], t))
                else:
                    print('ERROR: Mode', mode, 'not defined.')
        return np.array(output).reshape((data.shape[0], n_steps, data.shape[1]))

    def _create_layer(self, layer):
        """Creates a node or ensemble based on layers features. 

        Args:
            layer (dict): Dictionary containing all needed information to create a nengo.Node or nengo.Ensemble object

        Returns:
            nengo.Node or nengo.Ensemble: new layer
        """
        layer_name = list(layer.keys())[0]
        if layer_name == 'node':
            return nengo.Node(**layer[layer_name], seed=self.seed_)
        else:
            return nengo.Ensemble(**layer[layer_name], seed=self.seed_)

    def build_model(self):
        """ Build neural network model 
        """
        self.net = nengo.Network(seed=self.seed_)
        with self.net:
            # set up the default parameters for ensembles/connections
            # nengo_loihi.add_params(net)
            # Set neuron type used along the neural network
            if self.neuron_type == 'LIF':
                self.net.config[nengo.Ensemble].neuron_type = (
                    nengo.LIF(tau_rc=self.tau_rc, tau_ref=self.tau_ref, min_voltage=self.min_voltage, amplitude=self.amp))
            elif self.neuron_type == 'SoftLIF':
                self.net.config[nengo.Ensemble].neuron_type = (nengo_dl.SoftLIFRate(
                    sigma=1.0, tau_rc=self.tau_rc, tau_ref=self.tau_ref, amplitude=self.amp))
            else:
                self.net.config[nengo.Ensemble].neuron_type = (nengo.Sigmoid(tau_ref=self.tau_ref))
            # max_rate == neuron response magnitud when its value = max_value
            self.net.config[nengo.Ensemble].max_rates = nengo.dists.Choice([self.max_rate])
            # Intercepts == input value in which a neuron is going to start responding
            self.net.config[nengo.Ensemble].intercepts = nengo.dists.Choice([0])
            # Synapse low-pass filter
            self.net.config[nengo.Connection].synapse = self.synapse
            # expected magnitude of the inputs to that ensemble
            self.net.config[nengo.Ensemble].radius = self.radius

            prev_layer = nengo.Node(output=self.spike_func, size_out=self.input_size, label='input')
            self.probes['layer0_output'] = dict()
            self.probes['layer0_output']['probe'] = nengo.Probe(prev_layer,
                                                                attr='output', label='layer0_output', seed=self.seed_)

            for i in range(len(self.connections)):
                pos_layer = self._create_layer(self.layers[i + 1])
                conn_name = list(self.connections[i].keys())[0]
                if conn_name == 'conv':
                    pos_layer = pos_layer.neurons
                    self.probes['layer' + str(i + 1) + '_ref'] = dict()
                    self.probes['layer' + str(i + 1) + '_vol'] = dict()

                    self.probes['layer' + str(i + 1) + '_output'] = dict()
                    self.probes['layer' + str(i + 1) + '_output']['probe'] = nengo.Probe(pos_layer,
                                                                                         attr='output', label='layer' + str(i + 1) + "_output", seed=self.seed_)
                    self.probes['layer' + str(i + 1) + '_ref']['probe'] = nengo.Probe(pos_layer,
                                                                                      attr='refractory_time', label='layer' + str(i + 1) + "_ref", seed=self.seed_)
                    self.probes['layer' + str(i + 1) + '_vol']['probe'] = nengo.Probe(pos_layer,
                                                                                      attr='voltage', label='layer' + str(i + 1) + "_vol", seed=self.seed_)
                    conv = nengo.Convolution(**self.connections[i][conn_name]['conv'])
                    nengo.Connection(prev_layer, pos_layer, transform=conv, **self.connections[i][conn_name]['conn'])
                else:
                    nengo.Connection(prev_layer, pos_layer, **self.connections[i][conn_name])
                prev_layer = pos_layer

            # --- PROBES --- #
            # nengo.Probe -> objects that collect data from the simulation
            self.probes['output_no_syn']['probe'] = nengo.Probe(
                pos_layer, attr='decoded_output', label="output_p_nosyn", seed=self.seed_)
            self.probes['output_spikes']['probe'] = nengo.Probe(
                pos_layer.neurons, label='output_spikes', seed=self.seed_)
            if self.synapse_probe:
                self.probes['output_syn']['probe'] = nengo.Probe(pos_layer, synapse=nengo.Alpha(
                    self.synapse_probe), attr='decoded_output', label="output_p", seed=self.seed_)

    def fit(self, x_train, y_train, verbose=1):
        """Fit the SNN model 

        Args:
            x_train (numpy.array): matrix with the data to train the SNN. Shape must be (samples,time,values)
            y_train (numpy.array): matrix with the labels to train the SNN. Shape must be (samples,time,label)
            verbose (int, optional): Indicates if the verbose during training should be shown. Defaults to 1.

        Returns:
            _type_: _description_
        """
        with nengo_dl.Simulator(self.net, dt=self.dt, minibatch_size=self.minibatch_size, seed=self.seed_) as sim:
            sim.compile(
                optimizer=self._create_optimizer(),
                loss={self.probes['output_no_syn']['probe']: self.loss_train},
            )
            sim.fit(x_train, {self.probes['output_no_syn']['probe']: y_train},
                    epochs=self.epochs, callbacks=self.callbacks, verbose=verbose)
            #sim.compile(loss={self.probes['output_syn']: self.loss_function})
            sim.freeze_params(self.net)
        return self

    def score(self, x_test, y_test):
        """Get the score obtained in a set of data

        Args:
            x_test (numpy.array): dataset to predict
            y_test (numpy.array): labels of the dataset

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
            output = sim.evaluate(x_test, {self.probes['output_syn']['probe']: y_test}, verbose=0)
            if self.problem_type == 'regression':
                return - output['output_p_loss']  # MSE must me minimized
            else:
                return output['output_p_loss']

    def predict(self, x_test, verbose=1):
        """Get the score obtained in a set of data

        Args:
            x_test (numpy.array): dataset to predict
            verbose (int, optional): Indicates if the verbose during prediction should be shown. Defaults to 1.

        Returns:
            _type_: _description_
        """
        self.x_test = x_test
        # When fit is called from predict or score function
        if self.synapse_post_trainig:
            for conn in self.net.all_connections:
                conn.synapse = self.synapse_post_trainig
        with nengo_dl.Simulator(self.net, dt=self.dt, minibatch_size=self.minibatch_size, seed=self.seed_) as sim:
            sim.compile(loss={self.probes['output_syn']['probe']: self.loss_function})
            y_pred = sim.predict(x_test, verbose=verbose)
        self._save_probes(y_pred)
        return y_pred[self.probes['output_syn']['probe']]

    def save_params(self, filename):
        """Save neural network weights from filename.

        Args:
            filename (str): filename where to save the SNN parameters.
        """
        sim = nengo_dl.Simulator(self.net, dt=self.dt, minibatch_size=self.minibatch_size, seed=self.seed_)
        # sim.save_params(filename,include_state=True)

        np.save(filename, sim.keras_model.get_weights())
        new_weights = sim.keras_model.get_weights()
        for i in range(len(new_weights)):
            print(new_weights[i].shape)

    def load_params(self, filename):
        """Load neural network weights from filename.

        Args:
            filename (str): filename in from which the parameters should be loaded. 
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
