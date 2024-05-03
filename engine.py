import nltk
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re

# Preprocess the data
stop_words = set(stopwords.words('english'))
ps = PorterStemmer()

# Load the first CSV file without setting an index
df1 = pd.read_csv('/Users/omgitsshahg/Desktop/FilteredMobilePhones.csv', thousands=',', converters={'Price': lambda x: float(re.sub(r'[^0-9]', '', x))})

# Load the second CSV file without setting an index
df2 = pd.read_csv('/Users/omgitsshahg/Desktop/ReviewsInformation.csv', thousands=',', converters={'Seller Rating': lambda x: float(x.strip('%')) if pd.notnull(x) and x != 'Not enough data' else None})

# Merge DataFrames based on the index (assuming 'id' is the index in both DataFrames)
combined_df = pd.merge(df1, df2, left_index=True, right_index=True)

combined_df = combined_df.drop(columns=['ID'])
combined_df = combined_df.rename(columns={'Unnamed: 0': 'ID'})


# Save the combined DataFrame to a new CSV file
df=combined_df
df.head(20)

# Preprocess the data
stop_words = set(stopwords.words('english'))
ps = PorterStemmer()


def preprocess_text(text):
    tokens = word_tokenize(text)
    filtered_tokens = []

    for token in tokens:
        if token.isalpha():
            lowercase_token = token.lower()
            filtered_tokens.append(lowercase_token)

    return ' '.join(filtered_tokens)



df['Processed_Name'] = df['Name'].apply(preprocess_text)
df['Processed_Company'] = df['Company'].apply(preprocess_text)


all_results = []

count=0

