# CE1115 DSAI Project 
> Data Science Project to build a movie tagline predictor. 


#### We have documented all our methods and findings extensively on our Github Page. You can access it [here](https://benjamintdk.github.io/DSAI_proj/)


## Project motivation and utility

Ever found yourself staring at a certain movie tagline and wondering what on earth the directors were thinking about when they came up with it? Yes, we too. On the other hand, we've also often been on the other end of the spectrum, struggling to come up with creative titles for our projects or succinct one-liners to encapsulate our business pitches. Enter our movie tagline predictor, a model we have built which we hope will provide some enlightenment to the many lost souls described above.

We believe that this model can also eventually be transferrable to other salient applications, such as the information retrieval and search engine we often see accompanying our everyday Google searches. 

## Data Extraction

The main function in this package perform the following functions for data extraction via the TMDB API:
- Multi-threaded download of movie information via the extract_dataset_threaded function.
- Saving the data to a raw_data.csv file.

## Exploratory Data Analysis & Visualization

Now that we have our raw dataset to work with, we begin by looking at:
- The different types of data present.
- How they might be relevant to our task.
- Their respective distributions and whether there might be class imbalances.
- Missing data and other considerations to be had later during cleaning.

## Data Cleaning and Feature Engineering 

After the EDA step, we have generated insights from the data in terms of their distribution and relevance our overall task. The functions in this package we perform the following functions to clean and feature engineer the raw data:
- Drop columns which are irrelevant.
- For columns/features with json objects, unpack the json objects into new columns.
- For categorical features, ensure that they are categorized accordingly.
- For datetime features, ensure that they are separated out into year, month and day before either being rescaled or binned.
- Separate out examples with and without taglines.
- Save the dataset into separate train, valid, test and tagless csv files.

## Dataset

We next create the Dataset class to encapsulate all the different types of data which we will be working with. We also add in augmentations and transformations including:
- Tokenization of text based on the text based encoder which we will be using (DistilBert).
- RandomResizeCrop to resize all images to a standard size and crop them randomly.
- Normalization and Standardization of all images on the imagenet dataset statistics.
- Converting all features to Pytorch tensors. 

## Modelling

![](model_diagram.jpg)

Moving on, we model the problem by creating the architectures and modules required to map the various inputs to the predicted tagline. In our case, we will be using an encoder-decoder based structure, with the encoder consisting of separate networks for image, text and meta/tabular data respectively, while the decoder consists of a Conv1D, a linear layer, a Dropout layer and a final softmax layer to output the predicted sequence. 

## Training and Evaluation

We leverage the famous FastAI library to help us with training. The library provides us with numerous benefits, including advanced training techniques using learning rate schedulers and discriminative learning rates, along with seamless integration of features such as mixed precision training in the case where our model might be too big for GPU memory.

Here, we train our model and validate it on the validation dataset to give ourselves a good idea of how our model might perform in the real world. Then we save the model to use it for further testing.

## Results interpretation and Future Work

We interpret the results and provide recommendations/suggestions for how we could further improve the results. This is done by separating the sections for targeted improvement into data, model, loss function and problem reformulation.

## Individual Contributions

Ying Cheng: Cleaning, Preprocessing & Extraction

Mitchell: Exploratory Data Analysis and Visualization

Benjamin: Modelling, Training and Evaluation
