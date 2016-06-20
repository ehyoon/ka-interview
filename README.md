Khan Academy Infection Problem
==============================
This is a project assignment as part of the interview process for Khan Academy.


Requirements
============
Please make sure to have installed Python 2.7.


Test Instructions
=================
Navigate to the tests/ directory in this project, and run:
`python -m unittest discover`


Models
======
Users are represented by the User class in src/user.py.
This user model does not make the distinction between 'coached by' and 'coaching' relations.
This is because infection is transmitted between any of the two relationships, and so each user would just keep track of a list of users it is connected to.

Graph class is just a simple container class of these users, number of users, and has some common graph functions such as adding users and connecting users together.


Infection Algorithm - Part I: Total Infection
=============================================
The implementation for total infection is a breadth first search based algorithm.
Since we want to infect every users in the same connected component as the given user, it was just simple graph traversing problem.
This implementation is in 'infect_total' method under src/infection.py.


Infection Algorithm - Part II: Limited Infection
================================================
While maintaining infection by groups, that is all connected users, certain groups of users will be infected if the sum of their user count is closest to the desired infection count.
This problem became a variant of a subset-sum problem, where we would prioritize infection of subsets whose |sum(subsets) - target| is minimal.

Please see 'infect_limited' and its helper 'find_closest_subset_sum_of_graphs' in src/infection.py for the implementation of this algorithm.


Improvements To Be Made
=======================
- The subset variant algorithm I use to determine which components to infect needs to be converted to dynamic programming form for better performance.

- Instead of holding the notion of infect all or nothing in a connected component,
I could have made more precise infection algorithm that would infect as many "classes" between a teacher and the students.
So it would be choosing which classes to infect that would yield the closest infection count to the target.
This is an approach to consider since the objective of the problem was to roll out the new site version to users while minimizing the confusion that arises when users in the same class have different versions of the site.
There may be instances where the a teacher in some other class may be infected because that teacher may have been a student in a class that was infected.

- Instead of basing sheerly on the number of userbase, I could have also factored in other criteria, such as activity level of a class.
Again, this is because the objective is to get some feedback from users on how the new site is working, and infecting users in classes which have high level of activity would help us determine how well the new site is doing.




