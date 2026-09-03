# Findings

Analysis period: January–March 2025.

## 1. Station demand by rider type

Member trips account for the majority of trips with a recorded starting station. The highest-demand station/rider-type combination is Kingsbury St & Kinzie St for members, with 5,330 trips across the three-month period.

Station demand is concentrated among a relatively small set of high-volume starting stations. The results also show that station names are not always stable for the same historical station ID; for example, station `13017` appears as both `Franklin St & Chicago Ave` and `Franklin St & Chicago Ave*`. The analysis therefore preserves the historical station name rather than forcing it to match the current GBFS station snapshot.

## 2. Usage patterns by hour, day, and rider type

Members generate substantially more trips than casual riders across most hours and days. Member activity also shows a stronger concentration during daytime commuting hours, while casual usage is relatively more prominent during leisure-oriented periods.

Average ride duration is generally higher for casual riders than members. This suggests that casual usage is associated with longer rides even though members generate considerably more trips overall.

## 3. Bike type and rider type

Electric bikes account for the majority of trips for both rider types:

- Casual: 92,292 electric-bike trips vs. 45,484 classic-bike trips.
- Member: 283,045 electric-bike trips vs. 167,903 classic-bike trips.

Casual riders also have longer rides on average for both bike types. Classic-bike casual rides average about 2,023 seconds compared with about 742 seconds for members. For electric bikes, casual rides average about 658 seconds compared with about 574 seconds for members.

The median durations show the same directional pattern, although the gap is smaller than the average, indicating that longer rides and outliers contribute to the difference in average duration.

## Data-quality observations

- 588,724 trips were ingested across the three selected months.
- 104,117 trips do not have a recorded starting station ID.
- Historical trip station IDs do not directly overlap with the current GBFS station IDs, so the trip fact is not forced into an invalid station foreign-key relationship.
- Historical station names are preserved because the same station ID can appear with multiple names.
- The current GBFS station data is treated as a current station reference rather than as a historical snapshot for the trip period.
- Trip-duration and timestamp-ordering tests found no negative or invalidly ordered durations in the selected data.
