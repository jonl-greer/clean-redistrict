## Data format:
{
“state”: “”,\\
“has_statewide_shp”: bool,
“has_boundaries_results”: bool,
“data_sources”: [],
“data_format”: [],
“years_covered”:[],
“likely_joinable”: bool
}

## Data Gathering Checklist: 
1. Go to redistrictingdatahub.org
2. Go to “Download data”
3. Select a state
4. Filter for “Boundaries and Election Results” then for “Boundaries” and repeat steps
5. Ignore files with…
    a. Census
    b. Block / Track
    c. Congressional districts
    d. Legislative districts
    e. Disaggregated to block
6. For “state”
    a. Record state name exactly as shown on RDH 
7. For “has_statewide_shapefile”
    a. T if one precinct shapefile that covers entire state exists
    b. F if only county-by-county shapefiles or none at all
8. For “has_boundaries_results”
    a. T if includes BOTH precinct boundaries and election results
    b. F otherwise
9. For “data sources”
    a. List sources (RDH, MGGG, VEST, State, PGP, other)
10. For  “data_format”
    a. List formats (shapefile, geojson, csv, pdf, other)
11. For “years_covered”
    a. List all years across all applicable files, sort ascending order, no duplicates
12. For “likely_joinable”
    a. Answer following questions Y/N
        i. Are there multiple years in “Boundaries and Election Results”?
        ii. Do files use same naming style and source?
        iii. Are precinct counts roughly similar across years? (will have to download files and manually check)
        iv. Are files tied to common geography? (Projected to 2020 VTDs)
        v. Is there a single dominant data source? 
    b. If 3-5 Yes, put T, otherwise put F
