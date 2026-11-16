<a href="https://dishank25.github.io/Dishank25/"><picture>
  <source media="(max-width: 600px)" srcset="https://raw.githubusercontent.com/Dishank25/Dishank25/2a100f4d9834131c5c129b0d8cfeea1d2d21182d/assets/observatory-breathing-mobile.svg" />
  <img width="1080" src="assets/observatory-breathing.svg" alt="Dishank Jain, AI engineer. An illustrated engineer watches a luminous manta through the window of a deep-sea observatory. Open the portfolio." />
</picture></a>

**[Enter the observatory](https://dishank25.github.io/Dishank25/)** · [Featured project · Abyssal Observatory (Python/Django)](https://github.com/Dishank25/abyssal-portfolio) · [Connect on LinkedIn](https://www.linkedin.com/in/dishankjain25/)

## About me

I'm Dishank Jain, an AI engineer based in Noida, India. I build Python tools for semantic search, document extraction, and recommendations. I like being able to trace a result back to the input that produced it. With an FAQ assistant, that means checking which policy it retrieved. With a recommender, it means understanding why one product ranked above another.

I started in machine learning and Flutter development. Today I work in AI consulting and continue building projects that bring models, APIs, and interfaces together.

## AI engineering projects

- **PawSupport.** Customers can ask about the same policy in very different ways. This pet-care assistant tries an exact FAQ match, semantic search, and alias lookup. I evaluate it against expected FAQ identifiers so a fluent answer drawn from the wrong policy still counts as a miss. [Project page](https://dishank25.github.io/Dishank25/projects/pawsupport/) · [FAQ router](https://github.com/Dishank25/ZiglyPawSupport/blob/main/backend/rag/l1_router.py) · [Offline evaluation](https://github.com/Dishank25/ZiglyPawSupport/blob/main/evaluation/run_evaluation.py)
- **SupportPilot.** A FastAPI service retrieves three FAQs from ChromaDB. The closest match determines whether the service passes context to the language model or returns a fallback. You can change the match distance in the demo and see the decision flip. [Project and demo](https://dishank25.github.io/Dishank25/projects/supportpilot/) · [Retrieval code](https://github.com/Dishank25/supportpilot/blob/main/agents/retrieval_agent.py)
- **Veterinary document extraction.** A single PDF can mix patient details, treatment, and follow-up instructions. My service extracts and validates those fields, then writes each record type to a separate Excel sheet for review. [Project page](https://dishank25.github.io/Dishank25/projects/veterinary-records/)
- **Product recommendations.** I used cosine similarity to find customers with similar purchase histories. Ranking products by order frequency reduced the influence of one unusually large order, and filtering previous purchases kept suggestions new to each customer. [Project page](https://dishank25.github.io/Dishank25/projects/recommendations/)
- **Pet breed identification.** This computer vision prototype takes a photo, requests a structured prediction from GPT-4o Vision, and validates the response. It returns an explicit “unknown” when the model reports low confidence. [Project page](https://dishank25.github.io/Dishank25/projects/breed-identification/)

## Web, mobile, and Python projects

- **Abyssal Observatory.** I built this portfolio in Python and Django. A single content file feeds the homepage and individual project routes. A Django management command renders those same pages for GitHub Pages. [Project page](https://dishank25.github.io/Dishank25/projects/abyssal-portfolio/) · [Django source](https://github.com/Dishank25/abyssal-portfolio) · [Profile artwork and published site](https://github.com/Dishank25/Dishank25)
- **Student and recruiter job portal.** This Flutter project follows both sides of an application. Students browse openings and apply. Recruiters create job or internship postings and review applicants through a separate set of screens. The repository credits the original app snapshot to an109. [Project page](https://dishank25.github.io/Dishank25/projects/job-portal/) · [Source](https://github.com/Dishank25/Job-Portal)
- **Flutter job discovery.** This related version focuses on the candidate's path from selecting skills to filtering openings by location or experience. A BLoC handles the application event from the job detail screen. [Project page](https://dishank25.github.io/Dishank25/projects/job-discovery/) · [Source](https://github.com/Dishank25/rishabh6363-jobflutter-448f346c9d38)
- **Terminal tic-tac-toe.** One of my early Python projects. The player picks a numbered square and the computer chooses a free square at random. The board, turns, and win checks fit in a single standard-library script. [Project page](https://dishank25.github.io/Dishank25/projects/terminal-tic-tac-toe/) · [Source](https://github.com/Dishank25/python_project)

## Technical skills

| Area | Tools and techniques |
| --- | --- |
| Search and evaluation | Embeddings, ChromaDB, semantic retrieval, labeled FAQ tests |
| Python applications | FastAPI, Django, Pydantic, REST APIs, Streamlit |
| Machine learning and data | pandas, NumPy, scikit-learn, collaborative filtering, cosine similarity |
| Mobile development | Dart, Flutter, Provider, REST integration |

## Experience

| Period | Role | Focus |
| --- | --- | --- |
| Jul 2026 – present | Senior Executive, AI Consultant · Cosmo Ferrites | Applied AI adoption and prototyping |
| Nov 2025 – Jun 2026 | Junior AI / Generative AI Engineer · Zigly Pet Care & Cosmo Films | Python services, applied machine learning, and output evaluation |
| Jul – Dec 2024 | Software Developer, Flutter · Lloyd Group of Institutions | Reusable Dart widgets, state management, and API integrations |
| May – Jun 2024 | AI / Machine Learning Intern · Ethical Edufabrica | Data preparation, feature selection, and model evaluation |

B.Tech in Computer Science and Engineering, United College of Engineering and Research, Greater Noida (2020–2024).
