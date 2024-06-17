## Overview

This dataset encompasses a compilation of incidents, reports, and other activities documented by the Oklahoma Police Department. It has been enhanced to extract meaningful fields that can aid in analyzing patterns of incidents or identifying any biases in reported crimes. Furthermore, it holds potential for application in predictive policing.

## Data Description

The dataset is composed of 8 fields: Day of the Week, Time of Day, Weather, Location Rank, Side of Town, Incident Rank, Nature, and EMSSTAT. These fields are derived from the original incident reports, which encompass datetime, incident number, location, nature, and incident ori. The incident reports have been preprocessed, yet invalid entries have not been removed. In cases where augmentation of a field is not feasible, the field is populated with the term 'unknown' instead of being omitted. This approach allows users to retain more control over the data.

## Dataset Structure

### Day of the Week
This field specifies the day of the week when the incident occurred, extracted from the 'Date / Time' field of the incident report. The days are represented by numerical values ranging from 1 to 7, corresponding to Sunday through Saturday, respectively.

### Time of Day
Derived from the 'Date / Time' field of the incident report, this field indicates the hour when the incident was reported. It is represented by numerical values ranging from 0 to 23.

### Weather
This field provides information about the weather conditions at the time of the incident. It is represented by a VMO code, which is determined by using the 'Location' field of the incident report. The location is first converted into coordinates using the Google Geocoding API, and then these coordinates are used to obtain the weather conditions from the Open Meteo Weather API. If the location cannot be identified, the field is filled with 'unknown'.

### Location Rank
This field ranks the locations based on the frequency of reported incidents. It is determined using the 'Location' field of the original incident report. Locations with the same frequency of incidents are assigned the same rank.

### Side of Town
This field categorizes the incident location based on which part of the town it occurred in. It is determined using the 'Location' field of the incident report and the coordinates obtained from the Google Geocoding API, relative to the town's center. Possible values include N, S, E, W, NW, NE, SW, and SE. If the location cannot be identified, the field is filled with 'unknown'.

### Incident Rank
This field ranks incidents based on their frequency. It is determined using the 'Nature' field of the original incident report. Incidents with the same frequency are assigned the same rank.

### Nature
This field describes the actual nature of the incident, as recorded in the original report.

### EMSSTAT
This field indicates whether an incident is related to an emergency, based on the 'Incident Ori' field from the original report. It is represented by boolean values.

## Dataset Size

The size of the dataset is dynamic, with new information being added as the Oklahoma Police Department updates their reports. On average, there are approximately 350 incidents documented per day.

## Sources

1. Incident reports are sourced from the Norman Police Department website: [https://www.normanok.gov/public-safety/police-department/crime-prevention-data/department-activity-reports](https://www.normanok.gov/public-safety/police-department/crime-prevention-data/department-activity-reports)
2. Weather data is obtained from the Open Meteo API: [https://open-meteo.com/](https://open-meteo.com/)
3. Geocoding is provided by the Google Geocoding API: [https://developers.google.com/maps/documentation/geocoding/overview](https://developers.google.com/maps/documentation/geocoding/overview)

## Usage

This dataset can be utilized for various studies, including examining biases in policing, understanding crime patterns, and implementing predictive policing strategies. It can also assist in strategically positioning ambulances and police units.