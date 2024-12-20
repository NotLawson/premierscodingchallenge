# Premier's Coding Challenge 2024 ([WINNER!!](https://education.qld.gov.au/about-us/events-awards/awards-competitions/premiers-coding-challenge/winning-entries#:~:text=Lawson%2C%20West%20Moreton%20Anglican%20College%20(Karrabin)))
[![Check, build and deploy [DEV]](https://github.com/NotLawson/premierscodingchallenge/actions/workflows/dev.yml/badge.svg)](https://github.com/NotLawson/premierscodingchallenge/actions/workflows/dev.yml)
[![Check, build and deploy [PROD]](https://github.com/NotLawson/premierscodingchallenge/actions/workflows/prod.yml/badge.svg)](https://github.com/NotLawson/premierscodingchallenge/actions/workflows/prod.yml)
![GitHub Tag](https://img.shields.io/github/v/tag/notlawson/premierscodingchallenge?label=Version)

> <b>The app is now LIVE at https://premiers.thatrandompi.xyz</b>

This repository contains the code for my 2024 Premiers Coding Challenge. It is a web app similar to Quizlet, with a flashcards feature and lessons feature. 

## Background

<b>[Notion page for project tracking](https://notlawson.notion.site/Digital-Tech-Project-29619290f81d4ec6b35c3d7f72906a30?pvs=4)</b>

This year for Term 2 and 3, we make a submission for the [Premier's Coding Challenge.](https://education.qld.gov.au/about-us/events-awards/awards-competitions/premiers-coding-challenge)
There are a range of topics to pick from for your submission:
- redesigning school facilities
- supporting visitors to your school
- making learning fun
- redesigning teaching tools
- cultural awareness and inclusion
- healthy habits
- school safety (classroom, playground, pool, outside the gate, emergency procedures)
- sustainable practices
- study tools
- student, staff and community well-being
- safe environment
- assistive technology
- augmenting teaching and learning
- understanding school history
- school information
- building school spirit and teamwork
- being happy and healthy
- pathways beyond school
- school celebrations
- connecting schools with their communities
- exploring future opportunities in quantum computing
- being safe online.

## Ideas

### Notes/Study tools

The main topic I was leaning towards was study tools. I made some notes [here.](https://notlawson.notion.site/Ideas-9561d868620042ae8f3221c8a5e14802?pvs=4)

It would be a website that took your notes in Markdown. Sort of similar to [Notion](https://notion.so), but just the note taking side. 

- You would organise notes into folders, not databases like Notion.
- More tailored to students (timetable, assesment calendar, grade tracking) *side note: ohh, grade tracking, nice!*
- Stricter colaboration guard rails to prevent cheating or stealing work *e.g. if you invite someone to work on a page, they can only access subpages and not the entire notebook*
- Teachers would be able to share and asign homework from notes
- The app could also get information from a Wikipedia page

With the notes, you could link a sort of kahoot-like quiz to them (hence study tools).

- Very similar to games like [Kahoot](https://kahoot.it), [Gimkit](https://gimkit.com) and [Quizlet](https://quizlet.live)
- Flashcards?
- More focused on student led or solo games instead of whole class *e.g. solo study, or revision with friends
- Which links into another idea, a Discord Bot, that I'll discuss more on later

Since it's tailored to students (kids 10-16ish idk), it should be kinda gamified.

- Earn points for completing quiz sets or revision
- Leaderboard against friends, class, etc
- Use points to get cosmetics for the app?

Another extra I thought of was a Discord Bot for student led study servers.

- It could have a running leaderboard
- Join VCs and use the camera feature to display timers, notes, even quizzes
- !!! Use the new activites feature for interactive things !!!

Problems:

- Being student led, students can create their own quiz sets. This could lead to some students creating extremely easy sets and cheating points -> in app cosmetics
- Might be way beyond my skill level? (come to think of it, it probably is :D)


## Development
To make this app, I have used Flask (I know, bad practice) as a web server, Elara, a Python-specific database, and Docker to run the hold the entire contraption 

It took a while to make, as this is probably my biggest project yet. Let's hope the effort paid off!

## Quickstart
See the README inside the server folder
