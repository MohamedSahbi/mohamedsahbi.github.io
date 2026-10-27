---
title: "Data preparation (part 2)"
date: 2019-04-21T17:05:18+01:00
description: "In the previous post , we went through the pre-preparation phase,  collecting meta-data, data profiling and data preparation rules. This post is mainly about dealing with missing values aka Nulls. Before looking for methods to"
tags: ["data", "datapreparation", "DataSerie"]
archived: true
---

In the previous [post](/2019/03/16/data-preparation-part-1/), we went through the pre-preparation phase,  collecting meta-data, data profiling and data preparation rules. This post is mainly about dealing with missing values aka Nulls.

Before looking for methods to deal with nulls, confirm that you are really missing some data. It is possible to have some blanks in the data set that can be replaced with a value. Non quality data may have null in place of **no**. Let’s say a column that only has “yes” and “null” values. You should verify if the system/application that generates the data doesn't assign any value when it is negative/false response. In that case, you only replace **null** with **no** and don’t delete the column.

In addition, meta-data can help with missing data by mentioning the out-of-range entries with types: unknown, unrecorded, irrelevant, and that can be for different reasons such as

- Malfunctioning equipment
- Changes in database design
- Collation of different datasets
- Measurement not possible

## Missing data types

First, we need to understand the different types of missing data. There are 3 different types:

**Missing completely at Random (MCAR)**

The type title explains itself. The data are missing for random reasons (example: measurement sensor ran out of battery) and unrelated to any other measured variable. It just happened randomly.

Example:

We conducted a survey at University Campus about extracurricular activities, one of the questions is the student’s age. The survey was available online and we had some volunteers who asked students in the campus directly. After we collected the data, we started preparing it. We found out that some students did not mention their age because it was not mandatory. In this case, the age missing values are missing completely at random.

**Missing at Random (MAR)**

The missing data are independent on all the unobserved values, but it is dependent on the observed values. “What?!” Let’s make it simple:

We have a dataset of cars characteristics

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| **Brand** | **Model** | **Nbr of Doors** | **Nbr of Seats** | **Airbag** |
| Audi | A6 | 5 | 5 |  |
| Mercedes Benz | E63 | 5 | 5 | Yes |
| Audi | A4 | 5 | 5 |  |
| BMW | M3 | 3 | 2 | Yes |
| Renault | Megan | 5 | 5 | No |
| Skoda | Superb | 5 | 5 | Yes |
| Mercedes Benz | S560 | 5 | 5 | Yes |
| Peugeot | 508 | 5 | 5 | No |
| Skoda | Octavia RS | 5 | 5 | Yes |
| Tesla | Model S | 5 | 5 | Yes |
| Audi | A8 | 5 | 5 |  |
| Tesla | Model 3 | 5 | 5 | Yes |

We have missing values in the airbag column. You notice that the missing values are dependent on the column Brand. If we group the data by the brand value, we find out that all the missing values have as brand value “Audi”.

**Missing not at Random (MNAR)**

The missing data are not only dependent on the observed data, but also dependent on the unobserved data.

Example:

A survey was conducted about mental disorder treatment worldwide. The results showed that respondents from low/lower-income countries are significantly less likely to report treatment than high-income country respondents.

## Dealing with missing data

How to deal with the missing data? There are 3 different possibilities:

### 1 - Data Deletion

First, this method should be used only with MCAR case. There are 2 different deletion methods that most of data analysts/scientists are using:

**Drop them (Listwise deletion):**

Basically you have to remove the entire row if it has at least one missing value. This method is recommended if your data set is large enough so that the dropped data does not affect the analysis. Most of the labs or companies have a minimum percentage of data that is required and if that threshold is not attainable, they remove the rows with missing data. Personally, if most (more than 50%) values of a variable are null or missing, I "usually" drop the column.

**Pairwise deletion:**

Data will not be dropped in this case. If the analysis needs all the columns, you select only the rows without any missing values. Meanwhile, if the analysis task needs some variables (not all of them) and it happens that the rows with missing values have the required values for this task, you add them to the selected data for the task resolution.

Example:

