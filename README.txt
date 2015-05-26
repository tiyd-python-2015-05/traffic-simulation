Clinton,

Though I was out of town this weekend, that's not a good excuse for not having much for this assignment.
Below, I have an outline of the tasks, and a strategy on how to approach them. Before leaving on Thursday,
I was working with Tripp and Josh a little bit. I took a look at Tripp's turned in assignment, and I
understood most of it(had trouble following a few logic points(comprehensions) and some of the graphing
features in the notebook). I know that reading and writing code are very different things, but at this
point, I got a lot out of it. As always, let me know if you'd like to chat.

Also, today I had a fleeting thought of not continuing with Iron Yard. I know that either Friday or
Monday(today) is the last day to drop if I want to get any kind of a refund. I will very likely
NOT do this. It was partly coming out of a place of frustration from this weekend (not doing well/
much work on the assignment; I won't be out of town again though). Also, just thinking about cost, etc.
So far, I've learned I've learned a LOT, and have enjoyed the program/people/work, and I think I will
continue to. If you think it would be in
either of our best interests for me to drop at this point, definitely let me know tomorrow (maybe
before class starts). I've gotten the sense that you think I can do this. I think I can too, but, I
have admittedly struggled more than I would have liked to/thought I would so far. Those are my thoughts!
Let me know if you have any. I have a 1-1 w/dana tomorrow anyways, so I'll probably talk to her about
it as well.

Thanks!
Will


Initial plans/layout:

For each car: get speed/location, and get speed/location of car in front of it.
If distance of car in front of it > car's current speed and if current car speed < 120 km/hr:
    speed up 2 m/s
If distance of car in front of it < car's current speed, slow car down to equal distance to next car

For each car every second get a random number between 0 and 1. If number is <= .10, slow car down 2 m/s
in addition to above steps

Create 1000 positions for every meter on track. Use linspace to do this, evenly spaced, and numbered.
Pass in value to initialize each car.

Measure car length from same place every time (front of car) (account for this when checking distance
to next car

Give cars numbers to track where they are in line to help prevent passing

