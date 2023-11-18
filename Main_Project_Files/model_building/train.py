import tensorflow as tf

# Import Preproecessing Functions
import preprocess

def build_model(output_units: int, num_units=[256, 256], loss='sparse_categorical_crossentropy', learning_rate=0.001):
    # Create Model
    input_layer = tf.keras.layers.Input(shape=(None, output_units))
    
    x = input_layer
    for i, units in enumerate(num_units):
        x = tf.keras.layers.LSTM(units, return_sequences=(i < len(num_units) - 1))(x)
        x = tf.keras.layers.Dropout(0.2)(x)
    
    # Output layer
    output_layer = tf.keras.layers.Dense(output_units, activation='softmax')(x)
    
    # Define the model
    model = tf.keras.Model(inputs=input_layer, outputs=output_layer)
    
    # Compile Model
    optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
    model.compile(optimizer=optimizer, loss=loss, metrics=['accuracy'])
    
    print(model.summary())
    return model

def train(epochs=50, batch_size=32, val_split=0.05, model_name = "model.h5"):
    # Import Training Sequences
    inputs, targets, output_units = preprocess.main()

    num_units = [256] # You Can Replace It With [256, 256] For Two LSTM Layers Or As Per Your Need Alter Code

    loss = 'sparse_categorical_crossentropy'

    learning_rate = 0.001

    # Build The Network
    model = build_model(output_units, num_units, loss, learning_rate)

    # Train Network
    model.fit(inputs, targets, epochs=epochs, batch_size=batch_size, validation_split=val_split)  # You can adjust batch_size and validation_split as needed

    # Save Model
    model.save(model_name)  


if __name__ == "__main__":
    train()