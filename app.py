import streamlit as st
from datetime import date
import uuid
import json
import os

st.set_page_config(layout="wide", page_title="Checkway", initial_sidebar_state="expanded")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

DATA_FILE = "checklists_data.json"

def load_checklists():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}

def save_checklists():
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(st.session_state.checklists, f, indent=2)
    except IOError:
        pass

if "page"       not in st.session_state: st.session_state.page = "Checklist"
if "checklists" not in st.session_state: st.session_state.checklists = load_checklists()
if "open_id"    not in st.session_state: st.session_state.open_id = None
if "show_form"  not in st.session_state: st.session_state.show_form = False

PAGES = ["Checklist", "Autobiography", "Portfolio", "Components Used"]

with st.sidebar:
    for name in PAGES:
        if st.button(name, key=name, use_container_width=True):
            st.session_state.page = name
            st.session_state.open_id = None
            st.session_state.show_form = False
            st.rerun()

page = st.session_state.page
MAX_TITLE = 20

if page == "Checklist":

    if st.session_state.open_id is None:
        st.markdown('<p class="dash-title">Checklist Dashboard</p>', unsafe_allow_html=True)
        st.markdown("""
        <div class="section-card" style="margin-top: 0.25rem; margin-bottom: 1.25rem;">
            <p>
                <strong>Work in Progress</strong> —
                <em>I built this checklist module for personal use because most free checklist platforms
            have limitations or require paid plans. For example, Checkli's free version only allows
            up to two active checklists.
            Additionally, many platforms require users to log in repeatedly, which is a hassle for me.
            I prefer a session-based system where progress is automatically saved, so when I return
            to the website, my checklists remain accessible without the hassle of logging in again</em>
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("＋ Create New Checklist", key="create_toggle"):
            st.session_state.show_form = not st.session_state.show_form
            st.rerun()

        if st.session_state.show_form:
            with st.form("new_checklist_form", clear_on_submit=True):
                new_title = st.text_input("Title", placeholder="e.g. Morning Routine", max_chars=MAX_TITLE)
                st.caption(f"Maximum {MAX_TITLE} characters.")
                submitted = st.form_submit_button("Create")
                if submitted and new_title.strip():
                    uid = str(uuid.uuid4())[:8]
                    st.session_state.checklists[uid] = {
                        "title": new_title.strip()[:MAX_TITLE],
                        "date":  str(date.today()),
                        "tasks": []
                    }
                    save_checklists()
                    st.session_state.open_id = uid
                    st.session_state.show_form = False
                    st.rerun()

        st.markdown("""
        <div class="cl-table-header">
            <span>Title Name</span>
        </div>
        """, unsafe_allow_html=True)

        if not st.session_state.checklists:
            st.caption("No checklists yet. Click the button above to create one.")
        else:
            for uid, cl in sorted(st.session_state.checklists.items(), key=lambda x: x[1]["date"]):
                col1, col2 = st.columns([8, 1])
                with col1:
                    if st.button(cl["title"], key=f"open_{uid}"):
                        st.session_state.open_id = uid
                        st.rerun()
                with col2:
                    if st.button("Delete", key=f"del_{uid}"):
                        del st.session_state.checklists[uid]
                        save_checklists()
                        st.rerun()

    else:
        uid = st.session_state.open_id
        cl  = st.session_state.checklists[uid]
        tasks = cl["tasks"]

        if st.button("← Back"):
            st.session_state.open_id = None
            st.rerun()

        st.markdown(
            f'<div class="cl-detail-header">'
            f'<p class="cl-checklist-name">{cl["title"]}</p>'
            f'</div>'
            f'<p class="cl-detail-title">Checklist Items</p>',
            unsafe_allow_html=True,
        )

        for i, task in enumerate(tasks):
            col_check, col_del = st.columns([8, 0.3])
            with col_check:
                checked = st.checkbox(task["label"], value=task["done"], key=f"{uid}_{i}")
                if st.session_state.checklists[uid]["tasks"][i]["done"] != checked:
                    st.session_state.checklists[uid]["tasks"][i]["done"] = checked
                    save_checklists()
            with col_del:
                if st.button("✕", key=f"taskdel_{uid}_{i}"):
                    st.session_state.checklists[uid]["tasks"].pop(i)
                    save_checklists()
                    st.rerun()

        with st.form(key=f"form_{uid}", clear_on_submit=True):
            new_task = st.text_input("New task", placeholder="Enter a new item", label_visibility="collapsed")
            if st.form_submit_button("＋ Add Item"):
                if new_task.strip():
                    st.session_state.checklists[uid]["tasks"].append({"label": new_task.strip(), "done": False})
                    save_checklists()
                    st.rerun()

elif page == "Autobiography":
    st.markdown('<p class="dash-title">Autobiography</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="section-card">
        <div class="label">About Me</div>
        <h4>Christian Jayson Cantiller</h4>
        <p>
            I'm a BSIT student currently studying at Cebu Institute of Technology in Cebu City, Philippines.
            I grew up surrounded by technology — my family owned a computer shop, and that early exposure
            got me hooked on computers, gaming, and eventually web development. I've always been curious
            about how systems work and how they are built, which inspired my goal to turn this passion
            into a career.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### Early Life & Background")
    st.markdown("""
    <div class="timeline-item">
        <h4>Born & Raised — Cebu City, Sambag 1</h4>
        <div class="date">Cebu City, Philippines</div>
        <p>
            I was born and raised in Sambag 1, Cebu City. Growing up, I spent most of my time
            playing outside with neighborhood friends. Everything changed when I discovered computers —
            my family started a computer shop, and I was instantly hooked on its games.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### Education")
    st.markdown("""
    <div class="timeline-item">
        <h4>Primary & Secondary School — University of San Carlos</h4>
        <div class="date">Elementary — High School</div>
        <p>
            During my elementary and high school years at the University of San Carlos, I was an
            active student — joining clubs, serving as an officer in CAT (Citizenship Advancement
            Training), and volunteering as a sacristan, assisting the parish priest during church
            services. Despite all the extracurricular involvement, I always found time for my
            favorite escape: computer games. Those years taught me how to balance responsibility
            with the things I enjoy.
        </p>
    </div>
    <div class="timeline-item">
        <h4>Cebu Institute of Technology — University</h4>
        <div class="date">2022 — 2026</div>
        <p>
            I am currently pursuing a Bachelor of Science in Information Technology at the Cebu
            Institute of Technology. Throughout my studies, I have gained hands-on experience in
            programming, database management, and web development — building real projects that
            strengthened both my technical skills and ability to work in teams.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### Interests & Hobbies")
    st.markdown("""
    <div class="section-card">
        <p>
            🚶 <strong>Walking</strong> <br>
            🎮 <strong>Playing Online Games</strong> <br>
            📺 <strong>Watching YouTube Videos</strong> <br>
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### Goals & Aspirations")
    st.markdown("""
    <div class="section-card">
        <p>
            💼 <strong>Secure a stable job</strong> <br>
            💪 <strong>Get fit and healthy</strong> <br>
            🥗 <strong>Proper nutrition</strong> <br>
            🧠 <strong>Self-discipline</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

elif page == "Portfolio":
    st.markdown('<p class="dash-title">Portfolio</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="section-card">
        <div class="label">Who I Am</div>
        <h4>Christian Jayson Cantiller</h4>
        <p>A frontend developer and QA enthusiast with a passion for building clean,
        functional web applications. Experienced in leading project teams and delivering
        full-stack solutions from concept to deployment.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### Skills")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="section-card"><div class="label">Languages</div><p>JavaScript, HTML/CSS, SQL</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="section-card"><div class="label">Frameworks</div><p>Streamlit, React, Node.js</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="section-card"><div class="label">Other</div><p>Japanese (JLPT N5)</p></div>', unsafe_allow_html=True)

    st.markdown("#### Projects")
    for title, role, year, desc, tags, url in [
        (
            "STDE — Software Test Documentation Evaluator",
            "Frontend / QA", "Current",
            "An AI-powered tool that automates the evaluation and analysis of software test documentation. "
            "It leverages artificial intelligence to review test cases, validate documentation standards, "
            "and provide actionable feedback — streamlining the QA workflow and improving overall test quality.",
            ["JavaScript", "AI", "QA"],
            "https://github.com/Shanta413/STDE",
        ),
        (
            "School Maintenance Reporting & Management System",
            "Project Lead", "2025",
            "A web and mobile-based platform designed to streamline the process of reporting, tracking, "
            "and resolving maintenance issues within the school campus.",
            ["React", "Node.js", "SQL"],
            "https://github.com/Shanta413/SchoolMaintenanceReportingandManagementSystem-IT342-G01-Group3",
        ),
        (
            "Notes Application with Blockchain",
            "Frontend", "2025",
            "A decentralized notes app integrating blockchain principles. Each note is cryptographically "
            "linked to a block, creating an immutable ledger that ensures data integrity and demonstrates "
            "how blockchain can be applied beyond cryptocurrencies for secure recordkeeping.",
            ["Blockchain", "JavaScript", "Node.js"],
            "https://github.com/Lumity-13/notes-application-blockchain",
        ),
    ]:
        tag_html = "".join(f'<span class="tech-tag">{t}</span>' for t in tags)
        st.markdown(
            f'<div class="project-card">'
            f'<h4>{title}</h4>'
            f'<p style="font-size:0.78rem !important; color:#6b7280 !important; margin-bottom:0.3rem !important;">{role} · {year}</p>'
            f'<p>{desc}</p>'
            f'<div style="margin-top:6px;">{tag_html}'
            f'<a href="{url}" target="_blank" style="display:inline-block; background-color:#5b5fc7 !important; '
            f'color:#ffffff !important; font-size:0.72rem !important; font-weight:600; padding:2px 10px; '
            f'border-radius:4px; margin-left:4px; margin-top:8px; text-decoration:none;">GitHub ↗</a>'
            f'</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("#### Experience")
    st.markdown("""
    <div class="timeline-item">
        <h4>WordPress Developer — Knowles Training Institute</h4>
        <div class="date">January 2026 — Present</div>
        <p>Created a checklist website assignment and developed a knowledge-based interactive game
        for the company's training platform.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### Contact")
    st.markdown("""
    <div class="section-card">
        <p>
            <strong>Email:</strong> <a href="mailto:jaysoncan413@gmail.com" style="color:#5b5fc7 !important; text-decoration:none;">jaysoncan413@gmail.com</a><br>
            <strong>GitHub:</strong> <a href="https://github.com/Shanta413" target="_blank" style="color:#5b5fc7 !important; text-decoration:none;">github.com/Shanta413</a><br>
            <strong>LinkedIn:</strong> <a href="https://www.linkedin.com/in/christian-jayson-cantiller-60a653368" target="_blank" style="color:#5b5fc7 !important; text-decoration:none;">linkedin.com/in/christian-jayson-cantiller</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

elif page == "Components Used":
    from st_draggable_list import DraggableList

    st.markdown('<p class="dash-title">Components Used</p>', unsafe_allow_html=True)
    st.markdown('<p class="dash-sub">Drag to reorder the list below.</p>', unsafe_allow_html=True)

    st.markdown("""
    <div class="section-card" style="margin-top: 0.25rem; margin-bottom: 1.25rem;">
        <p>
            <strong>Work in Progress</strong> — This section uses the streamlit-draggable-list
            third-party component. The draggable list renders inside an iframe with its own
            internal styles, which makes it difficult to apply custom CSS from the parent page.
            I'm currently exploring ways to inject styles into the iframe to match the app's
            light theme. For now, the list items may appear with default dark styling.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if "drag_items" not in st.session_state:
        st.session_state.drag_items = [
            {"id": "drag",  "order": 1, "name": "streamlit-draggable-list"},
            {"id": "check", "order": 2, "name": "st.checkbox (Checklist)"},
            {"id": "btn",   "order": 3, "name": "st.button (Sidebar Nav)"},
            {"id": "form",  "order": 4, "name": "st.form (Add Task)"},
            {"id": "state", "order": 5, "name": "st.session_state"},
            {"id": "html",  "order": 6, "name": "st.markdown (HTML/CSS)"},
            {"id": "col",   "order": 7, "name": "st.columns (Layout)"},
            {"id": "json",  "order": 8, "name": "JSON file (Data Persistence)"},
        ]

    result = DraggableList(st.session_state.drag_items, width="100%", key="drag_list")
    if result:
        st.session_state.drag_items = result