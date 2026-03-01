# Data Management
## Loader for external data
- need end of season rankings data (pre bowl games if possible)
- need end of season s&p+ (end of season is preferred)

## Where to store data?
- right in the repository in parquet files, no need to make it hard

## How to access data?
- duckdb? probably light weight enough for pandas though
- there might be some shenanigans on how to join team names across sources, cross that bridge when we get there

# Analysis

## Postseason Scenario setup
- need a way to determine who would be in the BCS championship each season based off rankings - this is trivial
- need a way to determine who would be in a four team playoff each season based off rankings - this is trivial
- need a way to determine who would be in a 12 team playoff each season based off rankings - this is not trivial since there's some complex rules
- need an engine to simulate a playoff bracket based of s&p+ implied point spread win probabilities

