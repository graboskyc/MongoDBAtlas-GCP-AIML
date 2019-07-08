# Basic CRUD Operations

 ## Background
The purpose of this page is if you are following along on your own or want to copy/paste the answers:

## Prereqs
* Deploy the cluster and follow the guide for [AtlasSetup.md](AtlasSetup.md)
* Once complete, click the `...` button, then "Load Sample Dataset" and confirm the load. This may take several minutes. 

![](images/ss14.png)

* We will use the `sample_mflix.movies` collection. Press the "Collections" button on the cluster, then that database, then that collection to get to the Document Explorer
* We will paste the command below into the box. If using the shell, we should surround the query with `db.movies.find()`

## Find Queries

| Question                              | Answer |
|---------------------------------------|--------|
|From 1987                              | `{year:1987}` |
|“Comedy” as one of their genres        | `{genres: "Comedy"}` |
|“Comedy as only genre                  | `{genres:["Comedy"]}` |
|“Comedy” or “Drama”                    | `{genres:{$in:["Comedy", "Drama"]}}` |
|“Comedy” and “Drama”                   | `{ genres: { $all: ["Comedy", "Drama"] } }` |
|IMDB Rating>8.0 and PG Rating          | `{"imdb.rating" : {$gt: 8.0}, rated:"PG"}` |
|Title starting with “Dr. Strangelove”  | `{title: {$regex: '^Dr. Strangelove'}}`|

## Indexes

For the index section, we will want to identify an optimal indexes (following the ESR rule) for queries like:

```
db.movies.find(
    {
    "actors":"Bill Murray", 
    "year":{$gte: 2000}
    }
    ).sort(
        {"title":1}
    )
```

## Aggregations 1
Here we will want to find all comedies, create an individual document for each country, then group by country to get a count.

| Stage                                 | Answer |
|---------------------------------------|--------|
| How can you use $match to find all comedies? | `$match {genres: "Comedy"}`| 
| How can you use $unwind to create an individual document for each country? | `$unwind {path: "$countries"}` | 
| How can you use $group to count all the comedies grouped by country? | `$group { _id: "$countries", count: {$sum:1}}`| 

## Aggregations 2
Here we want to restrict output with a calculated field for each movie:

| Stage                                 | Answer |
|---------------------------------------|--------|
| Retrieve just the title and how many years old | `$project { _id:0, title:1,    yearsOld: { $subtract:    [2019,"$year"]}}`
| 