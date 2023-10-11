# Dedicated-hours-counter
A console application that counts dedicated hour entries in the specified folder

## What is a dedicated hour?
In 2020 I introduced a concept named "Dedicated hours" into my life.
I came up with Dedicated hours because I wanted to know the answer for this question: How much time did I spend to learn/complete/improve X? Where X can be any activity in my life, for example **learn Python language**. To learn basics of Python with zero knowledge it took me 25 dedicated hours.
But what exactly does mean 25 dedicated hours? It means that I set in front of my computer for 25 hours collectively - without **any** breaks like bathroom breaks, making a beverage or reading a mail. I use a timer that is set to 1 hour (it can be any amount of time) and if I need a break I pause it. Every time the timer expires I create an entry called `Learning Python` in a text file that is named today's date, thus creating a database that contains all my project/learning activity. If I would dedicate 30 minutes, I would make this entry instead: `30' Learning Python`.

## The purpose of this program
Dedicated hours counter was designed to walk through all the files filled with Dedicated hours entries and count the amount of time for the specified task.

## Miscellaneous
I use Notepad++ for creating Dedicated hour entries because I find it very efficient for adding new entries.
Every file contains also a separator `-------` below which I store recent activities so that I can easily move them above once I finished that activity.
If I dedicate more than one hour in a row, I simply duplicate the line with that activity.
If there is no amount of minutes specified, it means I dedicated 1 hour.
