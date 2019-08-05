# Homework 6

## Problem Statement: 
As the problem of drug abuse intensifies in the U.S., many studies that primarily utilize
social media data, such as postings on Twitter, to study drug abuse-related activities use machine learning as a
powerful tool for text classification and filtering. However, given the wide range of topics of Twitter users,
tweets related to drug abuse are rare in most of the datasets. This imbalanced data remains a major issue in
building effective tweet classifiers, and is especially obvious for studies that include abuse-related slang terms.
In this final challenge, we would like to explore two methods to facilitate the capturing process of drug abuse
activities more effectively (using Twitter data):
- Generate a visualization showing the distribution of drug-abuse-related tweets throughout the country
- Discover keywords in drug-abuse-related tweets using term-frequency/invert document frequency
Note that, in this initial study, we only want to apply the methods over major areas in the US, in particular,
within the top 500 largest cities in the US. Regardless of the method, we also need to filter a collection of
geo-tagged tweets to keep only those that are related to drug-abused based on a set of pre-defined
keywords.

# CHALLENGE 1: Visualizing the distribution of drug-abuse-related tweets
The geo-location information tagged in drug-related tweets is very useful to capture the distribution of drug
abuse-risk behaviors. An example of the tweet distribution across the US is shown in the figure below.
According to this visualization, the potential greatest drug threat regions could have been in the Florida
region, the Great Lakes region, the Mid-Atlantic region, the New York/New Jersey region, the New England
region, the Pacific region, the Southeast region, the Southwest region, and the West Central region. However,
this information might be biased since the geo-location distribution should be normalized by population
density. Your task is to produce the data needed for a less-biased visualization at the census tract level, where
each represents the normalized number of drug-related tweets per population density. In other words, for
each census tract, you need to compute the ratio of the number drug-related tweets over the population in the
tract.

## Project setup
- Instruction for project setup is available in readme file in the root directory.
  - 
