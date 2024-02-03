import json
import numpy as np
import music21 as m21
import tensorflow as tf
from model_building.preprocess import encode_song, transpose

Mapping_Path = r'model_building/Mapping.json'
Seq_Len = 64

class MelodyGenerator:

    def __init__(self, model_path=r"model_building/model.h5"):
        self.model_path = model_path
        self.model = tf.keras.models.load_model(model_path)

        with open(Mapping_Path, "r") as file:
            self._mappings = json.load(file)

        self._start_symbols = ["/"] * Seq_Len

    def _sample_with_temperature(self, probabilities, temperature):
        predictions = np.log(probabilities + 1e-8) / temperature
        probabilities = np.exp(predictions) / np.sum(np.exp(predictions))

        choices = range(len(probabilities))
        index = np.random.choice(choices, p=probabilities)

        return index

    def generate(self, seed, num_steps, max_seq_len, temperature):

        seed = seed.split()

        melody = seed

        seed = self._start_symbols + seed

        inputs = []
        for symbol in seed:
            try:
                if symbol in seed:  # This line can be removed
                    inputs.append(self._mappings[symbol])
                else:
                    try:
                        inputs.append(self._convert_keys_and_find_nearest(self._mappings, int(symbol)))
                    except:
                        inputs.append(self._mappings["_"])
            except:
                try:
                    inputs.append(self._convert_keys_and_find_nearest(self._mappings, int(symbol)))
                except:
                    inputs.append(self._mappings["_"])

            # Such Vigourous Exception Handling Just To Make Sure, It Works Correctly When Deployed
        seed = inputs

        for _ in range(num_steps):
            seed = seed[-max_seq_len:]

            one_hot_seed = tf.keras.utils.to_categorical(seed, num_classes=len(self._mappings))
            one_hot_seed = one_hot_seed[np.newaxis, ...]

            probabilities = self.model.predict(one_hot_seed)[0]

            output_int = self._sample_with_temperature(probabilities, temperature)

            seed.append(output_int)

            output_symbol = [k for k, v in self._mappings.items() if v == output_int][0]

            if output_symbol == "/":
                break

            melody.append(output_symbol)

        return melody

    def save_melody(self, melody, format="midi", file_name=r"static/generated_midi_file.midi", step_duration=0.25):
        stream = m21.stream.Stream()
        start_symbol = None
        step_counter = 1

        for i, symbol in enumerate(melody):
            if symbol != "_" or i + 1 == len(melody):
                if start_symbol is not None:
                    quarter_length_duration = step_duration * step_counter

                    if start_symbol == "r":
                        m21_event = m21.note.Rest(quarterLength=quarter_length_duration)
                    else:
                        m21_event = m21.note.Note(int(start_symbol), quarterLength=quarter_length_duration)

                    stream.append(m21_event)
                    step_counter = 1

                start_symbol = symbol

            else:
                step_counter += 1

        stream.write(format, file_name)

    def _convert_keys_and_find_nearest(self, dictionary, target_number):
        int_keys = [int(key) for key in dictionary.keys()]
        nearest_key = min(int_keys, key=lambda x: abs(x - int(target_number)))
        return nearest_key

    def midi_accept(self, file_path):
        song = encode_song(transpose(m21.converter.parse(file_path)))

        melody = self.generate(song, 100, Seq_Len, 0.3)
        self.save_melody(melody)

