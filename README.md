Key:    
    
    aop = Area of operation. For each vehicle, found the furthest Northern, Easter, Southern, and Western lat/lng coordinates. Stored monthly and total furthest points.
    
    frpv = fuel ratio per vehicle. For each vehicle, calculated the fuel/hour ratio. A high ratio should indicate that a vehicle is working hard and will require more frequent maintenance. Stored averages daily, monthly, total, per 150 hours, and per 300 hours. 150 hours was chosen because this is when oil fitlers are typically replaced. 300 hours was chosen because this is when fuel filters are typically replaced
    
    dpv = distance per vehicle. For each vehicle, calculated the difference in distance between days. Stored accumulated totals daily, monthly, and total.
    
    over_under_use = The vehicles that failed the t-test. As of right now, the columns in over_under_use.csv do not signify anything beyond simply identifying the vehicle IDs that failed the t-test.

Using a t-test, we tested the hypothesis that a vehicle's monthly fuel/hours ratio is the same as the total average fuel/hours ratio of vehicles of the same type ( i.e. motor grader, excavator, etc.) We found some vehicles with a p-value < 0.05 which indicates a significant difference between the set of a vehicles fuel/hour ratio and the total average population of that vehicles type. We believe fuel/hours ratio to be a good indicator of how hard a vehicle is working, thus the vehicles that failed the null hypothesis indicates they are either under or over utilized and might require maintenance. Also, failing the hypothesis could mean a bad fuel-air mixture in the engine, which would still indicate requiring maintenance. Differentiating between over/under utilized vehicles should be as simple as comparing their average fuel/hour ratio to the population's fuel/hour ratio.

Some of these vehicles could have failed the t-test because certain months did not have enough data collected, so in the future we will try to scrub the data more accurately. Also, in the future I would like to run a BIRCH clustering algorithm on the data which I believe would show which months had the highest fuel/hour ratios. Lastly, it would also be nice to run even more t-tests and test more hypotheses with the data generated.

The data used for the t-test:

frpv_month https://drive.google.com/file/d/1tvhfCbjVeoC0eS2z-fuSHvir2R2iouBV/view?usp=sharing

frpv_total https://drive.google.com/file/d/13z1qDPRjjXF4kEjloP10fC-c8V_qpPsd/view?usp=sharing