def search_phones(query, df=df):
    processed_query = preprocess_text(query)
    # Accumulate search results
    all_results = []

    def search_by_explicit_price():
        explicit_price_match = re.search(r'\$?(\d+(?:\.\d{2})?)', query)
        if explicit_price_match:
            explicit_price = float(explicit_price_match.group(1))
            results = df[df['Price'] == explicit_price]
            all_results.append(results[['ID', 'Name', 'Price', 'Company', 'Seller Rating', 'Reviews Score']])
            count = len(all_results)


    def search_by_price_condition(condition):
        numeric_match = re.search(r'\$?(\d+(?:\.\d{2})?)', query)
        if numeric_match:
            numeric_value = float(numeric_match.group(1))
            if condition == 'greater':
                results = df[df['Price'] > numeric_value]
            elif condition == 'lesser':
                results = df[df['Price'] < numeric_value]
            all_results.append(results[['ID', 'Name', 'Price', 'Company', 'Seller Rating', 'Reviews Score']])
            count = len(all_results)

    def search_by_rating_condition(condition, column='Seller Rating'):
        numeric_match = re.search(r'(\d+(?:\.\d{1,2})?)', query)
        if numeric_match:
            numeric_value = float(numeric_match.group(1))
            if condition == 'greater':
                results = df[df[column] > numeric_value]
            elif condition == 'lesser':
                results = df[df[column] < numeric_value]
            all_results.append(results[['ID', 'Name', 'Price', 'Company', 'Seller Rating', 'Reviews Score']])
            count = len(all_results)


    # def search_by_rating_and_price():

    #     price_match = re.search(r'\$?(\d+(?:\.\d{2})?)', query)
    #     rating_match = re.search(r'(\d+(?:\.\d{1,2})?)', query)

    #     if price_match and rating_match:
    #         price_value = float(price_match.group(1))
    #         rating_value = float(rating_match.group(1))

    #         # Check if price is less and rating is less
    #         if 'less' in query and price_value and rating_value:
    #             results = df[(df['Price'] < price_value) & (df['Seller Rating'] < rating_value)]
    #             all_results.append(results[['ID', 'Name', 'Price', 'Company', 'Seller Rating', 'Reviews Score']])

    #         # Check if price is less and rating is more
    #         elif 'less' in query and 'more' in query and price_value and rating_value:
    #             results = df[(df['Price'] < price_value) & (df['Seller Rating'] > rating_value)]
    #             all_results.append(results[['ID', 'Name', 'Price', 'Company', 'Seller Rating', 'Reviews Score']])

    #         # Check if price is more and rating is less
    #         elif 'greater' in query and 'less' in query and price_value and rating_value:
    #             results = df[(df['Price'] > price_value) & (df['Seller Rating'] < rating_value)]
    #             all_results.append(results[['ID', 'Name', 'Price', 'Company', 'Seller Rating', 'Reviews Score']])

    #         # Check if price is more and rating is more
    #         elif 'greater' in query and 'more' in query and price_value and rating_value:
    #             results = df[(df['Price'] > price_value) & (df['Seller Rating'] > rating_value)]
    #             all_results.append(results[['ID', 'Name', 'Price', 'Company', 'Seller Rating', 'Reviews Score']])


    def search_by_price_range():
        price_range_match = re.findall(r'\d+(?:[.,]\d*)?', query)

        minPrice=float(price_range_match[0])
        maxPrice=float(price_range_match[1])

        temp=0
        if (minPrice>maxPrice):
            temp=minPrice
            minPrice=maxPrice
            maxPrice=temp

        print(minPrice,maxPrice)

        results = df[(df['Price'] >= minPrice) & (df['Price'] <= maxPrice)]
        all_results.append(results[['ID', 'Name', 'Price', 'Company', 'Seller Rating', 'Reviews Score']])
        count = len(all_results)

    def search_by_rating_range():
        price_range_match = re.findall(r'\d+(?:[.,]\d*)?', query)

        minPrice=float(price_range_match[0])
        maxPrice=float(price_range_match[1])

        temp=0
        if (minPrice>maxPrice):
            temp=minPrice
            minPrice=maxPrice
            maxPrice=temp

        print(minPrice,maxPrice)

        results = df[(df['Price'] >= minPrice) & (df['Price'] <= maxPrice)]
        all_results.append(results[['ID', 'Name', 'Price', 'Company', 'Seller Rating', 'Reviews Score']])
        count = len(all_results)


    # def search_by_rating_and_price():
    #     #we know that there will be just 3 values high price, low price and rating
    #     numeric_values = re.findall(r'\d+(?:\.\d*)?', query)
    #     # Convert the extracted values to floats
    #     numeric_values = [float(value) for value in numeric_values]
    #     minPrice = numeric_values[0]
    #     maxPrice = numeric_values[1]
    #     rating = numeric_values[2]

    #     temp=0
    #     if (minPrice>maxPrice):
    #         temp=minPrice
    #         minPrice=maxPrice
    #         maxPrice=temp

    #     if 'above' in query.lower() or 'greater' in query.lower():
    #         results = df[(df['Price'] > minPrice) & (df['Price'] < maxPrice) & (df['Seller Rating'] > rating)].drop_duplicates(subset=['Name'])
    #         all_results.append(results[['ID', 'Name', 'Price', 'Company', 'Seller Rating', 'Reviews Score']])

    #         count = len(final_results)

    #         final_results = pd.concat(all_results, ignore_index=True).sort_values(by=['Seller Rating'], ascending=False)
    #         # Return both search results and count of all elements in list
    #         return final_results[['ID', 'Name', 'Price', 'Company', 'Seller Rating', 'Reviews Score']], count
            

        
    #     elif 'lower' in query.lower()or 'lesser' in query.lower():
    #         results = df[(df['Price'] > minPrice) & (df['Price'] < maxPrice) & (df['Seller Rating'] < rating)].drop_duplicates(subset=['Name'])
    #         final_results = pd.concat(all_results, ignore_index=True)
    #         count = len(final_results)

    # # Return both search results and count of all elements in list
    #         return final_results[['ID', 'Name', 'Price', 'Company', 'Seller Rating', 'Reviews Score']], count

    def search_by_PriceAndRating_range():
        range_match = re.findall(r'\d+(?:[.,]\d*)?', query)
        print(range_match)

        Price=float(range_match[0])
        rating=float(range_match[1])

        print(Price,rating)
        

        if 'lesser' in query and 'price' in query and 'lesser' in query and 'rating' in query:
            results = df[(df['Price'] <= Price) & (df['Seller Rating'] <= rating)]
        
        elif 'greater' in query and 'price' in query and 'lesser' in query and 'rating' in query:
            results = df[(df['Price'] >= Price) & (df['Seller Rating'] <= rating)]

        elif 'lesser' in query and 'price' in query and 'greater' in query and 'rating' in query:
            results = df[(df['Price'] <= Price) & (df['Seller Rating'] >= rating)]

        elif 'greater' in query and 'price' in query and 'greater' in query and 'rating' in query:
            results = df[(df['Price'] >= Price) & (df['Seller Rating'] >= rating)]

        
        all_results.append(results[['ID', 'Name', 'Price', 'Company', 'Seller Rating', 'Reviews Score']])
        count = len(all_results)


    # Explicit Price
    search_by_explicit_price()

    # Price Range
    # search_by_price_range()

    # if 'price' in query and 'between' in query and 'rating' in query:
    #     search_by_rating_and_price()
    print(query)



    if ('between' in query and 'price' in query):
        search_by_price_range()

    elif('price' in query and 'and'in query and 'rating' in query):
        search_by_PriceAndRating_range
    


    # Price conditions (greater, lesser)
    elif any(condition in query for condition in ['greater', 'more', 'more than', 'above']) and 'price' in query:
        search_by_price_condition('greater')

    elif any(condition in query for condition in ['lesser', 'less', 'under','below','lower']) and 'price' in query:
        search_by_price_condition('lesser')

    # Rating conditions (greater, lesser)
    elif any(condition in query for condition in ['greater', 'more', 'above']) and 'rating' in query:
        search_by_rating_condition('greater')

    elif any(condition in query for condition in ['lesser', 'less', 'under','below','lower']) and 'rating' in query:
        search_by_rating_condition('lesser')


    


    # Highest Rating
    if 'highest' in query and 'rating' in query:
        all_results = df[df['Seller Rating'] == df['Seller Rating'].max()].iloc[0]
        return all_results[['ID', 'Name', 'Price', 'Company', 'Seller Rating', 'Reviews Score']]

    # Lowest Rating
    if 'lowest' in query and 'rating' in query:
        all_results = df[df['Seller Rating'] == df['Seller Rating'].min()].iloc[0]
        return all_results[['ID', 'Name', 'Price', 'Company', 'Seller Rating', 'Reviews Score']]

    # Text search if no conditions are met
    results = df[df['Processed_Name'].str.contains(processed_query) | df['Processed_Company'].str.contains(processed_query)]
    all_results.append(results[['ID', 'Name', 'Price', 'Company', 'Seller Rating', 'Reviews Score']])

   

    # Concatenate all accumulated results
    final_results = pd.concat(all_results, ignore_index=True)
    count = len(final_results)

    # Return both search results and count of all elements in list
    return final_results[['ID', 'Name', 'Price', 'Company', 'Seller Rating', 'Reviews Score']], count



# implement price range and other extra information


# user_query = "phones greater than 600000 "

# user_query = "phones between 51000 and 60000 "

# search_results = search_phones(user_query.lower(), df)


# if not search_results.empty:
#     response = f"Based on your query, here are some options:\n{search_results}"
# else:
#     response = "Sorry, no matching phones found for your query."

# print(response)

search_phones(' price greater 100000 and rating greater than 92')



