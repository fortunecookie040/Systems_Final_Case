# Systems_Final_Case
Team: Chloe Wang and Angel Jiang
Final Project for Systems

#One-command run
pip install -r requirements.txt
python app.py 

1) Executive Summary

We created this app as a solution for college students trying to make sense of their financial state. Many of us enter college with little to no knowledge of how to budget or control our spending habits. Part of the issue is that we cannot easily keep track of our spending every day, as many opt to check occasionally or when they need to pay off their credit card bills. In fact, I have tried budgeting before; however, I found the process tedious and time-consuming. It was inconvenient as I couldn't easily edit the spreadsheet on my phone while I'm out, and it was hard to remember the exact amount I purchased. Therefore, this app offers a cute and efficient way for college students to track their spending. It's one page, so there is no need to navigate through many pages. In addition, it has a plot tracking the amount spent per day in a month, allowing simple visual comparisons. On the left, there are prompts for the user, allowing them to do a one-time setting of the budget. After that, the user only has to input a number and hit the log button. The graph will display a line plot with a blue line corresponding to how much the user spent and the orange representing the amount of budget left. Each will update whenever the log button is hit. When the lines intersect, that means the user has gone above their budget. This allows a quick, real time visual cue for the user. 

2) System Overview
Course Concept(s): In this project, we used a Flask API, a virtual environment, logging/metric, and azure deployment.
Architecture Diagram: <img width="960" height="540" alt="image" src="https://github.com/user-attachments/assets/66429471-b953-438c-9bbd-cd701990f310" />

Data/Models/Services: List sources, sizes, formats, and licenses.
| Source                   | Size                         | Format            | License             |
| ------------------------ | ---------------------------- | ----------------- | ------------------- |
| Data: User input (form fields) | varies; ephemeral | form data (strings, numbers) | N/A (user-provided) |
| Models: None | -- | -- | -- |
| ServicesL Azure App Service | F1 | Runs `app.py` in Python environment | Microsoft Azure Terms of Use |

3) How to Run (Local)

Choose Docker or Apptainer and provide a single command.
#Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt
#Expose the port the app runs on
EXPOSE 5000
#Command to run the application
CMD ["python", "app.py"]

4) Design Decisions

Why this concept? Alternatives considered and why not chosen: I chose this concept of Flask API and azure deployment because I thought it was the most applicable to future projects, especially in hackathons and such where I have to deploy an app. I thought this was a good way to recall what we learned in our case studies and apply it. I also thought that this was easier to understand than tinyllama and such. Thus, when I used github and azure, I felt like I could understand how to do so. I originally wanted to do a gpt, however, I think I need a little more practice with that since I had a lot of trouble making it work when doing the case study. 
Tradeoffs: Performance, cost, complexity, maintainability: The performance works well. If we had more time, we would add an undo button, or a subtraction button, in case the user enters a wrong value. Otherwise, the graph works fine. It is a little slow, but that's okay because the cost is free. In terms of complexity, it is not that complex as depicted with the architecture diagram. The app should be easy to maintain since we tried to keep it as simple as possible.
Security/Privacy: Secrets mgmt, input validation, PII handling: This project does not have any secrets or external APIs or databases. It won't be in the code or anywhere visible. There is input validations. Since the user must enter the budget and how much they spent, the input boxes only take numerical values. We do not collect any personally identifiable information. 
Ops: Logs/metrics, scaling considerations, known limitations: For logs and metrics, We use azure's built in log to check status of our app. For scaling, we aren't scaling anything. As for known limitations, we are expecting performance to degrade if there are too many inputs or if input values get too large.  

5) Results & Evaluation

Screenshots or sample outputs (place assets in /assets).
[Homepage] <img width="2256" height="1152" alt="image" src="https://github.com/user-attachments/assets/5af1d281-129f-4b33-b2c6-b92b0d7ead9d" />
[Example Input] <img width="2260" height="1158" alt="image" src="https://github.com/user-attachments/assets/3cfc42a6-26b5-4066-a6b8-9a86586637b1" />

Brief performance notes or resource footprint (if relevant).
- A little slow on clearing the plot. A refresh helped.
- Another limitation is that we lose data when the app is refreshed.
  
Validation/tests performed and outcomes.
Validation tests worked. We put values that were big in budget, small in inputs and vise versa. We also tried clearing the plot when there was no budget and We got an error telling us to put a budget number. I also tried putting a negative number and that did not work. 

6) What’s Next

Planned improvements, refactors, and stretch features
Next, we plan to make it so that data is being collected in a csv so that when refreshed, we won't lose the data that we currently have. In addition, we would like to add an undo or add to function in case the user accidentally puts the wrong input amount or want to edit their input amount. We could also change the x and y ticks to days of the week or just a number. We can change the dates to something more readable.
In terms of refractors, we could maybe do something to make it so that users can download their data, which means we need something to store the data in the first place. For stretch features, we could add images using azure blob storage and disply a certain image corresponding to how the user is with their financial goals. For example, a sad cat when spending goes above the budget.

7) Links (Required)

GitHub Repo: https://github.com/fortunecookie040/Systems_Final_Case.git

Public Cloud App (optional): https://sys-final-project-qtr7bs.azurewebsites.net/






