Semester Project - Hope Foundation
Quick Intro
Welcome to the semester project for Econ 8320 - Tools for Data Analysis! This project is designed to give you a chance to combine all of the material that we cover during the term, and to show that you can use these tools to collect and clean data, as well as to conduct some rudimentary analysis (other courses will focus much more on the analysis part).

The data for this project is available here Download here
, and a data dictionary explaining the variables available to you is available here Download here
.

You will create a StreamlitLinks to an external site. dashboard that is updated each time a spreadsheet in your repository is updated by the end user. The dashboard will be designed to help the Nebraska Cancer Specialists Hope FoundationLinks to an external site., an organization in Nebraska that offers help to families dealing with cancer and cancer treatments (and the associated challenges and expenses). In this project, you will

Create a GitHub repository to contain your code and data
Clean and organize data provided by the Hope Foundation. You can find this data (as well as a data dictionary) in the starter repository. Your dashboard should solve the following goals:
Create a page showing all of the applications that are "ready for review", and can be filtered by whether or not the application has been signed by the necessary committee members.
Create a page answering "how much support do we give, based on location, gender, income size, insurance type, age, etc". In other words, break out how much support is offered by the listed demographics.
Create a page showing how long it takes between when we receive a patient request and actually send support.
Create a page showing how many patients did not use their full grant amount in a given application year. What are the average amounts given by assistance type? This would help us in terms of budgeting and determining future programming needs.
Finally, create a page that showcases a high-level summary of impact and progress over the past year that can be shown to stakeholders in the foundation.
Your dashboard should update EACH TIME THAT DATA IS CHANGED, so that you can add each new month of data to your dashboard as it becomes available
Once you have processed the data, you will build an interactive dashboard using Streamlit addressing the above requirements, and launch a website from your GitHub using the free deployment process described on the Streamlit website (with the Community Cloud tool). Details can be found hereLinks to an external site..
Your tool should run a script once per month when new data is released through GitHub ActionsLinks to an external site. that will ensure that your dashboard always stays up to date.
NOTE: You are expected to learn several new skills during this project (how to create a github action, how to create a Streamlit dashboard, etc.). As a data scientist, you will frequently be expected to use new tools to solve new problems. Leverage what you know from class, and create a real product that you can showcase on your website and during interviews!

Steps to Completion
Clean and prepare the data for the dashboard.
Create a GitHub Action trigger to process new data each month as it is reported
This should update your dashboard as data is pushed!
Submit the following for your completed project:
A link to your GitHub repository
A link to your working dashboard
Any presentation materials that you use
A 2-5 page writeup (single spaced) describing what you learned in the project, and what you would do differently if you did a similar project in the future. (Page limit not including tables or figures)
NOTE: You do NOT need to submit the complete original data sets, since I already have access to them in your GitHub repository
