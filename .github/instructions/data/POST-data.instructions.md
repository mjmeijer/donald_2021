---
applyTo: "data/POST-data-20*.txt"
---
For tabular data in .txt files, use jdatamunch-mcp tools to explore and analyze the data. Always start by calling describe_dataset to understand the schema and structure of the data. When retrieving data, use get_rows with appropriate filters instead of loading the entire file. For any group-by or summary questions, utilize the aggregate function for efficient analysis

The column headings in these files are, description after comma:
- testID, a unique identifier for the test session
- testtCounter, the attempt number test for this testID
- testPARAMS, the version of the interaction tested
- T0_IDLE, time before interaction starts
- T1_WARN, time before sequence is shown
- T2_SHOWTEST, total time for displaying the test sequence
- T3_DECAY, time before you can enter the memorized sequence
- T4_COUNTDOWN, time to enter the meorized sequence
- requested sequence
- recorded sequence
- status, correct | wrong | timeout
- elapsed time, in frames at 60 fps
- remaining levels, at which error or timeout occurred, the current level is the length of the requested sequence
- windowHeight x windowWidth, size of the window in pixels (see whether it's a phone) separated by 'x'
- dtstamp, date+time stamp in RFC 3339 format

In the file POST-data-2024 there are extra columns before dtstamp:
- age, of the test subject in years
- hours awake, number of hours the test subject has been awake
- substance use, whether the test subject has used any substances that could affect performance categories

In the file POST-data-2025 there is one extra column before dtstamp:
- colorblind, whether the test subject is colorblind

In the file POST-data-2026 there are two extra columns before dtstamp:
- instructions, whether the test subject received instructions before the test
- experience, whether the test subject has played Donald before

For collating the data into a single dataset, you can use the collate_post_data.py python script, which will handle the differences in columns across the files and produce a unified dataset for analysis. Make sure to specify the correct file paths when running the script.

