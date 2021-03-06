import requests
from bs4 import BeautifulSoup
import courts_data as venue_datas
from termcolor import colored
import os

# 
# SOME BUG TO FIX ==> Some venues not displayed or show more courts than it have
# 

# 
# SOME SUGGESTIONS TO IMPROVE CODES ==> Add threading
# 

os.system('color')

# DD-MM-YYYY
date = input('Enter Date: ')

for key, value in venue_datas.venues.items():
    venue_name = key
    location_id = value
    date = date

    url = "https://onepa.gov.sg/facilities/" + \
          str(location_id) + '?date=' + str(date)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    timings_list = []

    # Gets time slots for each venue (Both booked and not booked)
    for time_slots in soup.find_all('div', attrs={'class': "slots"}):
        if len(time_slots):  # Some courts won't return court data so need check first
            # Gets the text displayed, which in this case is the timing
            timings = time_slots.get_text()
            timings_list.append(timings)

        else:
            continue

    if len(timings_list) == 0:
        
        print(colored('\n#### ' + str(venue_name) + ' ####', 'green'))
        print('\n')
        print(colored('Register over the counter.', 'red'))
        print('\n\n')


    def find_tags():
        slots_list = []

        for tag in soup.find_all('span'):
            if tag.get('class') is None:
                continue

            else:
                # The tag.get('class') returns a list where if its a timing slot it will be ['slots', 'availability status']
                if tag.get('class')[0] == 'slots':
                    slots = tag.get('class')
                    # slots[1] returns the availability status
                    slots_list.append(slots[1])

                #   print(slots_list)  #Uncomment this to show some cool thing
                # Basically just a list which adds on to each other each row

                else:
                    continue

        return slots_list


    # Returns slots_list which contains a long list of each availability
    slots_list = find_tags()


    # def main(slots_list, timings_list):
    if len(timings_list) > 0 and len(slots_list) > 0:
        number_of_courts = len(slots_list) / len(timings_list)
        number_of_courts_int = int(number_of_courts)

        # Dynamically create the empty 'slots_court' list contained in a dictionary
        courts_dict = {
            'slots_court' + str(int(court + 1)): [] for court in range(number_of_courts_int)}

        # Margin of court index to increase from one court to another
        court_index_margin = int(len(slots_list) / number_of_courts_int)

        # Specify the starting court index in a dictionary to be able to find which availability corresponds to which court
        initial_court_index = {'court' + str(int(court + 1)): int(
            court_index_margin * court) for court in range(number_of_courts_int)}

        # Add availability in the 'courts_dict' dictionary into the respective courts
        # Basically sorting the courts availability into the individual courts
        for num_courts in range(number_of_courts_int):  # Loop for each court
            # Loop for each timings in each court
            for slots_index in range(court_index_margin):
                # Iterate through each court in the courts_dict dictionary and append the respective availabilities to each court with the correct index
                # of slots_list list specified with the initial_court_index which gives the margin to tell which starting point to take start as the first index.
                courts_dict['slots_court' + str(int(num_courts + 1))].append(
                    slots_list[slots_index + initial_court_index['court' + str(int(num_courts + 1))]])

        print(colored('\n#### ' + str(venue_name) + ' ####', 'green'))
        # print('\n####'+ str(venue_name) + '####')

        # Loop through each court
        for slots_num in range(number_of_courts_int):
            # Loop through each slots in the court
            for slots in range(len(timings_list)):
                if slots == 0:  # To only run this part of script in the first iteration
                    print(colored('\n~~~~', 'blue') + colored('Court ' + str(int(slots_num + 1)
                    ) + ' Available Timings', 'cyan') + colored('~~~~\n', 'blue'))

                    #  print('\n~~~~'+'Court '+str(int(slots_num+1))+' Available Timings'+'~~~~\n')

                if courts_dict['slots_court' + str(int(slots_num + 1))][slots] == 'normal' or courts_dict['slots_court' + str(int(slots_num + 1))][slots] == 'peak':

                    text_color = 'yellow' if (courts_dict['slots_court' + str(int(slots_num + 1))][slots] == 'peak') else 'green'

                    status = 'Peak Period' if (courts_dict['slots_court' + str(int(slots_num + 1))][slots] == 'peak') else ' :)'

                    print(colored(timings_list[slots] + status, text_color))
                    # print(timings_list[slots] + status)

                # 'normal' not in courts_dict['slots_court' + str(int(slots_num + 1))]
                elif courts_dict['slots_court' + str(int(slots_num + 1))][slots] == 'notAvailable' :
                    # print(colored('Fully Booked :(', 'yellow'))
                    print(colored('Not available! :(', 'white'))

                else:
                    print(colored('Fully booked! :(', 'red'))


        print('\n\n')
