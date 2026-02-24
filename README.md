# Discord Integral Practice Bot

(Doesnt support definite integration, bot is also in early stages of development)

A Discord slash-command bot that generates random A-Level style integration questions, renders the question and a full worked solution as images, and lets users reveal the solution using an interactive button.

The bot supports several common integration techniques:
- substitution  
- integration by parts  
- trigonometric integrals  
- partial fractions (simple form)  
- exponential–trigonometric integrals  

---

## Features

- `/integral` slash command
- Randomly generated integration questions
- Fully worked step by step solutions
- Renders LaTeX style maths into PNG images using Matplotlib
- Interactive **Show Solution** button
- Automatic timeout and button disabling

---

## Requirements

Python 3.12 (recommended, as used in your project)

Install the required packages:

```bash
pip install discord.py matplotlib