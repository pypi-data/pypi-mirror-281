import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from nengo_extras.plot_spikes import plot_spikes


class SNNTemplate:
    def __init__(self):
        """This method will be implemented in each child class
        """
        pass

    def _create_optimizer(self):
        """Create tensorflow optimized from string indicating it's name.  

        Returns:
            tf.optimizer: Tensorflow optimizer object created from class global variables (self.optimizer, self.lr)
        """
        if self.optimizer == 'adam':
            return tf.optimizers.Adam(self.lr)
        elif self.optimizer == 'rmsprop':
            return tf.optimizers.RMSprop(self.lr)
        elif self.optimizer == 'sgd':
            return tf.optimizers.SGD(self.lr)
        elif self.optimizer == 'adadelta':
            return tf.optimizers.Adadelta(self.lr)
        elif self.optimizer == 'adagrad':
            return tf.optimizers.Adagrad(self.lr)
        elif self.optimizer == 'adamax':
            return tf.optimizers.Adamax(self.lr)
        elif self.optimizer == 'Nadam':
            return tf.optimizers.Nadam(self.lr)

    def _set_seed(self):
        """ Set seed in numpy and tensorflow
        """
        # seed(self.seed_)
        np.random.seed(self.seed_)
        tf.random.set_seed(self.seed_)

    def _set_default_loss_function(self):
        """Set a default loss function to use during prediction 
        """
        if self.problem_type == 'regression':
            self.loss_predict = tf.metrics.mean_squared_error
        else:
            self.loss_predict = tf.metrics.sparse_categorical_accuracy

    def loss_function(self, y_true, y_pred):
        """Calculate the loss value from the loss function depending to the problem type. 

        Args:
            y_true (numpy.array): real labels.
            y_pred (numpy.array): current prediction.

        Returns:
            float: Loss value. 
        """
        if self.problem_type == 'regression':
            return tf.metrics.mean_squared_error(y_true[:, -1, 0], y_pred[:, -1, 0])
        elif self.problem_type == 'classification-discrete':
            return 100 * tf.metrics.sparse_categorical_accuracy(y_true[:, -1], y_pred[:, -1])
        else:
            return 100 * tf.metrics.sparse_categorical_accuracy(y_true, y_pred)

    def _check_params(self):
        """Check if the set parameters are compatibles between them.
        """
        if not self.optimizer in self.possible_optimizers:
            raise ValueError('Unkown optimizer ' + self.optimizer +
                             '. It must be one of: ' + ', '.join(self.possible_optimizers))
        if not self.neuron_type in self.possible_neuron_types:
            raise ValueError('Unkown neuron type ' + self.neuron_type +
                             '. It must be one of: ' + ', '.join(self.possible_neuron_types))
        if self.amp and self.amp > 1 / self.max_rate:
            raise ValueError('Amplitude must be lower than 1/max_rate')
        if self.max_rate >= 1 / self.tau_ref:
            raise ValueError('Max rate must be lower than 1/tau_ref')

    def get_neurons_errors_in_firing_rate(self):
        """Search for neurons with a higher firing rate than the one specified in max_rate class atribute

        Returns:
            dict: dictionary containing error information per layer in the following format: [ [neuron,num_spikes], ...]
        """
        sampling_rate_errors = dict()

        run_time = self.probes['output_no_syn']['data'].shape[1] * self.dt
        max_spikes = run_time * self.max_rate

        num_layers = len(self.layers)
        if 'output_spikes' not in self.probes.keys():
            num_layers -= 1
        for l in range(num_layers):
            act_key = 'output_spikes' if l == len(self.layers) - 1 else 'layer' + str(l) + '_output'
            sampling_rate_errors[act_key] = []
            act_output_data = self.probes[act_key]['data']
            for neuron in range(act_output_data.shape[-1]):
                for sample in range(act_output_data.shape[0]):
                    spikes = np.sum(self.probes[act_key]['data'][sample, :, neuron] > 0)
                    if spikes > max_spikes:
                        sampling_rate_errors[act_key].append([neuron, spikes])

            print('* ', act_key)
            if len(sampling_rate_errors[act_key]) > 0:
                sampling_rate_errors[act_key] = np.array(sampling_rate_errors[act_key])
                print('\t * Error in',
                      len(np.unique(sampling_rate_errors[act_key][:, 0])), 'of', act_output_data.shape[-1], 'neurons')
                print('\t * Max. expected of spikes = ', max_spikes)
                print('\t * Max. actual num of spikes = ', np.max(sampling_rate_errors[act_key][:, 1]))
                print('\t * Actual max. rate', np.max(sampling_rate_errors[act_key][:, 1]) / run_time,
                      'instead of', self.max_rate)
            else:
                print('\t * No errors found.')
        return sampling_rate_errors

    def plot_probs(self, item_index, filename=''):
        """Plot output probes

        Args:
            item_index (int): indicates the sample index to plot.
            filename (str, optional): If you want to save the plot that indicates the name of the file that will be created. Defaults to ''.
        """
        plt.plot(tf.nn.softmax(self.probes['output_syn']['data'][item_index]))
        plt.legend([str(i) for i in range(10)], loc="upper left")
        plt.xlabel("timesteps")
        plt.ylabel("probability")
        plt.title("Predicted probability for image" + str(item_index))
        plt.tight_layout()
        if filename:
            plt.savefig(filename)
        plt.show()

    def plot_neuron_rate(self, sample=1, neuron=1, layer=1):
        """Plot output spikes.

        Args:
            sample (int, optional): Specify the sample to plot. Defaults to 1.
            neuron (int, optional): Specify the neuron to plot. Defaults to 1.
            layer (int, optional): Specify the layer to plot. Defaults to 1.
        """
        _, axs = plt.subplots(1, 2)
        axs[0].plot(self.probes['layer' + str(layer) + '_vol']['data'][sample, :, neuron])
        axs[0].plot(np.floor(self.probes['layer' + str(layer) + '_vol']['data'][sample, :, neuron]))
        axs[0].set_title('Voltage')
        axs[1].plot(self.probes['layer' + str(layer) + '_ref']['data'][sample, :, neuron])
        axs[1].set_title('Refactory Time')
        plt.show()

        plt.figure()
        plt.plot(self.probes['layer' + str(layer) + '_vol']['data'][sample, :, neuron])
        plt.plot(self.probes['layer' + str(layer) + '_ref']['data'][sample, :, neuron])
        plt.hlines(1, 0, len(self.probes['layer' + str(layer) + '_vol']['data'][sample, :, neuron]), color='gray')
        spikes = np.where(self.probes['layer' + str(layer) + '_output']['data'][sample, :, neuron] > 0)[0]
        plt.vlines(spikes, 0, 1, color='red', linestyles='dashed')
        plt.show()

    def plot_output_spikes(self, time_brand=None, max_time=None, img_name=''):
        """Plot output spikes.

        Args:
            time_brand (_type_, optional): Time window size to plot. Defaults to None.
            max_time (_type_, optional): Maximum time to plot. Defaults to None.
            img_name (str, optional): if you want to save the plot that indicates the name of the file that will be created. Defaults to ''.
        """
        # self.probes['output_spikes']['data'] --> [ img x time x neurons ]
        plt.figure()
        # Plot spikes
        spikes = self.probes['output_syn']['data'][:, :max_time,
                                                   :].T if max_time else self.probes['output_syn']['data'].T

        # 3D to 2D [ neurons x time ]
        spikes = spikes.reshape(spikes.shape[0], spikes.shape[1] * spikes.shape[2]).T
        time = np.arange(spikes.shape[0])
        # Plot spikes
        plot_spikes(time, spikes)
        # Plot vertical brands if required
        if time_brand:
            act_t = time_brand
            while act_t < time[-1:][0]:
                plt.axvline(x=act_t, linewidth=3, color='r')
                act_t += time_brand
        # Labels
        plt.xlabel("Time")
        plt.ylabel("Neuron number")

        # Custom yticks (neurons)
        names = np.arange(spikes.shape[1]) + 1
        sep = plt.yticks()[0][-1:][0] / len(names)
        new_ticks = [(sep * (i + 1)) - sep / 2 for i in range(len(names))]
        plt.yticks(new_ticks, names)

        # Save if required
        if img_name:
            plt.savefig(img_name)
        # Show
        plt.show()

    def _save_probes(self, y_pred):
        """Save probes from prediction.

        Args:
            y_pred (numpy.array): prediction obtained using predict method
        """
        for key in self.probes.keys():
            self.probes[key]['data'] = y_pred[self.probes[key]['probe']]

    def get_probes(self):
        """Get output probes.

        Returns:
            dict: Set of created probes.
        """
        return self.probes

    def get_output_spikes(self):
        """Get output spikes.

        Returns:
            numpy.array: Output spikes
        """
        return self.probes['output_spikes']['data']

    def get_network(self):
        """ Get network.

        Returns:
            nengo.Network.: Created SNN. 
        """
        return self.net
