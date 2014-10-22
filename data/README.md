Intro
=====

The data required is gathered from multiple sources.


ICUT
----
The [Independent Colleges and Universities of Texas, Inc.][ICUT] is an
association of privates institutions in Texas. They don't have a repeatable way
of getting data, and the data does is just a series of Excel sheets without any
identifiers. Skimming through the data we did get from ICUT showed that it was
similar (or the same) as the information we could get from IPEDS.

  [ICUT]: http://www.icut.org/


IPEDS
-----

The good thing about IPEDS is that it has a ton of information. You just have
to know how to get it out.

For a good introduction to IPEDS and what kind of data you'll find in there,
you should read this document:

https://github.com/myersjustinc/journalists-guide-datasets/blob/ipeds/datasets/integrated_postsecondary_education_data_system.md

For an overview of the intricacies of pulling data required for this project,
you should read:

https://github.com/crccheck/journalists-guide-datasets/blob/ipeds/datasets/ipeds.md


THECB
-----

The Texas Higher Education Coordinating Board is the best resource for getting
information about public institutions. Unfortunately, the data is scattered and
reported in multiple formats across multiple systems:

### Almanac

### Accountability

This data goes back to 2000, but gets spotty before 2004.

> The data has not been added at this end.  When the accountability system was
> first implemented in 04, we did not add all of the prior years for all of the
> measures.

### PREP

This data goes back to 1993, but gets spotty before 2004

### Texas Higher Education Data

http://www.txhighereddata.org Has a bunch of data designed for humans (PDF).

### Categories

THECB categorizes institutions into several categories, and provides different
data for each category. This can make it difficult to do apples to apples
comparisons (like what we're trying to do in this app). The categories we're
concerned with are:

Accountability:

* Universities (Texas public)
* Community Colleges

PREP:

* 2-Year College District (I think)
* Public 2-Year College
* Public University

The rest are things like out-of-state MOOCs, grad schools, and technical
schools.

Caveats
-------

There are institutions in the database that report data by campus to THECB,
but report by system to IPEDS:

* Tarrant County College
* San Jacinto College
* Lone Star College

There are some schools that you'll have trouble with:

* Alamo Community College District - Northeast Lakeview College -- This one
  campus is not in IPEDS, but their four campuses are
* Lon Morris College - Private school that's having financial trouble
* Texas Southmost College - Was lumped in with UT Brownsville until 2011
* Texas A&M University System - Texas A&M University-Central Texas
* Texas A&M University System - Texas A&M University-San Antonio
* Texas State University System - Sul Ross State University
* University of North Texas at Dallas


Data
====

Enrollment
----------

### Full-Time Equivalent

When we talk about the size of a school, the Full-Time Equivalent (FTE) number
will be quoted. It's a linear combination of the number of full time students
and part time students. The problem is, it's a derived variable, and the
formula changes from source to source. You're not going to get an apples to
apples comparison unless you derive it yourself, and we're not at that point
yet because it requires a better understanding of the data.

Sources: IPEDS, THECB Accountability (only for 4-year)

### Total

This is just the summation of all the students, full-time and part-time. The
problem with quoting this number is that it overcounts part-time students,
which inflates 2-year and community colleges counts and dilutes their
statistics.

Sources: THECB Prep

### Full-Time/Part-Time

This is decided by how many credit hours a student is taking. There are a lot
of different standards for different majors for how many credit hours it takes
to be a full-time student.

### Enrollment by Demographics

IPEDS Ethnicities:
* two or more races
* American Indian or Alaska Native
* Asian or Pacific Islander
* Asian/Native Hawaiian/Pacific Islander
* Asian
* Black, non-Hispanic
* Black or African American
* Hispanic
* Hispanic/Latino
* Native Hawaiian or Other PAcific Islander
* Non-resident Alien
* Race/ethnicity unknown
* White, non-Hispanic
* White


PREP Genders: Female, Male
PREP Ethnicities:
* White
* African American
* Hispanic
* Asian
* American Indian/Alaskan Native
* International
* Unknown or Not Reported (starts 2010)
* Native Hawaiian/Pacific Island (starts 2012)
* Multiracial (starts 2010)

Sources: IPEDS, THECB Accountability (only for 2-year), THECB PREP


Institution Notes
-----------------

If you're ever wondering about why an institution seems weird, the first thing
to do is to check WikiPedia. After that, try the official school website.

### Howard College

Has a few campuses, but all data is aggregated to Howard College and/or Howard
County Junior College District.

THECB graduation rates: District

### Lone Star College - University Park

One of the campuses of Lone Star College, opened in 2010.

### San Jacinto College

Has a three campuses and six extension centers.
