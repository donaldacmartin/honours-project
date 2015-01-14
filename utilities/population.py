#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

def get_global_population_database():
    pop_database = _read_in_data()
    return pop_database

def _read_in_data():
    csv_file = open("utilities/data/population.csv")
    record   = csv_file.readline()
    lookup   = {}

    while record != "":
        try:
            country_code, yearly_pop = _parse_record(record)
            lookup[country_code] = yearly_pop
        except:
            pass

        record = csv_file.readline()

    csv_file.close()
    return lookup

def _parse_record(record):
    record = record.split(",")

    country_code = record[1].replace("\"", "")
    yearly_pop   = _parse_record_years(record)

    return country_code, yearly_pop

def _parse_record_years(record):
    yearly_pop = {}
    column_pos = 44

    for year in range(2001, 2015):
        pop = record[column_pos].replace("\"", "")
        yearly_pop[year] = int(pop) if pop != "" else None
        column_pos += 1

    return yearly_pop
