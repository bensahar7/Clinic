import matplotlib.pyplot as plt
from pandas import np
from sympy.stats.drv_types import scipy

def extract_and_open_files(filename):
    f = open(filename, 'r', encoding='UTF-8')
    x = f.readlines()
    l = f.readline()
    return x,l

def writing_data_on_out_flile(t,lst,dic):
    for word in lst:
        t.write("Treatment-" +word+" Total of:" + ' ' + str(dic[word]) + '\n')
    return

def creat_relavent_dic(x,month):
    dtreat = {}
    date = []
    dprice = {}
    dclinic = {}
    dannual = {}

    for line in x:
        fields = line.strip().split(',')
        month_field = fields[0]
        treat = fields[1]
        loc = fields[2]
        mm = month_field.split()
        date = mm[0]
        if month in date:
            dtreat[treat] = dtreat.get(treat, 0) + 1

    for line in x:
        fields = line.strip().split(',')
        month_field = fields[0]
        mm = month_field.split()
        price = fields[2]
        clinic = fields[3]
        date = mm[0]
        if month in date:
            dclinic[clinic] = dclinic.get(clinic, 0) + 1
            dprice[clinic] = price

    return dtreat, dprice, dclinic, dannual

def sorted_dic(dic):
    dic_keys = dic.keys()
    sorted_dic = sorted(dic_keys, key=dic.get, reverse=True)
    return dic_keys, sorted_dic

def sorted_dic_for_graph(x,yearr):
    dannual = {}
    dprice = {}

    check = False
    for line in x:
        fields = line.strip().split(',')
        year_field = fields[0]
        mm = year_field.split()
        date = mm[0]
        price = fields[2]
        clinic = fields[3]
        if yearr in date:
            dannual[clinic] = dannual.get(clinic, 0) + 1
            dprice[clinic] = price
            check = True
    return check, dannual, dprice

def creating_the_graph(list_of_clinics, annual_income, check):
    if check != False:

        plt.xlabel('Clinic')
        plt.ylabel('Revenue')
        plt.title('Annual Revenue')

        plt.bar(list_of_clinics, annual_income)
        plt.show()

        plt.pie(annual_income, label=list_of_clinics)
        plt.show()
    else:
        print('There is no data for this year')

def what_is_the_best_treat(filename):

    x = None
    try:
        t = open('outfile.csv', 'w', encoding='UTF-8')

        month = input('What month and year do you want to check?\nMonth between (1-12) for example (1/2020): ')

        #Function that extract data from csv file
        extract_filee = extract_and_open_files(filename)

        x = extract_filee[0]
        l = extract_filee[1]

        #Function that creats a dic for a treatment and the number of apperance.

        relavent_dic = creat_relavent_dic(x, month)
        dtreat = relavent_dic[0]
        dprice = relavent_dic[1]
        dclinic = relavent_dic[2]

        # sorting dictionary by the highest value.
        sortedd_dic1 = sorted_dic(dtreat)
        sorted_treat = sortedd_dic1[1]
        sortedd_keys = sortedd_dic1[0]
        sortedd_dic2 = sorted_dic(dclinic)
        dclinic_keys = sortedd_dic2[0]
        sorted_clinic = sortedd_dic2[1]


        lst = ['Name of Treat ','Number of Treat\n']
        for i in lst:
            t.write(i)


        # Print the most popular treatment

        for dtreat_keys in sorted_treat:
            print("Treatment: "+ dtreat_keys, dtreat[dtreat_keys])


        #writing the dic in the file

        writing_data_on_out_flile(t, sorted_treat, dtreat)


        # print the most profitable clinic in $

        for dclinic_keys in sorted_clinic[:1]:
            print('The Most profitable clinic is:',dclinic_keys.capitalize(), ',with revenue of:','$', int(dclinic[dclinic_keys])*int(dprice[dclinic_keys]))

    except IOError:
        print('IOError encountered')

    finally:
        if x != None:
            return 0
            f.close()
            t.close()

def visual_best_treat(filename):
    x = None
    try:

        # Extract data from file.

        extract_filee = extract_and_open_files(filename)
        x = extract_filee[0]

        # Desired year the user want to check

        yearr = str(input('What year do you want to check?'))

        # Creating relavent dic

        relavent_dic = sorted_dic_for_graph(x,yearr)
        dannual = relavent_dic[1]
        dprice = relavent_dic[2]
        check = relavent_dic[0]

        # Sorting dic
        sortedd_dic = sorted_dic(dannual)
        sorted_annual= sortedd_dic[1]
        dannual_keys = sortedd_dic[0]

        # Creating a list that contains the annual income of all clinics.
        lst=[]

        for dannual_keys in sorted_annual:
            if dprice[dannual_keys] == 'תשלום לפגישה':
                break
            else:
                lst.append(int(dannual[dannual_keys]) * int(dprice[dannual_keys]))
        xx = list(sorted_annual)

        # Function for a graph.
        creating_the_graph(xx,lst,check)

    finally:
        if x != None:
            return 0
            f.close()

import numpy as np
import scipy.stats
import matplotlib.pyplot as plt

def variables_Connection(file_name):
    year_lst = []
    academic = []
    academic_encoding = [1, 2, 3, 4, 5]

    try:
        is_first_line = True
        with open(file_name, 'r', encoding='UTF-8') as file:
            for line in file:

                if is_first_line:
                    is_first_line = False
                    continue

                fields = line.strip().split(',')
                if fields[4] == "" or fields[6] == "":
                    continue

                #In this lines we re-encode the values of the academic field into numeric values.


                year_lst.append(int(fields[4]))
                if fields[6] == "במידה רבה מאוד":
                    academic.append(academic_encoding[4])
                elif fields[6] == "במידה רבה":
                    academic.append(academic_encoding[3])
                elif fields[6] == "במידה בינונית":
                    academic.append(academic_encoding[2])
                elif fields[6] == "במידה מועטה":
                    academic.append(academic_encoding[1])
                elif fields[6] == "לא רלוונטי":
                    academic.append(academic_encoding[0])
                elif fields[6] == "כלל לא":
                    academic.append(academic_encoding[0])

    except FileNotFoundError as e:
        print("The file entered does not exist!")
    except TypeError as e:
        print("Type error, probably failed converting year to int")

    finally:
        if academic is [] or year_lst is []:
            print("file does not contain expected data")
            return

        #In this lines we calculate the Person index to know if there is a correlation between the variables.


        pearson = scipy.stats.pearsonr(academic, year_lst)
        pearson_coefficient = pearson[0]
        p_value = pearson[1]
        if p_value > 0.05:
            print("There is no correlation between academic success and academic year")
        else:
            print("There is correlation between academic success and academic year")


        #In these lines we present a dot graph that visually illustrates the correlation between the two variables.


        x = np.array(year_lst)
        y = np.array(academic)
        plt.scatter(x, y)
        plt.show()

def main(filename,file_name):

    y = what_is_the_best_treat(filename)
    z = visual_best_treat(filename)
    x = variables_Connection(file_name)


    return x, y, z










