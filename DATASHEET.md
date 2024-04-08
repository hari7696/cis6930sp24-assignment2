

### BASICS: CONTACT, DISTRIBUTION, ACCESS

**Name:** Enhanced Norman Incident Report Data  
**Dataset Version:** v1.0, Released on April 8, 2024  
**Dataset Owner:** Hari Krishna Reddy, Email: golamari.h@ufl.edu, Phone: 352-XXX-XXXX  
**Access:** This dataset is licensed under Apache License 2.0.  
**Data Access:** For access to this dataset, please contact Dr. Grant at the University of Florida.

### DATASET CONTENTS

This dataset is an enriched compilation of incidents, reports, and other activities documented by the Norman Police Department in Oklahoma. It has been processed to extract meaningful fields that facilitate the analysis of incident patterns and the identification of potential biases in reported crimes. The dataset is also suitable for use in predictive policing models.

#### What does each item/data point represent?

The dataset consists of 8 fields derived from the original incident reports. These fields include:

1. **Day of the Week:** Indicates the day of the week on which the incident occurred, with numerical values from 1 to 7 representing Sunday to Saturday, respectively.

2. **Time of Day:** Represents the hour of the day when the incident was reported, with numerical values from 0 to 23.

3. **Weather:** Provides information about the weather conditions at the time of the incident, represented by a VMO code. Weather data is obtained using the Open Meteo Weather API, based on coordinates derived from the incident location.

4. **Location Rank:** Ranks the locations based on the frequency of reported incidents, with locations having the same frequency assigned the same rank.

5. **Side of Town:** Categorizes the incident location based on which part of the town it occurred in, with possible values including N, S, E, W, NW, NE, SW, and SE.

6. **Incident Rank:** Ranks incidents based on their frequency, with incidents having the same frequency assigned the same rank.

7. **Nature:** Describes the actual nature of the incident as recorded in the original report.

8. **EMSSTAT:** Indicates whether an incident is related to an emergency, based on the 'Incident Ori' field from the original report, represented by boolean values.

#### How many items are in the dataset?

The size of the dataset is dynamic, with new information being added as the Norman Police Department updates their reports. On average, there are approximately 350 incidents documented per day.

### INTENDED & INAPPROPRIATE USES

#### Intended Uses

The dataset is designed for a variety of purposes within the realms of public safety, academic research, and policy analysis:

1. **Crime Pattern Analysis:** Researchers and analysts can use the dataset to identify patterns and trends in crime, such as seasonal variations, time-of-day patterns, and hotspots.

2. **Predictive Policing:** Law enforcement agencies can utilize the dataset to develop predictive policing models that anticipate where and when crimes are likely to occur, enabling proactive deployment of resources.

3. **Bias Analysis:** The dataset can be used to examine potential biases in policing, such as disparities in incident reporting or response based on location or nature of the incident.

4. **Public Safety Planning:** Urban planners and public safety officials can use the dataset to inform the strategic positioning of emergency services, such as police patrols and ambulances.

5. **Academic Research:** Scholars and students in criminology, sociology, and data science can use the dataset for research projects, theses, and dissertations related to public safety and crime analysis.

#### Inappropriate Uses

While the dataset offers valuable insights, it is important to recognize and avoid inappropriate uses:

1. **High-Precision Location-Based Models:** The dataset should not be used for applications that require precise geolocation data, as the geocodes are rounded off for privacy reasons. its rounded upto 4 decimals, giving an accuracy of upto 11 meters.

2. **Individual Profiling:** The dataset should not be used to profile individuals or make assumptions about their behavior based on incident data.

3. **Discriminatory Practices:** The dataset should not be used to support discriminatory practices or policies, such as targeting specific communities based on the frequency of incidents.

4. **Commercial Exploitation:** The dataset should not be used for commercial purposes that conflict with its intended use for public safety and research.

5. **Misrepresentation of Data:** The dataset should not be misrepresented or manipulated to support unfounded conclusions or narratives.



### DATA COLLECTION PROCEDURES

The incident reports are collected from the Norman Police Department website using Python requests. The script is run by the author on a local system.

