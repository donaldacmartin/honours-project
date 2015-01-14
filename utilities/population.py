#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

def get_global_population_database():
    iso3to2 = _load_iso_mappings()
    pop_database = _read_in_data(iso3to2)
    return pop_database

def _load_iso_mappings():
    csv_file = open("utilities/data/fips2iso.txt")
    record   = csv_file.readline()
    iso3to2  = {}

    while record != "":
        if not record.startswith("#"):
            iso3to2 = _parse_iso_mapping(record, iso3to2)

        record = csv_file.readline()

    csv_file.close()
    return iso3to2

def _parse_iso_mapping(record, iso3to2):
    iso2 = record.split(",")[1]
    iso3 = record.split(",")[2]

    iso3to2[iso3] = iso2
    return iso3to2

def _read_in_data(iso_lookup):
    csv_file = open("utilities/data/population.csv")
    record   = csv_file.readline()
    lookup   = {}

    while record != "":
        country_code, yearly_pop = _parse_record(record, iso_lookup)
        lookup[country_code] = yearly_pop
        record = csv_file.readline()

    csv_file.close()
    return lookup

def _parse_record(record, iso_lookup):
    record = record.split(",")

    country_code = iso_lookup[record[1].replace("\"", "")]
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
