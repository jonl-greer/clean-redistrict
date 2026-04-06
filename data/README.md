## Data format:
{<br>
“state”: “”, <br>
“has_statewide_shp”: bool,<br>
“has_boundaries_results”: bool,<br>
“data_sources”: [],<br>
“data_format”: [],<br>
“years_covered”:[],<br>
“likely_joinable”: bool<br>
}

## Data Gathering Checklist: 
1. Go to redistrictingdatahub.org 
2. Go to “Download data” 
3. Select a state
4. Filter for “Boundaries and Election Results” then for “Boundaries” and repeat steps
5. Ignore files with… <br>
    a. Census <br>
    b. Block / Track <br>
    c. Congressional districts <br>
    d. Legislative districts <br>
    e. Disaggregated to block <br>
6. For “state” <br>
    a. Record state name exactly as shown on RDH <br>
7. For “has_statewide_shapefile” <br>
    a. T if one precinct shapefile that covers entire state exists <br>
    b. F if only county-by-county shapefiles or none at all <br>
8. For “has_boundaries_results” <br>
    a. T if includes BOTH precinct boundaries and election results <br>
    b. F otherwise <br>
9. For “data sources” <br>
    a. List sources (RDH, MGGG, VEST, State, PGP, other) <br>
10. For  “data_format” <br>
    a. List formats (shapefile, geojson, csv, pdf, other) <br>
11. For “years_covered” <br>
    a. List all years across all applicable files, sort ascending order, no duplicates <br>
12. For “likely_joinable” <br>
    a. Answer following questions Y/N <br>
        i. Are there multiple years in “Boundaries and Election Results”? <br>
        ii. Do files use same naming style and source? <br>
        iii. Are precinct counts roughly similar across years? (will have to download files and manually check) <br>
        iv. Are files tied to common geography? (Projected to 2020 VTDs) <br>
        v. Is there a single dominant data source? <br>
    b. If 4-5 Yes, put T, otherwise put F <br>
