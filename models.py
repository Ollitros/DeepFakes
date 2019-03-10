from keras.layers import Input, Conv2D, UpSampling2D, MaxPool2D, BatchNormalization, LeakyReLU, Dropout
from keras.models import Model
from keras.layers import Conv2DTranspose


def Autoencoders(input_shape):

    # #######################
    # ## Make encoder
    # #######################

    encoder_inputs = Input(shape=input_shape)
    x = Conv2D(64, (3, 3), padding='same', activation='relu')(encoder_inputs)
    x = Dropout(0.1)(x)
    x = MaxPool2D(pool_size=(2, 2))(x)
    x = Conv2D(128, (3, 3), padding='same', activation='relu')(x)
    x = Dropout(0.1)(x)
    x = MaxPool2D(pool_size=(2, 2))(x)
    x = Conv2D(256, (3, 3), padding='same', activation='relu')(x)
    x = Dropout(0.1)(x)
    x = MaxPool2D(pool_size=(2, 2))(x)
    encoder_output = Conv2D(512, (3, 3), padding='same', activation='relu')(x)

    # #######################
    # ## Make src_decoder
    # #######################

    src_inputs = Input(shape=(25, 25, 512))
    src_decoder_input = Conv2D(512, (3, 3), padding='same', activation='relu')(src_inputs)
    src_decoder_input = Dropout(0.1)(src_decoder_input)
    x = UpSampling2D((2, 2))(src_decoder_input)
    x = Conv2D(256, (3, 3), padding='same', activation='relu')(x)
    x = Dropout(0.1)(x)
    x = UpSampling2D((2, 2))(x)
    x = Conv2D(128, (3, 3), padding='same', activation='relu')(x)
    x = Dropout(0.1)(x)
    x = UpSampling2D((2, 2))(x)
    src_decoder_output = Conv2D(3, (3, 3), activation='sigmoid', padding='same')(x)

    # #######################
    # ## Make dst_decoder
    # #######################

    dst_inputs = Input(shape=(25, 25, 512))
    dst_decoder_input = Conv2D(512, (3, 3), padding='same', activation='relu')(dst_inputs)
    dst_decoder_input = Dropout(0.1)(dst_decoder_input)
    x = UpSampling2D((2, 2))(dst_decoder_input)
    x = Conv2D(256, (3, 3), padding='same', activation='relu')(x)
    x = Dropout(0.1)(x)
    x = UpSampling2D((2, 2))(x)
    x = Conv2D(128, (3, 3), padding='same', activation='relu')(x)
    x = Dropout(0.1)(x)
    x = UpSampling2D((2, 2))(x)
    dst_decoder_output = Conv2D(3, (3, 3), activation='sigmoid', padding='same')(x)

    encoder = Model(inputs=encoder_inputs, outputs=encoder_output)
    encoder.compile(loss='mean_squared_error', optimizer='adam')

    src_decoder = Model(inputs=src_inputs, outputs=src_decoder_output)
    src_decoder.compile(loss='mean_squared_error', optimizer='adam')

    dst_decoder = Model(inputs=dst_inputs, outputs=dst_decoder_output)
    dst_decoder.compile(loss='mean_squared_error', optimizer='adam')
    print(encoder.summary())
    return encoder, src_decoder, dst_decoder


# ###################################################################################
# This code just for example to investigate how create such model with gotten weights
# ###################################################################################

# def MergedAutoencoder(X, src_model, dst_model):
#
#     encoder = Model(inputs=src_model.input, outputs=src_model.get_layer('src_encoder_output').output)
#     encoder.compile(loss='mean_squared_error', optimizer='adam')
#     prediction = encoder.predict(X)
#
#     inputs = Input(shape=(25, 25, 512))
#     x = dst_model.get_layer('dst_decoder_input')(inputs)
#     x = dst_model.get_layer('up_sampling2d_3')(x)
#     x = dst_model.get_layer('conv2d_10')(x)
#     x = dst_model.get_layer('up_sampling2d_4')(x)
#     x = dst_model.get_layer('conv2d_11')(x)
#     x = dst_model.get_layer('up_sampling2d_5')(x)
#     x = dst_model.get_layer('decoder_output')(x)
#
#     decoder = Model(inputs=inputs, outputs=x)
#     decoder.compile(loss='mean_squared_error', optimizer='adam')
#     prediction = decoder.predict(prediction)
#
#     return prediction