For this example, the CAR data set will be used. *Let's assume it has 50 rows and there are missing data only in rows number 1 and 6

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  | **Brand** | **Model** | **Nbr of Doors** | **Nbr of Seats** | **Airbag** |
| 1 | Audi | A6 | 5 | 5 |  |
| 2 | Mercedes Benz | E63 | 5 | 5 | Yes |
| 3 | BMW | M3 | 3 | 2 | Yes |
| 4 | Skoda | Superb | 5 | 5 | Yes |
| 5 | Mercedes Benz | S560 | 5 | 5 | Yes |
| 6 | Peugeot | 508 | 5 | 5 | No |
| 7 | Skoda | Octavia RS | 5 | 5 | Yes |
| . . . |  |  |  |  |  |
| 50 | Tesla | Model 3 | 5 | 5 | Yes |

**1****st** **Task**: Association rules task to find association hypothesis between number of seats and number of doors. The needed attributes are: Brand, Model, Nbr of Seats and Nbr of doors. In this case, we can use all the data set because there are no missing values for the given models.

**2****nd** **Task**: Association rules task to find association hypothesis between number of seats and number of airbags. The needed attributes are: Brand, Model, Nbr of Seats and Nbr of airbags. To resolve the task, we eliminate rows number 1 and 6 and we use the rest.

### 2 - Replace missing values

The third option to deal with missing values is to replace them. Here it gets a bit complicated because there are different ways to achieve it.

**Mean/median substitution**

Replace missing values with the mean or median value. We use this method when the missing values are **numerical** type and the missing values represent less than 30%.

> However, with missing values that are not strictly random, especially in the presence of a great inequality in the number of missing values for the different variables, the mean substitution method may lead to inconsistent bias .
>
> Kang H. The prevention and handling of the missing data. *Korean J Anesthesiol*. 2013;64(5):402–406. doi:10.4097/kjae.2013.64.5.402

**Common value imputation**

We use the most common value to replace the missing values. For example, we have a column color in the Car dataset that we used previously which has 100 records. The color column has 5 values only, the most common value (67x) is Black. So, we replace the missing values with Black. **However, this method may lead also to inconsistent bias.**

**Regression imputation**

Regression imputation let us avoid biases in the analysis. We know that Mean/Median method replaces the missing values with current ones. Instead of doing that, we predict the missing values using the available data. This way, we gain new values and retain the cases with missing values.

**Multiple imputation**

> Multiple imputation "approach begin with a prediction of the missing data using the existing data from other variables [[15](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3668100/#B15)]. The missing values are then replaced with the predicted values, and a full data set called the imputed data set is created. This process iterates the repeatability and makes multiple imputed data sets (hence the term "multiple imputation"). Each multiple imputed data set produced is then analyzed using the standard statistical analysis procedures for complete data, and gives multiple analysis results. Subsequently, by combining these analysis results, a single overall analysis result is produced. "
>
>  Kang H. The prevention and handling of the missing data. *Korean J Anesthesiol*. 2013;64(5):402–406. doi:10.4097/kjae.2013.64.5.402

The purpose of multiple imputation is to have a statistically valid inference and not to find the true missing data, because there is no way to predict the missing data and get it 100% right. The main advantage of this method is the elimination of biases and it is easy to use. Meanwhile, to get a correct imputation model, you need to take in consideration the conditions needed for this method and avoid some pitfalls.

In case you want to use multiple imputation method, I recommend reading the following articles : [Multiple imputation for missing data in epidemiological and clinical research: potential and pitfalls](https://doi.org/10.1136/bmj.b2393) (BMJ 2009;338:b2393) and [When and how should multiple imputation be used for handling missing data in randomised clinical trials – a practical guide with flowcharts](https://doi.org/10.1186/s12874-017-0442-1) (DOI: 10.1186/s12874-017-0442-1)

### 3 - Create new field / variable

Missing data have its own usefulness mainly when it is not MCAR (Missing Completely At Random). Therefore, we create a new variable or field that records the witnessed behavior or pattern of the missing values. This can be also useful if you own the tool that generates the data, you can create a new engineered feature based on the missing data pattern.

## Further reading

1. [How to Handle Missing Data](https://towardsdatascience.com/how-to-handle-missing-data-8646b18db0d4)
2. [The prevention and handling of the missing data](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3668100/)

## References

1. ibm.com: *Pairwise vs. Listwise deletion: What are they and when should I use them?* , Accessed 27/02/2019 (<https://www-01.ibm.com/support/docview.wss?uid=swg21475199>)
2. ncbi.nlm.nih.gov: *The prevention and handling of the missing data*, Accessed 21/04/2019 ([https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3668100](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3668100/))
3. measuringu.com: *7 ways to handle missing data,* Accessed 15/04/2019 (<https://measuringu.com/handle-missing-data>)
