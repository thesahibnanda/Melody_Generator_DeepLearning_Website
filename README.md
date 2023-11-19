# **Melody Generator Website**
![README](https://img.shields.io/badge/README-Project-blue.svg)

<br>

## **Table of Contents**
- [**Introduction**](#introduction)
- [**Working**](#working)
- [**Enhance Model**](#enhance-model)
- [**Conclusion**](#conclusion)
- [**References**](#references)

<br>

## **Introduction**

I Have Engineered a Sophisticated Flask-Based Web Application Designed to Produce Musical Melodies. The Core of This Project Involves Training a Machine Learning Model on a Meticulously Prepared Dataset Comprised of Folk Songs Encoded in .krn Format. The Model Leverages the Power of a Long Short-Term Memory (LSTM) Network as Its Primary Layer, Implemented Through the Keras Library on the TensorFlow Platform.

To Ensure Optimal Performance, I Have Undertaken an Extensive Preprocessing Phase on the Dataset, Fine-Tuning It to Extract Meaningful Patterns and Nuances Inherent in the Folk Songs. The Model Is Adept at Learning the Intricate Structures and Relationships Within the Musical Data.

The User Interaction Is Intuitive and Seamless. Individuals Can Input a Melody in Midi Format, and the Model, Utilizing Its Trained Knowledge, Generates a Novel Melody by Predicting Subsequent Notes and Rests. The Outcome Is Presented to the User in Midi Format, Providing a Synthesized Representation of the Generated Musical Composition. This Process Not Only Showcases the Capabilities of the Model but Also Allows Users to Witness Firsthand the Creative Output Derived From Their Initial Musical Input.

## **Working**

1. Open Terminal And Clone Repository
    ```bash
    git clone https://github.com/thesahibnanda/Melody_Generator_DeepLearning_Website.git
    ```
2. Now Run Following Command To Navigate Inside Repository
    ```bash
    cd Melody_Generator_DeepLearning_Website
    ```
3. Now Install Requirements
    ```bash
    pip install -r requirements.txt
    ```
4. Now Execute Following Command In The Terminal To Navigate To The Folder `Main_Project_Files`
    ```bash
    cd Main_Project_Files
    ```
5. Now Run Flask App
    ```bash 
    py app.py
    ```
6. Now Go To ```http://127.0.0.1:5000/``` In Any Browser And Get Your Hands On The Website

## **Enhance Model**

To Enhance Model You Can Do The Following
- Go To The Folder `model_building` In `Main_Project_Files` & Edit [preprocess.py](Main_Project_Files/model_building/preprocess.py) As Follows  
    Edit _Line 198_ (In `main()` Function): Change From `tiny_dataset` (Has Very Less Datapoints) To `amount_dataset` (Has Good Amount Of Datapoints) Or `full_dataset` (Has All Datapoints) For Better Model Training
    
    ```py
    def main():
        folder_path = r'tiny_dataset' # This Is Line 198
        preprocess(folder_path)
        songs = create_single_file_dataset(folder_path+"_preprocessed", r'Songs.txt')
        output_units = create_map(songs, r'Mapping.json')
        int_songs = songs_to_int(r'Mapping.json', r'Songs.txt')
        inputs, targets = generate_sequence(int_songs)
        return inputs, targets, output_units
    ```
    **After Making Changes, Run [train.py](Main_Project_Files/model_building/train.py) In Same Folder Once** <br>
- Go To The Folder `model_building` In `Main_Project_Files` & Edit [train.py](Main_Project_Files/model_building/train.py) As Follows 
    Edit _Line 32_ (In `train()` Function): You Can Replace `[256]` With `[256, 256]` For Two LSTM Layers Or As Per Your Need Add Numbers In List To Add As Many Layers You Like
    ```py
    def train(epochs=50, batch_size=32, val_split=0.05, model_name = "model.h5"):
        # Import Training Sequences
        inputs, targets, output_units = preprocess.main()

        num_units = [256] # This Is Line 32

        loss = 'sparse_categorical_crossentropy'

        learning_rate = 0.001

        # Build The Network
        model = build_model(output_units, num_units, loss, learning_rate)

        # Train Network
        model.fit(inputs, targets, epochs=epochs, batch_size=batch_size, validation_split=val_split)  # You can adjust batch_size and validation_split as needed

        # Save Model
        model.save(model_name)  
    ```
    **After Making Changes, Run `train.py`** <br>

### You Can Make Both The Above Listed Changes

## **Conclusion**
In Conclusion, This Project Stands as a Testament to the Intricacies of Musical Composition Seamlessly Interwoven With Cutting-Edge Technology. Through the Meticulous Engineering of a Flask-Based Web Application and the Implementation of a Sophisticated Model, I've Not Only Demonstrated Technical Prowess but Also a Deep Understanding of the Artistry Inherent in Folk Melodies.

The Utilization of a Long Short-Term Memory (LSTM) Network, Orchestrated With Precision Using the Keras Library on the TensorFlow Platform, Underscores the Depth of My Expertise in Machine Learning and Neural Networks. The Model's Ability to Distill Intricate Patterns from Folk Songs Encoded in .krn Format Reflects the Meticulous Nature of the Dataset Preprocessing, Showcasing a Commitment to Excellence in Every Aspect of This Project.

This Endeavor Is More Than a Mere Amalgamation of Code and Data; It Is a Harmonious Symphony of Technical Proficiency and Creative Insight. The User-Friendly Interface Further Underscores My Commitment to Providing an Accessible Platform, Allowing Individuals to Actively Participate in the Creative Process of Music Generation.

In Crafting This Musical Melody Generation Model, I Have Not Only Demonstrated Technical Acumen but Also a Passion for Pushing the Boundaries of What Is Possible. This Project Serves as a Testament to My Skillset, Illustrating an Ability to Navigate the Complexities of Both Musical Composition and Machine Learning With Finesse. The Amalgamation of These Elements Culminates in a Model That Not Only Generates Melodies but Does So With a Nuanced Understanding of the Rich Tapestry of Folk Music.

## **References**
- [YouTube Link For Login / Sign Up Page](https://youtu.be/PlpM2LJWu-s?t=9)
- [Dataset](http://www.esac-data.org/)
