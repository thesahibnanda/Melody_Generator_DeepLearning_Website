import os
import json
import warnings
import numpy as np
import music21 as m21 
import tensorflow as tf



# Ignore all warnings temporarily
warnings.filterwarnings("ignore")

def load_songs(dataset_path):
    # Create an empty list to store parsed songs
    song_list = []
    
    # Generate a list of file paths by joining the dataset_path with each file in the directory
    file_list = [os.path.join(dataset_path, file_name) for file_name in os.listdir(dataset_path)]
    
    # Iterate through each file path
    for file_path in file_list:
        # Parse the music file using music21
        song = m21.converter.parse(file_path)
        
        # Add the parsed song to the list
        song_list.append(song)
    
    # Return the list of parsed songs
    return song_list


def acceptable_duration(song, acc_dur=[0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0]):
    # Iterate over each note and rest in the flattened representation of the 'song'
    for note in song.flat.notesAndRests:

        # Check if the duration of the current note or rest is not in the list of accepted durations
        if note.duration.quarterLength not in acc_dur:

            # If the duration is not in the accepted list, return False
            return False
        
    # If all notes and rests have durations in the accepted list, return True
    return True


def transpose(song):
    # Get key of the song
    parts = song.getElementsByClass(m21.stream.Part)
    measurePart0 = parts[0].getElementsByClass(m21.stream.Measure)
    key = measurePart0[0][4] # Here Is Where Key Is Stored At Index 4 In First Part's First Measure

    # Estimate key using music21
    if not isinstance(key, m21.key.Key):
        key = song.analyze("key")

    # Get interval for transposition (Example: B-Major -> C-Major)
    if key.mode == "major":
        interval = m21.interval.Interval(key.tonic, m21.pitch.Pitch("C"))
    elif key.mode == "minor":
        interval = m21.interval.Interval(key.tonic, m21.pitch.Pitch("A"))

    # Transpose Song By Calculated Interval
    transposedSong = song.transpose(interval)

    return transposedSong


def encode_song(song, time_step = 0.25):
    # Time Series Representation Encoding

    encoded_song = []

    for event in song.flat.notesAndRests:
        symbol = ""
        # Handle Notes
        if isinstance(event, m21.note.Note):
            symbol = event.pitch.midi  
        elif isinstance(event, m21.note.Rest):
            symbol = "r"
    
        # Convert It Into Time-Seriese
        steps = int(event.duration.quarterLength / time_step)
        for step in range(steps):
            if step == 0:
                encoded_song.append(symbol)
            else:
                encoded_song.append("_")
    encoded_song = " ".join(map(str, encoded_song))

    return encoded_song

def preprocess(dataset_path):
    
    output_path = dataset_path + "_preprocessed"

    # Create output directory if it doesn't exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Load Folk Songs From Dataset Folder
    # print("Loading Songs")
    songList = load_songs(dataset_path)
    # print(f"Length Of The Songs: {len(songList)}")

    # Preprocess
    for index, song in enumerate(songList):

        # Filter Out Songs Whith Non Acceptable Duration
        if not acceptable_duration(song):
            continue

        # Transpose Songs To C-Major/A-Minor (We Don't Learn About All The Keys,  We Just Wanna Reduce Everything To C-Major And A-Minor So That Model Learns Easily)
        song = transpose(song)

        # Encode Songs With Music Time Series Representation
        encoded_song = encode_song(song)

        # Save Songs
        save_path = os.path.join(output_path, str(index)+".txt")
        with open(save_path, 'w') as file:
            file.write(encoded_song)

    # Return 
    return

def load(file_path):
    with open(file_path, 'r') as file:
        song = file.read()
    return song

def create_single_file_dataset(dataset_path, single_file_path, seq_len: int = 64):

    delimiter = '/ ' * seq_len 

    songs = ""

    # Load Encoded Song And Add Delimiter

    for path, _, files in os.walk(dataset_path):
        for file in files:
            file_path = os.path.join(path, file)
            song = load(file_path)
            songs = songs + song + " " + delimiter
    
    songs = songs[:-1]

    with open(single_file_path, 'w') as file:
        file.write(songs)

    return songs

def create_map(songs, mapping_path):
    
    mappings = {}

    songs = songs.split()

    vocabs = list(set(songs))

    for index, vocab in enumerate(vocabs):
        mappings[vocab] = index
    
    with open(mapping_path, 'w') as file:
        json.dump(mappings, file, indent=2)
    
    return len(mappings)

def songs_to_int(mapping_path, songs_path) -> list:
    int_songs = []
    song_file = open(songs_path, 'r')
    songs = song_file.read()
    song_file.close()
    with open(mapping_path, 'r') as file:
        mappings = json.load(file)
    songs = songs.split()

    for symbol in songs:
        int_songs.append(mappings[symbol])
    
    return int_songs

def generate_sequence(int_songs:list, seq_len: int = 64):
    num_seq = len(int_songs) - seq_len
    inputs = []
    targets = []
    for i in range(num_seq):
        inputs.append(int_songs[i:i+seq_len])
        targets.append(int_songs[i+seq_len])
    # One Hot Encoding
    vocab_size = len(set(int_songs))
    inputs = tf.keras.utils.to_categorical(inputs, num_classes=vocab_size)
    targets = np.array(targets)

    return inputs, targets


def main():
    folder_path = r'tiny_dataset' # Change From `tiny_dataset` (Has Very Less Datapoints) To `amount_dataset` (Has Good Amount Of Datapoints) Or `full_dataset` (Has All Datapoints) For Better Model Training
    preprocess(folder_path)
    songs = create_single_file_dataset(folder_path+"_preprocessed", r'Songs.txt')
    output_units = create_map(songs, r'Mapping.json')
    int_songs = songs_to_int(r'Mapping.json', r'Songs.txt')
    inputs, targets = generate_sequence(int_songs)
    return inputs, targets, output_units

