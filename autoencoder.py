from keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D
from keras.models import Model
from keras.callbacks import History
import matplotlib.pyplot as plt

class Autoencoder:
    def __init__(self, input_shape=(28, 28, 1), latent_dim=10):
        self.input_shape = input_shape
        self.latent_dim = latent_dim
        self.autoencoder_model = self.__build_autoencoder()

    def __build_autoencoder(self):
        input_img = Input(shape=self.input_shape)

        # Encoder
        conv1 = Conv2D(32, (3, 3), activation='gelu', padding='same')(input_img)
        pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)
        conv2 = Conv2D(64, (3, 3), activation='gelu', padding='same')(pool1)
        pool2 = MaxPooling2D(pool_size=(2, 2))(conv2)
        conv3 = Conv2D(self.latent_dim, (3, 3), activation='gelu', padding='same')(pool2)
        #10 pixels

        # Decoder
        conv4 = Conv2D(64, (3, 3), activation='gelu', padding='same')(conv3)
        up1 = UpSampling2D((2, 2))(conv4)
        conv5 = Conv2D(32, (3, 3), activation='gelu', padding='same')(up1)
        up2 = UpSampling2D((2, 2))(conv5)
        decoded = Conv2D(1, (3, 3), activation='sigmoid', padding='same')(up2)

        # Autoencoder model
        autoencoder_model = Model(input_img, decoded)
        autoencoder_model.compile(optimizer='adam', loss='binary_crossentropy',metrics=['accuracy'])

        return autoencoder_model

    def train(self, x_train,x_val, epochs=40, batch_size=64):
        history = History()

        self.autoencoder_model.fit(x_train,x_train, epochs=epochs, batch_size=batch_size,validation_data=[x_val,x_val],callbacks=[history], shuffle=True,verbose=2)

        training_loss = history.history['loss']
        validation_loss = history.history['val_loss']

        #training_accuracy = history.history['accuracy']
        #validation_accuracy = history.history['val_accuracy']

        epochs_range = range(1, epochs + 1)

        self.PlotLearningCurve(training_loss,validation_loss,epochs_range)
        #self.PlotLearningCurve(training_accuracy,validation_accuracy,epochs_range,['Training Accuracy','Validation Accuracy'],'Training and Validation Accuracy','Accuracy','accuracy_fig')

    #Returns image in latent space
    def encode(self, x):
        encoder_model = Model(self.autoencoder_model.input, self.autoencoder_model.layers[4].output)
        return encoder_model.predict(x)

    def decode(self, x):
        decoder_model = Model(self.autoencoder_model.layers[5].input, self.autoencoder_model.layers[-1].output)
        return decoder_model.predict(x)
    
    def evaluate(self,validation_set):
        validation_loss = self.autoencoder_model.evaluate(validation_set,validation_set)
        print(f"Reconstruction Loss on Validation Set: {validation_loss}")


    def PlotLearningCurve(self,training_data,validation_data,epochs_range,labels=['Training Loss','Validation Loss'],title='Training and Validation Loss',ylabel='Loss',output_file='./Images/loss_fig2'):
        plt.figure(figsize=(8,4))

        plt.plot(epochs_range,training_data,label=labels[0])
        plt.plot(epochs_range,validation_data,label=labels[1])

        plt.title(title)

        plt.xlabel('Epochs')
        plt.ylabel(ylabel)

        plt.legend()
        plt.savefig(output_file)