The data is fetched via an HTTPS connection, ensuring the security of the source. The website for accessing the incident reports is [Norman Police Department](https://www.normanok.gov/public-safety/police-department/crime-prevention-data/department-activity-reports).

* Source Identification: The primary source of data is the official website of the Norman Police Department, where daily incident reports are published. These reports provide a comprehensive record of all incidents reported to the police within the city of Norman, Oklahoma.

* Automated Data Retrieval: A Python script is employed to automatically fetch the incident reports from the police department's website. The script is scheduled to run at regular intervals to ensure that the dataset is continuously updated with the latest available data.

* PDF Parsing: The incident reports are typically published in PDF format. The Python script uses libraries such as PyPDF2 or pdfplumber to extract the text content from the PDF files. Special attention is paid to maintaining the integrity of the data during the extraction process.

* Data Extraction: The extracted text is then processed to identify and extract relevant information for each incident, such as the date and time, location, nature of the incident, and any other pertinent details. Regular expressions and text parsing techniques are used to accurately extract this information.

* Data Transformation: The extracted data is transformed into a structured format suitable for analysis. This involves cleaning the data, standardizing formats, and converting data types as necessary. For example, dates and times are converted to a standard format, and location data is geocoded to obtain latitude and longitude coordinates.


### REPRESENTATIVENESS

The dataset is a detailed representation of incidents reported by the Norman Police Department, providing insights specific to the city of Norman, Oklahoma. It covers a wide range of incidents, from minor offenses to major crimes, offering a comprehensive view of public safety concerns within the city. 

* Geographic Coverage

    The dataset is geographically confined to the city of Norman, ensuring that the data accurately reflects the local context and dynamics. This focus allows for targeted analysis and interventions tailored to the specific needs and characteristics of the city.

* Temporal Coverage

    The dataset includes incidents reported over a specified time period, providing a snapshot of public safety issues during that timeframe. The dynamic nature of the dataset allows for continuous updates, enabling analysis of trends and patterns over time.

* Incident Diversity

    The dataset encompasses a diverse array of incidents, capturing a broad spectrum of public safety concerns. This diversity ensures that the dataset is representative of the various types of incidents that occur within the city, providing a holistic view of public safety.

* Limitations

    While the dataset provides valuable insights into incidents reported in Norman, it is important to acknowledge its limitations:

1. **Demographic Representation:** The dataset does not include demographic information, which limits the ability to analyze incidents in the context of demographic factors such as age, gender, or race.

2. **Unreported Incidents:** The dataset only includes incidents that have been reported to the police. Incidents that go unreported are not captured in the dataset, which may result in an incomplete picture of public safety in the city.

3. **External Validity:** The representativeness of the dataset is specific to the city of Norman and may not be generalizable to other cities or regions. Caution should be exercised when extrapolating findings beyond the local context.

#### Future Enhancements

Efforts to enhance the representativeness of the dataset may include:

1. **Integration of Demographic Data:** Incorporating demographic information into the dataset, where available and appropriate, could enable more nuanced analyses of incidents in relation to demographic factors.

2. **Community Engagement:** Engaging with the community to encourage reporting of incidents and to gather feedback on public safety concerns can help ensure that the dataset reflects the full spectrum of issues faced by the city.

3. **Comparative Analysis:** Comparing data from Norman with data from other cities could provide insights into the unique and common aspects of public safety across different contexts.

### DATA QUALITY

After fetching the incident report, the data goes through a Python script for enhancement and attribute addition. Not all fields may have values; in cases where a value cannot be determined, the field is filled with 'unknown'.

* Validation: The data is validated at various stages of the processing pipeline to ensure its accuracy and completeness. This includes checks for data consistency, range validation, and the identification of outliers.

* Error Handling: Any errors encountered during data processing are carefully handled to prevent data corruption. This includes logging errors, implementing fallback mechanisms, and manual review of problematic data points.

* Quality Assurance: Regular quality assurance checks are performed on the dataset to identify and address any quality issues. This includes periodic reviews of the data processing scripts, testing of the data against known benchmarks, and feedback from users.

Documentation: Comprehensive documentation is provided to describe the data collection, processing, and quality control procedures. This documentation helps users understand the strengths and limitations of the dataset and guides them in its appropriate use.

### PRE-PROCESSING, CLEANING, AND LABELING

The data is parsed from PDFs, assuming a static structure. Records that fail to extract or lack required values are dropped.

Weather and location data are obtained using the Open Meteo API and Google's Geocoding API, respectively. If these APIs fail to provide data, the corresponding fields are filled with 'unknown'.

The preprocessing code can be obtained from Dr. Grant at the University of Florida.

* Parsing: The data is extracted from PDF reports using automated scripts. The parsing process is designed to accurately capture the relevant information from the reports while handling variations in report formats.

* Cleaning: The extracted data is cleaned to remove any errors, inconsistencies, or irrelevant information. This includes correcting typos, standardizing formats, and dealing with missing or incomplete data.

* Augmentation: The data is augmented with additional information, such as weather conditions and geolocation data, to enhance its analytical value. This involves integrating data from external APIs and ensuring the accuracy of the added information.

* Labeling: The data is labeled with descriptive field names and categories to facilitate its interpretation and analysis. This includes assigning clear labels to each field and categorizing incidents based on their nature and characteristics.

### PRIVACY

The dataset does not contain any personally identifiable information (PII). It does not include details related to race, ethnicity, or criminal history.

### ADDITIONAL DETAILS ON DISTRIBUTION & ACCESS

* The dataset is dynamic, with updates possible when new incident reports are released by the Norman Police Department. The preprocessing script can be run again to obtain additional data.

* The dataset is distributed under the Apache License 2.0, which allows for flexibility in use while ensuring proper attribution and sharing of modifications. This licensing model promotes open access to the data while protecting the rights of the dataset owner and contributors.

* Access to the dataset is facilitated through direct contact with the dataset owner or designated representatives at the University of Florida. Prospective users are encouraged to reach out with a clear statement of their intended use of the data to ensure alignment with the dataset's intended purposes and licensing terms.

* The dataset is hosted on secure servers to prevent unauthorized access and ensure the integrity of the data. Users granted access to the dataset will receive instructions on how to securely download the data, along with any necessary documentation or support materials to facilitate its use
