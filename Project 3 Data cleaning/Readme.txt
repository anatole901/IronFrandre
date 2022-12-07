Project 3 Data cleaning

I Dealing with missing data

My datast has 9994 lines.

There are 14 lines with missing client name. I check if there are other rows with same client ID. In that case, I fill the name with the one I found.

There are lines with missing segment. When investigating this column in relation with client name, I saw that any client appears to have made transaction in only one segment. Thus I've also filled missing values in segment field thanks to the other rows with the same client.

There are lines with missing city. When investigating this column in relation with state, I saw that there is only one city corresponding to each state. I've filled missing cities thanks to other transaction in the same state.  

The most complex case I had to deal with is the missing values in the sales column. This column stores critical data from my dataset and at first I've thought that I might just delete these rows because a critical data is missing. But the profit column shows that these rows store transactions with a large amount of money and thus they are important data. I've decided to infer the missing values from the profit column by computing the average ratio sale's amount to profit, let's name it R, and filling the missing sales amount with R multiplied by thee absolute value of the profit.

II Dealing with inconsistencies

I've dealt with few inconsistencies. I've corrected a row with quantity = 10004 whereas other values in this field range from 1 to 14. I've replaced this value with 14. The column discount also had two values 1.5 and 1.2 whereas other values range from 0 to 0.8 and should intuitively sit between 0 and 1. I've replaced these values with 0.5 and 0.2 respectively.