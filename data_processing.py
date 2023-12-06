import csv, os
import copy

class DB:
    def __init__(self):
        self.database = []

    def insert(self, table):
        self.database.append(table)

    def search(self, table_name):
        for table in self.database:
            if table.table_name == table_name:
                return table
        return None


class Table:
    def __init__(self, table_name, table):
        self.table_name = table_name
        self.table = table

    def join(self, other_table, common_key):
        # Join two tables based on a common key
        joined_table = Table(self.table_name + '_joins_' + other_table.table_name, [])
        for item1 in self.table:
            for item2 in other_table.table:
                if item1[common_key] == item2[common_key]:
                    dict1 = copy.deepcopy(item1)
                    dict2 = copy.deepcopy(item2)
                    dict1.update(dict2)
                    joined_table.table.append(dict1)
        return joined_table

    def filter(self, condition):
        # Filter the table based on a given condition
        filtered_table = Table(self.table_name + '_filtered', [])
        for item1 in self.table:
            if condition(item1):
                filtered_table.table.append(item1)
        return filtered_table

    def __is_float(self, element):
        # Helper method to check if an element can be converted to float
        if element is None:
            return False
        try:
            float(element)
            return True
        except ValueError:
            return False

    def aggregate(self, function, aggregation_key):
        # Aggregate values in the table based on a given function and key
        temps = []
        for item1 in self.table:
            if self.__is_float(item1[aggregation_key]):
                temps.append(float(item1[aggregation_key]))
            else:
                temps.append(item1[aggregation_key])
        return function(temps)

    def select(self, attributes_list):
        # Select specific attributes from the table
        temps = []
        for item1 in self.table:
            dict_temp = {}
            for key in item1:
                if key in attributes_list:
                    dict_temp[key] = item1[key]
            temps.append(dict_temp)
        return temps

    def pivot_table(self, keys_to_pivot_list, keys_to_aggregate_list, aggregate_func_list):
        # Create a pivot table based on given keys and aggregation functions
        unique_values_list = []
        for key_item in keys_to_pivot_list:
            temp = []
            for dict_item in self.table:
                if dict_item[key_item] not in temp:
                    temp.append(dict_item[key_item])
            unique_values_list.append(temp)

        # Generate combinations of unique value lists
        import combination_gen
        comb_list = combination_gen.gen_comb_list(unique_values_list)

        pivot_table = []
        # Filter each combination
        for item in comb_list:
            temp_filter_table = self
            for i in range(len(item)):
                temp_filter_table = temp_filter_table.filter(lambda x: x[keys_to_pivot_list[i]] == item[i])

            # Aggregate over the filtered table
            aggregate_val_list = []
            for i in range(len(keys_to_aggregate_list)):
                aggregate_val = temp_filter_table.aggregate(aggregate_func_list[i], keys_to_aggregate_list[i])
                aggregate_val_list.append(aggregate_val)
            pivot_table.append([item, aggregate_val_list])
        return pivot_table

    def insert_row(self, row_dict):
        # Insert a row into the table
        # This method inserts a dictionary, dict, into a Table object, effectively adding a row to the Table.
        self.table.append(row_dict)

    def update_row(self, primary_attribute, primary_attribute_value, update_attribute, update_value):
        # Update a specific row in the table
        '''
        This method updates the current value of update_attribute to update_value
        For example, my_table.update_row('Film', 'A Serious Man', 'Year', '2022')
        will change the 'Year' attribute for the 'Film'
        'A Serious Man' from 2009 to 2022
        '''
        for item in self.table:
            if item[primary_attribute] == primary_attribute_value:
                item[update_attribute] = update_value

    def __str__(self):
        return self.table_name + ':' + str(self.table)


# Get the current directory of the script
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Read data from CSV file and create a Table object
movies = []
with open(os.path.join(__location__, 'movies.csv')) as f:
    rows = csv.DictReader(f)
    for r in rows:
        movies.append(dict(r))

my_table = Table("movies", movies)

# Count the number of 'Fantasy' movies before any changes
num_fantasy_before = len(my_table.filter(lambda x: x['Genre'] == 'Fantasy').table)
print(f'Number of Fantasy movies before: {num_fantasy_before}')

# Insert a new row
new_movie_dict = {
    'Film': 'The Shape of Water',
    'Genre': 'Fantasy',
    'Lead Studio': 'Fox',
    'Audience score %': '72',
    'Profitability': '9.765',
    'Rotten Tomatoes %': '92',
    'Worldwide Gross': '195.3',
    'Year': '2017'
}
my_table.insert_row(new_movie_dict)

# Count the number of 'Fantasy' movies after insertion
num_fantasy_after_insert = len(my_table.filter(lambda x: x['Genre'] == 'Fantasy').table)
print(f'Number of Fantasy movies after insertion: {num_fantasy_after_insert}')

# Update the 'Year' for the movie 'A Serious Man' to '2022'
my_table.update_row('Film', 'A Serious Man', 'Year', '2022')

# Select only 'Name' and 'Year' attributes
selected_attributes = ['Film', 'Year']
selected_table = my_table.select(selected_attributes)

# Print the selected table
for row in selected_table:
    print(row)
