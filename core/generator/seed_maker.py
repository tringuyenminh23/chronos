import pandas as pd
from config import mock_data_path
from math import ceil
import numpy as np
import datetime
from core.structure.PopulationPyramid import PopulationPyramid


def generate_people_basic_info(population, sex_ratio=1.01, pop_pyramid=None):
    """
    Generate a person's basic info: Name, Gender
    :param population: int
    :param sex_ratio: number of male for each female
    :param pop_pyramid: population pyramid for age distribution
    :return:
    """
    # TODO: a person does not follow common norm for naming based on gender (e.g: Jane -> Male)
    surname_data= pd.read_csv(mock_data_path() / 'surname.csv.gz', delimiter=',', compression='gzip')
    first_name_data = pd.read_csv(mock_data_path() / 'firstname.csv.gz', delimiter=',', compression='gzip')

    n_female = ceil(population / (sex_ratio + 1))
    n_male = population - n_female

    male_first_name_data = first_name_data[first_name_data['Gender'] == 'Male']
    female_first_name_data = first_name_data[first_name_data['Gender'] == 'Female']
    male_first_name = set(np.random.choice(male_first_name_data['Name'].as_matrix(),
                                           size=n_male,
                                           p=male_first_name_data['% Frequency'].as_matrix()))
    female_first_name = np.random.choice(female_first_name_data['Name'].as_matrix(),
                                         size=n_female,
                                         p=female_first_name_data['% Frequency'].as_matrix())

    population = [{'gender': 'male'}] * n_male + [{'gender': 'female'}] * n_female
    np.random.shuffle(population)


    female_population = [{'first_name': }for i in range(n_female)]


    surname_samples = surname_data.sample(population, axis=0)
    firstname_samples = firstname_data.sample(population, axis=0)

    is_typical_gender_distribution = np.random.binomial(1, 0.8, population)
    opposite_gender = {'male': 'female', 'female': 'male'}

    people = []

    for idx in range(population):
        info = {}
        info['first_name'] = firstname_samples.iloc[idx]['Name'].capitalize()
        info['last_name'] = surname_samples.iloc[idx]['Surname'].capitalize()
        typical_gender = firstname_samples.iloc[idx]['Gender'].lower()
        if is_typical_gender_distribution[idx]:
            info['gender'] = typical_gender
        else:
            info['gender'] = opposite_gender[typical_gender]
        info['email'] = email_generator(info['first_name'], info['last_name'])

        people.append(info)

    df = pd.DataFrame(people)
    df = df[['first_name', 'last_name', 'gender', 'email']]
    return df


def email_generator(first_name, last_name):
    first_name = first_name.lower()
    last_name = last_name.lower()
    domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'aol.com', 'msn.com', 'comcast.net', 'verizon.net', 'cox.net']

    option = np.random.randint(8)
    if option == 0:
        address = first_name[0] + last_name
    elif option == 1:
        address = first_name[0] + '.' + last_name
    elif option == 2:
        address = first_name[0] + '_' + last_name
    elif option == 3:
        address = first_name + last_name
    elif option == 4:
        address = first_name + '_' + last_name
    elif option == 5:
        address = first_name + '.' + last_name
    elif option == 6:
        address = first_name
    elif option == 7:
        address = last_name
    return address + '@' + np.random.choice(domains)








