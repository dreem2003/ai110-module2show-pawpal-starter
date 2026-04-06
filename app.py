import streamlit as st
from models import Owner, Pet, Task
from services import Scheduler, PlanExplainer
from utils import parse_priority

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.caption("Pet care planning assistant")
st.markdown(
    """
Welcome to PawPal+.

PawPal+ helps you stay consistent with your pet’s daily care by organizing tasks like walks,
feeding, and grooming into a clear, prioritized plan based on your time and preferences.

This starter app provides a simple interface, but the core scheduling logic is yours to build.
As you develop the system, this app will serve as your interactive dashboard for generating and visualizing daily care plans.
"""
)

st.divider()

# ── Owner & Pet ───────────────────────────────────────────────────────────────
st.subheader("Owner & Pet")

col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Owner name", value="Jordan")
    available_minutes = st.number_input(
        "Available time today (minutes)", min_value=30, max_value=840, value=480, step=30
    )
with col2:
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "rabbit", "bird", "other"])
    pet_age = st.number_input("Pet age (years)", min_value=0, max_value=30, value=3)

st.divider()

# ── Task input ────────────────────────────────────────────────────────────────
st.subheader("Tasks")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
with col4:
    category = st.text_input("Category", value="exercise")

if st.button("Add task"):
    if task_title.strip():
        st.session_state.tasks.append(
            {
                "title": task_title.strip(),
                "duration_minutes": int(duration),
                "priority": priority,
                "category": category.strip() or "general",
            }
        )

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)

    if st.button("Clear all tasks", type="secondary"):
        st.session_state.tasks = []
        st.rerun()
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# ── Generate schedule ─────────────────────────────────────────────────────────
st.subheader("Build Schedule")

if st.button("Generate schedule", type="primary"):
    if not st.session_state.tasks:
        st.warning("Add at least one task before generating a schedule.")
    else:
        owner = Owner(name=owner_name, available_minutes=int(available_minutes))
        pet = Pet(name=pet_name, species=species, age=int(pet_age))

        scheduler = Scheduler(owner=owner, pet=pet)
        for t in st.session_state.tasks:
            task = Task(
                title=t["title"],
                duration_minutes=t["duration_minutes"],
                priority=parse_priority(t["priority"]),
                category=t["category"],
            )
            scheduler.add_task(task)

        scheduled, skipped = scheduler.generate_plan()
        explainer = PlanExplainer(scheduled, skipped, owner, pet)

        st.success(explainer.summarize())

        if scheduled:
            st.markdown("### Scheduled tasks")
            for st_task in scheduled:
                with st.container(border=True):
                    st.markdown(explainer.explain_task(st_task))

        if skipped:
            st.markdown("### Skipped tasks")
            st.warning(explainer.explain_skipped())
