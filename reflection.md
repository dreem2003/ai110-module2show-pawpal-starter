# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
  - Utilized the idea of customers, having pets (with their attributes), having a scheduler that run their tasks, having tasks based on what    needs to be done and claude suggested having an additional class for the plan explainer
- What classes did you include, and what responsibilities did you assign to each?
   - Created custoemer class pet class, tasks, and scheduled task class, scheduler, plan explainer, and priority


**b. Design changes**

- Did your design change during implementation?
  - Yes
- If yes, describe at least one change and why you made it.
  - Claude suggested 2 main time saving redistrubtions, scheduled tasks as an extra class distinguihable from tasks
    and the plan explainer, to take information from the scheduler and display what atsks can be accomplsihed and what have to be skipped

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
  - it considers total time available for each customer in a day, the priority of each task.
- How did you decide which constraints mattered most?
  - understanding what is most important is doing the tasks that need to be done first.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
  - it compares duration of tasks and priorities to determine which tasks are done first
- Why is that tradeoff reasonable for this scenario?
  - it is reasonable because it ensure that the most mportant taks get done, and when there are a number of small
    important ones it is not overshadowed by one long important one.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
  - used tools to generate the UML, refactore, brainstorm relationships between classes
- What kinds of prompts or questions were most helpful?
  - prompts that i asked to build on my idea, seemed to set me off in the right direction

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
  - all of the AI suggestions wer on point and utilized, but i never asked broad, disruptive questions
    so they were always small changes at a time and focused
- How did you evaluate or verify what the AI suggested?
  - Testing

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
  - Connections, validation of input and expected outcomes to user interactions
- Why were these tests important?
  - to ensure good cutomer experience

**b. Confidence**

- How confident are you that your scheduler works correctly?
  - 99%
- What edge cases would you test next if you had more time?
  - handling multiple pets

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
  - time management mechanics

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
  - expand on the multiple pets module, and include preferences to suggest activities.
    eg. active dogs would have increased priorites on excercise activities

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
  - It makes brainstorming and collecting thoughts so much easier, but lettingit run wild can affect your understanding of the code.
