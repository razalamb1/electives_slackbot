# Duke University Elective SlackBot

### Background and Motivation

Duke’s Masters in Interdisciplinary Data Science (MIDS) is a relatively new 2 year-long graduate science program. One of the strengths of the program is the ability for students to take electives in any of Duke’s graduate schools. However, this leads to a somewhat predictable and simultaneously frustrating question: “What gosh-darn elective do I take??” As a solution, the program administrator has put together a Google Sheet for students to add courses they have taken and any relevant feedback. However, as visible below, this spreadsheet can be very difficult to use, as there’s no easy sort functionality, and students may enter classes with slightly different names.



The purpose of this project is to rectify this issue, and provide an easy platform for current students to both view and add feedback on electives they have taken.

### Project Design

We chose to implement this tool in Slack, given the widely prevalent use of the tool in MIDS. We utilized a SlackBot, and the “slash” commands to create interactivity, and utilized AWS AppRunner to deploy our SlackBot. The elective data is hosted on DynamoDB, and AppRunner can read and write from the database.

To build our database in DynamoDB we used the spreadsheet containing the information and formatted it in a way that DynamoDB can read and that can be interacted with in the slackbot. The restructured spreadsheet included the Class Number, the student name, their feedback as well as a new field where students can add a rating for the course (0-5). We used the class number and student names as primary and secondary keys in the database.

![alt text](https://user-images.githubusercontent.com/87722995/145469450-7b21b655-6284-4af3-8b7d-8d8543003e26.jpg)

The flowchart below displays the full project design. A user utilizes one of two slash commands (elective or feedback) and the SlackBot sends the request to AWS AppRunner, which is set to deploy on push to this GitHub (hosted on an EC2 instance). AppRunner can then interact with the Dynamo DataBase. If the slash command “/elective” is called, the database is searched for relevant feedback on that specific elective, while if the slash command “/feedback” is called, AppRunner adds the student’s feedback to the DataBase as a new entry.
This project still has a few limitations that we hope to address with future work. For example, right now students must exactly specify the correct class name to access feedback. Future integration will focus on Slack “workflows” for users to have a more interactive and less error prone experience.



___        ______     ____ _                 _  ___  
        / \ \      / / ___|   / ___| | ___  _   _  __| |/ _ \ 
       / _ \ \ /\ / /\___ \  | |   | |/ _ \| | | |/ _` | (_) |
      / ___ \ V  V /  ___) | | |___| | (_) | |_| | (_| |\__, |
     /_/   \_\_/\_/  |____/   \____|_|\___/ \__,_|\__,_|  /_/ 
 ----------------------------------------------------------------- 


Hi there! Welcome to AWS Cloud9!

To get started, create some files, play with the terminal,
or visit https://docs.aws.amazon.com/console/cloud9/ for our documentation.

Happy coding!
